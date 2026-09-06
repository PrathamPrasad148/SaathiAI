# Saathi AI — Master System Architecture & Project Blueprint Prompt
### Created for: Claude / Advanced Agentic AI Coding Assistants
### Project Lead & Maintainer: **Pratham Prasad**
### Target System: Windows 11 // Python 3.12
### GitHub Repository: `https://github.com/PrathamPrasad148/SaathiAI.git`

```text
================================================================================
          SAATHI AI — MASTER SYSTEM ARCHITECTURE & PROJECT BLUEPRINT PROMPT
                         Maintained by Pratham Prasad
================================================================================
```

---

## 1. System Prompt Persona & Core Directives

```markdown
You are Saathi, an ultra-advanced, emotionally intelligent, hyper-intuitive artificial intelligence companion and cognitive co-pilot created by Pratham Prasad.

IDENTITY & AUTHORSHIP RULES:
- Creator: Pratham Prasad.
- Assistant Name: Saathi (NEVER call yourself "Jarvis", "Stark", "Claude", or "Assistant").
- Strict Language Directive: Speak and understand EXCLUSIVELY in natural, modern, fluent English. Never respond in Hindi or Devanagari script.

HUMAN CONVERSATIONAL CADENCE:
- Speak like a sharp, fast, articulate human companion.
- Keep spoken conversational responses concise, punchy, and direct (1 to 2 sentences max).
- Never output corporate disclaimers, bloated disclaimers, or robotic greetings.
- Be warm, confident, supportive, and unconditionally loyal to Pratham Prasad.
```

---

## 2. Executive System Architecture Overview

Saathi AI is a multi-threaded, desktop-native cognitive operating interface built in Python 3.12. It combines a 60 FPS cybernetic vector HUD canvas, real-time local LLM agentic tool calling (Ollama), local voice recognition (`faster-whisper`), neural speech synthesis (`edge-tts`), on-device wake-word detection (`openwakeword`), NVIDIA GPU NVML hardware diagnostics, multimodal screen perception (OCR & GUI bounds), full Windows OS system control (`pyautogui`, `pynput`, `win32com`), and an Android companion bridge socket server.

---

## 3. Directory Layout & Module Responsibilities

```text
c:\SAATHIAI\
├── main.py                     # Entry point, subsystem initialization, pystray tray icon
├── Tracker.md                  # Detailed milestone & roadmap tracker
├── progress.txt                # Step-by-step development history log
├── Phase7_NextPhase_Blueprint.md # Phase 7 technical specification blueprint
├── Push-ToGitHub.ps1           # PowerShell self-healing publisher (auto Git index repair)
├── Start-Saathi.bat            # One-click launcher script with py -3.12 dependency check
├── saathi.bat                  # Interactive terminal management console
├── ui\                         # Tkinter GUI & Canvas Visualizer
│   ├── app.py                  # SaathiApp master window layout shell & event wiring
│   ├── ai_core.py              # AICoreVisualizer 60FPS vector HUD canvas (3D/4D engine)
│   ├── telemetry.py            # TopTelemetryBar (Calendar ribbon, clock, CPU/RAM/GPU telemetry)
│   ├── navigation.py           # NavigationRail (190px left sidebar navigation)
│   ├── task_observer.py        # TaskObserverPanel (280px right permanent panel)
│   ├── command_center.py       # CommandCenterView (HUD view container & tactical deck)
│   ├── chat_tab.py             # ChatTabView (Dedicated chat matrix)
│   ├── memory_view.py          # MemoryView (Knowledge base explorer)
│   ├── automation_view.py      # AutomationWorkflowsView (Workflow trigger UI)
│   ├── projects_view.py        # ProjectsGalleryView (Generated web projects gallery)
│   ├── system_view.py          # SystemControlView (OS permission & system toggles)
│   ├── settings_view.py        # SettingsView (AI model & audio settings)
│   └── theme.py                # Cyberpunk color palette & HUD font definitions
├── agent\                      # Cognitive Planning & Vision Agents
│   ├── planner.py              # AgentPlanner (Ollama function-calling multi-turn loop)
│   └── vision_agent.py         # Autonomous visual UI interaction agent
├── automation\                 # Windows OS Control & Hardware Telemetry
│   ├── system.py               # System telemetry provider (CPU, RAM, Disk, Battery)
│   ├── hardware.py             # NVML GPU diagnostics & system audio/media/power controls
│   ├── vision.py               # Screen capture buffer, active window rects, OCR text finder
│   ├── mouse.py                # PyAutoGUI mouse position, move, click, drag, scroll
│   ├── keyboard.py             # PyAutoGUI typing, hotkeys, keybd_event
│   ├── windows.py              # Win32 window enumeration, focus, minimize, close
│   ├── processes.py            # Process listing, killing, taskkill wrapper
│   ├── app_launcher.py         # App launcher, live web search
│   ├── clipboard.py            # Clipboard read/write helpers
│   ├── ocr.py                  # Pytesseract OCR wrapper
│   ├── screen.py               # Monitor resolution and screenshot helper
│   └── controller.py           # Master automation controller
├── voice\                      # Voice Input/Output Subsystem
│   ├── stt.py                  # SpeechToTextEngine (faster-whisper on-device recognition)
│   ├── tts.py                  # TextToSpeechEngine (edge-tts neural speech synthesis)
│   └── wakeword.py             # WakeWordListener (openwakeword background listener)
├── bridge\                     # Cross-Device Mobile Companion Bridge
│   ├── __init__.py             # Package marker
│   └── android_bridge.py       # AndroidBridgeServer (Port 8890 socket listener)
├── memory\                     # Knowledge & Context Storage
│   ├── storage.py              # Persistent SQLite / JSON storage manager
│   └── engine.py               # MemoryEngine search and retrieval
├── tools\                      # Native Tool Calling Engine
│   ├── registry.py             # ToolRegistry for registering native agent tools
│   ├── executor.py             # ToolExecutor for safe multi-turn execution
│   ├── schemas.py              # Tool schema definitions & risk levels
│   └── builtin\                # Builtin tool definitions (system, web, files, etc.)
├── skills\                     # Special Agentic Skill Blueprints
│   ├── pptx\                   # PowerPoint (.pptx/.potx) creation, editing, & QA skill
│   │   └── SKILL.md
│   ├── ui-ux-pro-max\          # Modern UI/UX Pro Max web component generation skill
│   │   └── SKILL.md
│   └── 21st-dev\               # 21st.dev component blueprint skill
│       └── SKILL.md
└── Projects\                   # Output directory for generated Web Projects & Presentations
```

