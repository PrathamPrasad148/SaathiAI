"""
Saathi AI 2.0 — Hierarchical Task Planner & Decomposition Engine
"""

from typing import List, Dict, Any, Optional

class TaskPlanStep:
    def __init__(self, step_id: int, description: str, tool_name: Optional[str] = None):
        self.step_id = step_id
        self.description = description
        self.tool_name = tool_name
        self.status = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
        self.result = ""

class TaskPlanner:
    """Decomposes complex directives into ordered, executable plan steps."""

    def create_plan(self, instruction: str) -> List[TaskPlanStep]:
        lowered = instruction.lower().strip()
        steps = []

        if "research" in lowered or "search" in lowered:
            steps.append(TaskPlanStep(1, f"Search web and local knowledge for '{instruction}'", tool_name="web_search"))
            steps.append(TaskPlanStep(2, "Synthesize findings and compile citations", tool_name="summarize"))
        elif "code" in lowered or "script" in lowered or "build" in lowered:
            steps.append(TaskPlanStep(1, "Draft code implementation", tool_name="write_code"))
            steps.append(TaskPlanStep(2, "Validate AST syntax and execute sandbox test", tool_name="run_python"))
        elif "math" in lowered or "solve" in lowered:
            steps.append(TaskPlanStep(1, "Formulate mathematical problem statement"))
            steps.append(TaskPlanStep(2, "Compute numerical/symbolic solution"))
            steps.append(TaskPlanStep(3, "Verify consistency of mathematical steps"))
        else:
            steps.append(TaskPlanStep(1, f"Process directive: {instruction}"))

        return steps

