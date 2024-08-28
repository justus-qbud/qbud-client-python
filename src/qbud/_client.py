from __future__ import annotations

import base64
import os
import requests

from ._constants import BASE_URL, API_PATH
from ._exceptions import QBudAuthenticationError, QBudInvalidCredentialsError


class Client:

    client_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.client_id = os.getenv('QBUD_CLIENT_ID')
        self.client_secret = os.getenv('QBUD_CLIENT_SECRET')
        if not self.client_id or not self.client_secret:
            raise QBudAuthenticationError("You need to set 'QBUD_CLIENT_ID' and 'QBUD_CLIENT_SECRET' environment variables.")

    def _get_headers(self, auth_type: str):
        """Copies the default client headers and adds an Authorization header.

        Args:
            auth_type: adds the relevant credentials based on if the access token, refresh token or client credentials
            are required.

        Returns:
            A dict with all necessary request headers.
        """
        headers = dict(self.client_headers)
        if auth_type == "access":
            headers["Authorization"] = "Bearer " + self.access_token
        elif auth_type == "refresh":
            headers["Authorization"] = "Bearer " + self.refresh_token
        elif auth_type == "login":
            headers["Authorization"] = "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        return headers

    def retrieve_tokens(self, refresh: bool = False) -> None:
        """Gets new JWTs from the authentication service.

        Args:
            refresh: specifies if tokens should be retrieved via client credentials or a previously issued refresh
                token.
        """
        url = f"{BASE_URL}/auth/" + ("refresh" if refresh else "token")
        headers = self._get_headers("refresh" if refresh else "login")
        response = requests.post(url, data={}, headers=headers)
        if response.status_code == 401:
            raise QBudAuthenticationError()

        if response.status_code == 200:
            response_json = response.json().get("data")
            self.access_token = response_json.get("access_token")
            self.refresh_token = response_json.get("refresh_token")

    def post(self, url, data: dict = None, recursive: bool = False) -> requests.models.Response:
        """Defines the control flow and format of POST requests.

        Args:
            url: the full URL to which the POST request is made.
            data: a dict that is convertible to JSON. Used as payload in the request. Defaults to None, which is treated
                as an empty payload.
            recursive: if a request fails because of 401, the original request is attempted again by recursively calling
                post(). This flag prevents an infinite loop of refreshes.

        Returns:
            Upon a successful request: a dictionary with the JSON response.

        Raises:
            QbudInvalidCredentialsError: if 401 is returned by the endpoint and tokens cannot be refreshed successfully.
        """
        if self.access_token is None:
            self.retrieve_tokens()

        response = requests.post(url, json=data or {}, headers=self._get_headers("access"))
        if response.status_code == 401:
            if recursive:
                raise QBudInvalidCredentialsError()
            self.retrieve_tokens(refresh=True)
            return self.post(url, data, recursive=True)

        return response