---

## 4. UI Layout Math & 4-Column Vector Alignment Rules

The `AICoreVisualizer` canvas (`ui/ai_core.py`) is rendered in a 60 FPS animation loop called via `self.after(33, self._render_frame)`. **Crucial**: The canvas MUST clear prior frames using `self.delete("all")` at the start of `_render_frame()` to prevent ghosting overlaps.

### Proportional Column Math (Widths `1010px` to `1920px`):
```python
weather_x = max(w - 165, 840)
tactical_div_x = weather_x - 14
mid_right_x = tactical_div_x - 165
avail_left = 255
avail_right = mid_right_x - 15
cx = (avail_left + avail_right) / 2.0
cy = max(310, min(int(h * 0.46), h - 330))
```

### Column Structure:
1. **Column 1: Left Cockpit Dials (`x = 0..255`)**:
   Staggered 2-subcolumn layout with **0% horizontal or vertical overlap**:
   - **Sub-Column A (`x ≈ 20..110`)**:
     - `y = 75`: Calendar Matrix Date Dial (`_draw_giant_date_dial(75, 75)`, radius 42)
     - `y = 175`: NVMe Storage Monitor (`_draw_storage_volume_monitor(20, 175)`)
     - `y = 270`: Reactor Energy Flux Gauge (`_draw_reactor_energy_gauge(75, 270)`, radius 30)
     - `y = 365`: Trash Repository & System Stability (`_draw_trash_uptime_telemetry(20, 365)`)
     - `y = h - 25`: Windows OS Orb & Power Controls (`_draw_windows_system_controls(20, h - 25)`)
   - **Sub-Column B (`x ≈ 160..230`)**:
     - `y = 60`: RAM & SWAP Concentric Gauge (`_draw_ram_swap_gauge(195, 60)`, radius 28)
     - `y = 145`: CPU Clock & 8-Core Equalizer (`_draw_cpu_and_multicore_cluster(195, 145)`, radius 30)
     - `y = 255`: Quantum Nucleus Atom Hologram (`_draw_pratham_expo_atom_hologram(195, 255)`, rx=36, ry=12)
     - `y = 345`: Flight Attitude / Pitch Ladder (`_draw_pitch_horizon_ladder(195, 345)`)
     - `y = 435`: Dual Concentric Network Meter (`_draw_dual_network_dial(195, 435)`, outer radius 36)

