# Saathi AI — Cognitive Operating Interface & Desktop Co-Pilot
### Designed, Engineered & Built by **Pratham Prasad**

[![Platform](https://img.shields.io/badge/Platform-Windows%2011%20%7C%2010-00f0ff?style=flat-square&logo=windows)](https://github.com/PrathamPrasad148/SaathiAI)
[![Python](https://img.shields.io/badge/Python-3.12-38bdf8?style=flat-square&logo=python)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Ollama%20%7C%20Qwen%20Local-ffd700?style=flat-square)](https://ollama.ai)
[![Author](https://img.shields.io/badge/Author-Pratham%20Prasad-00ff88?style=flat-square)](https://github.com/PrathamPrasad148)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)

---

## Executive Summary

**Saathi AI** is a next-generation personal desktop artificial intelligence operating system and cognitive co-pilot built for Windows. Engineered from the ground up by **Pratham Prasad**, Saathi bridges the gap between deep local agentic intelligence and an ultra-futuristic tactical Heads-Up Display (HUD).

Saathi operates entirely on-device using local Large Language Models (powered by Ollama), guaranteeing 100% privacy with zero cloud data leakages, zero subscription fees, and complete offline autonomy. It speaks and understands natural Roman-script **Hinglish** and **English**, listening through on-device Whisper models and speaking with fluid neural text-to-speech.

---

## Key Architectural Innovations

### 1. Futuristic Cybernetic HUD & AI Core Visualizer
- **60 FPS Vector Canvas**: Rendered directly in Python Tkinter without sluggish webview wrappers or heavy Electron dependencies.
- **Dynamic 28-Node Neural Plexus**: Real-time simulated synaptic constellation network with autonomous vector drift, distance-based synaptic filament connections, and high-velocity action potential pulses.
- **High-Voltage Arc Reactor Energy Assembly**: Central magnetic confinement rings, 12 stator induction coils, dynamic fractal lightning arcs, and holographic honeycomb forcefield shields.
- **Tactical Flight & Navigation Telemetry**: 3D wireframe rotating gyroscope gimbal, 360° sweeping laser radar scope with dynamic target blips, 8-core CPU hardware thread monitors, and 48-band reactive audio spectrum equalizers.

### 2. Autonomous Multi-Tool Agentic Reasoning
- **Native Tool-Calling Loop**: Autonomous multi-turn iterative execution supporting file manipulation, computer commands, web requests, knowledge retrieval, reminders, and notes.
- **Safe Execution Policy**: Sandboxed permission architecture that requires explicit user confirmation before executing system commands or destructive file operations.
- **Protected System Paths**: Strict guardrails preventing unauthorized modifications to critical system directories.

### 3. Voice & Acoustic Subsystem
- **On-Device STT**: Integrated with `faster-whisper` for lightning-fast speech-to-text without cloud roundtrips.
- **Neural Speech Synthesis**: Integrated with `edge-tts` for articulate Indian-English spoken responses.
- **Audio Activity Feedback**: Waveform and spectrum visualizers animate dynamically according to microphone input and speech synthesis audio RMS.

### 4. Autonomous Project & Web Application Generator
- **Instant Full-Stack Generation**: Builds complete responsive websites, landing pages, and interactive utilities under `Projects/<ProjectName>/`.
- **UI/UX Pro Max & 21st.dev Design System Integration**: Adheres to modern design standards (contrast ratios, fluid typography, micro-interactions, responsive grids, and accessible components).
- **Auto-Launch Verification**: Automatically opens generated web applications in the default browser upon compilation.

---

## Repository Structure

```text
SAATHIAI/
├── agent/                  # Autonomous planner and tool-calling engine
│   └── planner.py          # Cognitive co-pilot system prompt & execution loop
├── automations/            # Windows OS automation routines & system tasks
│   └── engine.py           # Process control, file manager, system utilities
├── memory/                 # Persistent memory and storage subsystems
│   └── storage.py          # Chat history, reminder schedules, local notes
├── ui/                     # Futuristic HUD, FUI canvases & widget controls
│   ├── ai_core.py          # 60 FPS vector Arc Reactor, neural plexus & radar
│   ├── app.py              # Main desktop window & window management
│   ├── command_center.py   # Tactical directive deck, mission logs & telemetry
│   ├── navigation.py       # Mode selector & status monitors
│   ├── telemetry.py        # System hardware gauges & clock telemetry
│   └── theme.py            # High-contrast cybernetic palette tokens
├── voice/                  # Acoustic input/output subsystems
│   ├── engine.py           # Speech recognition & Edge TTS synthesis
│   └── listener.py         # Voice activity detection & microphone capture
├── tools/                  # Built-in agent tool schemas & execution handlers
├── Projects/               # Workspaces for generated apps and websites
├── main.py                 # Application bootstrapper and orchestrator
├── Start-Saathi.bat        # Instant dependency check & launcher
├── saathi.bat              # Interactive terminal manager
├── push-to-github.bat      # Self-healing automated Git publisher
└── requirements.txt        # Python package dependencies
```

---

## Quick Start Guide

### Prerequisites
1. **Windows 10 or 11 (64-bit)**
2. **Python 3.12** installed and added to `PATH`
3. **Ollama** installed and running locally (`ollama serve`)

### Installation & Launch

1. **Clone the Repository**:
   ```powershell
   git clone https://github.com/PrathamPrasad148/SaathiAI.git
   cd SaathiAI
   ```

2. **Pull the Recommended Models**:
   ```powershell
   ollama pull qwen2.5:7b
   ollama pull qwen3:14b
   ollama pull qwen3:4b-instruct
   ```

3. **Launch Saathi**:
   Double-click `Start-Saathi.bat` or run from PowerShell:
   ```powershell
   .\Start-Saathi.bat
   ```

Alternatively, launch directly using Python:
```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 main.py
```

---

## Interactive Controls & Capabilities

| Command / Trigger | Action Performed |
| :--- | :--- |
| **"Create a modern portfolio website"** | Generates HTML/CSS/JS in `Projects/` and launches it in the browser. |
| **"Organize Downloads folder"** | Groups loose files into Images, Documents, Videos, Music, and Archives. |
| **"Remind me in 30 minutes to review code"** | Schedules an autonomous desktop reminder and speaks it aloud when due. |
| **"What's the weather in New Delhi?"** | Fetches live meteorological conditions via free live endpoints. |
| **"Take a screenshot"** | Captures display snapshot directly to the active project workspace. |
| **"Summarize clipboard"** | Reads and synthetically condenses the current Windows clipboard content. |
| **"Run command: dir /w"** | Presents a safety prompt with the exact command for user confirmation. |

---

## Development & Automation Scripts

- **`Start-Saathi.bat`**: Automatic interpreter verification, dependency auto-installer, and one-click app launch.
- **`saathi.bat`**: Full management console with quick-launch, GitHub synchronization, and dependency audits.
- **`push-to-github.bat`**: Self-healing Git publisher created by Pratham Prasad that detects index corruption, fixes repository locks, stages all assets, and publishes to GitHub.
- **`erasegitdata.bat`**: Safe remote file cleanup script preserving local repository state.

---

## Security & Safety Guardrails

- **Zero Remote Telemetry**: Conversations, notes, and reminders remain 100% on the local disk under `data/`.
- **Human-in-the-Loop Confirmation**: Destructive file deletions, file moves, and terminal commands are blocked until explicitly confirmed by the user.
- **Protected Paths**: Windows system roots, `System32`, user application roots, and core script directories cannot be accidentally deleted or overwritten.

---

## Author & Maintainer

**Pratham Prasad**  
*Lead Architect & Engineer of Saathi AI*  
- GitHub: [@PrathamPrasad148](https://github.com/PrathamPrasad148)  
- Repository: [https://github.com/PrathamPrasad148/SaathiAI.git](https://github.com/PrathamPrasad148/SaathiAI.git)

---
*Built with passion, precision, and an uncompromising standard for futuristic user experience.*
