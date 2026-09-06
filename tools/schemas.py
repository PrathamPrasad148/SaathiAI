from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Callable, Optional

class RiskLevel(str, Enum):
    LOW = "low"          # Harmless: read files, get weather, open harmless targets
    MEDIUM = "medium"    # Modifying: create file, run benign terminal, delete to trash
    HIGH = "high"        # Dangerous: system configuration, destructive commands

@dataclass
class Tool:
    name: str
    category: str
    description: str
    parameters: Dict[str, Any]
    risk_level: RiskLevel = RiskLevel.LOW
    timeout: int = 30
    run: Optional[Callable] = None

    def to_ollama_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
