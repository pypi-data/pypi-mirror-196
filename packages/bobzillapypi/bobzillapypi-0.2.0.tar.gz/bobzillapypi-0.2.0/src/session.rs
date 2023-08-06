use std::{
    sync::Arc,
    time::Duration,
};

// the lib.name and the pymodule below need to be 'ngrok' for that to be the python library
// name, so this has to explicitly set this as a crate with the '::' prefix
use ::ngrok::session::Session;
use ngrok::session::{
    SessionBuilder,
    Update,
};
use parking_lot::Mutex as SyncMutex;
use pyo3::{
    pyclass,
    pymethods,
    PyAny,
    PyErr,
    PyObject,
    PyRefMut,
    PyResult,
    Python,
};
use tracing::{
    debug,
    info,
};

use crate::{
    py_err,
    tunnel::remove_global_tunnel,
    tunnel_builder::{
        NgrokHttpTunnelBuilder,
        NgrokLabeledTunnelBuilder,
        NgrokTcpTunnelBuilder,
        NgrokTlsTunnelBuilder,
    },
};

/// The builder for an ngrok session.
#[pyclass]
#[allow(dead_code)]
pub(crate) struct NgrokSessionBuilder {
    raw_builder: Arc<SyncMutex<SessionBuilder>>,
}

#[pymethods]
impl NgrokSessionBuilder {
    fn __str__(&self) -> String {
        "ngrok_session_builder".to_string()
    }

    /// Create a new session builder
    #[new]
    pub fn new() -> Self {
        NgrokSessionBuilder {
            raw_builder: Arc::new(SyncMutex::new(Session::builder())),
        }
    }

    /// Configures the session to authenticate with the provided authtoken. You
    /// can [find your existing authtoken] or [create a new one] in the ngrok
    /// dashboard.
    ///
    /// See the [authtoken parameter in the ngrok docs] for additional details.
    ///
    /// [find your existing authtoken]: https://dashboard.ngrok.com/get-started/your-authtoken
    /// [create a new one]: https://dashboard.ngrok.com/tunnels/authtokens
    /// [authtoken parameter in the ngrok docs]: https://ngrok.com/docs/ngrok-agent/config#authtoken
    pub fn authtoken(self_: PyRefMut<Self>, authtoken: String) -> PyRefMut<Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder.clone().authtoken(authtoken);
        drop(builder);
        self_
    }

    /// Shortcut for calling [SessionBuilder::authtoken] with the value of the
    /// NGROK_AUTHTOKEN environment variable.
    pub fn authtoken_from_env(self_: PyRefMut<Self>) -> PyRefMut<Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder.clone().authtoken_from_env();
        drop(builder);
        self_
    }

    /// Configures how often the session will send heartbeat messages to the ngrok
    /// service to check session liveness.
    ///
    /// See the [heartbeat_interval parameter in the ngrok docs] for additional
    /// details.
    ///
    /// [heartbeat_interval parameter in the ngrok docs]: https://ngrok.com/docs/ngrok-agent/config#heartbeat_interval
    pub fn heartbeat_interval(self_: PyRefMut<Self>, heartbeat_interval: u32) -> PyRefMut<Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder
            .clone()
            .heartbeat_interval(Duration::new(heartbeat_interval.into(), 0));
        drop(builder);
        self_
    }

    /// Configures the duration to wait for a response to a heartbeat before
    /// assuming the session connection is dead and attempting to reconnect.
    ///
    /// See the [heartbeat_tolerance parameter in the ngrok docs] for additional
    /// details.
    ///
    /// [heartbeat_tolerance parameter in the ngrok docs]: https://ngrok.com/docs/ngrok-agent/config#heartbeat_tolerance
    pub fn heartbeat_tolerance(self_: PyRefMut<Self>, heartbeat_tolerance: u32) -> PyRefMut<Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder
            .clone()
            .heartbeat_tolerance(Duration::new(heartbeat_tolerance.into(), 0));
        drop(builder);
        self_
    }

    /// Configures the opaque, machine-readable metadata string for this session.
    /// Metadata is made available to you in the ngrok dashboard and the Agents API
    /// resource. It is a useful way to allow you to uniquely identify sessions. We
    /// suggest encoding the value in a structured format like JSON.
    ///
    /// See the [metdata parameter in the ngrok docs] for additional details.
    ///
    /// [metdata parameter in the ngrok docs]: https://ngrok.com/docs/ngrok-agent/config#metadata
    pub fn metadata(self_: PyRefMut<Self>, metadata: String) -> PyRefMut<Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder.clone().metadata(metadata);
        drop(builder);
        self_
    }

    /// Configures the network address to dial to connect to the ngrok service.
    /// Use this option only if you are connecting to a custom agent ingress.
    ///
    /// See the [server_addr parameter in the ngrok docs] for additional details.
    ///
    /// [server_addr parameter in the ngrok docs]: https://ngrok.com/docs/ngrok-agent/config#server_addr
    pub fn server_addr(self_: PyRefMut<Self>, addr: String) -> PyRefMut<Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder.clone().server_addr(addr);
        drop(builder);
        self_
    }

    /// Configures a function which is called when the ngrok service requests that
    /// this [Session] stops. Your application may choose to interpret this callback
    /// as a request to terminate the [Session] or the entire process.
    ///
    /// Errors returned by this function will be visible to the ngrok dashboard or
    /// API as the response to the Stop operation.
    ///
    /// Do not block inside this callback. It will cause the Dashboard or API
    /// stop operation to time out. Do not call [std::process::exit] inside this
    /// callback, it will also cause the operation to time out.
    pub fn handle_stop_command(self_: PyRefMut<'_, Self>, handler: PyObject) -> PyRefMut<'_, Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder.clone().handle_stop_command(move |_req| {
            let handler = handler.clone();
            async move {
                Python::with_gil(|py| -> PyResult<()> { handler.call(py, (), None).map(|_o| ()) })
                    .map_err(|e| format!("Callback error {e:?}"))
            }
        });

        drop(builder);
        self_
    }

    /// Configures a function which is called when the ngrok service requests
    /// that this [Session] updates. Your application may choose to interpret
    /// this callback as a request to restart the [Session] or the entire
    /// process.
    ///
    /// Errors returned by this function will be visible to the ngrok dashboard or
    /// API as the response to the Restart operation.
    ///
    /// Do not block inside this callback. It will cause the Dashboard or API
    /// stop operation to time out. Do not call [std::process::exit] inside this
    /// callback, it will also cause the operation to time out.
    pub fn handle_restart_command(
        self_: PyRefMut<'_, Self>,
        handler: PyObject,
    ) -> PyRefMut<'_, Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder.clone().handle_restart_command(move |_req| {
            let handler = handler.clone();
            async move {
                Python::with_gil(|py| -> PyResult<()> { handler.call(py, (), None).map(|_o| ()) })
                    .map_err(|e| format!("Callback error {e:?}"))
            }
        });

        drop(builder);
        self_
    }

    /// Configures a function which is called when the ngrok service requests
    /// that this [Session] updates. Your application may choose to interpret
    /// this callback as a request to update its configuration, itself, or to
    /// invoke some other application-specific behavior.
    ///
    /// Errors returned by this function will be visible to the ngrok dashboard or
    /// API as the response to the Restart operation.
    ///
    /// Do not block inside this callback. It will cause the Dashboard or API
    /// stop operation to time out. Do not call [std::process::exit] inside this
    /// callback, it will also cause the operation to time out.
    pub fn handle_update_command(
        self_: PyRefMut<'_, Self>,
        handler: PyObject,
    ) -> PyRefMut<'_, Self> {
        let mut builder = self_.raw_builder.lock();
        *builder = builder.clone().handle_update_command(move |req: Update| {
            let handler = handler.clone();
            async move {
                Python::with_gil(|py| -> PyResult<()> {
                    handler
                        .call(py, (req.version, req.permit_major_version), None)
                        .map(|_o| ())
                })
                .map_err(|e| format!("Callback error {e:?}"))
            }
        });

        drop(builder);
        self_
    }

    // Omitting these configurations:
    // tls_config(&mut self, config: rustls::ClientConfig)
    // connector(&mut self, connect: ConnectFn)

    /// Attempt to establish an ngrok session using the current configuration.
    pub fn connect<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        let builder = self.raw_builder.lock().clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            NgrokSessionBuilder::_connect(builder).await
        })
    }
}

