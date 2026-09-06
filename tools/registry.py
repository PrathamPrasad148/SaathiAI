from typing import Dict, List, Any, Optional
from .schemas import Tool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def get_all(self) -> List[Tool]:
        return list(self._tools.values())

    def get_ollama_schemas(self) -> List[Dict[str, Any]]:
        return [tool.to_ollama_schema() for tool in self._tools.values()]
