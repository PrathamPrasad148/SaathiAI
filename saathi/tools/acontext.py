"""
Saathi AI 2.0 — Acontext Skill Memory Adapter (Acontext-main/ integration)
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class AcontextTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the Acontext skill memory layer."""

    def __init__(self, acontext_dir: Optional[Path] = None):
        self.acontext_dir = (acontext_dir or Path(__file__).resolve().parent.parent.parent / "Acontext-main").resolve()
        metadata = ToolMetadata(
            name="acontext",
            description="Interface with Acontext skill memory layer for reading and exporting markdown agent skills.",
            category="MEMORY",
            parameters={
                "action": "str - Subsystem action ('list_skills', 'inspect_spec', 'status')",
                "skill_name": "str - Optional target skill name"
            },
            risk_level=RiskLevel.LOW,
            requires_network=False,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, action: str = "status", skill_name: str = "", **kwargs) -> Dict[str, Any]:
        if not self.acontext_dir.exists():
            return {"status": "error", "message": f"Acontext directory missing at {self.acontext_dir}"}

        agents_doc = self.acontext_dir / "AGENTS.md"

        return {
            "status": "success",
            "message": f"Acontext skill memory active at {self.acontext_dir}",
            "action": action,
            "skill_name": skill_name,
            "has_agents_spec": agents_doc.exists()
        }

