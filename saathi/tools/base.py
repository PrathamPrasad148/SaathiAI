"""
Saathi AI 2.0 — Base Tool Abstraction & Risk Levels
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

class RiskLevel:
    LOW = "LOW"            # e.g., Calculator, Weather check
    MEDIUM = "MEDIUM"      # e.g., Read File, Web Search
    HIGH = "HIGH"          # e.g., Write File, Delete Cache
    CRITICAL = "CRITICAL"  # e.g., Shell Execution, Install Software, Modify System

@dataclass
class ToolMetadata:
    name: str
    description: str
    category: str  # WEB, FILESYSTEM, MATHEMATICS, CODING, SYSTEM, BROWSER, MEMORY, KNOWLEDGE
    parameters: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    risk_level: str = RiskLevel.LOW
    requires_network: bool = False
    requires_confirmation: bool = False
    timeout: int = 30
    version: str = "1.0.0"

class BaseTool(ABC):
    """Abstract Base Class for all Saathi AI 2.0 Tools."""

    def __init__(self, metadata: ToolMetadata):
        self.metadata = metadata

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def description(self) -> str:
        return self.metadata.description

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute tool logic with specified parameters."""
        pass
