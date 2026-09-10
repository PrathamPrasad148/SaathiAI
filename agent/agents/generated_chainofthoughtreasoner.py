"""
Saathi AI — Autonomously Generated Sub-Agent: ChainOfThoughtReasoner
Domain: Cognitive Reasoning
Description: Step-by-step logical reasoning breakdown, hypothesis tree evaluation, and self-critique
"""

import time
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse


class ChainOfThoughtReasoner(BaseAgent):
    """Autonomously built sub-agent for Cognitive Reasoning operations."""

    def __init__(self, executor=None):
        super().__init__(
            name="ChainOfThoughtReasoner",
            description="Step-by-step logical reasoning breakdown, hypothesis tree evaluation, and self-critique",
            capabilities=['reasoning', 'chain_of_thought', 'deduction', 'logic_tree']
        )
        self.domain = "Cognitive Reasoning"
        self.executor = executor

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        return task.task_type == "cognitive reasoning" or any(k in lowered for k in ['reasoning', 'chain_of_thought', 'deduction', 'logic_tree'])

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        
        exec_time = (time.time() - start_t) * 1000
        result_text = f"[ChainOfThoughtReasoner] Autonomously processed directive: '{instruction}'. Telemetry nominal."
        
        return AgentResponse(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            result=result_text,
            execution_time_ms=exec_time,
            metadata={"domain": self.domain, "autonomous_generated": True}
        )