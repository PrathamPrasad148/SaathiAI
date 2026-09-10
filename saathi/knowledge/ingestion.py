"""
Saathi AI 2.0 — Document Chunking & Knowledge Ingestion Engine
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from .store import LocalKnowledgeStore

class KnowledgeIngestionPipeline:
    """Ingests, cleans, chunks, and indexes documents into the local knowledge store."""

    def __init__(self, store: LocalKnowledgeStore, chunk_size: int = 500, chunk_overlap: int = 50):
        self.store = store
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        if not words:
            return []

        chunks = []
        i = 0
        while i < len(words):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append(" ".join(chunk_words))
            i += self.chunk_size - self.chunk_overlap

        return chunks

    def ingest_file(self, file_path: Path, topic: str = "GENERAL", source_quality: float = 0.85) -> int:
        path = file_path.resolve()
        if not path.exists():
            return 0

        ext = path.suffix.lower()
        if ext not in (".txt", ".md", ".py", ".json", ".csv", ".html", ".log"):
            return 0

        try:
            raw_text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return 0

        chunks = self.chunk_text(raw_text)
        added_count = 0

        for chunk_idx, chunk in enumerate(chunks):
            metadata = {
                "file_name": path.name,
                "file_path": str(path),
                "chunk_index": chunk_idx,
                "total_chunks": len(chunks)
            }
            inserted = self.store.add_item(
                content=chunk,
                source=str(path),
                topic=topic,
                confidence=0.9,
                source_quality=source_quality,
                metadata=metadata
            )
            if inserted:
                added_count += 1

        return added_count
