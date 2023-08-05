#![allow(clippy::borrow_deref_ref)] // clippy warns about code generated by #[pymethods]

use dora_node_api::{DoraNode, EventStream};
use dora_operator_api_python::{process_python_output, pydict_to_metadata, PyEvent};
use eyre::Context;
use pyo3::prelude::*;
use pyo3::types::PyDict;

/// The custom node API lets you integrate `dora` into your application.
/// It allows you to retrieve input and send output in any fashion you want.
///
/// Use with:
///
/// ```python
/// from dora import Node
///
/// node = Node()
/// ```
///
#[pyclass]
pub struct Node {
    events: EventStream,
    node: DoraNode,
}

#[pymethods]
impl Node {
    #[new]
    pub fn new() -> eyre::Result<Self> {
        let (node, events) = DoraNode::init_from_env()?;

        Ok(Node { events, node })
    }

    /// `.next()` gives you the next input that the node has received.
    /// It blocks until the next input becomes available.
    /// It will return `None` when all senders has been dropped.
    ///
    /// ```python
    /// input_id, value, metadata = node.next()
    /// ```
    ///
    /// You can also iterate over the node in a loop
    ///
    /// ```python
    /// for input_id, value, metadata in node:
    /// ```
    #[allow(clippy::should_implement_trait)]
    pub fn next(&mut self, py: Python) -> PyResult<Option<PyEvent>> {
        self.__next__(py)
    }

    pub fn __next__(&mut self, py: Python) -> PyResult<Option<PyEvent>> {
        let event = py.allow_threads(|| self.events.recv());
        Ok(event.map(PyEvent::from))
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    /// `send_output` send data from the node.
    ///
    /// ```python
    /// Args:
    ///    output_id: str,
    ///    data: Bytes|Arrow,
    ///    metadata: Option[Dict],
    /// ```
    ///
    /// ```python
    /// node.send_output("string", b"string", {"open_telemetry_context": "7632e76"})
    /// ```
    ///
    pub fn send_output(
        &mut self,
        output_id: String,
        data: PyObject,
        metadata: Option<&PyDict>,
        py: Python,
    ) -> eyre::Result<()> {
        process_python_output(&data, py, |data| {
            self.send_output_slice(output_id, data.len(), data, metadata)
        })
    }

    /// Returns the full dataflow descriptor that this node is part of.
    ///
    /// This method returns the parsed dataflow YAML file.
    pub fn dataflow_descriptor(&self, py: Python) -> pythonize::Result<PyObject> {
        pythonize::pythonize(py, self.node.dataflow_descriptor())
    }
}

impl Node {
    fn send_output_slice(
        &mut self,
        output_id: String,
        len: usize,
        data: &[u8],
        metadata: Option<&PyDict>,
    ) -> eyre::Result<()> {
        let metadata = pydict_to_metadata(metadata)?;
        self.node
            .send_output(output_id.into(), metadata, len, |out| {
                out.copy_from_slice(data);
            })
            .wrap_err("failed to send output")
    }

    pub fn id(&self) -> String {
        self.node.id().to_string()
    }
}

/// Start a runtime for Operators
#[pyfunction]
fn start_runtime() -> eyre::Result<()> {
    dora_runtime::main().wrap_err("Dora Runtime raised an error.")
}

#[pymodule]
fn dora(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_runtime, m)?)?;
    m.add_class::<Node>().unwrap();
    Ok(())
}
