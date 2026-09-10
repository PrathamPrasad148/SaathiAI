"""
Saathi AI 2.0 — Security Sandbox & AST Execution Validator
"""

import ast
import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
from ..tools.base import RiskLevel

class ExecutionSandbox:
    """Provides isolated execution environment for generated code, shell scripts, and high-risk tools."""

    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir.resolve()

    def validate_ast(self, code_str: str) -> Tuple[bool, Optional[str]]:
        """Perform AST parsing and syntax validation on Python code."""
        try:
            ast.parse(code_str)
            return True, None
        except SyntaxError as syntax_err:
            return False, f"SyntaxError at line {syntax_err.lineno}: {syntax_err.msg}"
        except Exception as e:
            return False, f"AST Validation Error: {e}"

    def check_permissions(self, risk_level: str, autonomy_level: int) -> bool:
        """Evaluate if risk level is permitted for current autonomy setting."""
        if risk_level == RiskLevel.LOW:
            return True
        if risk_level == RiskLevel.MEDIUM and autonomy_level >= 1:
            return True
        if risk_level == RiskLevel.HIGH and autonomy_level >= 2:
            return True
        if risk_level == RiskLevel.CRITICAL and autonomy_level >= 4:
            return True
        return False

    def run_python_code(self, code_str: str, timeout_s: int = 30) -> Tuple[bool, str, str]:
        """Execute Python code in isolated subprocess with timeout and AST check."""
        is_valid, err_msg = self.validate_ast(code_str)
        if not is_valid:
            return False, "", err_msg or "Invalid Python AST syntax"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as temp_f:
            temp_f.write(code_str)
            temp_file_path = temp_f.name

        try:
            res = subprocess.run(
                [sys.executable, temp_file_path],
                cwd=str(self.workspace_dir),
                capture_output=True,
                text=True,
                timeout=timeout_s
            )
            return (res.returncode == 0), res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return False, "", f"Execution timed out after {timeout_s} seconds."
        except Exception as e:
            return False, "", f"Sandbox execution failure: {e}"
        finally:
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except OSError:
                    pass
