"""Local model-driven self-coding and evaluation engine.

The engine proposes source changes in an isolated temporary copy, evaluates them,
and records outcomes as learning traces. It never edits the live repository.
"""

from __future__ import annotations

import difflib
import ast
import importlib.util
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
MAX_CONTEXT_CHARS = 24000
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
        lowered_task = task.lower()
        chunks: List[str] = []
        used = 0
        for path in self._source_files():
            relative = path.relative_to(self.repo_root).as_posix()
            relevant = any(term in (lowered_task + " " + relative.lower()) for term in (
                "codingagent", "coding_agent", "ast", "lint", "test", "orchestrator", "memory", "vision", "webagent", "web_agent"
            ))
            if not relevant and used > 8000:
                continue
            content = path.read_text(encoding="utf-8", errors="replace")
            remaining = MAX_CONTEXT_CHARS - used
            if remaining <= 0:
                break
            content = content[: min(len(content), remaining, 8000)]
            chunks.append(f"\n--- {relative} ---\n{content}")
            used += len(content)
        learning = ""
        if self.trace_file.exists():
            traces = self.trace_file.read_text(encoding="utf-8", errors="replace").splitlines()[-5:]
            learning = "\n\nRECENT EVALUATION TRACES:\n" + "\n".join(traces)[-6000:]
        return "".join(chunks) + learning

    def _target_file_for_task(self, task: str) -> str:
        """Choose the smallest likely owning module for a backlog task."""
        lowered = task.lower().replace("-", "_")
        targets = (
            ("webagent", "agent/agents/web_agent.py"),
            ("web_agent", "agent/agents/web_agent.py"),
            ("visionagent", "agent/agents/vision_agent.py"),
            ("vision_agent", "agent/agents/vision_agent.py"),
            ("codingagent", "agent/agents/coding_agent.py"),
            ("coding_agent", "agent/agents/coding_agent.py"),
            ("sharedcontextstore", "agent/shared_memory.py"),
            ("shared_context_store", "agent/shared_memory.py"),
            ("orchestrator", "agent/orchestrator.py"),
        )
        for marker, path in targets:
            if marker in lowered:
                return path
        return "agent/orchestrator.py"

    def _request_candidate(self, task: str) -> Dict[str, Any]:
        target_file = self._target_file_for_task(task)
        target_path = self.repo_root / target_file
        api_hint = ""
        if target_path.exists():
            source = target_path.read_text(encoding="utf-8", errors="replace")
            signatures = [line.strip() for line in source.splitlines() if line.strip().startswith(("class ", "def __init__", "def can_handle", "def handle"))]
            api_hint = " Preserve these existing public declarations: " + "; ".join(signatures[:8])
        patch_prompt = (
            "Return only JSON in this exact shape: "
            f"{{\"summary\":\"...\",\"patches\":[{{\"path\":\"{target_file}\",\"diff\":\"unified diff\"}}]}} "
            "Create the smallest unified diff needed for the task. Preserve all existing public APIs, imports, "
            "constructor signatures, and unrelated behavior. Do not rewrite the whole file. "
            "Do not add third-party imports unless the package already appears in requirements.txt. "
            "Do not return an empty patches array or explanations outside JSON.\n"
            f"TASK: {task}.{api_hint}\n\nCURRENT SOURCE:\n{self._build_context(task)}"
        )
        try:
            patch_candidate = self._normalize_patch_candidate(self._call_model(patch_prompt))
            if patch_candidate["patches"]:
                return patch_candidate
        except ValueError:
            pass
        compact_prompt = (
            "Return only JSON in this exact shape: "
            f"{{\"summary\":\"...\",\"files\":[{{\"path\":\"{target_file}\",\"content\":\"...\"}}]}} "
            "Return one concise complete Python implementation for the requested change. "
            "Preserve existing imports, public classes, constructor signatures, and behavior; add changes minimally. "
            "Do not add third-party dependencies or import modules absent from requirements.txt. "
            "Do not return an empty files array or explanations outside JSON.\n"
            f"TASK: {task}.{api_hint}"
        )
        try:
            return self._normalize_candidate(self._call_model(compact_prompt))
        except ValueError:
            pass

        prompt = (
            "You are a senior Python maintainer improving an existing project.\n"
            "Return ONLY valid JSON with this shape: "
            "{\"summary\": string, \"files\": [{\"path\": string, \"content\": string}]}\n"
            "The files array must contain complete replacement contents, not diffs. "
            "The files array must contain at least one changed Python file; do not return an empty array. "
            "Change only the smallest number of files needed for the task. Preserve public APIs. "
            "Add or update focused tests when appropriate. Never include secrets, shell commands, "
            "absolute paths, or files outside the source/test directories.\n\n"
            f"TASK:\n{task}\n\nCURRENT SOURCE:\n{self._build_context(task)}"
        )
        candidate = self._call_model(prompt)
        try:
            return self._normalize_candidate(candidate)
        except ValueError as error:
            if "no file changes" not in str(error):
                raise
            raise

    def _call_model(self, prompt: str) -> Any:
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
        return candidate

    def _normalize_patch_candidate(self, candidate: Any) -> Dict[str, Any]:
        if not isinstance(candidate, dict):
            raise ValueError("Model returned an invalid patch structure")
        raw_patches = candidate.get("patches") or candidate.get("diffs")
        if not isinstance(raw_patches, list):
            raise ValueError("Model returned no patches")
        patches = []
        for item in raw_patches:
            if not isinstance(item, dict) or not item.get("path") or not item.get("diff"):
                raise ValueError("Model returned an invalid patch")
            patches.append({"path": item["path"], "diff": item["diff"]})
        normalized = dict(candidate)
        normalized["patches"] = patches
        normalized["files"] = []
        return normalized

    def _normalize_candidate(self, candidate: Any) -> Dict[str, Any]:
        """Normalize common local and hosted model response shapes."""
        if not isinstance(candidate, dict):
            raise ValueError("Model returned an invalid candidate structure")

        raw_files = candidate.get("files")
        if raw_files is None:
            for alias in ("changes", "edits", "modified_files"):
                if candidate.get(alias) is not None:
                    raw_files = candidate[alias]
                    break
        if raw_files is None and candidate.get("path") and candidate.get("content") is not None:
            raw_files = [{"path": candidate["path"], "content": candidate["content"]}]

        if isinstance(raw_files, dict):
            raw_files = [{"path": path, "content": content} for path, content in raw_files.items()]
        if not isinstance(raw_files, list):
            raise ValueError("Model returned no file changes")

        files: List[Dict[str, Any]] = []
        for item in raw_files:
            if not isinstance(item, dict):
                raise ValueError("Model returned an invalid file change")
            path = item.get("path") or item.get("file") or item.get("filename")
            content = item.get("content")
            if content is None:
                content = item.get("new_content")
            if path is None or content is None:
                raise ValueError("Model returned a file change without path or content")
            files.append({"path": path, "content": content})

        normalized = dict(candidate)
        normalized["files"] = files
        return normalized

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

    def _validate_patches(self, candidate: Dict[str, Any]) -> None:
        if len(json.dumps(candidate)) > MAX_OUTPUT_CHARS:
            raise ValueError("Patch output is too large")
        allowed_roots = {"agent", "automation", "automations", "devloop", "memory", "tools", "tests", "ui"}
        for item in candidate["patches"]:
            relative = str(item["path"]).replace("\\", "/")
            path = Path(relative)
            if not relative or path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Invalid patch path: {relative}")
            if path.parts[0] not in allowed_roots or path.suffix != ".py":
                raise ValueError(f"Patch path is outside source policy: {relative}")

    def _validate_dependencies(self, candidate_root: Path, changed_files: List[str]) -> None:
        """Reject candidates that add imports unavailable to the current project."""
        requirements = self.repo_root / "requirements.txt"
        declared = set()
        if requirements.exists():
            for line in requirements.read_text(encoding="utf-8", errors="replace").splitlines():
                package = line.strip().split("[", 1)[0].split("=", 1)[0].split(">", 1)[0].split("<", 1)[0]
                if package and not package.startswith(("#", "-")):
                    declared.add(package.lower().replace("-", "_"))
        for relative in changed_files:
            source = (candidate_root / relative).read_text(encoding="utf-8", errors="replace")
            try:
                tree = ast.parse(source, filename=relative)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                names = [node.module] if isinstance(node, ast.ImportFrom) and node.module else []
                if isinstance(node, ast.Import):
                    names.extend(alias.name for alias in node.names)
                for name in names:
                    top_level = name.split(".", 1)[0]
                    if top_level in {"agent", "automation", "automations", "devloop", "memory", "tools", "ui", "voice", "bridge", "typing", "pathlib", "json", "time", "os", "sys", "re", "ast", "threading", "urllib", "subprocess", "tempfile", "shutil", "difflib", "importlib"}:
                        continue
                    if top_level.lower().replace("-", "_") in declared:
                        continue
                    if importlib.util.find_spec(top_level) is None:
                        raise ValueError(f"Candidate adds unavailable dependency: {top_level}")

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
            is_patch_candidate = bool(candidate.get("patches"))
            if is_patch_candidate:
                self._validate_patches(candidate)
            else:
                self._validate_candidate(candidate)
            with tempfile.TemporaryDirectory(prefix="saathi_candidate_") as temp_dir:
                candidate_root = Path(temp_dir) / "repo"
                shutil.copytree(self.repo_root, candidate_root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
                changed_files: List[str] = []
                diff_lines: List[str] = []
                if is_patch_candidate:
                    for item in candidate["patches"]:
                        patch_path = Path(temp_dir) / "candidate.patch"
                        patch_path.write_text(item["diff"], encoding="utf-8")
                        applied = subprocess.run(
                            ["git", "apply", "--whitespace=nowarn", str(patch_path)],
                            cwd=str(candidate_root), capture_output=True, text=True, check=False
                        )
                        if applied.returncode != 0:
                            raise ValueError(f"Patch failed for {item['path']}: {applied.stderr.strip()}")
                        changed_files.append(item["path"])
                        diff_lines.append(item["diff"])
                for item in candidate.get("files", []):
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
                self._validate_dependencies(candidate_root, changed_files)
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
