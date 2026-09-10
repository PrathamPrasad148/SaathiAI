"""
Saathi AI 2.0 — File Parsing & Utility Helpers
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional

class FileUtils:
    """Standard file parsing utilities for JSON, CSV, and text files."""

    @staticmethod
    def read_json(file_path: Path) -> Optional[Dict[str, Any]]:
        """Read and parse JSON file safely."""
        path = file_path.resolve()
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    @staticmethod
    def write_json(file_path: Path, data: Any, indent: int = 2) -> bool:
        """Write data to JSON file safely."""
        path = file_path.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.write_text(json.dumps(data, indent=indent), encoding="utf-8")
            return True
        except OSError:
            return False

    @staticmethod
    def read_csv(file_path: Path) -> List[Dict[str, str]]:
        """Read CSV file and return rows as list of dictionaries."""
        path = file_path.resolve()
        if not path.exists():
            return []
        try:
            with open(path, mode="r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception:
            return []

    @staticmethod
    def read_text_safe(file_path: Path) -> str:
        """Read text file safely with utf-8 fallback."""
        path = file_path.resolve()
        if not path.exists():
            return ""
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""

