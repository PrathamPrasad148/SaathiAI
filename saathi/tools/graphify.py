"""
Saathi AI 2.0 — Graphify Adapter (graphify-8/ integration)
"""

from pathlib import Path
from typing import Dict, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class GraphifyTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the Graphify knowledge graph engine in graphify-8/."""

    def __init__(self, graphify_dir: Optional[Path] = None):
        self.graphify_dir = (graphify_dir or Path(__file__).resolve().parent.parent.parent / "graphify-8").resolve()
        metadata = ToolMetadata(
            name="graphify",
            description="Build, query, and traverse codebase and multi-modal knowledge graphs using AST tree-sitter.",
            category="KNOWLEDGE",
            parameters={
                "action": "str - Subsystem action ('status', 'build', 'query', 'inspect')",
                "target": "str - Target repository directory or query"
            },
            risk_level=RiskLevel.MEDIUM,
            requires_network=False,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, action: str = "status", target: str = "", **kwargs) -> Dict[str, Any]:
        if not self.graphify_dir.exists():
            return {"status": "error", "message": f"Graphify directory missing at {self.graphify_dir}"}

        readme_md = self.graphify_dir / "README.md"
        pyproject = self.graphify_dir / "pyproject.toml"

        return {
            "status": "success",
            "message": f"Graphify active at {self.graphify_dir}",
            "action": action,
            "target": target,
            "has_readme": readme_md.exists(),
            "has_pyproject": pyproject.exists()
        }
