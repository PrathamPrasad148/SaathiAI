# Saathi AI — Technical Specification
### Engineered by **Pratham Prasad**

```text
================================================================================
                    SAATHI AI TECHNICAL SPECIFICATION & STACK
                           Engineered by Pratham Prasad
================================================================================
```

## 1. System Architecture Overview

Saathi AI is an event-driven, multithreaded desktop operating system and cognitive co-pilot built natively in Python for Windows.

```text
+-------------------------------------------------------------------------------+
|                       PRATHAM PRASAD // SAATHI AI HUD                         |
+-------------------------------------------------------------------------------+
|  Top Telemetry Deck (ui/telemetry.py): Clock, FPS, CPU Load, Model Switcher   |
+---------------------------------------+---------------------------------------+
|  AI Core Vector Canvas (ui/ai_core):  |  Tactical Deck (ui/command_center):   |
|  - 60 FPS Canvas Redraw Engine        |  - Scrollable Multi-Turn Chat Log     |
|  - 28-Node Synaptic Plexus & Pulses   |  - Real-Time Action & Status Badges   |
|  - High-Voltage Arc Reactor & Sparks  |  - Instant Directive Stream Input Bar |
|  - 3D Gyroscope & 360 Tactical Radar  |  - Mic VAD & Spoken Speech Controls   |
+---------------------------------------+---------------------------------------+
|  Background Multi-Threaded Engine Subsystems:                                 |
|  - Ollama Agent Reasoning Client      |  - faster-whisper On-Device STT       |
|  - Autonomous Tool Dispatcher         |  - edge-tts Audio Neural Synthesizer  |
|  - Windows Automations & Shell Bridge |  - 20-Second Scheduler & Cron Worker  |
+---------------------------------------+---------------------------------------+
```

---

## 2. Technology Stack & Dependencies

- **Language & Runtime**: Python 3.12 64-bit on Windows 10/11
- **User Interface Framework**: Python Tkinter (Native Windows Win32 graphics bridge)
- **Local AI Inference Engine**: Ollama HTTP API (`http://127.0.0.1:11434`)
  - Default Model: `qwen2.5:7b` (High-speed tool execution & coding)
  - Secondary Models: `qwen3:14b`, `qwen3:4b-instruct`
- **Speech-to-Text**: `faster-whisper` (CTranslate2-optimized local Whisper)
- **Speech Synthesis**: `edge-tts` (Microsoft Neural Speech API with Indian-English voice profile)
- **Audio Output & Channels**: `pygame` mixer streaming
- **Computer Vision & Capture**: `Pillow` (`ImageGrab`)
- **System Tray Integration**: `pystray` Windows shell notifications
- **Safe File Management**: `send2trash` recycle bin bridge

---

## 3. Concurrency & Performance Model

1. **Main UI Thread**:
   - Manages the Tkinter event loop, canvas vector rendering, and input focus.
   - Vector canvas uses mathematical coordinate calculations with batch canvas updates to achieve smooth 50-60 FPS performance without lagging user input.

2. **Asynchronous Worker Thread Pool**:
   - `_reply_worker`: Manages multi-turn network streaming with the local Ollama daemon.
   - `_speech_worker`: Streams and synthesizes audio without freezing the HUD.
   - `_transcribe_worker`: Processes raw audio PCM buffers through Whisper.
   - `_reminder_checker_loop`: Autonomous daemon waking every 20 seconds to monitor scheduled directives.

3. **Message & State Synchronization**:
   - Worker threads push structured events into `queue.Queue` buffers (`reply_queue`, `status_queue`).
   - The UI thread polls queues during frame ticks using `root.after(50, self._process_queues)`.

---

## 4. Security & Isolation Matrix

| Capability | Policy | Implementation Mechanism |
| :--- | :--- | :--- |
| **System Terminal Commands** | Restricted / Human Approval Required | `confirm_action` modal displaying exact command line. |
| **File Deletions / Moves** | Restricted / Human Approval Required | `confirm_action` modal displaying source and destination. |
| **Protected System Folders** | Strictly Forbidden | Path validation against system blacklists. |
| **Conversation Memory** | 100% On-Device | Plaintext / JSON stored locally in `data/history.json`. |
| **External Network Calls** | Read-Only Live Endpoints | wttr.in (weather), Wikipedia, open exchange APIs. |
