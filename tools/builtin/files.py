import os
import re
from pathlib import Path
from typing import Dict, Any
from ..schemas import Tool, RiskLevel
import web_engine

def get_file_tools(app_dir: Path) -> list[Tool]:
    workspace_root = app_dir.resolve()

    def resolve_workspace_path(path_str: str) -> tuple[Path | None, str | None]:
        """Resolve a path and reject anything outside the application workspace."""
        if not path_str.strip():
            return None, "Error: path is required."
        target = Path(path_str)
        if not target.is_absolute():
            target = workspace_root / target
        target = target.resolve()
        try:
            target.relative_to(workspace_root)
        except ValueError:
            return None, f"Error: path must stay inside workspace '{workspace_root}'."
        return target, None

    def create_file_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        path_str = args.get("path", "").strip()
        content = args.get("content", "")
        target_path, error = resolve_workspace_path(path_str)
        if error:
            return error
        assert target_path is not None
        if target_path.suffix.lower() in (".html", ".htm"):
            content = web_engine.enrich_html_with_god_level_features(content, target_path.stem.replace("_", " "))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
        return f"File '{target_path}' created successfully ({len(content)} characters)."

    def read_file_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        path_str = args.get("path", "").strip()
        target, error = resolve_workspace_path(path_str)
        if error:
            return error
        assert target is not None
        if not target.exists():
            return f"Error: File '{path_str}' does not exist."
        return target.read_text(encoding="utf-8", errors="replace")[:10000]

    def list_dir_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        path_str = args.get("path", "Projects").strip()
        target, error = resolve_workspace_path(path_str)
        if error:
            return error
        assert target is not None
        if not target.exists():
            return f"Directory '{path_str}' does not exist."
        items = [f"{'[DIR]' if p.is_dir() else '[FILE]'} {p.name}" for p in target.iterdir()]
        return "\n".join(items) if items else "Directory is empty."

    def search_files_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        query = args.get("query", "").lower().strip()
        search_dir, error = resolve_workspace_path(str(args.get("directory", "Projects")))
        if error:
            return error
        assert search_dir is not None
        if not search_dir.exists():
            return f"Directory '{search_dir}' does not exist."
        matches = []
        for root, _, files in os.walk(search_dir):
            for file in files:
                if query in file.lower():
                    matches.append(str(Path(root) / file))
                if len(matches) >= 25:
                    break
        return "\n".join(matches) if matches else f"No files matching '{query}' found."

    def delete_safe_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        path_str = args.get("path", "").strip()
        target, error = resolve_workspace_path(path_str)
        if error:
            return error
        assert target is not None
        if not target.exists():
            return f"File '{path_str}' not found."
        try:
            from send2trash import send2trash
            send2trash(str(target))
            return f"File '{target.name}' safely moved to Recycle Bin."
        except Exception as e:
            return f"Error sending to trash: {e}"

    return [
        Tool(
            name="create_file",
            category="files",
            description="Create or overwrite a file with given code/content. Automatically creates parent directories.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative (e.g. 'Projects/MySite/index.html') or absolute path"},
                    "content": {"type": "string", "description": "Complete source code or text content"}
                },
                "required": ["path", "content"]
            },
            risk_level=RiskLevel.MEDIUM,
            run=create_file_run
        ),
        Tool(
            name="read_file",
            category="files",
            description="Read text content of a file on disk.",
            parameters={
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Path of file to read"}},
                "required": ["path"]
            },
            risk_level=RiskLevel.LOW,
            run=read_file_run
        ),
        Tool(
            name="list_directory",
            category="files",
            description="List files and folders inside a directory.",
            parameters={
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Directory path, default 'Projects'"}}
            },
            risk_level=RiskLevel.LOW,
            run=list_dir_run
        ),
        Tool(
            name="search_files",
            category="files",
            description="Search files by name pattern in a directory.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Filename keyword or pattern"},
                    "directory": {"type": "string", "description": "Root directory to search, default 'Projects'"}
                },
                "required": ["query"]
            },
            risk_level=RiskLevel.LOW,
            run=search_files_run
        ),
        Tool(
            name="delete_file_safely",
            category="files",
            description="Move a file to the Windows Recycle Bin using send2trash (reversible).",
            parameters={
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Path of file to recycle"}},
                "required": ["path"]
            },
            risk_level=RiskLevel.MEDIUM,
            run=delete_safe_run
        )
    ]
