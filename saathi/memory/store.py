"""
Saathi AI 2.0 — Multi-Tier Memory System & Memory Consolidation Engine
"""

import json
import time
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class MultiTierMemoryStore:
    """Manages Short-Term, Episodic, Semantic, and Project Memory with scoring and privacy features."""

    def __init__(self, memory_dir: Optional[Path] = None):
        self.memory_dir = memory_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "memory")
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.short_term_file = self.memory_dir / "short_term.json"
        self.episodic_file = self.memory_dir / "episodic.json"
        self.semantic_file = self.memory_dir / "semantic.json"

        self.short_term: List[Dict[str, Any]] = self._load_file(self.short_term_file)
        self.episodic: List[Dict[str, Any]] = self._load_file(self.episodic_file)
        self.semantic: List[Dict[str, Any]] = self._load_file(self.semantic_file)

    def _load_file(self, file_path: Path) -> List[Dict[str, Any]]:
        if file_path.exists():
            try:
                return json.loads(file_path.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save_all(self) -> None:
        try:
            self.short_term_file.write_text(json.dumps(self.short_term, indent=2), encoding="utf-8")
            self.episodic_file.write_text(json.dumps(self.episodic, indent=2), encoding="utf-8")
            self.semantic_file.write_text(json.dumps(self.semantic, indent=2), encoding="utf-8")
        except OSError:
            pass

    # --- Short-Term Memory ---
    def add_short_term(self, role: str, content: str) -> None:
        entry = {"role": role, "content": content, "timestamp": time.time()}
        self.short_term.append(entry)
        if len(self.short_term) > 50:  # Max 50 short-term turns
            self.short_term = self.short_term[-50:]
        self._save_all()

    def get_short_term(self) -> List[Dict[str, Any]]:
        return self.short_term

    # --- Episodic Memory ---
    def add_episodic(self, task: str, result: str, success: bool = True) -> None:
        entry = {
            "task": task,
            "result": result,
            "success": success,
            "timestamp": time.time(),
            "importance": 0.8
        }
        self.episodic.append(entry)
        self._save_all()

    def get_episodic(self, limit: int = 10) -> List[Dict[str, Any]]:
        return sorted(self.episodic, key=lambda x: x.get("timestamp", 0), reverse=True)[:limit]

    # --- Semantic Memory ---
    def add_semantic(self, fact: str, category: str = "GENERAL", confidence: float = 0.9, importance: float = 0.7) -> None:
        # Check deduplication
        for item in self.semantic:
            if item.get("fact", "").lower().strip() == fact.lower().strip():
                item["confidence"] = max(item["confidence"], confidence)
                item["timestamp"] = time.time()
                self._save_all()
                return

        entry = {
            "fact": fact,
            "category": category,
            "confidence": confidence,
            "importance": importance,
            "timestamp": time.time()
        }
        self.semantic.append(entry)
        self._save_all()

    def get_semantic(self, query: str = "") -> List[Dict[str, Any]]:
        if not query:
            return self.semantic
        lowered = query.lower()
        results = []
        for s in self.semantic:
            score = 0.0
            if any(w in s["fact"].lower() for w in lowered.split()):
                recency = 1.0 / (1.0 + (time.time() - s.get("timestamp", time.time())) / 86400.0)
                score = s.get("importance", 0.5) * s.get("confidence", 0.5) * recency
                results.append((score, s))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results]

    # --- Memory Consolidation ---
    def consolidate(self) -> None:
        """Compress old short-term turns into semantic & episodic facts."""
        if len(self.short_term) < 10:
            return

        # Extract user preferences and factual statements
        for turn in self.short_term:
            content = turn.get("content", "")
            if turn.get("role") == "user" and ("my name is" in content.lower() or "i prefer" in content.lower() or "remember that" in content.lower()):
                self.add_semantic(content, category="USER_PREFERENCE", importance=0.95)

        # Truncate short-term buffer after consolidation
        self.short_term = self.short_term[-10:]
        self._save_all()

    # --- Privacy Control ---
    def forget(self, target_text: str) -> int:
        lowered = target_text.lower()
        count = 0
        before_sem = len(self.semantic)
        self.semantic = [s for s in self.semantic if lowered not in s.get("fact", "").lower()]
        count += before_sem - len(self.semantic)

        before_ep = len(self.episodic)
        self.episodic = [e for e in self.episodic if lowered not in e.get("task", "").lower()]
        count += before_ep - len(self.episodic)

        self._save_all()
        return count

    def forget_all(self) -> None:
        self.short_term = []
        self.episodic = []
        self.semantic = []
        self._save_all()

