"""
Saathi AI 2.0 — Local Hybrid RAG Knowledge Database (SQLite + Metadata + Vector/BM25)
"""

import sqlite3
import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

class LocalKnowledgeStore:
    """Local SQLite-backed hybrid RAG knowledge database with provenance and content hashing."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (Path(__file__).resolve().parent.parent.parent / "data" / "knowledge.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_hash TEXT UNIQUE,
                    source TEXT,
                    topic TEXT,
                    content TEXT,
                    confidence REAL,
                    source_quality REAL,
                    timestamp REAL,
                    metadata TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic ON knowledge_items(topic)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash ON knowledge_items(content_hash)")
            conn.commit()

    def add_item(self, content: str, source: str, topic: str = "GENERAL", confidence: float = 0.8, source_quality: float = 0.8, metadata: Optional[Dict[str, Any]] = None) -> bool:
        clean_text = content.strip()
        if not clean_text:
            return False

        content_hash = hashlib.sha256(clean_text.encode('utf-8')).hexdigest()
        meta_json = json.dumps(metadata or {})

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO knowledge_items (content_hash, source, topic, content, confidence, source_quality, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (content_hash, source, topic, clean_text, confidence, source_quality, time.time(), meta_json))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Deduplication: already exists
                return False

    def query(self, search_text: str, topic: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        keywords = [w.lower() for w in search_text.split() if len(w) > 2]
        if not keywords:
            return []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query_sql = "SELECT * FROM knowledge_items"
            params = []

            if topic:
                query_sql += " WHERE topic = ?"
                params.append(topic)

            cursor.execute(query_sql, params)
            rows = cursor.fetchall()

        scored_results = []
        for r in rows:
            content_lower = r["content"].lower()
            match_count = sum(1 for kw in keywords if kw in content_lower)
            if match_count > 0:
                # Score = match ratio * confidence * source quality
                score = (match_count / len(keywords)) * r["confidence"] * r["source_quality"]
                scored_results.append((score, dict(r)))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_results[:limit]]

    def delete_by_source(self, source: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM knowledge_items WHERE source = ?", (source,))
            count = cursor.rowcount
            conn.commit()
            return count

    def count(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM knowledge_items")
            return cursor.fetchone()[0]

    def close(self) -> None:
        pass
