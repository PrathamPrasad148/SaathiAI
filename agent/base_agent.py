"""
Saathi AI — Base Agent Contracts & Abstractions
Defines the core data structures and interface for all specialized agents.
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


@dataclass
class AgentTask:
    """Standardized envelope for tasks assigned to agents."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    task_type: str = "general"
    instruction: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    priority: str = "normal"  # low, normal, high, critical
    timeout_s: float = 30.0
    parent_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)


@dataclass
class AgentResponse:
    """Standardized result returned by agents after task execution."""
    task_id: str
    agent_name: str
    status: str = "success"  # success, error, in_progress, cancelled
    result: str = ""
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    execution_time_ms: float = 0.0
    error_msg: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract Base Class for all Saathi AI Specialized Sub-Agents."""

    def __init__(self, name: str, description: str, capabilities: List[str]):
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.is_active = True

    @abstractmethod
    def can_handle(self, task: AgentTask) -> bool:
        """Return True if this agent can process the given task."""
        pass

    @abstractmethod
    def handle(self, task: AgentTask) -> AgentResponse:
        """Process the assigned task and return a standardized AgentResponse."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', capabilities={self.capabilities})>"
