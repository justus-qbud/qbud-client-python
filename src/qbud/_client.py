from __future__ import annotations

import base64
import os
import threading
import time

import requests

from ._constants import BASE_URL, VERSION
from ._exceptions import QBudAuthenticationError, QBudInvalidCredentialsError


class Client:

    client_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": f"qbud-python/{VERSION}",
    }

    # Re-mint slightly before the server's stated expiry to avoid clock-skew 401s.
    _EXPIRY_SKEW_SECONDS = 30
    _REQUEST_TIMEOUT_SECONDS = 30

    def __init__(self):
        self.access_token = None
        self.access_token_expires_at = 0.0
        self.client_id = os.getenv('QBUD_CLIENT_ID')
        self.client_secret = os.getenv('QBUD_CLIENT_SECRET')
        self._token_lock = threading.Lock()
        if not self.client_id or not self.client_secret:
            raise QBudInvalidCredentialsError()

    def _get_headers(self, auth_type: str, extra: dict | None = None):
        headers = dict(self.client_headers)
        if auth_type == "access":
            headers["Authorization"] = "Bearer " + self.access_token
        elif auth_type == "login":
            headers["Authorization"] = "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        if extra:
            headers.update(extra)
        return headers

    def _mint_access_token(self) -> None:
        """Exchanges client credentials for a fresh access token via /auth/token."""
        response = requests.post(
            f"{BASE_URL}/auth/token",
            json={},
            headers=self._get_headers("login"),
            timeout=self._REQUEST_TIMEOUT_SECONDS,
        )
        if response.status_code == 401:
            raise QBudInvalidCredentialsError()
        if response.status_code != 200:
            raise QBudAuthenticationError(f"Failed to obtain access token (status {response.status_code}).")

        data = response.json().get("data") or {}
        self.access_token = data.get("access_token")
        expires_in = data.get("access_token_expires") or 0
        self.access_token_expires_at = time.time() + max(0.0, expires_in - self._EXPIRY_SKEW_SECONDS)

    def _ensure_access_token(self) -> None:
        with self._token_lock:
            if self.access_token is None or time.time() >= self.access_token_expires_at:
                self._mint_access_token()

    def post(self, url, data: dict = None, extra_headers: dict | None = None, recursive: bool = False) -> requests.models.Response:
        """Sends an authenticated POST. On 401, re-mints the access token once and retries."""
        self._ensure_access_token()

        response = requests.post(
            url,
            json=data or {},
            headers=self._get_headers("access", extra=extra_headers),
            timeout=self._REQUEST_TIMEOUT_SECONDS,
        )
        if response.status_code == 401:
            if recursive:
                raise QBudInvalidCredentialsError()
            self.access_token = None
            return self.post(url, data, extra_headers=extra_headers, recursive=True)

        return response
