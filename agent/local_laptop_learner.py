"""
Saathi AI — Autonomous Local Laptop Drive Knowledge Ingestion Engine
Crawls local laptop directories (Documents, Desktop, Downloads, Projects, SAATHIAI workspace),
extracts code patterns, documentation, text transcripts, and project structures, and ingests
the knowledge into Saathi's long-term memory store and self-learning dataset.
"""

import os
import sys
import re
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

REPO_ROOT = Path(r"C:\SAATHIAI").resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Supported file extensions for local laptop knowledge crawling
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".html", ".css", ".json", ".md", ".txt",
    ".csv", ".sql", ".cpp", ".c", ".h", ".rs", ".java", ".xml", ".yml", ".yaml"
}

# Laptop target directories to scan for self-learning
DEFAULT_SCAN_DIRS = [
    REPO_ROOT,
    Path(os.path.expandvars(r"%USERPROFILE%\Documents")),
    Path(os.path.expandvars(r"%USERPROFILE%\Desktop")),
    Path(os.path.expandvars(r"%USERPROFILE%\Downloads")),
    Path(os.path.expandvars(r"%USERPROFILE%\Projects"))
]


class LocalLaptopLearner:
    """Engine for autonomous crawling and self-learning from local laptop files and projects."""

    def __init__(self, scan_dirs: Optional[List[Path]] = None):
        self.scan_dirs = scan_dirs or DEFAULT_SCAN_DIRS
        self.learning_data_file = REPO_ROOT / "data" / "self_learning.jsonl"
        self.learning_data_file.parent.mkdir(parents=True, exist_ok=True)
        self.processed_files: Set[str] = set()
        self._load_processed_history()

    def log(self, msg: str):
        print(f"[{time.strftime('%H:%M:%S')}] [LOCAL-LAPTOP-LEARNER] {msg}")

    def _load_processed_history(self):
        """Load previously processed file paths to prevent redundant re-indexing."""
        if not self.learning_data_file.exists():
            return
        try:
            for line in self.learning_data_file.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if "file_path" in data:
                        self.processed_files.add(data["file_path"])
                except Exception:
                    pass
        except Exception as e:
            self.log(f"History load warning: {e}")

    def extract_file_knowledge(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract structured code patterns, concepts, and text from a single local laptop file."""
        if not file_path.exists() or file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return None

        # Ignore huge binary or node_modules / .git files
        if file_path.stat().st_size > 2 * 1024 * 1024:  # > 2MB
            return None

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace").strip()
            if not content:
                return None

            ext = file_path.suffix.lower()
            file_str = str(file_path)

            # Extract key code entities (classes, functions, imports, titles)
            classes = re.findall(r"^\s*class\s+([a-zA-Z0-9_]+)", content, re.MULTILINE)
            functions = re.findall(r"^\s*def\s+([a-zA-Z0-9_]+)", content, re.MULTILINE)
            imports = re.findall(r"^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)", content, re.MULTILINE)

            snippet = content[:500]  # First 500 chars summary snippet

            knowledge_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "local_laptop_drive",
                "file_name": file_path.name,
                "file_path": file_str,
                "extension": ext,
                "size_bytes": len(content),
                "classes_found": classes[:10],
                "functions_found": functions[:15],
                "imports_found": list(set(imports[:15])),
                "snippet": snippet
            }
            return knowledge_entry
        except Exception as e:
            return None

    def scan_and_learn_from_laptop(self, max_files_per_run: int = 25) -> int:
        """Scan target laptop directories and ingest new file knowledge into self_learning.jsonl."""
        self.log("Scanning local laptop directories for new code patterns and knowledge...")
        ingested_count = 0

        for target_dir in self.scan_dirs:
            if not target_dir.exists():
                continue

            self.log(f"Crawling directory: '{target_dir}'...")
            try:
                for root, dirs, files in os.walk(target_dir):
                    # Skip hidden directories like .git, __pycache__, node_modules, .venv
                    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "node_modules", ".venv")]

                    for fname in files:
                        fpath = Path(root) / fname
                        fstr = str(fpath)

                        if fstr in self.processed_files:
                            continue

                        entry = self.extract_file_knowledge(fpath)
                        if entry:
                            with open(self.learning_data_file, "a", encoding="utf-8") as f:
                                f.write(json.dumps(entry) + "\n")

                            self.processed_files.add(fstr)
                            ingested_count += 1
                            self.log(f"Ingested local knowledge from: '{fpath.name}' ({entry['size_bytes']} bytes)")

                            if ingested_count >= max_files_per_run:
                                break
                    if ingested_count >= max_files_per_run:
                        break
            except Exception as e:
                self.log(f"Directory crawl notice for '{target_dir}': {e}")

        self.log(f"Local Laptop Knowledge Ingestion complete! Added {ingested_count} new local files to knowledge store.")
        return ingested_count


if __name__ == "__main__":
    learner = LocalLaptopLearner()
    learner.scan_and_learn_from_laptop(max_files_per_run=10)

