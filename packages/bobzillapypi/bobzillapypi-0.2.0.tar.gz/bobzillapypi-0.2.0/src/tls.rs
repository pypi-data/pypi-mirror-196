use bytes::Bytes;
use pyo3::{
    pymethods,
    types::PyByteArray,
    PyRefMut,
};

use crate::tunnel_builder::NgrokTlsTunnelBuilder;

#[pymethods]
#[allow(dead_code)]
impl NgrokTlsTunnelBuilder {
    /// The domain to request for this edge.
    pub fn domain(self_: PyRefMut<Self>, domain: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().domain(domain);
        drop(builder);
        self_
    }
    /// Certificates to use for client authentication at the ngrok edge.
    pub fn mutual_tlsca<'a>(
        self_: PyRefMut<'a, Self>,
        mutual_tlsca: &PyByteArray,
    ) -> PyRefMut<'a, Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder
            .clone()
            .mutual_tlsca(Bytes::from(mutual_tlsca.to_vec()));
        drop(builder);
        self_
    }
    /// The key to use for TLS termination at the ngrok edge in PEM format.
    pub fn termination<'a>(
        self_: PyRefMut<'a, Self>,
        cert_pem: &PyByteArray,
        key_pem: &PyByteArray,
    ) -> PyRefMut<'a, Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().termination(
            Bytes::from(cert_pem.to_vec()),
            Bytes::from(key_pem.to_vec()),
        );
        drop(builder);
        self_
    }
}
