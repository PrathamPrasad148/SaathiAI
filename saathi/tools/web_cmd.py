"""
Saathi AI 2.0 — WebCmd Browser & Tool Adapter (web/ integration)
"""

import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from .base import BaseTool, ToolMetadata, RiskLevel

class WebCmdTool(BaseTool):
    """Tool adapter interfacing Saathi AI with the webcmd CLI subsystem in web/."""

    def __init__(self, web_dir: Optional[Path] = None):
        self.web_dir = (web_dir or Path(__file__).resolve().parent.parent.parent / "web").resolve()
        metadata = ToolMetadata(
            name="web_cmd",
            description="Interface with webcmd CLI engine for deterministic web and browser session tasks.",
            category="WEB",
            parameters={
                "command": "str - CLI subcommand to execute with webcmd"
            },
            risk_level=RiskLevel.MEDIUM,
            requires_network=True,
            requires_confirmation=False
        )
        super().__init__(metadata)

    def execute(self, command: str = "help", **kwargs) -> Dict[str, Any]:
        if not self.web_dir.exists():
            return {"status": "error", "message": f"Web directory missing at {self.web_dir}"}

        node_exe = shutil.which("node") or "node"
        main_script = self.web_dir / "dist" / "src" / "main.js"

        if not main_script.exists():
            return {
                "status": "info",
                "message": f"WebCmd target directory ready at {self.web_dir}. Build dist/src/main.js to activate CLI execution."
            }

        try:
            res = subprocess.run(
                [node_exe, str(main_script)] + command.split(),
                cwd=str(self.web_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "status": "success" if res.returncode == 0 else "error",
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

