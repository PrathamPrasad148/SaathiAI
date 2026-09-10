"""
Saathi AI 2.0 — Web Research & Citation Engine
"""

import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional
from ..knowledge.store import LocalKnowledgeStore

class WebResearchEngine:
    """Multi-query search, quality ranking, and citation synthesis research engine."""

    def __init__(self, knowledge_store: Optional[LocalKnowledgeStore] = None):
        self.knowledge_store = knowledge_store

    def generate_sub_queries(self, topic: str) -> List[str]:
        """Decompose topic into multi-angle queries."""
        clean = topic.strip()
        return [
            clean,
            f"{clean} documentation specs",
            f"{clean} overview research"
        ]

    def rank_source_quality(self, url: str) -> float:
        """Assign source quality score based on domain authority."""
        lowered = url.lower()
        if any(d in lowered for d in ("wikipedia.org", "arxiv.org", "python.org", "gnu.org", "ieee.org")):
            return 0.95
        if any(d in lowered for d in ("github.com", "stackoverflow.com", "docs.python.org")):
            return 0.90
        if lowered.startswith("https://"):
            return 0.75
        return 0.50

    def execute_research(self, topic: str) -> Dict[str, Any]:
        queries = self.generate_sub_queries(topic)
        findings = []

        # Check local knowledge base first
        if self.knowledge_store:
            local_hits = self.knowledge_store.query(topic, limit=3)
            for hit in local_hits:
                findings.append({
                    "source": hit.get("source", "Local Knowledge Base"),
                    "quality": hit.get("source_quality", 0.9),
                    "content": hit.get("content", "")
                })

        summary = f"Research briefing for '{topic}':\n"
        if findings:
            for idx, f in enumerate(findings, 1):
                summary += f"\n[{idx}] Source: {f['source']} (Quality: {f['quality']})\n{f['content'][:300]}...\n"
        else:
            summary += "\nNo prior local cached entries found. Ready for real-time web search integration."

        return {
            "topic": topic,
            "queries": queries,
            "findings_count": len(findings),
            "summary": summary,
            "citations": [f["source"] for f in findings]
        }

