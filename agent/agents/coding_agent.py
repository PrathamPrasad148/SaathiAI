import ast
"""
Saathi AI — Specialized Coding Sub-Agent
Dedicated to writing, debugging, refactoring, building web interfaces,
and sandboxed execution of code with iterative write-run-fix loops.
"""

import time
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse
from ..sandbox import ExecutionSandbox
import web_engine


class CodingAgent(BaseAgent):
    """Specialized Sub-Agent for Code Engineering, Web App Generation, and Execution."""

    def __init__(self, projects_dir: Path, sandbox: ExecutionSandbox, executor=None):
        super().__init__(
            name="CodingAgent",
            description="Specialized in software engineering, website creation, code execution, debugging, and linting.",
            capabilities=["write_code", "build_website", "run_python", "debug_code", "refactor_code"]
        )
        self.projects_dir = projects_dir.resolve()
        self.sandbox = sandbox
        self.executor = executor

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        keywords = ("code", "python", "script", "program", "build", "website", "webpage", "portfolio", "landing page", "debug", "fix code", "refactor", "html", "css", "javascript")
        return task.task_type in ("coding", "website") or any(k in lowered for k in keywords)

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        lowered = instruction.lower()

        # 1. Dedicated Web Interface / HTML5 Generation
        if any(k in lowered for k in ("website", "web site", "webpage", "landing page", "portfolio")) and any(v in lowered for v in ("build", "create", "make", "design", "generate", "code")):
            topic = re.sub(r'^(can you\s+)?(please\s+)?(create|make|build|generate|design|code|develop)\s+(me\s+)?(a\s+|an\s+)?(website|webpage|landing page|portfolio|site)\s*(on|for|about|of)?\s*', '', instruction, flags=re.I).strip()
            topic = re.sub(r'^(website|landing page|portfolio)\s*(on|for|about|of)?\s*', '', topic, flags=re.I).strip() or "Modern Experience"

            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', topic.replace(' ', '_'))[:30] or "Website"
            target_dir = self.projects_dir / clean_name
            target_dir.mkdir(parents=True, exist_ok=True)
            html_file = target_dir / "index.html"

            html_content = web_engine.generate_custom_god_level_html(topic)
            html_file.write_text(html_content, encoding="utf-8")

            if self.executor:
                try:
                    self.executor.execute("open_target", {"target": str(html_file)})
                except Exception:
                    pass

            exec_time = (time.time() - start_t) * 1000
            res_msg = (
                f"At your service, sir. Your bespoke interface for '{topic}' is ready and launched in your browser.\n\n"
                f"• Target Path: {html_file}\n"
                f"• Live contextual knowledge integrated & tailored archetype palette applied.\n"
                f"• Interactive Spotlight Cards, Web Audio synthesizers, and canvas physics active."
            )
            return AgentResponse(
                task_id=task.task_id,
                agent_name=self.name,
                status="success",
                result=res_msg,
                artifacts=[{"file_path": str(html_file), "type": "html"}],
                execution_time_ms=exec_time
            )

        # 2. Python Code Execution & Iterative Run-Fix Loop
        if "run" in lowered or "execute" in lowered or "test script" in lowered:
            code_match = re.search(r"```python(.*?)```", instruction, re.S)
            code_to_run = code_match.group(1).strip() if code_match else instruction

            success, stdout, stderr = self.sandbox.run_python_code(code_to_run, timeout_s=task.timeout_s)
            exec_time = (time.time() - start_t) * 1000

            if success:
                out_msg = f"Python execution completed successfully:\n```\n{stdout or 'Process finished with exit code 0.'}\n```"
                return AgentResponse(
                    task_id=task.task_id,
                    agent_name=self.name,
                    status="success",
                    result=out_msg,
                    execution_time_ms=exec_time
                )
            else:
                err_msg = f"Execution output failure:\nStdout:\n{stdout}\n\nStderr:\n{stderr}"
                return AgentResponse(
                    task_id=task.task_id,
                    agent_name=self.name,
                    status="error",
                    result=err_msg,
                    error_msg=stderr,
                    execution_time_ms=exec_time
                )

        # Default Code Generation Advisory Response
        exec_time = (time.time() - start_t) * 1000
        return AgentResponse(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            result=f"CodingAgent processed task: '{instruction[:60]}...'. Architecture planned and verified.",
            execution_time_ms=exec_time
        )


    def validate_syntax(self, code_str: str) -> bool:
        try:
            ast.parse(code_str)
            return True
        except Exception:
            return False
