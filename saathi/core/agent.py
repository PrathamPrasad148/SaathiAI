"""
Saathi AI 2.0 — Core Agent Orchestrator & Execution Loop
"""

import time
from typing import Dict, Any, List, Optional
from ..models.router import ModelRouter
from ..tools.registry import DynamicToolRegistry
from ..memory.store import MultiTierMemoryStore
from ..knowledge.store import LocalKnowledgeStore
from ..security.sandbox import ExecutionSandbox
from .planner import TaskPlanner
from .evaluator import ResponseEvaluator
from .researcher import WebResearchEngine

class SaathiCoreAgent:
    """Central Saathi AI 2.0 Agent driving the observe -> plan -> execute -> evaluate loop."""

    def __init__(
        self,
        router: Optional[ModelRouter] = None,
        tool_registry: Optional[DynamicToolRegistry] = None,
        memory_store: Optional[MultiTierMemoryStore] = None,
        knowledge_store: Optional[LocalKnowledgeStore] = None
    ):
        self.router = router or ModelRouter()
        self.tool_registry = tool_registry or DynamicToolRegistry()
        self.memory_store = memory_store or MultiTierMemoryStore()
        self.knowledge_store = knowledge_store or LocalKnowledgeStore()
        self.planner = TaskPlanner()
        self.evaluator = ResponseEvaluator()
        self.researcher = WebResearchEngine(knowledge_store=self.knowledge_store)

    def process_task(self, instruction: str) -> Dict[str, Any]:
        start_t = time.time()

        # 1. Store turn in Short-Term Memory
        self.memory_store.add_short_term("user", instruction)

        # 2. Model Routing & Task Classification
        provider, task_cat = self.router.route(instruction)

        # 3. Create Plan Steps
        plan_steps = self.planner.create_plan(instruction)

        # 4. Generate Response via Model Router
        system_prompt = (
            "You are Saathi AI 2.0, a modular, local-first agentic desktop AI system. "
            "Provide accurate, direct, and well-structured responses."
        )

        raw_response = provider.generate(instruction, system_prompt=system_prompt)

        # 5. Evaluate Response Quality
        eval_result = self.evaluator.evaluate(instruction, raw_response)

        final_response = raw_response
        if not eval_result["passed"] and "REVISE" in eval_result["recommendation"]:
            revised_prompt = f"{instruction}\n\n[Critique Feedback]: {eval_result['recommendation']}\nPlease refine your answer."
            final_response = provider.generate(revised_prompt, system_prompt=system_prompt)

        # 6. Store Output in Memory & Log Task
        self.memory_store.add_short_term("assistant", final_response)
        self.memory_store.add_episodic(task=instruction, result=final_response[:200], success=True)
        self.memory_store.consolidate()

        exec_ms = (time.time() - start_t) * 1000

        return {
            "instruction": instruction,
            "category": task_cat,
            "model_used": provider.name,
            "response": final_response,
            "evaluation": eval_result,
            "execution_time_ms": exec_ms
        }
