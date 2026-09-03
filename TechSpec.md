# Saathi AI Technical Specification

## Architecture

Saathi is a single-process Python desktop application built with Tkinter. The `Saathi` class owns UI state, local persistence, command routing, tool execution, background workers, and lifecycle management.

```text
Tkinter UI
  |-- direct shortcut handlers
  |-- conversation history
  |-- status/reply queues
  '-- Ollama HTTP client
          '-- model response and tool calls

Local files: data/history.json, data/reminders.json, data/notes.txt
External services: Ollama, wttr.in, ExchangeRate API, Wikipedia, Edge TTS
Windows integrations: os.startfile, tray icon, clipboard, screenshots
```

## Runtime

- Python 3.12 is the documented target.
- Tkinter is used for the native UI.
- Ollama is expected at `http://127.0.0.1:11434`.
- Default coding model: `qwen2.5:7b`.
- Optional packages are listed in `requirements.txt`.

## Concurrency

Tkinter must remain on the main thread. Ollama requests, speech synthesis, and microphone transcription run in worker threads. Workers communicate with the UI through `reply_queue`, `status_queue`, and `root.after(...)` callbacks.

## Model and Tool Protocol

The application sends a system prompt, recent conversation messages, the selected model, and `TOOLS_SCHEMA` to Ollama's `/api/chat` endpoint. Tool calls are executed locally, their results are appended to the conversation, and the model may continue for up to four iterations before a final reply is displayed.

## Persistence

- `data/history.json`: recent role/text message tuples, capped during save.
- `data/reminders.json`: reminder objects containing text, ISO timestamp, and completion state.
- `data/notes.txt`: timestamped append-only notes.

All paths are derived from `APP_DIR`; required directories are created during initialization.

## Error Handling

Network, model, audio, and file errors should be converted into user-visible messages or safe fallback values. Background failures must not crash the Tkinter event loop. Timeouts should explain that CPU inference may be slow and suggest the lightweight model.

## Security

Resolve relative paths against `APP_DIR`. Use protected-path checks before destructive operations. Require confirmation for command execution and destructive file operations. Do not log secrets or expose private local data in external queries.

## Extension Guidance

New tools require a schema entry, an `execute_tool` branch, confirmation policy, user-facing status handling, and a focused test or manual verification path. New web-generation behavior belongs in the system prompt and the 21st.dev/UI UX skill guidance, not in Tkinter rendering code.
