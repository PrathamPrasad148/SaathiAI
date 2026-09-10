"""
Saathi AI 2.0 — DeepSeek Harness Adapter (deepseek-harness-master/ integration)
"""

from pathlib import Path
from typing import Dict, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class DeepSeekHarnessTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the DeepSeek Harness (dsh) agent subsystem."""

    def __init__(self, harness_dir: Optional[Path] = None):
        self.harness_dir = (harness_dir or Path(__file__).resolve().parent.parent.parent / "deepseek-harness-master").resolve()
        metadata = ToolMetadata(
            name="deepseek_harness",
            description="Interface with DeepSeek Harness (dsh) plugin architecture and agent specifications.",
            category="CODING",
            parameters={
                "action": "str - Subsystem action ('status', 'inspect', 'list_plugins')",
                "target": "str - Optional target plugin or spec"
            },
            risk_level=RiskLevel.MEDIUM,
            requires_network=False,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, action: str = "status", target: str = "", **kwargs) -> Dict[str, Any]:
        if not self.harness_dir.exists():
            return {"status": "error", "message": f"DeepSeek Harness directory missing at {self.harness_dir}"}

        agents_md = self.harness_dir / "AGENTS.md"

        return {
            "status": "success",
            "message": f"DeepSeek Harness active at {self.harness_dir}",
            "action": action,
            "target": target,
            "has_agents_spec": agents_md.exists()
        }

