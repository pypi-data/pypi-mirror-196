use std::str::FromStr;

use bytes::Bytes;
use ngrok::config::{
    OauthOptions,
    OidcOptions,
    Scheme,
};
use pyo3::{
    pymethods,
    types::PyByteArray,
    PyRefMut,
};

use crate::tunnel_builder::NgrokHttpTunnelBuilder;

#[pymethods]
#[allow(dead_code)]
impl NgrokHttpTunnelBuilder {
    /// The scheme that this edge should use.
    /// Defaults to [Scheme::HTTPS].
    pub fn scheme(self_: PyRefMut<Self>, scheme: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().scheme(
            Scheme::from_str(scheme.as_str())
                .unwrap_or_else(|_| panic!("Unknown scheme: {scheme:?}")),
        );
        drop(builder);
        self_
    }
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
    /// Enable gzip compression for HTTP responses.
    pub fn compression(self_: PyRefMut<Self>) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().compression();
        drop(builder);
        self_
    }
    /// Convert incoming websocket connections to TCP-like streams.
    pub fn websocket_tcp_conversion(self_: PyRefMut<Self>) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().websocket_tcp_conversion();
        drop(builder);
        self_
    }
    /// Reject requests when 5XX responses exceed this ratio.
    /// Disabled when 0.
    pub fn circuit_breaker(self_: PyRefMut<Self>, circuit_breaker: f64) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().circuit_breaker(circuit_breaker);
        drop(builder);
        self_
    }

    /// with_request_header adds a header to all requests to this edge.
    pub fn request_header(self_: PyRefMut<Self>, name: String, value: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().request_header(name, value);
        drop(builder);
        self_
    }
    /// with_response_header adds a header to all responses coming from this edge.
    pub fn response_header(self_: PyRefMut<Self>, name: String, value: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().response_header(name, value);
        drop(builder);
        self_
    }
    /// with_remove_request_header removes a header from requests to this edge.
    pub fn remove_request_header(self_: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().remove_request_header(name);
        drop(builder);
        self_
    }
    /// with_remove_response_header removes a header from responses from this edge.
    pub fn remove_response_header(self_: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().remove_response_header(name);
        drop(builder);
        self_
    }

    /// Credentials for basic authentication.
    /// If not called, basic authentication is disabled.
    pub fn basic_auth(self_: PyRefMut<Self>, username: String, password: String) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().basic_auth(username, password);
        drop(builder);
        self_
    }

    /// OAuth configuration.
    /// If not called, OAuth is disabled.
    pub fn oauth(
        self_: PyRefMut<Self>,
        provider: String,
        allow_emails: Option<Vec<String>>,
        allow_domains: Option<Vec<String>>,
        scopes: Option<Vec<String>>,
    ) -> PyRefMut<Self> {
        let mut oauth = OauthOptions::new(provider);
        if let Some(allow_emails) = allow_emails {
            allow_emails.iter().for_each(|v| {
                oauth = oauth.clone().allow_email(v);
            });
        }
        if let Some(allow_domains) = allow_domains {
            allow_domains.iter().for_each(|v| {
                oauth = oauth.clone().allow_domain(v);
            });
        }
        if let Some(scopes) = scopes {
            scopes.iter().for_each(|v| {
                oauth = oauth.clone().scope(v);
            });
        }

        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().oauth(oauth);
        drop(builder);
        self_
    }

    /// OIDC configuration.
    /// If not called, OIDC is disabled.
    pub fn oidc(
        self_: PyRefMut<Self>,
        issuer_url: String,
        client_id: String,
        client_secret: String,
        allow_emails: Option<Vec<String>>,
        allow_domains: Option<Vec<String>>,
        scopes: Option<Vec<String>>,
    ) -> PyRefMut<Self> {
        let mut oidc = OidcOptions::new(issuer_url, client_id, client_secret);
        if let Some(allow_emails) = allow_emails {
            allow_emails.iter().for_each(|v| {
                oidc = oidc.clone().allow_email(v);
            });
        }
        if let Some(allow_domains) = allow_domains {
            allow_domains.iter().for_each(|v| {
                oidc = oidc.clone().allow_domain(v);
            });
        }
        if let Some(scopes) = scopes {
            scopes.iter().for_each(|v| {
                oidc = oidc.clone().scope(v);
            });
        }

        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().oidc(oidc);
        drop(builder);
        self_
    }

    /// WebhookVerification configuration.
    /// If not called, WebhookVerification is disabled.
    pub fn webhook_verification(
        self_: PyRefMut<Self>,
        provider: String,
        secret: String,
    ) -> PyRefMut<Self> {
        let mut builder = self_.tunnel_builder.lock();
        *builder = builder.clone().webhook_verification(provider, secret);
        drop(builder);
        self_
    }
}
