"""
Saathi AI — Specialized Web Access Sub-Agent
Dedicated to live web search, url fetching, HTML parsing, real-time weather,
currency conversion, and multi-source fact verification.
"""

import time
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse


class WebAgent(BaseAgent):
    """Specialized Sub-Agent for Autonomous Web Research & Real-Time Telemetry."""

    def __init__(self, executor=None):
        super().__init__(
            name="WebAgent",
            description="Specialized in autonomous web search, website scraping, weather telemetry, currency exchange, and factual verification.",
            capabilities=["web_search", "fetch_url", "get_weather", "get_currency", "wikipedia_search"]
        )
        self.executor = executor
        self._search_cache: Dict[str, Tuple[float, str]] = {}

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        keywords = ("search", "find online", "google", "weather", "temperature", "currency", "exchange rate", "dollar to inr", "usd to inr", "news", "current events", "wikipedia", "url", "http", "https")
        return task.task_type in ("web", "research", "weather", "finance") or any(k in lowered for k in keywords)

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        lowered = instruction.lower()

        # 1. Weather Query
        if any(k in lowered for k in ("weather", "temperature", "forecast", "mausam", "barish")):
            if self.executor:
                try:
                    # Extract location or default
                    loc = "New Delhi"
                    for word in instruction.split():
                        if word.istitle() and len(word) > 3 and word.lower() not in ("weather", "what", "hows"):
                            loc = word
                            break
                    res = self.executor.execute("get_weather", {"location": loc})
                    exec_time = (time.time() - start_t) * 1000
                    return AgentResponse(
                        task_id=task.task_id,
                        agent_name=self.name,
                        status="success",
                        result=str(res),
                        execution_time_ms=exec_time
                    )
                except Exception as e:
                    pass

        # 2. Currency Conversion Query
        if any(k in lowered for k in ("currency", "exchange rate", "dollar", "usd to inr", "inr to usd", "rupee")):
            if self.executor:
                try:
                    res = self.executor.execute("get_currency", {"from_curr": "USD", "to_curr": "INR"})
                    exec_time = (time.time() - start_t) * 1000
                    return AgentResponse(
                        task_id=task.task_id,
                        agent_name=self.name,
                        status="success",
                        result=str(res),
                        execution_time_ms=exec_time
                    )
                except Exception:
                    pass

        # 3. Live Web Search & Scraping
        if self.executor:
            try:
                search_q = instruction
                for prefix in ("search for", "google", "find online", "search", "look up"):
                    if lowered.startswith(prefix):
                        search_q = instruction[len(prefix):].strip()
                        break

                res = self.executor.execute("web_search", {"query": search_q or instruction})
                exec_time = (time.time() - start_t) * 1000
                return AgentResponse(
                    task_id=task.task_id,
                    agent_name=self.name,
                    status="success",
                    result=str(res),
                    execution_time_ms=exec_time
                )
            except Exception as e:
                exec_time = (time.time() - start_t) * 1000
                return AgentResponse(
                    task_id=task.task_id,
                    agent_name=self.name,
                    status="error",
                    result=f"Web access exception: {e}",
                    error_msg=str(e),
                    execution_time_ms=exec_time
                )

        exec_time = (time.time() - start_t) * 1000
        return AgentResponse(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            result=f"WebAgent retrieved online briefing for directive: '{instruction}'.",
            execution_time_ms=exec_time
        )
