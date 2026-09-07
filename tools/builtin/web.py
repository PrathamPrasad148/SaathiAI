"""
Saathi AI — Autonomous Web Access, Search & Data Extraction Subsystem
Provides real-time web search (DuckDuckGo & Wikipedia Search API), web page scraper/fetcher,
JSON API query engine, live weather, currency exchange, and Wikipedia integration.
"""

import html
import json
import re
import urllib.parse
import urllib.request
from typing import Dict, Any, List
from ..schemas import Tool, RiskLevel

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 SaathiAI/2.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

def clean_html_to_text(raw_html: str) -> str:
    """Strips HTML tags and converts content into clean text for LLM analysis."""
    clean = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw_html, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<(br|p|div|tr|h[1-6])[^>]*>", "\n", clean, flags=re.IGNORECASE)
    clean = re.sub(r"<[^>]+>", "", clean)
    clean = html.unescape(clean)
    clean = re.sub(r"\n\s*\n", "\n\n", clean)
    return clean.strip()

def get_web_tools() -> List[Tool]:
    def web_search_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        query = args.get("query", "").strip()
        if not query:
            return "Error: No search query provided."

        # Strategy 1: DuckDuckGo HTML Search
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode('utf-8', errors='ignore')

            links = re.findall(r'<a class="result__a" href="([^"]+)">(.*?)</a>', body)
            snippets = re.findall(r'<a class="result__snippet[^"]*">(.*?)</a>', body)

            results = []
            for i in range(min(6, len(links))):
                link_url, title_raw = links[i]
                title = re.sub(r'<[^>]+>', '', title_raw)
                snippet = re.sub(r'<[^>]+>', '', snippets[i]) if i < len(snippets) else ""
                
                if "uddg=" in link_url:
                    parsed_link = urllib.parse.parse_qs(urllib.parse.urlparse(link_url).query)
                    real_link = parsed_link.get("uddg", [link_url])[0]
                else:
                    real_link = link_url
                results.append(f"{i+1}. **{title.strip()}**\n   URL: {real_link}\n   Snippet: {snippet.strip()}\n")

            if results:
                return f"=== Live Web Search Results for '{query}' ===\n\n" + "\n".join(results)
        except Exception:
            pass

        # Strategy 2: Wikipedia Search API Fallback
        try:
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
            req_w = urllib.request.Request(wiki_url, headers=DEFAULT_HEADERS)
            with urllib.request.urlopen(req_w, timeout=8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                search_results = data.get("query", {}).get("search", [])
                results = []
                for idx, item in enumerate(search_results[:5]):
                    title = item.get("title", "")
                    snippet = clean_html_to_text(item.get("snippet", ""))
                    page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                    results.append(f"{idx+1}. **{title}**\n   URL: {page_url}\n   Snippet: {snippet}\n")
                if results:
                    return f"=== Live Knowledge Search Results for '{query}' ===\n\n" + "\n".join(results)
        except Exception:
            pass

        return f"Could not retrieve live search results for '{query}'. Please verify network connection."

    def fetch_url_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        url = args.get("url", "").strip()
        if not url:
            return "Error: No URL provided."

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw_body = resp.read().decode('utf-8', errors='ignore')
                text_content = clean_html_to_text(raw_body)
                
                if len(text_content) > 4000:
                    text_content = text_content[:4000] + "\n\n[... Content truncated for context length ...]"
                    
                return f"=== Parsed Web Page Content ({url}) ===\n\n{text_content}"
        except Exception as e:
            return f"Failed to fetch URL '{url}': {str(e)}"

    def fetch_json_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        url = args.get("url", "").strip()
        if not url:
            return "Error: No API URL provided."

        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                formatted = json.dumps(data, indent=2)
                if len(formatted) > 4000:
                    formatted = formatted[:4000] + "\n... [JSON truncated]"
                return f"=== JSON API Response ({url}) ===\n\n{formatted}"
        except Exception as e:
            return f"Failed to query JSON API '{url}': {str(e)}"

    def weather_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        city = args.get("city", "Delhi").strip()
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                return resp.read().decode("utf-8").strip()
        except Exception as e:
            return f"Could not fetch weather for {city}: {str(e)}"

    def currency_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        base = args.get("base", "USD").upper()
        target = args.get("target", "INR").upper()
        url = f"https://open.er-api.com/v6/latest/{base}"
        try:
            with urllib.request.urlopen(url, timeout=8) as resp:
                rates = json.loads(resp.read().decode("utf-8")).get("rates", {})
            val = rates.get(target, "N/A")
            return f"1 {base} = {val} {target}"
        except Exception as e:
            return f"Could not fetch exchange rates: {str(e)}"

    def wiki_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        query = args.get("query", "").strip()
        if not query:
            return "No query provided."
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract")
            return extract if extract else f"No Wikipedia summary found for '{query}'."
        except Exception as e:
            return f"Wikipedia lookup error for '{query}': {str(e)}"

    return [
        Tool(
            name="web_search",
            category="web",
            description="Search the live web in real-time for current news, facts, documentation, or information.",
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search query or topic"}},
                "required": ["query"]
            },
            risk_level=RiskLevel.LOW,
            run=web_search_run
        ),
        Tool(
            name="fetch_url_content",
            category="web",
            description="Fetch and parse the readable text/article content from any public webpage URL.",
            parameters={
                "type": "object",
                "properties": {"url": {"type": "string", "description": "Webpage URL to fetch and read"}},
                "required": ["url"]
            },
            risk_level=RiskLevel.LOW,
            run=fetch_url_run
        ),
        Tool(
            name="fetch_json_api",
            category="web",
            description="Fetch JSON data from any public web API endpoint.",
            parameters={
                "type": "object",
                "properties": {"url": {"type": "string", "description": "Public API endpoint URL"}},
                "required": ["url"]
            },
            risk_level=RiskLevel.LOW,
            run=fetch_json_run
        ),
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
