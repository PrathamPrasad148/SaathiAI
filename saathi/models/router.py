"""
Saathi AI 2.0 — Dynamic Task Classification & Model Router
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from .base import ModelProvider
from .providers.ollama import OllamaProvider

class TaskCategory:
    CONVERSATION = "casual_conversation"
    MATHEMATICS = "mathematics"
    CODING = "coding"
    RESEARCH = "research"
    SUMMARIZATION = "summarization"
    DOCUMENT_ANALYSIS = "document_analysis"
    REASONING = "reasoning"
    VISION = "vision"
    PLANNING = "planning"
    SYSTEM_OPERATION = "system_operation"

class ModelRouter:
    """Classifies user tasks and routes prompts to optimal available model provider with fallback."""

    def __init__(self, providers: Optional[List[ModelProvider]] = None):
        self.providers: List[ModelProvider] = providers or [
            OllamaProvider(model_id="saathi-distill-brain:latest"),
            OllamaProvider(model_id="qwen2.5-coder:7b")
        ]

    def register_provider(self, provider: ModelProvider) -> None:
        self.providers.append(provider)

    def classify_task(self, prompt: str) -> str:
        lowered = prompt.lower().strip()

        if any(k in lowered for k in ("code", "python", "script", "function", "debug", "refactor", "html", "css", "git", "bug")):
            return TaskCategory.CODING
        if any(k in lowered for k in ("solve", "math", "equation", "proof", "integral", "derivative", "calculus", "matrix", "algebra", "theorem")):
            return TaskCategory.MATHEMATICS
        if any(k in lowered for k in ("search", "research", "find online", "who is", "what is", "news", "paper", "wikipedia", "latest")):
            return TaskCategory.RESEARCH
        if any(k in lowered for k in ("summarize", "summary", "tldr", "digest", "condense")):
            return TaskCategory.SUMMARIZATION
        if any(k in lowered for k in ("pdf", "docx", "file", "document", "parse", "read file")):
            return TaskCategory.DOCUMENT_ANALYSIS
        if any(k in lowered for k in ("plan", "schedule", "steps", "workflow", "roadmap", "architecture")):
            return TaskCategory.PLANNING
        if any(k in lowered for k in ("why", "reason", "evaluate", "compare", "think step by step", "analyze")):
            return TaskCategory.REASONING

        return TaskCategory.CONVERSATION

    def route(self, prompt: str) -> Tuple[ModelProvider, str]:
        category = self.classify_task(prompt)

        # Filter available providers
        available_providers = [p for p in self.providers if p.available()]

        if not available_providers:
            # Fallback to default first provider even if offline check failed, or raise clear error
            return self.providers[0], category

        # Specialized routing logic
        if category == TaskCategory.CODING:
            for p in available_providers:
                if "coder" in p.model_id.lower():
                    return p, category

        # Default: return highest priority available provider
        return available_providers[0], category

    def generate_with_fallback(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        provider, category = self.route(prompt)
        try:
            return provider.generate(prompt, system_prompt=system_prompt)
        except Exception as primary_err:
            # Try secondary available providers
            for alt_provider in self.providers:
                if alt_provider != provider and alt_provider.available():
                    try:
                        return alt_provider.generate(prompt, system_prompt=system_prompt)
                    except Exception:
                        continue
            raise RuntimeError(f"All model providers failed to generate response: {primary_err}")

