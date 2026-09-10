"""
Saathi AI 2.0 — Dynamic Tool Registry
"""

from typing import Dict, List, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class DynamicToolRegistry:
    """Registry managing available Saathi AI tools, metadata inspection, and category filtering."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def unregister(self, name: str) -> bool:
        if name in self._tools:
            del self._tools[name]
            return True
        return False

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        result = []
        for name, tool in self._tools.items():
            if category and tool.metadata.category.upper() != category.upper():
                continue
            result.append({
                "name": tool.metadata.name,
                "description": tool.metadata.description,
                "category": tool.metadata.category,
                "parameters": tool.metadata.parameters,
                "risk_level": tool.metadata.risk_level,
                "requires_confirmation": tool.metadata.requires_confirmation
            })
        return result

    def get_all_categories(self) -> List[str]:
        return list(set(t.metadata.category for t in self._tools.values()))

    def __len__(self) -> int:
        return len(self._tools)

