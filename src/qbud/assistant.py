from __future__ import annotations

from .chat import Chat
from ._client import Client
from ._constants import BASE_URL, API_PATH
from ._exceptions import QBudAssistantNotFound, QBudBaseException


class Assistant:

    def __init__(self, id: str, client: Client | None = None):
        if not isinstance(id, str) or not id:
            raise TypeError("Assistant id must be a non-empty string.")
        self._id = id
        self._client = client

    @property
    def id(self):
        return self._id

    def _get_client(self) -> Client:
        if self._client is None:
            self._client = Client()
        return self._client

    def create_chat(self) -> Chat:
        """Requests a new chat from the API and creates the corresponding Chat instance.

        Returns:
             The created Chat instance.
        """
        client = self._get_client()
        response = client.post(f"{BASE_URL}{API_PATH}/assistants/{self._id}/chats")
        if response.status_code == 201:
            response_data = response.json()["data"]["chat"]
            return Chat(
                assistant_id=self.id,
                id=response_data.get("id"),
                access_key=response_data.get("access_key"),
                client=client
            )
        elif response.status_code == 404:
            raise QBudAssistantNotFound()
        raise QBudBaseException(
            f"Failed to create chat (status {response.status_code}): {response.text}"
        )

