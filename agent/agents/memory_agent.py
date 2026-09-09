"""
Saathi AI — Specialized Memory & Knowledge Sub-Agent
Dedicated to long-term factual recall, user preferences, durable memory persistence,
and semantic context management across sessions.
"""

import time
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse


class MemoryAgent(BaseAgent):
    """Specialized Sub-Agent for Durable Memory Persistence & Recall."""

    def __init__(self, memory_engine=None):
        super().__init__(
            name="MemoryAgent",
            description="Specialized in long-term memory retrieval, fact persistence, and user preferences.",
            capabilities=["store_memory", "recall_memory", "search_facts", "context_summary"]
        )
        self.memory_engine = memory_engine

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        keywords = ("remember", "remind", "memory", "note", "what do you know about me", "my preference", "save note", "add fact")
        return task.task_type in ("memory", "facts") or any(k in lowered for k in keywords)

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        lowered = instruction.lower()

        # 1. Store Fact / Note
        if any(k in lowered for k in ("remember that", "remember", "add note", "take note", "save fact")):
            fact_str = instruction
            for prefix in ("remember that", "remember", "add note:", "take note:", "save fact:"):
                if lowered.startswith(prefix):
                    fact_str = instruction[len(prefix):].strip()
                    break

            if self.memory_engine and hasattr(self.memory_engine, "add_fact"):
                self.memory_engine.add_fact(fact_str)

            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(
                task_id=task.task_id,
                agent_name=self.name,
                status="success",
                result=f"Persisted to neural memory ledger: '{fact_str}', Pratham.",
                execution_time_ms=exec_time
            )

        # 2. Context / Factual Recall
        mem_summary = ""
        if self.memory_engine and hasattr(self.memory_engine, "get_context_for_prompt"):
            mem_summary = self.memory_engine.get_context_for_prompt()

        exec_time = (time.time() - start_t) * 1000
        return AgentResponse(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            result=f"Retrieved memory context:\n{mem_summary or 'All user preferences nominal.'}",
            execution_time_ms=exec_time
        )
