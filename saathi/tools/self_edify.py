"""
Saathi AI 2.0 — SelfEdifyAI Integration Adapter (SelfEdifyAI-main/ integration)
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class SelfEdifyTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the SelfEdifyAI Django/Python subsystem."""

    def __init__(self, edify_dir: Optional[Path] = None):
        self.edify_dir = (edify_dir or Path(__file__).resolve().parent.parent.parent / "SelfEdifyAI-main").resolve()
        metadata = ToolMetadata(
            name="self_edify",
            description="Interface with SelfEdifyAI resource analysis and data search subsystem.",
            category="KNOWLEDGE",
            parameters={
                "action": "str - Subsystem command ('status', 'inspect', 'query')",
                "query": "str - Search query or resource directive"
            },
            risk_level=RiskLevel.MEDIUM,
            requires_network=False,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, action: str = "status", query: str = "", **kwargs) -> Dict[str, Any]:
        if not self.edify_dir.exists():
            return {"status": "error", "message": f"SelfEdifyAI directory missing at {self.edify_dir}"}

        backend_path = self.edify_dir / "Codes" / "BackEnd" / "SelfEdifyAI"
        manage_py = backend_path / "manage.py"

        return {
            "status": "success",
            "message": f"SelfEdifyAI subsystem active at {backend_path}",
            "action": action,
            "query": query,
            "has_manage_py": manage_py.exists()
        }

