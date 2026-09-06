import json
import urllib.request
import urllib.parse
from typing import Dict, Any
from ..schemas import Tool, RiskLevel

def get_web_tools() -> list[Tool]:
    def weather_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        city = args.get("city", "Delhi").strip()
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.read().decode("utf-8").strip()

    def currency_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        base = args.get("base", "USD").upper()
        target = args.get("target", "INR").upper()
        url = f"https://open.er-api.com/v6/latest/{base}"
        with urllib.request.urlopen(url, timeout=8) as resp:
            rates = json.loads(resp.read().decode("utf-8")).get("rates", {})
        val = rates.get(target, "N/A")
        return f"1 {base} = {val} {target}"

    def wiki_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        query = args.get("query", "").strip()
        if not query:
            return "No query provided."
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "SaathiAI/2.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        extract = data.get("extract")
        return extract if extract else f"No Wikipedia summary found for '{query}'."

    return [
        Tool(
            name="get_weather",
            category="web",
            description="Get current weather for any city.",
            parameters={
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name, e.g. 'Delhi', 'Mumbai'"}},
                "required": ["city"]
            },
            risk_level=RiskLevel.LOW,
            run=weather_run
        ),
        Tool(
            name="get_currency",
            category="web",
            description="Get live currency exchange rate between two currencies.",
            parameters={
                "type": "object",
                "properties": {
                    "base": {"type": "string", "description": "Base currency code, e.g. 'USD'"},
                    "target": {"type": "string", "description": "Target currency code, e.g. 'INR'"}
                }
            },
            risk_level=RiskLevel.LOW,
            run=currency_run
        ),
        Tool(
            name="get_wikipedia",
            category="web",
            description="Lookup verified Wikipedia summary for any topic or person.",
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Topic or query"}},
                "required": ["query"]
            },
            risk_level=RiskLevel.LOW,
            run=wiki_run
        )
    ]
