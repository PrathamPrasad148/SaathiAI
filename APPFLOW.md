# Saathi AI Application Flow

## Startup

1. Python starts `main.py`.
2. `Saathi.__init__` creates the Tk root and initializes paths, state, theme, persistence, UI, tray icon, queues, and reminder polling.
3. The UI opens with Chat & Agent, Projects & Tools, and Settings tabs.
4. Ollama availability is checked shortly after rendering.

## Chat Flow

```text
User types or speaks
        |
        v
process_user_text
        |
        +--> direct shortcut? --> execute local handler --> append reply
        |
        '--> start_next_reply --> worker thread
                                  |
                                  v
                           Ollama /api/chat
                                  |
                  +---------------+---------------+
                  |                               |
             tool calls                       final text
                  |                               |
          execute_tool loop                 reply_queue
                  |                               |
                  '------------> process_queues --> chat log + speech
```

## Voice Flow

The user presses Voice. Saathi records a short microphone sample, transcribes it with faster-whisper, and forwards non-empty text through the normal chat path. The final assistant message may be spoken with Edge TTS.

## File and Command Flow

1. The model or direct command identifies an operation.
2. The operation resolves a path or target.
3. Saathi checks protected paths and permission policy.
4. A confirmation dialog appears for risky operations.
5. The operation runs and returns a concise result.
6. The result is shown as an action/status entry and included in the assistant context.

## Reminder Flow

Reminders are loaded at startup, checked every 20 seconds, marked done when due, displayed in chat, spoken aloud, and persisted again.

## Website Generation Flow

1. The user requests a website or 21st.dev-inspired component.
2. The model receives UI/UX Pro Max and 21st.dev integration guidance.
3. The model detects the target stack.
4. It creates complete local files under `Projects/<ProjectName>/`.
5. Static HTML projects receive HTML/CSS/JavaScript; React projects receive local React components.
6. The generated page is opened in the default browser when applicable.

## Shutdown

Closing the window saves history and destroys the Tk root. The tray menu can show the window or quit the application.