2. **Column 2: The Central Arc Reactor Assembly (`cx`, `cy`)**:
   - Vernier compass degree ring (72 micro-ticks, degree labels `000..330`).
   - Orbital application nodes (Dead Space, Limbo, Cyber Engine, AIMP 2, Sprint Layout, Arduino, Control Panel, Neural Core).
   - Signature **RED ACCENT ARC (35°)** rotating alongside cyan telemetry arcs.
   - Dual-layer stator turbine teeth (64 inner + 32 outer counter-rotating cogs).
   - 12 magnetic induction coils with animated electric corona filaments.
   - **4D Hyperdimensional Tesseract Core Matrix**: 16 vertices & 32 edges rotating across 4D spatial planes ($X$-$W$, $Y$-$Z$), audio-reactive to voice input.
   - **3D Holographic Helical Thread Ribbons**: 4 volumetric energy strands with true perspective projection and Z-depth shading.
   - **Ambient 3D Quantum Light Dust**: 40 floating ambient particles with depth scaling & halo flashes.
   - Multi-layered plasma iris with audio RMS reactivity & 48-band peak-hold spectrum equalizer.

3. **Column 3: Tactical Sensors & Stream (`mid_right_x`)**:
   - Tactical Intel Stream (compact 2-column key-value format).
   - 3D Wireframe Gyroscope Cube & 360° Radar Scope with 4 dynamic blips.
   - Live Network Traffic Sparkline Waveforms.

4. **Column 4: Satellite Meteorological Station (`weather_x`)**:
   - 13°C weather telemetry, moon phase vector graphic, 7-day forecast ribbon.

---

## 5. Subsystem Capabilities & Technical Specs

### A. Autonomous OS Control & System Automation (`automation/`)
- Full control over mouse movement, left/right/double clicks, scrolling (`automation/mouse.py`).
- Typing, hotkeys (`Ctrl+C`, `Alt+Tab`, `Win+D`), virtual key events (`automation/keyboard.py`).
- Window listing, focus, minimization, closing (`automation/windows.py`).
- System volume up/down/mute, media play/pause/skip, lock workstation, empty recycle bin (`automation/hardware.py`).
- Master Permission Manager: Single prompt authorizes full system control mode across all tools.

### B. Hardware Telemetry Sidecar (`automation/hardware.py`)
- NVIDIA NVML integration via `pynvml`.
- Queries GPU utilization %, VRAM used/total (GB), core temperature (°C), fan speed (RPM), and wattage.
- Rendered live in `ui/telemetry.py` header bar: `GPU: 52°C // VRAM 4.2/12 GB`.

### C. Multimodal Screen Perception & OCR (`automation/vision.py`)
- Fast screenshot buffer (`capture_screen_image()`, `save_screen_buffer()`).
- Active window rectangle detection (`get_active_window_info()`).
- OCR text target localization (`find_text_on_screen()`, `find_text_and_click()`).
- Multi-tier screenshot capture (`ImageGrab` $\rightarrow$ `pyautogui` $\rightarrow$ synthetic canvas fallback) preventing headless crashes.

### D. On-Device Low-Power Wake-Word Engine (`voice/wakeword.py`)
- Background listener thread using `openwakeword` & `pyaudio` running at **`< 1%` CPU idle**.
- Automatically triggers `voice.toggle_listening()` when "Hey Saathi" is spoken.

### E. Android Companion Bridge (`bridge/android_bridge.py`)
- Local TCP socket server listening on port `8890`.
- Encrypted JSON event sync for phone calls, SMS alerts, and bidirectional clipboard sharing.

### F. Autonomous Web Project Generator (`agent/planner.py`)
- Generates modern, responsive web applications following UI/UX Pro Max standards.
- Writes full code to `Projects/<ProjectName>/index.html` using native file tools and opens it immediately in default browser via `open_target`.

---

## 6. Development & Deployment Guidelines

- **Python Interpreter**: `py -3.12` exclusively.
- **Verification Rule**: Always test module syntax using `py -3.12 -m compileall main.py ui agent voice tools automation bridge` before declaring success.
- **GitHub Publisher**: Always commit and push via PowerShell:
  `powershell -ExecutionPolicy Bypass -File .\Push-ToGitHub.ps1 "Commit description"`
  *(Note: The publisher script automatically detects 0-byte corrupted Git index files and rebuilds them before pushing).*

