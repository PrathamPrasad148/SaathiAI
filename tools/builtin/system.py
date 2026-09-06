import os
import webbrowser
import subprocess
import urllib.parse
from pathlib import Path
from typing import Dict, Any
from ..schemas import Tool, RiskLevel
from automation.system import get_system_telemetry
from automation.processes import list_running_processes
from automation.windows import focus_window_by_title, minimize_all_windows

def get_system_tools(app_dir: Path) -> list[Tool]:
    def open_target_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        target = args.get("target", "").strip()
        if not target:
            return "Error: target is required."
        p = Path(target)
        if not p.is_absolute():
            p = (app_dir / p).resolve()
        if p.exists():
            if p.suffix.lower() in (".html", ".htm"):
                webbrowser.open(p.as_uri())
            else:
                os.startfile(str(p))
            return f"Opened file '{p}'."
        if target.startswith(("http://", "https://", "spotify:")):
            webbrowser.open(target)
            return f"Opened URL '{target}'."
        apps = {"notepad": "notepad.exe", "calc": "calc.exe", "calculator": "calc.exe", "explorer": "explorer.exe", "code": "code.cmd"}
        app_cmd = apps.get(target.lower(), target)
        try:
            os.startfile(app_cmd)
            return f"Launched '{app_cmd}'."
        except OSError:
            webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(target))
            return f"Searched web for '{target}'."

    def sys_info_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        info = get_system_telemetry()
        return (
            f"OS: {info['os']} ({info['hostname']})\n"
            f"CPU Usage: {info['cpu_percent']}%\n"
            f"RAM: {info['ram_used_gb']}GB / {info['ram_total_gb']}GB ({info['ram_percent']}%)\n"
            f"Disk: {info['disk_percent']}% used"
        )

    def run_cmd_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        cmd = args.get("command", "")
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45)
        out = (res.stdout or res.stderr or "").strip()
        return out if out else "Command executed successfully with no output."

    return [
        Tool(
            name="open_target",
            category="system",
            description="Open a file (e.g. HTML in browser), launch an app (notepad, calc, spotify), or open a web URL.",
            parameters={
                "type": "object",
                "properties": {"target": {"type": "string", "description": "File path, app name, or URL"}},
                "required": ["target"]
            },
            risk_level=RiskLevel.LOW,
            run=open_target_run
        ),
        Tool(
            name="system_info",
            category="system",
            description="Retrieve live CPU, RAM, Disk, and OS telemetry information.",
            parameters={"type": "object", "properties": {}},
            risk_level=RiskLevel.LOW,
            run=sys_info_run
        ),
        Tool(
            name="run_command",
            category="system",
            description="Execute a terminal shell command on Windows.",
            parameters={
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Shell command to run"}},
                "required": ["command"]
            },
            risk_level=RiskLevel.MEDIUM,
            run=run_cmd_run
        )
    ]
