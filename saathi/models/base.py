"""
Saathi AI 2.0 — Universal Model Provider Interface
"""

from abc import ABC, abstractmethod
from typing import Generator, List, Dict, Any, Optional

class ModelProvider(ABC):
    """Abstract Base Class for all Saathi AI 2.0 Model Providers."""

    def __init__(self, name: str, model_id: str):
        self.name = name
        self.model_id = model_id

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate a complete text response synchronously."""
        pass

    @abstractmethod
    def stream(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Generator[str, None, None]:
        """Stream response tokens as a generator."""
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate vector embedding for input text."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if provider endpoint and model are reachable."""
        pass

    @abstractmethod
    def capabilities(self) -> List[str]:
        """Return list of model capabilities (e.g. ['chat', 'coding', 'math', 'reasoning'])."""
        pass

    @abstractmethod
    def estimate_cost(self, prompt: str) -> float:
        """Estimate execution cost in USD (0.0 for local models)."""
        pass

    @abstractmethod
    def available(self) -> bool:
        """Return True if model is currently online and ready."""
        pass
