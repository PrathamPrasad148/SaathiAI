"""
Saathi AI 2.0 — Ollama Local Model Provider Adapter
"""

import json
import urllib.request
import urllib.error
from typing import Generator, List, Dict, Any, Optional
from ..base import ModelProvider

class OllamaProvider(ModelProvider):
    """Adapter for local Ollama server models."""

    def __init__(self, model_id: str = "saathi-distill-brain:latest", host: str = "http://localhost:11434", timeout: int = 120):
        super().__init__(name=f"Ollama-{model_id}", model_id=model_id)
        self.host = host.rstrip('/')
        self.timeout = timeout

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            payload["system"] = system_prompt

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                return res_data.get("response", "").strip()
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed for '{self.model_id}': {e}")

    def stream(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Generator[str, None, None]:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": True
        }
        if system_prompt:
            payload["system"] = system_prompt

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                for line in response:
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        text_piece = chunk.get("response", "")
                        if text_piece:
                            yield text_piece
                        if chunk.get("done", False):
                            break
        except Exception as e:
            yield f"\n[Ollama Stream Error: {e}]"

    def embed(self, text: str) -> List[float]:
        url = f"{self.host}/api/embeddings"
        payload = {
            "model": self.model_id,
            "prompt": text
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                return res_data.get("embedding", [])
        except Exception:
            return []

    def health_check(self) -> bool:
        url = f"{self.host}/api/tags"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def capabilities(self) -> List[str]:
        return ["chat", "coding", "reasoning", "math", "summarization", "local"]

    def estimate_cost(self, prompt: str) -> float:
        return 0.0  # 100% Free local execution

    def available(self) -> bool:
        return self.health_check()
