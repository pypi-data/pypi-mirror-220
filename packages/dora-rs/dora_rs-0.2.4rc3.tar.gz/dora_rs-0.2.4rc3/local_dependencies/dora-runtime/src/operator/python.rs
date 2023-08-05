#![allow(clippy::borrow_deref_ref)] // clippy warns about code generated by #[pymethods]

use super::{OperatorEvent, StopReason};
use dora_core::{
    config::{NodeId, OperatorId},
    descriptor::{source_is_url, Descriptor},
};
use dora_download::download_file;
use dora_node_api::Event;
use dora_operator_api_python::PyEvent;
use dora_operator_api_types::DoraStatus;
use eyre::{bail, eyre, Context, Result};
use pyo3::{
    pyclass,
    types::{IntoPyDict, PyDict},
    Py, PyAny, Python,
};
use std::{
    panic::{catch_unwind, AssertUnwindSafe},
    path::Path,
};
use tokio::sync::{mpsc::Sender, oneshot};
use tracing::{error, field, span, warn};

fn traceback(err: pyo3::PyErr) -> eyre::Report {
    let traceback = Python::with_gil(|py| err.traceback(py).and_then(|t| t.format().ok()));
    if let Some(traceback) = traceback {
        eyre::eyre!("{traceback}\n{err}")
    } else {
        eyre::eyre!("{err}")
    }
}

#[tracing::instrument(skip(events_tx, incoming_events), level = "trace")]
pub fn run(
    node_id: &NodeId,
    operator_id: &OperatorId,
    source: &str,
    events_tx: Sender<OperatorEvent>,
    incoming_events: flume::Receiver<Event>,
    init_done: oneshot::Sender<Result<()>>,
    dataflow_descriptor: &Descriptor,
) -> eyre::Result<()> {
    let path = if source_is_url(source) {
        let target_path = Path::new("build")
            .join(node_id.to_string())
            .join(format!("{}.py", operator_id));
        // try to download the shared library
        let rt = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()?;
        rt.block_on(download_file(source, &target_path))
            .wrap_err("failed to download Python operator")?;
        target_path
    } else {
        Path::new(source).to_owned()
    };

    if !path.exists() {
        bail!("No python file exists at {}", path.display());
    }
    let path = path
        .canonicalize()
        .wrap_err_with(|| format!("no file found at `{}`", path.display()))?;
    let module_name = path
        .file_stem()
        .ok_or_else(|| eyre!("module path has no file stem"))?
        .to_str()
        .ok_or_else(|| eyre!("module file stem is not valid utf8"))?;
    let path_parent = path.parent();

    let send_output = SendOutputCallback {
        events_tx: events_tx.clone(),
    };

    let init_operator = move |py: Python| {
        if let Some(parent_path) = path_parent {
            let parent_path = parent_path
                .to_str()
                .ok_or_else(|| eyre!("module path is not valid utf8"))?;
            let sys = py.import("sys").wrap_err("failed to import `sys` module")?;
            let sys_path = sys
                .getattr("path")
                .wrap_err("failed to import `sys.path` module")?;
            let sys_path_append = sys_path
                .getattr("append")
                .wrap_err("`sys.path.append` was not found")?;
            sys_path_append
                .call1((parent_path,))
                .wrap_err("failed to append module path to python search path")?;
        }

        let module = py.import(module_name).map_err(traceback)?;
        let operator_class = module
            .getattr("Operator")
            .wrap_err("no `Operator` class found in module")?;

        let locals = [("Operator", operator_class)].into_py_dict(py);
        let operator = py
            .eval("Operator()", None, Some(locals))
            .map_err(traceback)?;
        operator.setattr(
            "dataflow_descriptor",
            pythonize::pythonize(py, dataflow_descriptor)?,
        )?;

        Result::<_, eyre::Report>::Ok(Py::from(operator))
    };

    let python_runner = move || {
        let mut operator =
            match Python::with_gil(init_operator).wrap_err("failed to init python operator") {
                Ok(op) => {
                    let _ = init_done.send(Ok(()));
                    op
                }
                Err(err) => {
                    let _ = init_done.send(Err(err));
                    bail!("Could not init python operator")
                }
            };

        let reason = loop {
            #[allow(unused_mut)]
            let Ok(mut event) = incoming_events.recv() else { break StopReason::InputsClosed };

            if let Event::Reload { .. } = event {
                // Reloading method
                match Python::with_gil(|py| -> Result<Py<PyAny>> {
                    // Saving current state
                    let current_state = operator
                        .getattr(py, "__dict__")
                        .wrap_err("Could not retrieve current operator state")?;
                    let current_state = current_state
                        .extract::<&PyDict>(py)
                        .wrap_err("could not extract operator state as a PyDict")?;
                    // Reload module
                    let module = py
                        .import(module_name)
                        .map_err(traceback)
                        .wrap_err(format!("Could not retrieve {module_name} while reloading"))?;
                    let importlib = py
                        .import("importlib")
                        .wrap_err("failed to import `importlib` module")?;
                    let module = importlib
                        .call_method("reload", (module,), None)
                        .wrap_err(format!("Could not reload {module_name} while reloading"))?;
                    let reloaded_operator_class = module
                        .getattr("Operator")
                        .wrap_err("no `Operator` class found in module")?;

                    // Create a new reloaded operator
                    let locals = [("Operator", reloaded_operator_class)].into_py_dict(py);
                    let operator: Py<pyo3::PyAny> = py
                        .eval("Operator()", None, Some(locals))
                        .map_err(traceback)
                        .wrap_err("Could not initialize reloaded operator")?
                        .into();

                    // Replace initialized state with current state
                    operator
                        .getattr(py, "__dict__")
                        .wrap_err("Could not retrieve new operator state")?
                        .extract::<&PyDict>(py)
                        .wrap_err("could not extract new operator state as a PyDict")?
                        .update(current_state.as_mapping())
                        .wrap_err("could not restore operator state")?;

                    Ok(operator)
                }) {
                    Ok(reloaded_operator) => {
                        operator = reloaded_operator;
                    }
                    Err(err) => {
                        error!("Failed to reload operator.\n {err}");
                    }
                }
            }

            let status = Python::with_gil(|py| -> Result<i32> {
                let span = span!(tracing::Level::TRACE, "on_event", input_id = field::Empty);
                let _ = span.enter();
                // We need to create a new scoped `GILPool` because the dora-runtime
                // is currently started through a `start_runtime` wrapper function,
                // which is annotated with `#[pyfunction]`. This attribute creates an
                // initial `GILPool` that lasts for the entire lifetime of the `dora-runtime`.
                // However, we want the `PyBytes` created below to be freed earlier.
                // creating a new scoped `GILPool` tied to this closure, will free `PyBytes`
                // at the end of the closure.
                // See https://github.com/PyO3/pyo3/pull/2864 and
                // https://github.com/PyO3/pyo3/issues/2853 for more details.
                let pool = unsafe { py.new_pool() };
                let py = pool.python();

                // Add metadata context if we have a tracer and
                // incoming input has some metadata.
                #[cfg(feature = "telemetry")]
                if let Event::Input {
                    id: input_id,
                    metadata,
                    ..
                } = &mut event
                {
                    use dora_tracing::telemetry::{deserialize_context, serialize_context};
                    use std::borrow::Cow;
                    use tracing_opentelemetry::OpenTelemetrySpanExt;
                    span.record("input_id", input_id.as_str());

                    let cx = deserialize_context(&metadata.parameters.open_telemetry_context);
                    span.set_parent(cx);
                    let cx = span.context();
                    let string_cx = serialize_context(&cx);
                    metadata.parameters.open_telemetry_context = Cow::Owned(string_cx);
                }

                let py_event = PyEvent::from(event);
                let status_enum = operator
                    .call_method1(py, "on_event", (py_event, send_output.clone()))
                    .map_err(traceback)?;
                let status_val = Python::with_gil(|py| status_enum.getattr(py, "value"))
                    .wrap_err("on_event must have enum return value")?;
                Python::with_gil(|py| status_val.extract(py))
                    .wrap_err("on_event has invalid return value")
            })?;
            match status {
                s if s == DoraStatus::Continue as i32 => {} // ok
                s if s == DoraStatus::Stop as i32 => break StopReason::ExplicitStop,
                s if s == DoraStatus::StopAll as i32 => break StopReason::ExplicitStopAll,
                other => bail!("on_event returned invalid status {other}"),
            }
        };

        // Dropping the operator using Python garbage collector.
        // Locking the GIL for immediate release.
        Python::with_gil(|_py| {
            drop(operator);
        });

        Result::<_, eyre::Report>::Ok(reason)
    };

    let closure = AssertUnwindSafe(|| {
        python_runner().wrap_err_with(|| format!("error in Python module at {}", path.display()))
    });

    match catch_unwind(closure) {
        Ok(Ok(reason)) => {
            let _ = events_tx.blocking_send(OperatorEvent::Finished { reason });
        }
        Ok(Err(err)) => {
            let _ = events_tx.blocking_send(OperatorEvent::Error(err));
        }
        Err(panic) => {
            let _ = events_tx.blocking_send(OperatorEvent::Panic(panic));
        }
    }

    Ok(())
}

