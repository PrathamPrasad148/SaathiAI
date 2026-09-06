# Saathi AI — System Application Flow
### Architecture by **Pratham Prasad**

```text
================================================================================
                         SAATHI AI APPLICATION PIPELINE
                        Engineered by Pratham Prasad
================================================================================
```

## 1. System Boot & Initialization Sequence

```text
[main.py: Application Entry Point]
       |
       +---> Check Python 3.12 Environment & Runtime Flags
       |
       +---> Instantiate SaathiApp Controller (ui/app.py)
       |        |
       |        +---> Initialize High-Contrast FUI Theme Tokens (ui/theme.py)
       |        +---> Bootstrap 60 FPS Hardware Vector HUD Canvas (ui/ai_core.py)
       |        +---> Setup Telemetry Deck & Navigation Matrix (ui/telemetry.py)
       |        +---> Initialize Local Persistence & Schemas (memory/storage.py)
       |        +---> Bind Windows System Tray Icon & Intercept Handlers
       |
       +---> Start Background System Daemon Workers
                |
                +---> Ollama Engine Health & Model Discovery Daemon
                +---> Acoustic Engine Listener & VAD Service (voice/)
                +---> Smart Reminder & Scheduler Cron Loop (20s cycle)
                +---> Automation Queue Dispatcher (automations/engine.py)
```

---

## 2. Multi-Modal Cognitive Communication Flow

```text
[User Input: Microphone or Keyboard Directive]
       |
       +--- [Acoustic Branch] ---> faster-whisper On-Device Transcriber
       |                                   |
       |                                   v (Stream text to prompt buffer)
       +--- [Text Input Branch]  ---> Directive Input Stream Deck
                                           |
                                           v
                             [Intent Pre-Processor & Filter]
                                           |
             +-----------------------------+-----------------------------+
             |                                                           |
      [Direct Shortcut]                                           [Agent Reasoning]
  (Volume, Theme, Exit, Clear)                                            |
             |                                             Ollama /api/chat Native Loop
             v                                                           |
   Immediate Execution                                     +-------------+-------------+
                                                           |                           |
                                                      [Tool Calls]               [Direct Text]
                                                           |                           |
                                                  Execute Tool Dispatcher              |
                                                  (Sandboxed with Confirmation)        |
                                                           |                           |
                                                           +------------+--------------+
                                                                        |
                                                                        v
                                                            [Synthesize Spoken Audio]
                                                            (edge-tts Indian-English)
                                                                        |
                                                                        v
                                                             Update 60 FPS Visualizer
                                                             (Waveform & Spectrum EQ)
```

---

## 3. Sandboxed Tool Execution Pipeline

```text
Model Emits Tool Call: { name: "run_command", args: { ... } }
       |
       v
Check Permission Policy:
       |
       +---> Is Target Path Protected? (e.g., Windows root, System32)
       |        `---> YES: Terminate with Security Exception.
       |
       +---> Is Action High-Impact or Destructive? (Delete, Move, Execute)
                |
                +---> YES: Trigger Tactical User Confirmation Dialog
                |        |
                |        +---> User Approves: Run in Subprocess / File System
                |        `---> User Rejects:  Abort with User Rejection Feedback
                |
                `---> NO: Execute Silently in Background & Return Payload
       |
       v
Inject Tool Response Payload into Conversation Context (`role: tool`)
       |
       v
Allow Model to Complete Multi-Step Reasoning Cycle (Max 4 Iterations)
```

---

## 4. Autonomous Web & Project Generation Flow

```text
User Requests: "Build a cybernetic dashboard landing page"
       |
       v
Cognitive Co-Pilot Activates Project Builder Module
       |
       +---> Resolve target path: Projects/<ProjectName>/
       +---> Apply UI/UX Pro Max standards & 21st.dev component blueprints
       +---> Synthesize complete static or modern stack assets:
       |        |-- index.html (Responsive, semantic, accessible)
       |        |-- style.css  (Modern CSS variables, animations, dark mode)
       |        `-- app.js     (Vanilla JavaScript or component logic)
       +---> Record build log in Mission Telemetry stream
       `---> Automatically launch rendered application in default Windows browser
```

---

## 5. Lifecycle & Teardown Protocol

- **Window Close Event**: Application intercepts window closure; minimizes smoothly to the Windows System Tray to maintain background monitoring and reminder dispatching without consuming primary screen real estate.
- **Graceful Termination**: User can quit cleanly via system tray or command center; saves conversation state, releases audio hardware devices, terminates worker threads safely, and cleanly closes the Tk event loop.
