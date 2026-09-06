# Saathi AI — Implementation & Developer Guide
### Engineered by **Pratham Prasad**

```text
================================================================================
                    SAATHI AI IMPLEMENTATION & ARCHITECTURE GUIDE
                           Engineered by Pratham Prasad
================================================================================
```

## 1. Development Environment Setup

### Recommended Setup:
- **Operating System**: Windows 10/11 64-bit
- **Runtime Environment**: Python 3.12 (Native Windows installer or `py -3.12`)
- **Language Model Host**: Ollama v0.1.30+ running locally on port `11434`

### Installation Commands:
```powershell
# 1. Clone repository
git clone https://github.com/PrathamPrasad148/SaathiAI.git
cd SaathiAI

# 2. Install dependencies via pip
py -3.12 -m pip install -r requirements.txt

# 3. Pull recommended local models
ollama pull qwen2.5:7b
ollama pull qwen3:14b
ollama pull qwen3:4b-instruct

# 4. Launch Saathi AI
py -3.12 main.py
```

---

## 2. Core Subsystem Architecture

### A. Main Orchestrator (`main.py`)
Initializes the runtime environment, parses command-line arguments, validates local dependencies, and hands execution to `ui.app.SaathiApp`.

### B. High-Performance HUD Canvas (`ui/ai_core.py`)
Built on Tkinter `Canvas` with an optimized redraw loop that minimizes redraw overhead:
- Computes mathematical angles, vectors, and projections using optimized coordinate math.
- Manages 28 synaptic nodes with Euclidean distance connection thresholds.
- Simulates fractal lightning arcs with randomized midpoint displacement.
- Maintains a steady 50-60 FPS refresh rate via `root.after(16, self._render_loop)`.

### C. Agent Reasoning & Tool Execution Engine (`agent/planner.py`)
- Formulates multi-turn prompt payloads with the paternal, protective cognitive co-pilot persona created by Pratham Prasad.
- Intercepts Ollama tool call responses (`create_file`, `read_file`, `run_command`, `open_target`, `get_weather`, etc.).
- Evaluates actions against safety policies before routing them to `automations.engine`.

### D. Windows System Automations (`automations/engine.py`)
- Cross-platform process launcher using `os.startfile` and `subprocess`.
- File manager with directory organization routines and trash safety.
- Screen capture via Pillow `ImageGrab`.
- Clipboard reader and text condensing pipelines.

### E. Acoustic Processing (`voice/`)
- Voice Activity Detection (VAD) listening loop.
- Offline transcription via `faster-whisper` using local quantized weights.
- Asynchronous speech synthesis with `edge-tts` streaming into `pygame` audio channels.

---

## 3. Extending the Agent Toolset

To register a new tool in Saathi:

1. **Define Schema**: Add JSON tool specification into `agent/planner.py` under `TOOLS_SCHEMA`.
2. **Implement Logic**: Add the corresponding operational method in `automations/engine.py`.
3. **Bind Execution**: Add the dispatcher branch inside `execute_tool()` in `agent/planner.py`.
4. **Safety Check**: If the tool performs destructive writes or executes code, route through `confirm_action()`.
5. **Update Documentation**: Record tool capabilities in `README.md` and `Schema.md`.

---

## 4. Verification & Validation Protocol

```powershell
# Syntax & Bytecode Compilation Check
py -3.12 -m compileall main.py ui agent automations memory voice tools

# Headless Offscreen Validation
py -3.12 -c "from ui.ai_core import AICoreVisualizer; print('[SUCCESS] Core Visualizer validated')"

# Launch via Manager Script
.\saathi.bat
```
