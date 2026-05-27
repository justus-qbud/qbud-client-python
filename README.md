## qBud Python Client
`qbud` helps to make interaction with qBud assistants easier. Its aim is to provide a low-code solution for interactions with assistants that you have configured via the UI.

### How to Install
Installing is easy:
```commandline
pip install qbud
```
We recommend `python>=3.9`, but the client may run with older versions as well. The only external dependency is the widely used `requests` library, which is installed when running the above command.

### Configuration
Authentication is done with a per-assistant access key, generated from your account.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `QBUD_ASSISTANT_ACCESS_KEY` | yes* | — | Access key for the assistant. *Optional if you pass `access_key=...` to `Assistant()` directly. |
| `QBUD_BASE_URL` | no | `https://api.qbud.ai` | Override the API host (e.g. for staging). |

### Quickstart

#### 1. Connect to an assistant
Make sure you have built an assistant via our UI. When you're editing the assistant there, copy the ID from the address bar (after `/assistants/`) and pair it with your assistant access key:
```python
from qbud import Assistant

assistant = Assistant("<your-assistant-id>", access_key="<your-access-key>")
# or, with QBUD_ASSISTANT_ACCESS_KEY set in the environment:
assistant = Assistant("<your-assistant-id>")
```

#### 2. Send messages
Create a chat with `assistant.create_chat()` and call `send_message(...)` on it:
```python
chat = assistant.create_chat()
response = chat.send_message("Hi!")
print(response)
> {"content": "Hi there!", "role": "assistant"}
```

### Saving and loading chats
By design, chat message history cannot be retrieved from our API. If you need history across sessions, save chats locally:
```python
from qbud import Chat

# save a Chat object as JSON (message history only — the access key is
# never written to disk, since it is a bearer credential for the chat)
chat.save("chat.json")

# ...session terminates

# load a Chat instance from the saved JSON. The result is read-only:
# get_messages() works, but send_message() requires a live chat created
# via Assistant.create_chat().
chat = Chat.load("chat.json")
```

You can also inspect the in-memory history with `get_messages(...)`:
```python
print(chat.get_messages())
> [{"content": "Hi!", "role": "user"}, {"content": "Hi there!", "role": "assistant"}]
```
