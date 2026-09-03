# Saathi AI Data Schema

## Conversation History

File: `data/history.json`

```json
[
  ["user", "Remind me in ten minutes"],
  ["assistant", "Reminder set kar diya."]
]
```

Each entry is an array with a role and message text. Supported persisted roles are normally `user` and `assistant`; transient display roles may include `action` and `system`.

## Reminders

File: `data/reminders.json`

```json
[
  {
    "text": "Call mom",
    "when": "2026-09-03T18:30:00",
    "done": false
  }
]
```

`when` is a local ISO datetime. `done` prevents repeated notification.

## Notes

File: `data/notes.txt`

```text
[2026-09-03 18:00] Buy milk tomorrow
```

Notes are append-only timestamped UTF-8 text lines.

## Ollama Message Shape

```json
{
  "model": "qwen2.5:7b",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "tools": [],
  "keep_alive": "60m",
  "stream": false
}
```

Tool responses are appended with role `tool`; assistant tool-call messages may include `tool_calls`.

## Tool Contract

Each tool schema has a function name, description, JSON parameter object, and required fields. Tool execution returns a string suitable for both status display and model context. New tools must preserve this contract.

## Compatibility Rules

Readers must tolerate missing files, invalid JSON, empty arrays, and older entries. Writes should use UTF-8 and should preserve only the intended retention limit for history.
