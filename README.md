## qBud Python Client
`qbud` helps to make interaction with qBud assistants easier. Its aim is to provide a low-code solution for interactions with assistants that you have configured via the UI.

### How to Install
Installing is easy:
```commandline
pip install qbud
```
We recommend `python>=3.9`, but the client may run with older versions as well. The only external dependency is the widely used `requests` library, which is installed when running the above command.

### Quickstart
You can quickly get started by following the steps below:

#### 1. Configure credentials
The client consumes the environment variables `QBUD_CLIENT_ID` and `QBUD_CLIENT_SECRET`. Retrieve your credentials from [the application](https://app.qbud.ai/account) and set them. Never send credentials to others.

#### 2. Connect to an assistant
Make sure you have built an assistant via our UI. When you're editing the assistant there, copy the ID from the address bar (after '/assistants/') to connect with our client.
```python
from qbud import Assistant

assistant = Assistant("<your-assistant-id>")
```

#### 3. Send messages
Sending messages is simple. Create a `Chat` instance for the relevant assistant and call `send_message(...)` with whatever you'd like to send:
```python
chat = assistant.create_chat()
response = chat.send_message("Hi!")
print(response)
> {"content": "Hi there!", "role": "assistant"}
```

### Other features
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