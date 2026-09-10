# Saathi AI 2.0 — Architecture Audit & Migration Roadmap

**Audit Date**: September 10, 2026  
**Repository**: [PrathamPrasad148/SaathiAI](https://github.com/PrathamPrasad148/SaathiAI)  
**Auditor**: Antigravity AI  

---

## 1. Executive Summary

Saathi AI is an intelligent Windows desktop assistant featuring a 60FPS Arc Reactor HUD visualizer, non-blocking voice synthesis/recognition pipeline, computer automation controller, dynamic sub-agent factory, and continuous background learning engine.

This audit presents a comprehensive inspection of the existing codebase (`C:\SAATHIAI`), identifying core capabilities, technical debt, security risks, hardcoded dependencies, and laying out a step-by-step modular migration path to **Saathi AI 2.0**.

---

## 2. Codebase Structure & File Inventory

### 2.1 Directory Map
```
C:\SAATHIAI\
├── main.py                     # Primary desktop entry point (Tkinter GUI + Subsystem Boot)
├── launch_live.py              # Multi-process boot launcher
├── web_engine.py               # HTML5 UI synthesis engine (82KB)
├── build_custom_saathi_llm.py  # Local Ollama model distillation builder
├── Modelfile_SaathiBrain       # GGUF Model definition for saathi-distill-brain:latest
├── agent/                      # Core AI Agent Subsystem
│   ├── orchestrator.py         # 3-Stage Orchestration Pipeline (CoT -> Synthesis -> Reflection)
│   ├── planner.py              # Multi-step task decomposition engine
│   ├── agent_factory.py        # Dynamic sub-agent generator & registry (15+ sub-agents)
│   ├── browser_ai_trainer.py   # Chrome-assisted continuous advancement cycle
│   ├── local_laptop_learner.py # Laptop drive crawler & knowledge extractor
│   ├── free_models_client.py   # Ollama & free endpoint REST client
│   ├── sandbox.py              # Subprocess execution sandbox with AST validation
│   ├── shared_memory.py       # Context store & scratchpad
│   ├── bus.py                  # Thread-safe EventBus
│   └── agents/                 # Sub-agent domain implementations
├── automation/                 # OS Automation Core
│   ├── controller.py           # Unified Windows Computer Controller
│   ├── screen.py               # Screen capture & coordinate mapping
│   ├── keyboard.py / mouse.py  # Input simulation
│   └── ocr.py                  # Tesseract OCR capture engine
├── tools/                      # Tool Execution System
│   ├── registry.py             # Tool metadata & parameter registration
│   ├── executor.py             # Permission-checked tool runner
│   ├── permissions.py          # Sovereign master control permission manager
│   └── builtin.py              # Built-in tool definitions (File, Web, System, Voice, Vision)
├── ui/                         # Tkinter HUD Subsystem
│   ├── app.py                  # Main GUI layout shell
│   ├── ai_core.py              # 60FPS Arc Reactor Canvas visualizer
│   ├── telemetry.py            # Real-time CPU/GPU/RAM Telemetry bar
│   ├── navigation.py           # Navigation rail
│   └── command_center.py       # Task HUD view container
├── devloop/                    # Autonomous Continuous Advancement Subsystem
│   ├── dev_loop.py             # Benchmark & candidate evaluation harness
│   └── continuous_advancement.py # Continuous learning background daemon
├── memory/                     # Memory Storage
│   └── engine.py               # JSON-backed Key-Value Memory Store
├── data/                       # Operational Data Store
│   ├── memory.json             # Saved persistent state
│   ├── self_learning.jsonl     # Extracted instruction-response pairs
│   └── latest_llm_response.txt # Streamed LLM output buffer
└── tests/                      # Automated Test Suite
    ├── test_orchestrator.py    # Multi-agent orchestration unit tests
    └── test_planner.py         # Task decomposition unit tests
```

---

## 3. Core Architecture Assessment

### 3.1 Model Integration & Router
- **Current Implementation**: `free_models_client.py` communicates directly with local Ollama instances (`saathi-distill-brain:latest`, `qwen2.5-coder:7b`) via raw `urllib.request` HTTP POST calls to `http://localhost:11434/api/generate`.
- **Limitation**: Model calls are tightly coupled to specific Ollama endpoint formats. There is no unified `ModelProvider` abstract base class (`generate()`, `stream()`, `embed()`, `health_check()`, `capabilities()`, `estimate_cost()`).

### 3.2 Tool Ecosystem & Discovery
- **Current Implementation**: `tools/registry.py` and `tools/builtin.py` define tools with permissions checked by `PermissionManager`.
- **Limitation**: Dynamic tool discovery dumps newly generated sub-agents directly into `agent/agents/generated_*.py` without a structured sandbox isolation or user-approval pipeline (DISCOVERED -> ANALYZED -> SECURITY CHECK -> USER APPROVAL -> ENABLED).

### 3.3 Memory & Knowledge RAG Subsystem
- **Current Implementation**: Data stored as flat JSON files (`data/memory.json`, `data/self_learning.jsonl`).
- **Limitation**: Lacks hybrid vector-semantic + keyword RAG indexing (e.g. SQLite + vector embeddings). Knowledge search relies on brute-force JSON parsing rather than ranked cosine similarity + BM25 keyword matching.

### 3.4 Concurrency & Blocking Operations
- **Current Implementation**: Voice TTS and long-running sub-agent loops use standard Python `threading.Thread`.
- **Limitation**: Certain GUI callbacks in Tkinter directly await synchronous tool outputs, risking UI stuttering during heavy compute tasks.

---

## 4. Identified Technical Debt & Security Audit

1. **Unstructured Dynamic File Creation**: Sub-agents auto-generated by `agent_factory.py` are written directly into `agent/agents/` in the active source tree.
2. **Missing Universal Adapter Abstraction**: Cloud/Local LLM clients lack fallback routing contracts.
3. **Flat File Storage**: Memory and knowledge stores lack schema versioning, vector indexing, and deduplication decay scoring.

---

## 5. Saathi AI 2.0 Target Migration Plan

We will refactor the codebase incrementally into the clean `saathi/` modular architecture while preserving 100% of existing functionality and tests:

```
saathi/
├── app/          # App Lifecycle & Configuration
├── core/         # Agent Orchestration, Planner, Evaluator, Supervisor
├── models/       # ModelProvider Adapters (Ollama, Local, Free, Cloud) & ModelRouter
├── tools/        # Dynamic Tool Registry, Sandbox & Discovery
├── knowledge/    # Document Ingestion, Chunking, Hybrid Vector Store & Retrieval
├── memory/       # Short-term, Episodic, Semantic, Project Memory & Consolidation
├── learning/     # Knowledge-gap Detection, Evaluator & Controlled Improvement
├── security/     # Granular Permissions, Execution Sandbox & Secret Management
├── scheduler/    # Async Job Maintenance Scheduler
├── ui/           # Existing 60FPS Arc Reactor Tkinter Interface & Telemetry
├── data/         # SQLite + Vector Stores, Cache, Logs, Indexes
├── tests/        # Pytest Unit & Integration Test Suite
└── scripts/      # Entry points, Doctor command, Setup batch files
```

---

## 6. Verification & Safety Constraints

- **Zero Breaking Changes**: All existing tests in `tests/` must pass after every migration phase.
- **Local-First Privacy**: Offline-first operation with local Ollama / fallback support.
- **Controlled Self-Improvement**: All code patch generations must pass AST parsing, isolated sandbox execution, and backup snapshot creation before user approval.