impl NgrokSessionBuilder {
    async fn _connect(builder: SessionBuilder) -> Result<NgrokSession, PyErr> {
        builder
            .connect()
            .await
            .map(|s| {
                info!("Session created");
                NgrokSession {
                    raw_session: Arc::new(SyncMutex::new(s)),
                }
            })
            .map_err(|e| py_err(format!("failed to connect session, {e:?}")))
    }
}

impl Drop for NgrokSessionBuilder {
    fn drop(&mut self) {
        debug!("NgrokSessionBuilder drop");
    }
}

#[pyclass]
#[derive(Clone)]
pub(crate) struct NgrokSession {
    raw_session: Arc<SyncMutex<Session>>,
}

#[pymethods]
impl NgrokSession {
    fn __str__(&self) -> String {
        "ngrok_session".to_string()
    }

    /// Start building a tunnel backing an HTTP endpoint.
    pub fn http_endpoint(&self) -> NgrokHttpTunnelBuilder {
        let session = self.raw_session.lock().clone();
        NgrokHttpTunnelBuilder::new(session.clone(), session.http_endpoint())
    }

    /// Start building a tunnel backing a TCP endpoint.
    pub fn tcp_endpoint(&self) -> NgrokTcpTunnelBuilder {
        let session = self.raw_session.lock().clone();
        NgrokTcpTunnelBuilder::new(session.clone(), session.tcp_endpoint())
    }

    /// Start building a tunnel backing a TLS endpoint.
    pub fn tls_endpoint(&self) -> NgrokTlsTunnelBuilder {
        let session = self.raw_session.lock().clone();
        NgrokTlsTunnelBuilder::new(session.clone(), session.tls_endpoint())
    }

    /// Start building a labeled tunnel.
    pub fn labeled_tunnel(&self) -> NgrokLabeledTunnelBuilder {
        let session = self.raw_session.lock().clone();
        NgrokLabeledTunnelBuilder::new(session.clone(), session.labeled_tunnel())
    }

    /// Close a tunnel with the given ID.
    pub fn close_tunnel<'a>(&self, py: Python<'a>, id: String) -> PyResult<&'a PyAny> {
        let session = self.raw_session.lock().clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            NgrokSession::_close_tunnel(session, id).await
        })
    }
}

impl NgrokSession {
    async fn _close_tunnel(session: Session, id: String) -> Result<(), PyErr> {
        // close tunnel
        let res = session
            .close_tunnel(id.clone())
            .await
            .map_err(|e| py_err(format!("failed to close tunnel, {e:?}")));

        if res.is_ok() {
            // remove our reference to allow it to drop
            remove_global_tunnel(&id).await;
        }
        res
    }
}

impl Drop for NgrokSession {
    fn drop(&mut self) {
        debug!("NgrokSession drop");
    }
}
