"""
Saathi AI 2.0 — Ponytail Senior Developer Adapter (ponytail-main/ integration)
"""

from pathlib import Path
from typing import Dict, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class PonytailTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the Ponytail senior developer skill plugin."""

    def __init__(self, ponytail_dir: Optional[Path] = None):
        self.ponytail_dir = (ponytail_dir or Path(__file__).resolve().parent.parent.parent / "ponytail-main").resolve()
        metadata = ToolMetadata(
            name="ponytail",
            description="Interface with Ponytail concise code optimization skill plugin.",
            category="CODING",
            parameters={
                "action": "str - Subsystem action ('status', 'inspect', 'list_skills')",
                "target": "str - Optional target code path"
            },
            risk_level=RiskLevel.LOW,
            requires_network=False,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, action: str = "status", target: str = "", **kwargs) -> Dict[str, Any]:
        if not self.ponytail_dir.exists():
            return {"status": "error", "message": f"Ponytail directory missing at {self.ponytail_dir}"}

        agents_md = self.ponytail_dir / "AGENTS.md"

        return {
            "status": "success",
            "message": f"Ponytail plugin active at {self.ponytail_dir}",
            "action": action,
            "target": target,
            "has_agents_spec": agents_md.exists()
        }

