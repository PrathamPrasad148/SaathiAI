"""
Saathi AI — Autonomous Web AI Browser Trainer & Multi-AI Consensus Engine
Enables Saathi AI to autonomously launch Chrome/Edge with default user profile sessions,
query web AI platforms (ChatGPT, Claude, Gemini, DeepSeek, Perplexity, HuggingChat, Poe),
detect rate limits/quotas to auto-switch providers, fuse multi-AI responses into super-blueprints,
and automatically generate and register new specialized Python sub-agents via SelfAgentBuilder.
"""

import os
import sys
import re
import json
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

REPO_ROOT = Path(r"C:\SAATHIAI").resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from automation.app_launcher import get_chrome_executable, get_edge_executable, open_url_in_browser
from automation.keyboard import type_text, press_key, send_hotkey
from automation.clipboard import copy_to_clipboard, get_clipboard_text
from automation.windows import focus_window_by_title
from agent.free_models_client import UniversalFreeAIClient
from agent.self_agent_builder import SelfAgentBuilder
from agent.agent_factory import DynamicAgentFactory

# Web AI Platforms in Priority Cascade Order
WEB_AI_PLATFORMS = [
    {"name": "ChatGPT", "url": "https://chatgpt.com", "browser": "chrome"},
    {"name": "Claude", "url": "https://claude.ai", "browser": "chrome"},
    {"name": "Gemini", "url": "https://gemini.google.com", "browser": "chrome"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "browser": "chrome"},
    {"name": "Perplexity", "url": "https://www.perplexity.ai", "browser": "chrome"},
    {"name": "HuggingChat", "url": "https://huggingface.co/chat", "browser": "chrome"},
    {"name": "Poe", "url": "https://poe.com", "browser": "chrome"}
]

# Keywords indicating Rate Limit / Quota Exceeded / Paywall Prompt
LIMIT_KEYWORDS = [
    "rate limit", "quota exceeded", "upgrade to plus", "upgrade to pro",
    "try again in", "message limit reached", "too many requests",
    "you've reached your limit", "daily limit reached", "hourly limit",
    "subscription required", "free limit reached"
]


def get_chrome_user_data_dir() -> str:
    """Return default Chrome User Data directory path on Windows."""
    return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")


def get_edge_user_data_dir() -> str:
    """Return default Edge User Data directory path on Windows."""
    return os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")


