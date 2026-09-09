"""
Saathi AI — Universal Free Internet AI Models Client
Connects Saathi to all free AI model endpoints available across the web:
- Pollinations AI (Unlimited Free Text Generation: Qwen, DeepSeek, Mistral, Llama3)
- OpenRouter Free API (Gemini 2.0 Flash, DeepSeek-R1 Free, Llama 3.3 70B Free)
- HuggingFace Free Inference API
- Local Ollama High-Speed Fallback
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import time
from typing import Dict, Any, List, Optional, Tuple


FREE_MODEL_PROVIDERS = [
    {
        "name": "Pollinations-QwenCoder",
        "type": "pollinations",
        "model": "qwen-coder",
        "url": "https://text.pollinations.ai/"
    },
    {
        "name": "Pollinations-DeepSeek",
        "type": "pollinations",
        "model": "deepseek",
        "url": "https://text.pollinations.ai/"
    },
    {
        "name": "Pollinations-OpenAI",
        "type": "pollinations",
        "model": "openai",
        "url": "https://text.pollinations.ai/"
    },
    {
        "name": "OpenRouter-GeminiFlash-Free",
        "type": "openrouter",
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "url": "https://openrouter.ai/api/v1/chat/completions"
    },
    {
        "name": "OpenRouter-DeepSeekR1-Free",
        "type": "openrouter",
        "model": "deepseek/deepseek-r1:free",
        "url": "https://openrouter.ai/api/v1/chat/completions"
    },
    {
        "name": "OpenRouter-Llama33-Free",
        "type": "openrouter",
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "url": "https://openrouter.ai/api/v1/chat/completions"
    }
]


class UniversalFreeAIClient:
    """Client that queries free AI model endpoints across the internet with auto-failover."""

    def __init__(self):
        self.providers = FREE_MODEL_PROVIDERS

    def query_pollinations_free(self, prompt: str, system_prompt: str = "", model_name: str = "qwen-coder") -> Optional[str]:
        """Query Pollinations AI free unlimited API endpoint."""
        try:
            full_prompt = f"{system_prompt}\n\nUser Directive: {prompt}".strip()
            payload = {
                "messages": [
                    {"role": "system", "content": system_prompt or "You are Saathi AI, an omniscient AI co-pilot created by Pratham Prasad."},
                    {"role": "user", "content": prompt}
                ],
                "model": model_name,
                "jsonMode": False
            }
            req = urllib.request.Request(
                "https://text.pollinations.ai/",
                json.dumps(payload).encode("utf-8"),
                {"Content-Type": "application/json", "User-Agent": "SaathiAI/2.0"}
            )
            with urllib.request.urlopen(req, timeout=25) as resp:
                result_text = resp.read().decode("utf-8").strip()
                if result_text:
                    return result_text
        except Exception as e:
            pass
        return None

    def query_openrouter_free(self, prompt: str, system_prompt: str = "", model_name: str = "google/gemini-2.0-flash-lite-preview-02-05:free") -> Optional[str]:
        """Query OpenRouter free tier models API."""
        try:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt or "You are Saathi AI."},
                    {"role": "user", "content": prompt}
                ]
            }
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                json.dumps(payload).encode("utf-8"),
                {
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/PrathamPrasad148/SaathiAI",
                    "X-Title": "Saathi AI OS"
                }
            )
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            pass
        return None

    def generate_with_free_web_models(self, prompt: str, system_prompt: str = "") -> Tuple[bool, str, str]:
        """Auto-failover generator across all free internet AI models."""
        # 1. Try Pollinations Qwen-Coder
        res = self.query_pollinations_free(prompt, system_prompt, model_name="qwen-coder")
        if res:
            return True, res, "Pollinations-QwenCoder"

        # 2. Try Pollinations DeepSeek
        res = self.query_pollinations_free(prompt, system_prompt, model_name="deepseek")
        if res:
            return True, res, "Pollinations-DeepSeek"

        # 3. Try Pollinations OpenAI
        res = self.query_pollinations_free(prompt, system_prompt, model_name="openai")
        if res:
            return True, res, "Pollinations-OpenAI"

        # 4. Try OpenRouter Gemini 2.0 Flash Free
        res = self.query_openrouter_free(prompt, system_prompt, model_name="google/gemini-2.0-flash-lite-preview-02-05:free")
        if res:
            return True, res, "OpenRouter-GeminiFlash-Free"

        # 5. Try OpenRouter DeepSeek R1 Free
        res = self.query_openrouter_free(prompt, system_prompt, model_name="deepseek/deepseek-r1:free")
        if res:
            return True, res, "OpenRouter-DeepSeekR1-Free"

        return False, "", "None"
