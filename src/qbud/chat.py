from __future__ import annotations

from ._client import Client
from ._constants import API_PATH, BASE_URL
from ._exceptions import QbudChatNotFound


class Chat:

    def __init__(
        self,
        assistant_id: str,
        id: str,
        access_key: str,
        message_log: list | None = None,
        client: Client | None = None
    ):
        self._assistant_id = assistant_id
        self._id = id
        self._access_key = access_key
        self._message_log = message_log if message_log else []
        self._client = client if client else Client()

    @property
    def assistant_id(self):
        return self._assistant_id

    @property
    def id(self):
        return self._id

    @property
    def key(self):
        return self._access_key

    def get_messages(self) -> list[dict]:
        """Returns an overview of the local message history.

        Returns:
             A list of dicts, each of which has a "content" key with the message content and a "role" key to show if
                the message was sent by the "user" or the "assistant".
        """
        return self._message_log

    def send_message(self, message: str) -> dict:
        """Sends a message to the chat to which the current instance is connected. Also adds messages to the
        message_log.

        Args:
            message: the message to be sent.

        Returns:
            A dict with the reply mapped to the key "content" and
        """
        url = f"{BASE_URL}{API_PATH}/assistants/{self._assistant_id}/chats/{self._id}"
        response = self._client.post(url, {"prompt": message, "access_key": self._access_key})
        if response.status_code == 200:
            response_message = {
                "content": response.json()["data"]["message"]["content"],
                "role": "assistant"
            }
            self._message_log.extend([{"content": message, "role": "user"}, response_message])
            return response_message
        elif response.status_code == 404:
            raise QbudChatNotFound()