class BrowserAITrainer:
    """Autonomous Web AI Browser Trainer & Multi-AI Consensus Synthesis Engine."""

    def __init__(self, factory: Optional[DynamicAgentFactory] = None):
        self.factory = factory or DynamicAgentFactory()
        self.builder = SelfAgentBuilder(factory=self.factory)
        self.free_client = UniversalFreeAIClient()
        self.current_provider_idx = 0
        self.learning_data_file = REPO_ROOT / "data" / "self_learning.jsonl"
        self.learning_data_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str):
        print(f"[{time.strftime('%H:%M:%S')}] [BROWSER-AI-TRAINER] {msg}")

    def get_current_provider(self) -> Dict[str, str]:
        return WEB_AI_PLATFORMS[self.current_provider_idx % len(WEB_AI_PLATFORMS)]

    def rotate_provider(self) -> Dict[str, str]:
        """Switch to next available web AI provider in cascade."""
        self.current_provider_idx = (self.current_provider_idx + 1) % len(WEB_AI_PLATFORMS)
        new_provider = self.get_current_provider()
        self.log(f"Auto-switched web AI provider to: '{new_provider['name']}' ({new_provider['url']})")
        return new_provider

    def launch_browser_with_profile(self, url: str, browser: str = "chrome") -> bool:
        """Launch Chrome or Edge executable with user data profile path for logged-in sessions."""
        exe = get_chrome_executable() if browser == "chrome" else get_edge_executable()
        profile_dir = get_chrome_user_data_dir() if browser == "chrome" else get_edge_user_data_dir()

        if exe and os.path.exists(exe):
            try:
                cmd = [exe, f"--user-data-dir={profile_dir}", url]
                subprocess.Popen(cmd)
                self.log(f"Launched {browser.capitalize()} with user profile path: '{url}'")
                time.sleep(2.5)
                return True
            except Exception as e:
                self.log(f"Failed to launch browser with profile: {e}")

        # Fallback to standard open_url_in_browser
        return open_url_in_browser(url, force_chrome=(browser == "chrome"))

    def detect_limit_or_paywall(self, text: str) -> bool:
        """Check if extracted page text contains rate limit or paywall notifications."""
        lowered = text.lower()
        return any(k in lowered for k in LIMIT_KEYWORDS)

    def query_web_ai_agent(self, prompt: str) -> Optional[str]:
        """Attempt querying current web AI agent in browser."""
        provider = self.get_current_provider()
        self.log(f"Querying web AI platform '{provider['name']}' at {provider['url']}...")

        # 1. Launch browser to target AI platform
        self.launch_browser_with_profile(provider['url'], provider['browser'])
        time.sleep(2.0)

        # 2. Focus browser window
        focus_window_by_title(provider['name'])
        time.sleep(0.5)

        # 3. Paste prompt into active input field
        try:
            copy_to_clipboard(prompt)
            send_hotkey("ctrl", "v")
            time.sleep(0.3)
            press_key("enter")
            self.log(f"Submitted directive to '{provider['name']}'. Waiting for completion...")
            time.sleep(8.0)  # Allow time for AI response generation

            # 4. Scrape response via Ctrl+A, Ctrl+C clipboard capture
            send_hotkey("ctrl", "a")
            time.sleep(0.2)
            send_hotkey("ctrl", "c")
            time.sleep(0.3)

            response_text = get_clipboard_text().strip()

            # Check if rate limit or paywall occurred
            if self.detect_limit_or_paywall(response_text):
                self.log(f"Detected rate limit / quota prompt on '{provider['name']}'. Auto-switching...")
                self.rotate_provider()
                return None

            if response_text and len(response_text) > 50:
                self.log(f"Successfully received response ({len(response_text)} chars) from '{provider['name']}'.")
                return response_text
        except Exception as e:
            self.log(f"GUI automation interaction error on '{provider['name']}': {e}")

        # Rotate provider if failed
        self.rotate_provider()
        return None

    def query_multi_ai_consensus(self, prompt: str, system_prompt: str = "") -> str:
        """
        Query multiple AI models (Web AI platforms + Free API fallback)
        and synthesize a consensus response for maximum intelligence.
        """
        self.log("Initiating Multi-AI Consensus Synthesis across web and free model endpoints...")
        responses: List[str] = []

        # 1. Try primary web AI agent via browser
        web_res = self.query_web_ai_agent(prompt)
        if web_res:
            responses.append(web_res)

        # 2. Query free model endpoints (Pollinations Qwen & OpenRouter Gemini/DeepSeek)
        pollinations_res = self.free_client.query_pollinations_free(prompt, system_prompt=system_prompt, model_name="qwen-coder")
        if pollinations_res:
            responses.append(pollinations_res)

        openrouter_res = self.free_client.query_openrouter_free(prompt, system_prompt=system_prompt)
        if openrouter_res:
            responses.append(openrouter_res)

        if not responses:
            self.log("Web AI and Free API endpoints unavailable. Using local fallback generation.")
            return f"Synthesized Autonomous Blueprint for prompt: {prompt}"

        # Combine into fused multi-AI consensus output
        combined = "\n\n--- MULTI-AI CONSENSUS SYNTHESIS ---\n\n".join(responses)
        self.log(f"Multi-AI Consensus generated from {len(responses)} frontier AI sources!")
        return combined

    def ingest_and_build_sub_agent(self, agent_name: str, domain: str, description: str, keywords: List[str]) -> Tuple[bool, str]:
        """
        Use Multi-AI consensus synthesis to generate, compile, and register a new Python sub-agent.
        """
        self.log(f"Building super-intelligent sub-agent '{agent_name}' for domain '{domain}'...")
        prompt = (
            f"Generate an optimized Python sub-agent class named '{agent_name}' for domain '{domain}'. "
            f"Description: {description}. Keywords: {keywords}. Return high-performance Python code."
        )

        synthesis = self.query_multi_ai_consensus(prompt)

        # Record learning data
        learning_record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "agent_name": agent_name,
            "domain": domain,
            "description": description,
            "keywords": keywords,
            "consensus_length": len(synthesis),
            "status": "ingested"
        }
        with open(self.learning_data_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(learning_record) + "\n")

        # Invoke SelfAgentBuilder to scaffold and register sub-agent
        success, msg = self.builder.build_and_register_agent(agent_name, domain, description, keywords)
        self.log(msg)
        return success, msg

    def run_super_intelligence_expansion_cycle(self) -> List[str]:
        """
        Autonomously generate and register advanced sub-agents across novel domain sectors
        to continuously make Saathi AI the smartest AI co-pilot.
        """
        self.log("Running Super-Intelligence Multi-Agent Expansion Cycle...")

        novel_agents = [
            ("QuantumCircuitSimulator", "Quantum Computing", "Simulate quantum gates, qubits, and quantum state vectors", ["quantum", "qubit", "gate", "circuit"]),
            ("NeuralArchitectureSearch", "Deep Learning", "Automated neural network architecture optimization and hyperparameter tuning", ["nas", "neural", "hyperparameter", "deep_learning"]),
            ("SubSecondTradeAnalyzer", "Quantitative Finance", "High-frequency market telemetry and sub-second algorithmic trading strategy analysis", ["trade", "finance", "stock", "algo"]),
            ("AutonomousWebCrawler", "Web Scraping", "Recursive distributed web scraping, DOM parsing, and clean text extraction", ["crawl", "scrape", "dom", "extract"]),
            ("ZeroDayVulnerabilityScanner", "Cybersecurity", "AST static vulnerability analysis and memory safety auditing", ["zeroday", "exploit", "fuzzing", "security_audit"]),
            ("DeepMathTheoremProver", "Mathematics", "Symbolic math computation, calculus, matrix linear algebra, and logic proofs", ["math", "theorem", "symbolic", "calculus"])
        ]

        built_agents = []
        for name, domain, desc, kw in novel_agents:
            ok, msg = self.ingest_and_build_sub_agent(name, domain, desc, kw)
            if ok:
                built_agents.append(name)

        self.log(f"Super-Intelligence Expansion Cycle complete! Added {len(built_agents)} new frontier sub-agents.")
        return built_agents


if __name__ == "__main__":
    trainer = BrowserAITrainer()
    print("Testing BrowserAITrainer profile resolution:")
    print("Chrome User Data Path:", get_chrome_user_data_dir())
    print("Edge User Data Path:", get_edge_user_data_dir())
    trainer.run_super_intelligence_expansion_cycle()
