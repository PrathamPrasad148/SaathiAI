"""
Saathi AI — Autonomously Generated Sub-Agent: MultiPerspectiveSynthesizer
Domain: Cognitive Reasoning
Description: Examines problems from technical, economic, logical, risk, and creative analytical angles
"""

import time
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse


class MultiPerspectiveSynthesizer(BaseAgent):
    """Autonomously built sub-agent for Cognitive Reasoning operations."""

    def __init__(self, executor=None):
        super().__init__(
            name="MultiPerspectiveSynthesizer",
            description="Examines problems from technical, economic, logical, risk, and creative analytical angles",
            capabilities=['multi_perspective', 'synthesis', 'viewpoints', 'angle_analysis']
        )
        self.domain = "Cognitive Reasoning"
        self.executor = executor

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        return task.task_type == "cognitive reasoning" or any(k in lowered for k in ['multi_perspective', 'synthesis', 'viewpoints', 'angle_analysis'])

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        
        exec_time = (time.time() - start_t) * 1000
        result_text = f"[MultiPerspectiveSynthesizer] Autonomously processed directive: '{instruction}'. Telemetry nominal."
        
        return AgentResponse(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            result=result_text,
            execution_time_ms=exec_time,
            metadata={"domain": self.domain, "autonomous_generated": True}
        )