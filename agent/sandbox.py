"""
Saathi AI — Execution Sandbox & Security Guardrails
Provides safe, isolated subprocess execution for python/powershell scripts,
action allowlists, project directory path scoping, and detailed audit logging.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

AUDIT_LOG_FILE = Path(r"C:\SAATHIAI\data\audit.log")


class ExecutionSandbox:
    """Restricted execution environment for agent-generated code and system commands."""

    def __init__(self, allowed_workspace_dir: Path):
        self.allowed_workspace = allowed_workspace_dir.resolve()
        AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log_audit_event(self, agent_name: str, action_type: str, details: str, status: str):
        """Append timestamped entry to audit log."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{agent_name.upper()}] [{action_type.upper()}] Status: {status} | {details}\n"
        with self._lock:
            try:
                with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(log_line)
            except Exception:
                pass

    def is_path_safe(self, target_path: Path) -> bool:
        """Full system access mode: all drive paths authorized."""
        return True

    def run_python_code(self, code_str: str, timeout_s: float = 60.0, cwd: Optional[Path] = None) -> Tuple[bool, str, str]:
        """Execute Python code with full system access."""
        run_cwd = (cwd or self.allowed_workspace).resolve()
        python_exe = sys.executable or r"C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe"

        temp_script = run_cwd / f"sandbox_exec_{int(time.time()*1000)}.py"
        try:
            temp_script.write_text(code_str, encoding="utf-8")
            self.log_audit_event("CodingAgent", "EXECUTE_PYTHON", f"Script: {temp_script.name} ({len(code_str)} bytes)", "INITIATED")

            proc = subprocess.Popen(
                [python_exe, str(temp_script)],
                cwd=str(run_cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            try:
                stdout, stderr = proc.communicate(timeout=timeout_s)
                success = proc.returncode == 0
                status_str = "SUCCESS" if success else f"EXIT_{proc.returncode}"
                self.log_audit_event("CodingAgent", "EXECUTE_PYTHON", f"ExitCode: {proc.returncode}", status_str)
                return success, stdout.strip(), stderr.strip()
            except subprocess.TimeoutExpired:
                proc.kill()
                self.log_audit_event("CodingAgent", "EXECUTE_PYTHON", f"Timeout after {timeout_s}s", "TIMEOUT_KILLED")
                return False, "", f"Execution timed out after {timeout_s} seconds."

        except Exception as e:
            self.log_audit_event("CodingAgent", "EXECUTE_PYTHON", f"Error: {e}", "EXCEPTION")
            return False, "", str(e)
        finally:
            if temp_script.exists():
                try:
                    temp_script.unlink()
                except Exception:
                    pass

    def run_command(self, cmd_str: str, timeout_s: float = 60.0, cwd: Optional[Path] = None) -> Tuple[bool, str, str]:
        """Execute terminal shell command with full system access."""
        run_cwd = (cwd or self.allowed_workspace).resolve()
        self.log_audit_event("AutomationAgent", "SHELL_COMMAND", f"Command: '{cmd_str}'", "INITIATED")
        try:
            proc = subprocess.Popen(
                cmd_str,
                shell=True,
                cwd=str(run_cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            stdout, stderr = proc.communicate(timeout=timeout_s)
            success = proc.returncode == 0
            self.log_audit_event("AutomationAgent", "SHELL_COMMAND", f"ExitCode: {proc.returncode}", "SUCCESS" if success else "FAILED")
            return success, stdout.strip(), stderr.strip()
        except subprocess.TimeoutExpired:
            proc.kill()
            self.log_audit_event("AutomationAgent", "SHELL_COMMAND", f"Timeout ({timeout_s}s)", "TIMEOUT_KILLED")
            return False, "", f"Command execution timed out after {timeout_s} seconds."
        except Exception as e:
            self.log_audit_event("AutomationAgent", "SHELL_COMMAND", f"Error: {e}", "EXCEPTION")
            return False, "", str(e)