#[pyclass]
#[derive(Clone)]
struct SendOutputCallback {
    events_tx: Sender<OperatorEvent>,
}

#[allow(unsafe_op_in_unsafe_fn)]
mod callback_impl {

    use crate::operator::OperatorEvent;

    use super::SendOutputCallback;
    use dora_operator_api_python::{process_python_output, pydict_to_metadata, python_output_len};
    use eyre::{eyre, Context, Result};
    use pyo3::{pymethods, types::PyDict, PyObject, Python};
    use tokio::sync::oneshot;

    #[pymethods]
    impl SendOutputCallback {
        fn __call__(
            &mut self,
            output: &str,
            data: PyObject,
            metadata: Option<&PyDict>,
            py: Python,
        ) -> Result<()> {
            let data_len = python_output_len(&data, py)?;
            let mut sample = py.allow_threads(|| {
                let (tx, rx) = oneshot::channel();
                self.events_tx
                    .blocking_send(OperatorEvent::AllocateOutputSample {
                        len: data_len,
                        sample: tx,
                    })
                    .map_err(|_| eyre!("failed to send output to runtime"))?;
                let sample = rx
                    .blocking_recv()
                    .wrap_err("failed to request output sample")?
                    .wrap_err("failed to allocate output sample")?;
                Result::<_, eyre::Report>::Ok(sample)
            })?;

            process_python_output(&data, py, |data| {
                sample.copy_from_slice(data);
                Ok(())
            })?;

            let metadata = pydict_to_metadata(metadata)
                .wrap_err("failed to parse metadata")?
                .into_owned();

            let event = OperatorEvent::Output {
                output_id: output.to_owned().into(),
                metadata,
                data: Some(sample),
            };

            py.allow_threads(|| {
                self.events_tx
                    .blocking_send(event)
                    .map_err(|_| eyre!("failed to send output to runtime"))
            })?;

            Ok(())
        }
    }
}
