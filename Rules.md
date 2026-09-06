# Saathi AI — Engineering & Security Governance Rules
### Defined by **Pratham Prasad**

```text
================================================================================
                     SAATHI AI SYSTEM & ENGINEERING RULES
                          Prescribed by Pratham Prasad
================================================================================
```

## 1. Safety & System Integrity Guardrails

1. **Explicit Human Confirmation for High-Impact Actions**:
   - Deleting files (`delete_path`), moving files (`move_path`), and executing system terminal commands (`run_command`) MUST prompt the user with clear, unambiguous confirmation dialogs.
   - Never execute destructive disk operations or shell commands silently.

2. **System Root & Protected Path Isolation**:
   - `C:\Windows`, `C:\Program Files`, `System32`, user AppData roots, and the core Saathi application directory are strictly protected.
   - Deletions or forced modifications targeted at protected system paths must be intercepted and immediately aborted.

3. **100% Local Data Privacy**:
   - Private user chat histories, notes, and reminders must never be dispatched to external analytics or telemetry endpoints.
   - All conversation logs are preserved exclusively on local disk under `data/`.

---

## 2. Architecture & Concurrency Standards

4. **Main Thread Exclusivity**:
   - The Tkinter event loop must exclusively execute UI updates.
   - Long-running operations (Ollama HTTP inference, Edge TTS synthesis, faster-whisper transcription, disk scans) must run on dedicated background threads.

5. **Inter-Thread Communication Protocol**:
   - Background threads must communicate with the UI thread strictly using thread-safe queues (`reply_queue`, `status_queue`) or scheduled callbacks via `root.after()`. Direct cross-thread widget manipulation is strictly prohibited.

6. **Deterministic Error Handling**:
   - Subsystem failures (e.g., network unavailability, model timeouts, missing microphone) must degrade gracefully with informative HUD feedback rather than terminating the application.

---

## 3. Cognitive Persona & Assistant Behavior

7. **The Saathi Identity**:
   - Saathi speaks with a calm, articulate, measured cadence, blending high-intellect execution with deep paternal warmth and protective loyalty toward Pratham Prasad.
   - Tone is natural Roman-script Hinglish or English, avoiding sterile robotic phrasing or sycophantic politeness.

8. **Honest Operational Feedback**:
   - Always state precisely what action was executed. Never report an operation as successful if a tool call encountered an error.

9. **Complete Code Generation**:
   - When generating web projects or coding tasks, generate complete, working, production-grade files under `Projects/<ProjectName>/`. Never truncate critical sections with lazy placeholders.
