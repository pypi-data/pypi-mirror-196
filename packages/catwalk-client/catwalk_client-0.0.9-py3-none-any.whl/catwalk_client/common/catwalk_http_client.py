from os import environ

from urllib.request import Request

from ._http_client import HTTPClient
from .constants import (
    CATWALK_AUTH_HEADER,
    CATWALK_USER_AGENT_HEADER_VALUE,
)


class CatwalkHTTPClient(HTTPClient):
    def __init__(self, catwalk_url: str, auth_token: str, insecure: bool = True):
        super().__init__(
            catwalk_url or environ.get("CATWALK_URL"),
            auth_token or environ.get("CATWALK_AUTH_TOKEN"),
            insecure,
        )

    def _apply_headers(self, request: Request):
        self._add_auth_token_header(request, self.auth_token)
        self._add_user_agent_header(request, CATWALK_USER_AGENT_HEADER_VALUE)

    def _add_auth_token_header(self, request: Request, header_value: str = ""):
        request.add_header(CATWALK_AUTH_HEADER, f"Bearer {header_value}")
