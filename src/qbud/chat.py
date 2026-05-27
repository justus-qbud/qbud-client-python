from __future__ import annotations

import json

from ._client import Client
from ._constants import API_PATH, BASE_URL
from ._exceptions import QBudBaseException, QbudChatNotFound


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

    def serialize(self) -> dict:
        """Serializes the Chat instance to a JSON-safe dict (excluding the HTTP client)."""
        return {
            "assistant_id": self._assistant_id,
            "id": self._id,
            "access_key": self._access_key,
            "message_log": self._message_log,
        }

    @staticmethod
    def deserialize(chat_dict: dict) -> Chat:
        """Reconstructs a Chat instance from the dict produced by serialize()."""
        return Chat(
            assistant_id=chat_dict["assistant_id"],
            id=chat_dict["id"],
            access_key=chat_dict["access_key"],
            message_log=chat_dict.get("message_log"),
        )

    def save(self, path: str) -> None:
        """Saves the chat as a JSON file at the given path."""
        with open(path, mode="w") as f:
            json.dump(self.serialize(), f)

    @staticmethod
    def load(path: str) -> Chat:
        """Loads a chat from a JSON file previously written by save()."""
        with open(path, mode="r") as f:
            return Chat.deserialize(json.load(f))

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
            A dict with the assistant's reply: {"content": <str>, "role": "assistant"}.
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
        raise QBudBaseException(
            f"Failed to send message (status {response.status_code}): {response.text}"
        )
