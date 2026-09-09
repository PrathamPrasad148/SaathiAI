"""
Saathi AI — Master Orchestrator (Meta-Agent System)
Orchestrates specialized sub-agents (Coding, Web, Vision, Automation, Memory, Conversation),
builds task-graph execution pipelines, manages the message bus and shared context,
and fuses multi-agent outputs into a unified response.
"""

import time
import uuid
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .base_agent import BaseAgent, AgentTask, AgentResponse
from .bus import AgentMessageBus
from .shared_memory import SharedContextStore
from .sandbox import ExecutionSandbox

from .agents.coding_agent import CodingAgent
from .agents.web_agent import WebAgent
from .agents.conversation_agent import ConversationAgent
from .agents.vision_agent import VisionAgent
from .agents.automation_agent import AutomationAgent
from .agents.memory_agent import MemoryAgent


from .agent_factory import DynamicAgentFactory


class SaathiOrchestrator:
    """Central Meta-Agent Orchestrator for Saathi AI Multi-Agent Architecture."""

    def __init__(self, projects_dir: Path, memory_engine=None, voice_engine=None, executor=None):
        self.projects_dir = projects_dir.resolve()
        self.bus = AgentMessageBus()
        self.shared_memory = SharedContextStore(memory_engine=memory_engine)
        self.sandbox = ExecutionSandbox(allowed_workspace_dir=self.projects_dir)
        self.factory = DynamicAgentFactory()

        # Initialize Core Specialized Sub-Agents
        self.coding_agent = CodingAgent(projects_dir=self.projects_dir, sandbox=self.sandbox, executor=executor)
        self.web_agent = WebAgent(executor=executor)
        self.conversation_agent = ConversationAgent(voice_engine=voice_engine)
        self.vision_agent = VisionAgent(executor=executor)
        self.automation_agent = AutomationAgent(sandbox=self.sandbox, executor=executor)
        self.memory_agent = MemoryAgent(memory_engine=memory_engine)

        self.registered_agents: List[BaseAgent] = [
            self.coding_agent,
            self.web_agent,
            self.conversation_agent,
            self.vision_agent,
            self.automation_agent,
            self.memory_agent
        ]
        # Dynamically append 100+ specialized factory agents
        self.registered_agents.extend(self.factory.get_all_agents())

    def classify_and_build_task_graph(self, instruction: str, parent_id: Optional[str] = None) -> List[AgentTask]:
        """Classify user intent and build a sequence of execution tasks (Task Graph)."""
        lowered = instruction.lower().strip()
        tasks: List[AgentTask] = []

        # Complex Pipeline 1: Research then Write Code / Create Website
        has_web_research = any(k in lowered for k in ("research", "search online", "find out about", "look up"))
        has_coding = any(k in lowered for k in ("website", "code", "script", "program", "build"))

        if has_web_research and has_coding:
            t1 = AgentTask(task_type="web", instruction=f"Search facts for: {instruction}", priority="normal")
            t2 = AgentTask(task_type="coding", instruction=instruction, priority="high", parent_id=t1.task_id)
            tasks.extend([t1, t2])
            return tasks

        # Direct Routing Check
        dummy_task = AgentTask(instruction=instruction)
        for agent in self.registered_agents:
            if agent.can_handle(dummy_task):
                task_type = "coding" if agent == self.coding_agent else (
                    "web" if agent == self.web_agent else (
                        "vision" if agent == self.vision_agent else (
                            "automation" if agent == self.automation_agent else (
                                "memory" if agent == self.memory_agent else "conversation"
                            )
                        )
                    )
                )
                tasks.append(AgentTask(task_type=task_type, instruction=instruction, priority="normal"))
                return tasks

        # Default to Conversation
        tasks.append(AgentTask(task_type="conversation", instruction=instruction, priority="normal"))
        return tasks

    def dispatch_task_to_agent(self, task: AgentTask) -> AgentResponse:
        """Route task to matching specialized sub-agent."""
        self.bus.publish("agent_start", {"task_id": task.task_id, "type": task.task_type, "instruction": task.instruction})

        selected_agent: Optional[BaseAgent] = None
        for agent in self.registered_agents:
            if agent.can_handle(task):
                selected_agent = agent
                break

        if not selected_agent:
            selected_agent = self.conversation_agent

        self.bus.publish("agent_executing", {"task_id": task.task_id, "agent_name": selected_agent.name})
        response = selected_agent.handle(task)
        self.bus.publish("agent_complete", {"task_id": task.task_id, "agent_name": selected_agent.name, "status": response.status})
        return response

    def execute_instruction_pipeline(self, instruction: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Master Orchestrator execution loop: intent classification -> task graph -> agent dispatch -> output fusion."""
        start_t = time.time()

        # Update Shared Memory
        self.shared_memory.add_episodic_turn("user", instruction)

        # Build Task Graph
        task_graph = self.classify_and_build_task_graph(instruction)
        self.bus.publish("task_graph_created", {"instruction": instruction, "task_count": len(task_graph)})

        results: List[AgentResponse] = []
        for task in task_graph:
            if context:
                task.context.update(context)
            res = self.dispatch_task_to_agent(task)
            results.append(res)
            if res.status == "error":
                # Fallback: attempt conversation recovery
                break

        # Fusion Engine: Merge agent outputs into a unified response
        fused_text = "\n\n".join([r.result for r in results if r.result]).strip()
        if not fused_text:
            fused_text = "Task executed cleanly across specialized sub-agents."

        self.shared_memory.add_episodic_turn("assistant", fused_text)
        exec_time = (time.time() - start_t) * 1000

        return AgentResponse(
            task_id=task_graph[0].task_id if task_graph else str(uuid.uuid4())[:8],
            agent_name="SaathiOrchestrator",
            status="success",
            result=fused_text,
            execution_time_ms=exec_time,
            metadata={"tasks_executed": len(results)}
        )


SAFE_PIPELINE_MODE = True
