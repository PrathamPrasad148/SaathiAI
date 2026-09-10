"""
Saathi AI 2.0 — PrevJarvis Adapter (prevjarvis/ integration)
"""

from pathlib import Path
from typing import Dict, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class PrevJarvisTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the legacy PrevJarvis architecture."""

    def __init__(self, jarvis_dir: Optional[Path] = None):
        self.jarvis_dir = (jarvis_dir or Path(__file__).resolve().parent.parent.parent / "prevjarvis").resolve()
        metadata = ToolMetadata(
            name="prev_jarvis",
            description="Interface with PrevJarvis legacy core, desktop UI capabilities, and Rust acceleration modules.",
            category="SYSTEM",
            parameters={
                "action": "str - Subsystem action ('status', 'inspect', 'list_modules')",
                "target": "str - Optional target component or module"
            },
            risk_level=RiskLevel.MEDIUM,
            requires_network=False,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, action: str = "status", target: str = "", **kwargs) -> Dict[str, Any]:
        if not self.jarvis_dir.exists():
            return {"status": "error", "message": f"PrevJarvis directory missing at {self.jarvis_dir}"}

        readme_md = self.jarvis_dir / "README.md"

        return {
            "status": "success",
            "message": f"PrevJarvis active at {self.jarvis_dir}",
            "action": action,
            "target": target,
            "has_readme": readme_md.exists()
        }

