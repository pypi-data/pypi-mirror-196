use pyo3::{
    pymethods,
    PyRefMut,
};

use crate::tunnel_builder::NgrokTcpTunnelBuilder;

#[pymethods]
#[allow(dead_code)]
impl NgrokTcpTunnelBuilder {
    /// The TCP address to request for this edge.
    pub fn remote_addr(self_: PyRefMut<Self>, remote_addr: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().remote_addr(remote_addr);
        drop(builder);
        self_
    }
}
