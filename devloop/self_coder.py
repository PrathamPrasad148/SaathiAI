"""Local model-driven self-coding and evaluation engine.

The engine proposes source changes in an isolated temporary copy, evaluates them,
and records outcomes as learning traces. It never edits the live repository.
"""

from __future__ import annotations

import difflib
import json
import os
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "qwen2.5-coder:7b"
MAX_CONTEXT_CHARS = 60000
MAX_OUTPUT_CHARS = 120000


class SelfCodingEngine:
    """Generate, test, and learn from isolated source candidates."""

    def __init__(
        self,
        repo_root: Path,
        model: str = DEFAULT_MODEL,
        ollama_url: str = OLLAMA_CHAT_URL,
        trace_file: Optional[Path] = None,
    ):
        self.repo_root = repo_root.resolve()
        self.model = model
        self.ollama_url = ollama_url
        self.trace_file = (trace_file or self.repo_root / "data" / "self_learning.jsonl").resolve()

    def _source_files(self) -> Iterable[Path]:
        roots = ("agent", "automation", "automations", "devloop", "memory", "tools", "tests", "ui")
        for root_name in roots:
            root = self.repo_root / root_name
            if not root.exists():
                continue
            yield from sorted(path for path in root.rglob("*.py") if path.is_file())

    def _build_context(self, task: str) -> str:
        chunks: List[str] = []
        used = 0
        for path in self._source_files():
            content = path.read_text(encoding="utf-8", errors="replace")
            remaining = MAX_CONTEXT_CHARS - used
            if remaining <= 0:
                break
            content = content[: min(len(content), remaining, 8000)]
            relative = path.relative_to(self.repo_root).as_posix()
            chunks.append(f"\n--- {relative} ---\n{content}")
            used += len(content)
        learning = ""
        if self.trace_file.exists():
            traces = self.trace_file.read_text(encoding="utf-8", errors="replace").splitlines()[-5:]
            learning = "\n\nRECENT EVALUATION TRACES:\n" + "\n".join(traces)[-6000:]
        return "".join(chunks) + learning

    def _request_candidate(self, task: str) -> Dict[str, Any]:
        prompt = (
            "You are a senior Python maintainer improving an existing project.\n"
            "Return ONLY valid JSON with this shape: "
            "{\"summary\": string, \"files\": [{\"path\": string, \"content\": string}]}\n"
            "The files array must contain complete replacement contents, not diffs. "
            "Change only the smallest number of files needed for the task. Preserve public APIs. "
            "Add or update focused tests when appropriate. Never include secrets, shell commands, "
            "absolute paths, or files outside the source/test directories.\n\n"
            f"TASK:\n{task}\n\nCURRENT SOURCE:\n{self._build_context(task)}"
        )
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You produce precise, testable repository changes."},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.2, "num_predict": 12000},
        }
        request = urllib.request.Request(
            self.ollama_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
        content = data.get("message", {}).get("content", "").strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        try:
            candidate = json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}")
            if start < 0 or end <= start:
                raise ValueError("Model returned no JSON candidate object")
            candidate = json.loads(content[start:end + 1])
        if not isinstance(candidate, dict) or not isinstance(candidate.get("files"), list):
            raise ValueError("Model returned an invalid candidate structure")
        return candidate

    def _validate_candidate(self, candidate: Dict[str, Any]) -> None:
        if len(json.dumps(candidate)) > MAX_OUTPUT_CHARS:
            raise ValueError("Candidate output is too large")
        allowed_roots = {"agent", "automation", "automations", "devloop", "memory", "tools", "tests", "ui"}
        for item in candidate["files"]:
            relative = str(item.get("path", "")).replace("\\", "/")
            path = Path(relative)
            if not relative or path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Invalid candidate path: {relative}")
            if path.parts[0] not in allowed_roots or path.suffix != ".py":
                raise ValueError(f"Candidate path is outside source policy: {relative}")
            if not isinstance(item.get("content"), str):
                raise ValueError(f"Candidate content is not text: {relative}")

    def _run_tests(self, candidate_root: Path) -> tuple[bool, str]:
        result = subprocess.run(
            [os.fspath(Path(os.sys.executable)), "-m", "unittest", "discover", "-s", "tests"],
            cwd=str(candidate_root),
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode == 0, output[-12000:]

    def _write_trace(self, trace: Dict[str, Any]) -> None:
        self.trace_file.parent.mkdir(parents=True, exist_ok=True)
        with self.trace_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(trace, ensure_ascii=True) + "\n")

    def run_once(self, task: str) -> Dict[str, Any]:
        """Generate and evaluate one isolated candidate, returning its report."""
        started = time.time()
        result: Dict[str, Any] = {"task": task, "model": self.model, "status": "failed"}
        try:
            candidate = self._request_candidate(task)
            self._validate_candidate(candidate)
            with tempfile.TemporaryDirectory(prefix="saathi_candidate_") as temp_dir:
                candidate_root = Path(temp_dir) / "repo"
                shutil.copytree(self.repo_root, candidate_root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
                changed_files: List[str] = []
                diff_lines: List[str] = []
                for item in candidate["files"]:
                    relative = item["path"].replace("\\", "/")
                    target = candidate_root / relative
                    before = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(item["content"], encoding="utf-8")
                    changed_files.append(relative)
                    diff_lines.extend(difflib.unified_diff(
                        before.splitlines(), item["content"].splitlines(),
                        fromfile=f"a/{relative}", tofile=f"b/{relative}", lineterm=""
                    ))
                passed, test_output = self._run_tests(candidate_root)
                result.update({
                    "status": "passed" if passed else "failed",
                    "summary": candidate.get("summary", ""),
                    "changed_files": changed_files,
                    "tests": test_output,
                    "diff": "\n".join(diff_lines)[-50000:],
                })
                if passed:
                    candidate_id = time.strftime("%Y%m%d_%H%M%S")
                    snapshot_dir = self.repo_root / "data" / "self_learning" / "candidates" / candidate_id
                    for relative in changed_files:
                        source = candidate_root / relative
                        target = snapshot_dir / relative
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, target)
                    result["candidate_dir"] = str(snapshot_dir)
        except Exception as error:
            result["error"] = str(error)
        result["duration_s"] = round(time.time() - started, 2)
        self._write_trace(result)
        return result
