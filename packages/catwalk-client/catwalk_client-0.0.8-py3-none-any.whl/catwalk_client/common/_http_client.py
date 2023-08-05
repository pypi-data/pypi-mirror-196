from __future__ import annotations

from json import loads
from ssl import SSLContext, CERT_NONE, create_default_context
from typing import Any, Optional

from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, Request


class HTTPClient:
    def __init__(self, url: str, auth_token: str, insecure: bool = True):
        self.url = url
        self.auth_token = auth_token
        self.insecure = insecure

    def get_url(self, path: str):
        return self.url.rstrip("/") + path

    def get(
        self, url_postfix: str, query_params: Optional[dict[str, Any]] = None
    ) -> tuple[str, bool]:
        url = self.get_url(url_postfix) + self._encode_query_params(query_params)
        req = Request(url=url)
        return self._make_request(req)

    def post(
        self,
        url_postfix: str,
        payload: str,
        query_params: Optional[dict[str, Any]] = None,
    ) -> tuple[str, bool]:
        url = self.get_url(url_postfix) + self._encode_query_params(query_params)
        req = Request(url=url, data=payload.encode())
        req.add_header("Content-Type", "application/json")
        return self._make_request(req)

    def _make_request(self, request: Request):
        self._apply_headers(request)
        try:
            resp = urlopen(request, timeout=5, context=self._get_ssl_context())
        except HTTPError as e:
            e_body = self._parse_http_error_json(e)
            return f"Error: {e}\n[URL] {e.geturl()}\n[DETAILS] {e_body}", False
        except URLError as e:
            return f"Connection error: {e.reason}", False

        return resp.read().decode(), True

    def _parse_http_error_json(self, error: HTTPError):
        if error.headers.get_content_type() == "application/json":
            return loads(error.read().decode())
        return None

    def _get_ssl_context(self) -> SSLContext:
        ctx = create_default_context()
        if self.insecure:
            ctx.check_hostname = False
            ctx.verify_mode = CERT_NONE
        return ctx

    def _encode_query_params(self, query_params: Optional[dict[str, Any]]) -> str:
        if query_params is None or len(query_params) == 0:
            return ""
        encoded_params = urlencode(query_params)
        return "?" + encoded_params

    def _apply_headers(self, request: Request):
        self._add_user_agent_header(request)
        self._add_auth_token_header(request, self.auth_token)

    def _add_auth_token_header(self, request: Request, header_value: str = ""):
        request.add_header("Authorization", f"Bearer {header_value}")

    def _add_user_agent_header(
        self, request: Request, header_value: str = "Request/1.0"
    ):
        if not request.has_header("User-Agent"):
            request.add_header("User-Agent", header_value)
