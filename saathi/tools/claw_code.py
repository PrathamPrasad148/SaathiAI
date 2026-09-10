"""
Saathi AI 2.0 — Claw Code Harness Adapter (claw-code-main/ integration)
"""

from pathlib import Path
from typing import Dict, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class ClawCodeTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the Claw Code agent harness."""

    def __init__(self, claw_dir: Optional[Path] = None):
        self.claw_dir = (claw_dir or Path(__file__).resolve().parent.parent.parent / "claw-code-main").resolve()
        metadata = ToolMetadata(
            name="claw_code",
            description="Interface with Claw Code agent coding harness and execution specs.",
            category="CODING",
            parameters={
                "action": "str - Subsystem action ('status', 'inspect', 'parity_check')",
                "target": "str - Optional target specification"
            },
            risk_level=RiskLevel.MEDIUM,
            requires_network=False,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, action: str = "status", target: str = "", **kwargs) -> Dict[str, Any]:
        if not self.claw_dir.exists():
            return {"status": "error", "message": f"Claw Code directory missing at {self.claw_dir}"}

        agents_md = self.claw_dir / "AGENTS.md"

        return {
            "status": "success",
            "message": f"Claw Code harness active at {self.claw_dir}",
            "action": action,
            "target": target,
            "has_agents_spec": agents_md.exists()
        }
