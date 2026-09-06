# Saathi AI — Product Requirements Document (PRD)
### Authored by **Pratham Prasad**

```text
================================================================================
                    SAATHI AI PRODUCT REQUIREMENTS DOCUMENT
                            Created by Pratham Prasad
================================================================================
```

## 1. Vision & Core Mission

**Saathi AI** is designed to be the definitive personal desktop artificial intelligence companion and cognitive operating interface for Windows. Conceived and engineered by **Pratham Prasad**, Saathi transforms the traditional desktop computing paradigm by providing an ultra-futuristic, high-bandwidth holographic control center coupled with an emotionally intelligent, paternal, and protective AI persona (*Saathi*).

Saathi prioritizes:
- **Complete Privacy & Data Sovereignty**: Operates 100% locally on user hardware.
- **Cognitive Protection**: Anticipates needs, protects blind spots, and guards system integrity.
- **High-Bandwidth Interaction**: Combines multi-turn agentic execution, voice I/O, and real-time kinetic telemetry.

---

## 2. Target Persona & User Base

- **Software Engineers & Creators**: Requiring automated project scaffolding, website generation, file management, and terminal execution without cloud dependency.
- **Power Users & Enthusiasts**: Seeking an advanced, visually stunning cybernetic cockpit interface (HUD) for daily Windows operations.
- **Privacy-Conscious Users**: Individuals who demand full data isolation without remote telemetry or corporate data harvesting.

---

## 3. Product Goals & Key Results (OKRs)

### Goal 1: Zero-Cloud Privacy & Reliability
- 100% on-device model execution via Ollama.
- Persistent local SQLite/JSON storage under `data/` for history, schedules, and notes.

### Goal 2: Unrivaled User Experience & Visual Fidelity
- Native 60 FPS vector canvas HUD in Tkinter with zero webview overhead.
- Intricate cybernetic instrumentation: 28-node neural constellation plexus, high-voltage plasma arcs, 3D rotating gyroscope, and 360° tactical radar.
- Real-time acoustic reactivity to speech input and voice playback.

### Goal 3: Safe, Autonomous Agency
- Multi-step tool-calling agent capable of running up to 4 autonomous iterative cycles per request.
- Strict human-in-the-loop confirmation for file deletions, moves, and terminal commands.
- Absolute path protection for critical system roots.

---

## 4. Functional Specifications

| Subsystem | Requirement | Priority |
| :--- | :--- | :--- |
| **Agent Reasoning** | Native Ollama `/api/chat` tool calling with multi-turn memory | P0 (Critical) |
| **Tactical Canvas** | 60 FPS vector HUD with neural plexus, arc reactor, and 3D gyro | P0 (Critical) |
| **Voice Engine** | On-device Whisper transcription and Indian-English neural TTS | P1 (High) |
| **Automations** | File operations, app launching, screenshot capture, clipboard tools | P1 (High) |
| **Project Builder** | Autonomous generation of complete websites/apps in `Projects/` | P1 (High) |
| **System Scheduler** | Autonomous background reminder loop with audio alerts | P1 (High) |
| **External Knowledge** | Free, live lookups for weather, currency exchange, Wikipedia | P2 (Medium) |

---

## 5. Non-Functional Requirements

- **Performance**: HUD frame rendering must execute within `< 16ms` per frame to sustain 60 FPS without UI freezing.
- **Thread Safety**: All networking, model inference, and audio processing must run on asynchronous worker threads, keeping the Tkinter UI event loop responsive.
- **Portability**: Native Python 3.12 architecture with self-contained batch launchers for Windows 10/11.
