"""
Saathi AI — Shared Memory & Context Store
Unified thread-safe memory architecture across all sub-agents.
Manages Episodic Memory (conversation logs), Long-Term Facts (user memory),
and Task Scratchpad (active execution state).
"""

import time
import threading
from typing import Dict, Any, List, Optional
from pathlib import Path


class SharedContextStore:
    """Centralized Context Store accessible by Orchestrator and all Sub-Agents."""

    def __init__(self, memory_engine=None):
        self.memory_engine = memory_engine
        self._lock = threading.Lock()
        
        # 1. Episodic Rolling Memory
        self._episodic_history: List[Dict[str, str]] = []
        
        # 2. Task Scratchpad (Active Task State & Interim Artifacts)
        self._scratchpad: Dict[str, Any] = {}
        
        # 3. Durable Key-Value Store
        self._fact_store: Dict[str, Any] = {}

    def add_episodic_turn(self, role: str, content: str, agent_name: Optional[str] = None):
        """Append a conversational turn to episodic memory."""
        with self._lock:
            entry = {
                "role": role,
                "content": content,
                "timestamp": time.time()
            }
            if agent_name:
                entry["agent"] = agent_name
            self._episodic_history.append(entry)
            if len(self._episodic_history) > 100:
                self._episodic_history = self._episodic_history[-100:]

    def get_recent_conversation(self, max_turns: int = 10) -> List[Dict[str, str]]:
        """Retrieve recent conversation history."""
        with self._lock:
            return list(self._episodic_history[-max_turns:])

    def set_scratchpad_value(self, key: str, value: Any):
        """Set a temporary value in the active task scratchpad."""
        with self._lock:
            self._scratchpad[key] = value

    def get_scratchpad_value(self, key: str, default: Any = None) -> Any:
        """Get a temporary value from the scratchpad."""
        with self._lock:
            return self._scratchpad.get(key, default)

    def clear_scratchpad(self):
        """Clear active task scratchpad after completion."""
        with self._lock:
            self._scratchpad.clear()

    def store_fact(self, key: str, value: Any):
        """Store a durable user/project fact."""
        with self._lock:
            self._fact_store[key] = value
        if self.memory_engine and hasattr(self.memory_engine, "add_fact"):
            try:
                self.memory_engine.add_fact(f"{key}: {value}")
            except Exception:
                pass

    def get_fact(self, key: str, default: Any = None) -> Any:
        """Retrieve a durable fact."""
        with self._lock:
            return self._fact_store.get(key, default)

    def assemble_agent_context(self, task_instruction: str) -> Dict[str, Any]:
        """Compile relevant context slice for an agent invocation."""
        with self._lock:
            mem_facts = ""
            if self.memory_engine and hasattr(self.memory_engine, "get_context_for_prompt"):
                try:
                    mem_facts = self.memory_engine.get_context_for_prompt()
                except Exception:
                    pass

            return {
                "recent_turns": list(self._episodic_history[-6:]),
                "scratchpad": dict(self._scratchpad),
                "facts": dict(self._fact_store),
                "memory_summary": mem_facts
            }
