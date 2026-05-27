from __future__ import annotations

import requests

from ._constants import VERSION
from ._exceptions import QBudInvalidCredentialsError


class Client:

    client_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": f"qbud-python/{VERSION}",
    }

    _REQUEST_TIMEOUT_SECONDS = 30

    def __init__(self, assistant_access_key: str):
        if not assistant_access_key:
            raise QBudInvalidCredentialsError()
        self._assistant_access_key = assistant_access_key

    def _headers(self, extra: dict | None = None) -> dict:
        headers = dict(self.client_headers)
        headers["X-Assistant-Access-Key"] = self._assistant_access_key
        if extra:
            headers.update(extra)
        return headers

    def post(self, url, data: dict | None = None, extra_headers: dict | None = None) -> requests.models.Response:
        return requests.post(
            url,
            json=data or {},
            headers=self._headers(extra_headers),
            timeout=self._REQUEST_TIMEOUT_SECONDS,
        )
