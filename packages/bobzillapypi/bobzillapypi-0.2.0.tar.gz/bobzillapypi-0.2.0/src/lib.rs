use pyo3::{
    exceptions::PyValueError,
    pymodule,
    types::PyModule,
    wrap_pyfunction,
    PyErr,
    PyResult,
    Python,
};
use session::NgrokSessionBuilder;
use tracing::debug;

use crate::logging::log_level;

pub mod http;
pub mod logging;
pub mod session;
pub mod tcp;
pub mod tls;
pub mod tunnel;
pub mod tunnel_builder;

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn bobzillapypi(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(log_level, m)?)?;
    m.add_class::<NgrokSessionBuilder>()?;
    // turn on logging bridge by default, since user won't see unless they activate Python logging
    if let Err(e) = log_level(py, None) {
        debug!("Error enabling logging: {e:?}")
    }
    Ok(())
}

// Shorthand for PyValueError creation
pub(crate) fn py_err(message: impl Into<String>) -> PyErr {
    PyValueError::new_err(message.into())
}
