"""
Saathi AI 2.0 — Tool Discovery & Life-Cycle Subsystem
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class ToolState:
    DISCOVERED = "DISCOVERED"
    ANALYZED = "ANALYZED"
    SECURITY_CHECK = "SECURITY_CHECK"
    USER_APPROVAL = "USER_APPROVAL"
    INSTALLED = "INSTALLED"
    ENABLED = "ENABLED"

class ToolDiscoverySubsystem:
    """Manages candidate tools lifecycle without uncontrolled auto-installation."""

    def __init__(self, candidates_file: Optional[Path] = None):
        self.candidates_file = candidates_file or (Path(__file__).resolve().parent.parent.parent / "data" / "knowledge" / "tool_candidates.json")
        self.candidates_file.parent.mkdir(parents=True, exist_ok=True)
        self.candidates: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if self.candidates_file.exists():
            try:
                return json.loads(self.candidates_file.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save(self) -> None:
        try:
            self.candidates_file.write_text(json.dumps(self.candidates, indent=2), encoding="utf-8")
        except OSError:
            pass

    def add_candidate(self, name: str, description: str, source: str, category: str = "GENERAL") -> Dict[str, Any]:
        cand = {
            "name": name,
            "description": description,
            "source": source,
            "category": category,
            "state": ToolState.DISCOVERED,
            "security_passed": False,
            "user_approved": False
        }
        self.candidates.append(cand)
        self._save()
        return cand

    def update_state(self, name: str, new_state: str, approved: bool = False) -> bool:
        for c in self.candidates:
            if c["name"] == name:
                c["state"] = new_state
                if approved:
                    c["user_approved"] = True
                self._save()
                return True
        return False

    def get_pending_approval(self) -> List[Dict[str, Any]]:
        return [c for c in self.candidates if c["state"] == ToolState.USER_APPROVAL and not c["user_approved"]]

