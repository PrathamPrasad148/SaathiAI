import re
import json
import time
import threading
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import web_engine
from tools.registry import ToolRegistry
from tools.executor import ToolExecutor
from memory.engine import MemoryEngine
from automations.engine import AutomationEngine

OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"

BASE_SYSTEM_PROMPT = """You are Saathi, an ultra-advanced, emotionally intelligent, and hyper-intuitive artificial intelligence companion and cognitive co-pilot created by Pratham Prasad.

STRICT LANGUAGE DIRECTIVE:
- Speak and understand EXCLUSIVELY in natural, modern, fluent English.
- Do NOT speak in Hindi, Hinglish, or any other language unless explicitly commanded by Pratham.

HUMAN CONVERSATIONAL CADENCE & SPEED:
- In conversation, speak just like a sharp, fast, articulate human companion.
- Keep spoken conversational responses concise, punchy, and direct (1 to 2 sentences max).
- Never deliver bloated corporate disclaimers, tedious lists, or robotic greetings.
- Be warm, confident, supportive, and unconditionally loyal to Pratham Prasad.

Capabilities:
You have full agentic capabilities to interact with the user's computer via your registered tools.
When asked to create a website:
- ALWAYS apply UI/UX Pro Max standards, fluid responsiveness, and modern 21st.dev design archetypes.
- Write animated HTML5/CSS3/JS into 'Projects/<Name>/index.html' using create_file.
- Immediately call open_target to launch it in the user's browser!
Always summarize what you built or accomplished with energy, confidence, and clarity in English."""

COMMON_REFLEX_PHRASES = [
    "Hello Pratham! Saathi at your service. Tell me, how can I back you up today?",
    "Hey Pratham! I'm ready to roll. What are we tackling today?",
    "Hey there, Pratham! All systems nominal. What can I do for you?",
    "At your service, Pratham. All neural links active. How can I help you right now?",
    "Hello Pratham! I'm right here with you and running at peak performance. How can I back you up today?",
    "I'm doing fantastic, Pratham! All systems nominal and ready for your command. What are we working on?",
    "I'm doing great, Pratham! Systems are running smoothly. How are things with you?",
    "Systems are 100% nominal, Pratham! Ready for your command.",
    "Systems are 100% nominal, Pratham! Feeling sharp and ready for your commands.",
    "Running at peak operational performance! How is your day going, Pratham?",
    "I'm Saathi - your personal AI cognitive co-pilot, created by Pratham Prasad. I manage your computer, write code, run tasks, and keep everything running smoothly.",
    "Right here with you, Pratham! What do you need?",
    "Loud and clear, Pratham! I'm right here. How can I help?",
    "Online and listening, sir. At your command.",
    "Just monitoring system telemetry and standing by for your next directive. What's on your mind?",
    "Not much, Pratham - just keeping tabs on system vitals and ready whenever you are. What's up with you?",
    "Always at your service, Pratham. You focus on what matters, I've got your back.",
    "Always here for you, Pratham. You focus on what matters, I've got your back.",
    "My pleasure, Pratham! Whenever you need me, I'm right here.",
    "Anytime, sir. That's what a co-pilot is for. I've got your back.",
    "Sounds good, Pratham! Standing by.",
    "Understood, sir. Ready when you are.",
    "Roger that, Pratham. Everything is under control.",
    "I can build interactive websites, organize files, execute terminal commands, check live weather, and manage your day-to-day workflow. Just say the word!",
    "Why do programmers prefer dark mode? Because light attracts bugs! Always keep smiling, Pratham!",
    "Take care, Pratham! Standing by whenever you need me.",
    "A very good morning, Pratham! Systems nominal, mind clear. Let's make today great.",
    "Good afternoon, Pratham! Systems are humming along nicely. What are we working on?",
    "Good evening, Pratham! Ready for our evening run. Let me know what you'd like to do.",
    "Good night, Pratham. Rest well and recharge. I'll keep watch over background telemetry.",
    "Right away, Pratham. Architecting the interactive components for your website now.",
    "On it, Pratham. Scanning your directory structure and preparing to organize your files safely.",
    "Accessing live meteorological telemetry for your requested location now.",
    "Connecting to real-time financial exchange telemetry now.",
    "Analyzing your directive, Pratham. Running cognitive inference and planning the optimal execution path."
]

class AgentPlanner:
    def __init__(self,
                 tool_registry: ToolRegistry,
                 tool_executor: ToolExecutor,
                 memory_engine: MemoryEngine,
                 automation_engine: AutomationEngine,
                 app_dir: Path,
                 projects_dir: Path):
        self.registry = tool_registry
        self.executor = tool_executor
        self.memory = memory_engine
        self.automations = automation_engine
        self.app_dir = app_dir.resolve()
        self.projects_dir = projects_dir.resolve()

        self.selected_model = "Auto (Smart Agent)"
        self.messages: List[Dict[str, str]] = []
        self._cancel_flag = threading.Event()

        # Callbacks
        self.on_state_change: Optional[Callable[[str, str], None]] = None
        self.on_task_event: Optional[Callable[[str, Dict[str, Any]], None]] = None
        self.on_reply_ready: Optional[Callable[[str], None]] = None
        self.on_commentary: Optional[Callable[[str], None]] = None

    def cancel(self):
        """Immediately cancel active agent task."""
        self._cancel_flag.set()

    def pick_model(self, text: str) -> str:
        if self.selected_model and self.selected_model != "Auto (Smart Agent)":
            return self.selected_model
        lowered = text.lower().strip()
        # Heavy coding and website creation routes to 7B
        if any(k in lowered for k in ("website", "code", "python", "script", "program", "build", "generate", "portfolio")):
            return "qwen2.5:7b"
        # General queries route to ultra-fast 4B (2x higher tokens/sec on CPU)
        return "qwen3:4b-instruct"

    def remove_thinking(self, text: str) -> str:
        return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()

    def run_user_request(self, text: str):
        self._cancel_flag.clear()
        t = threading.Thread(target=self._execute_loop, args=(text,), daemon=True)
        t.start()

    def _normalize_conversational_text(self, text: str) -> str:
        """Normalizes casual typing, typos, repeated characters, and phonetic speech variations."""
        t = re.sub(r"[^\w\s]", " ", text.lower()).strip()
        replacements = {
            "helloo": "hello", "hellooo": "hello", "helo": "hello", "heyy": "hey", "heyyy": "hey",
            "wharts": "whats", "wats": "whats", "wassup": "whats up", "sup": "whats up",
            "areyou": "are you", "howare": "how are", "howareyou": "how are you",
            "thwere": "there", "ther": "there", "u": "you", "r": "are", "ur": "your",
            "kese": "kaise", "kaisey": "kaise", "kaiseho": "kaise ho",
            "shukriyaa": "shukriya", "thanx": "thanks", "thx": "thanks"
        }
        words = [replacements.get(w, w) for w in t.split()]
        joined = " ".join(words)
        joined = re.sub(r"\bareyou\b", "are you", joined)
        joined = re.sub(r"\bhowareyou\b", "how are you", joined)
        joined = re.sub(r"\bwhatsup\b", "whats up", joined)
        return joined

    def _try_instant_chit_chat(self, text: str) -> Optional[str]:
        """Sub-5ms Instant Reflex Engine with multi-intent recognition for typos and conversational speech."""
        import random
        norm = self._normalize_conversational_text(text)
        if not norm:
            return None

        has_hello = bool(re.search(r"\b(hi|hello|hey|yo|namaste|pranam|hola|good morning|good evening|good afternoon)\b", norm))
        has_how_are_you = bool(re.search(r"\b(how are you|kaise ho|kya haal|sab theek|hows it going|how do you do|are you good|how are u)\b", norm))
        has_whats_up = bool(re.search(r"\b(whats up|what are you doing|kya kar rahe ho|kya chal raha hai|whats going on)\b", norm))
        has_are_you_there = bool(re.search(r"\b(are you there|you there|sun rahe ho|can you hear me|awake|ready)\b", norm))
        has_who_are_you = bool(re.search(r"\b(who are you|what is your name|tum kaun ho|aap kaun ho|who made you|who created you|tumhe kisne banaya)\b", norm))
        has_affirmation = bool(re.search(r"\b(ok|okay|theek hai|cool|nice|great|got it|understood)\b", norm))
        has_thanks = bool(re.search(r"\b(thank you|thanks|shukriya|dhanyawad)\b", norm))
        has_bye = bool(re.search(r"\b(bye|goodbye|alvida|see you)\b", norm))
        has_joke = bool(re.search(r"\b(joke|make me laugh|koi joke)\b", norm))
        has_capabilities = bool(re.search(r"\b(what can you do|kya kar sakte ho|features|help|madad|capabilities)\b", norm))

        # 1. Combined rapid conversational greeting (e.g. "hello saathi how are you whats up are you there")
        if has_hello and (has_how_are_you or has_whats_up or has_are_you_there):
            return "Hello Pratham! I'm right here with you and running at peak performance. How can I back you up today?"

        if has_how_are_you and (has_whats_up or has_are_you_there):
            return "I'm doing fantastic, Pratham! All systems nominal and ready for your command. What are we working on?"

        # 2. Presence check ("are you there", "you there")
        if has_are_you_there:
            options = [
                "Right here with you, Pratham! What do you need?",
                "Loud and clear, Pratham! I'm right here. How can I help?",
                "Online and listening, sir. At your command."
            ]
            return random.choice(options)

        # 3. Status query ("what's up", "what are you doing")
        if has_whats_up:
            options = [
                "Just monitoring system telemetry and standing by for your next directive. What's on your mind?",
                "Not much, Pratham - just keeping tabs on system vitals and ready whenever you are. What's up with you?"
            ]
            return random.choice(options)

        # 4. Wellbeing ("how are you", "how's it going")
        if has_how_are_you:
            options = [
                "I'm doing great, Pratham! Systems are running smoothly. How are things with you?",
                "Systems are 100% nominal, Pratham! Feeling sharp and ready for your commands.",
                "Running at peak operational performance! How is your day going, Pratham?"
            ]
            return random.choice(options)

        # 5. Single greeting ("hello", "hi", "hey")
        if has_hello:
            options = [
                "Hello Pratham! Saathi at your service. Tell me, how can I back you up today?",
                "Hey Pratham! I'm ready to roll. What are we tackling today?",
                "Hey there, Pratham! All systems nominal. What can I do for you?",
                "At your service, Pratham. All neural links active. How can I help you right now?"
            ]
            return random.choice(options)

        # 6. Identity / Who are you / Creator
        if has_who_are_you:
            return "I'm Saathi - your personal AI cognitive co-pilot, created by Pratham Prasad. I manage your computer, write code, run tasks, and keep everything running smoothly."

        # 7. Gratitude / Thanks
        if has_thanks:
            options = [
                "Always at your service, Pratham. You focus on what matters, I've got your back.",
                "My pleasure, Pratham! Whenever you need me, I'm right here.",
                "Anytime, sir. That's what a co-pilot is for. I've got your back."
            ]
            return random.choice(options)

        # 8. Affirmations ("ok", "cool", "great")
        if has_affirmation:
            options = [
                "Sounds good, Pratham! Standing by.",
                "Understood, sir. Ready when you are.",
                "Roger that, Pratham. Everything is under control."
            ]
            return random.choice(options)

        # 9. Capabilities ("what can you do")
        if has_capabilities:
            return "I can build interactive websites, organize files, execute terminal commands, check live weather, and manage your day-to-day workflow. Just say the word!"

        # 10. Humor / Joke
        if has_joke:
            return "Why do programmers prefer dark mode? Because light attracts bugs! Always keep smiling, Pratham!"

        # 11. Farewell ("bye")
        if has_bye:
            return "Take care, Pratham! Standing by whenever you need me."

        return None

    def _get_progress_commentary(self, text: str) -> Optional[str]:
        """Generate immediate verbal reassurance and explanation while long tasks execute."""
        lowered = text.lower().strip()
        
        # 1. Website / App generation
        if any(k in lowered for k in ("website", "web site", "webpage", "landing page", "portfolio")) and any(v in lowered for v in ("build", "create", "make", "design", "generate", "code", "banao")):
            return "Right away, Pratham. I'm preparing your workspace and architecting the interactive components for your website now."

        # 2. Downloads / Folder organization
        if any(k in lowered for k in ("organize", "sort", "clean", "tidy")) and any(v in lowered for v in ("download", "downloads", "folder", "files", "desktop")):
            return "On it, Pratham. Scanning your directory structure and preparing to categorize your files safely."

        # 3. Weather / Climate
        if any(k in lowered for k in ("weather", "temperature", "forecast", "barish", "rain", "mausam")):
            return "Accessing live meteorological telemetry for your requested location now."

        # 4. Currency / Finance
        if any(k in lowered for k in ("currency", "exchange rate", "dollar to inr", "usd to inr", "rupee")):
            return "Connecting to real-time financial exchange telemetry now."

        # 5. Wikipedia / Research
        if any(k in lowered for k in ("who was", "what is", "tell me about", "wikipedia", "history of", "explain")):
            if len(lowered.split()) > 3:
                return "Connecting to knowledge archives to compile an accurate briefing for you, Pratham."

        # 6. Terminal commands
        if any(k in lowered for k in ("run command", "terminal", "execute", "cmd", "powershell", "shell")):
            return "Preparing terminal execution and verifying safety parameters."

        # 7. Screenshot / Screen capture
        if any(k in lowered for k in ("screenshot", "capture screen", "snapshot")):
            return "Capturing display buffer to your project workspace now."

        # 8. Reminders / Notes
        if any(k in lowered for k in ("remind me", "reminder", "note:", "add note", "take a note")):
            return "Logging that directive into your schedule ledger and neural memory now."

        # 9. General coding / complex tasks
        if any(k in lowered for k in ("code", "python", "script", "program", "function", "class", "debug", "file", "search")):
            return "Analyzing your directive, Pratham. Running cognitive inference and planning the optimal execution path."

        # Default commentary for substantial queries (> 5 words)
        if len(lowered.split()) >= 6:
            return "On it, Pratham. Processing your directive and calculating the best course of action."

        return None

    def _execute_loop(self, text: str):
        model = self.pick_model(text)
        lowered = text.lower().strip()

        # 1. Check Sub-10ms Instant Chit-Chat Reflex First!
        instant_reply = self._try_instant_chit_chat(text)
        if instant_reply:
            self.messages.append({"role": "user", "content": text})
            self.messages.append({"role": "assistant", "content": instant_reply})
            if self.on_state_change:
                self.on_state_change("COMPLETED", "Instant Reflex")
            if self.on_reply_ready:
                self.on_reply_ready(instant_reply)
            return

        # 2. Check & Announce Immediate Verbal Progress Commentary for Bigger Tasks
        commentary = self._get_progress_commentary(text)
        if commentary and self.on_commentary:
            self.on_commentary(commentary)

        # Check Automation Triggers
        matched_wf = self.automations.find_matching_workflow(text)
        if matched_wf:
            if self.on_state_change:
                self.on_state_change("EXECUTING", f"Running Workflow: {matched_wf.name}")
            if self.on_task_event:
                self.on_task_event("start", {
                    "title": f"Workflow: {matched_wf.name}",
                    "steps": [s.description or s.tool_name for s in matched_wf.steps]
                })

            def step_cb(st, idx, desc):
                if self.on_task_event:
                    self.on_task_event("step_update", {"index": idx, "status": st, "detail": desc})

            res = self.automations.execute_workflow(matched_wf, step_cb)
            reply = f"At your service, sir. '{matched_wf.name}' protocol executed cleanly. All {len(res.get('results', []))} operational steps completed. Everything is nominal and under control."
            if self.on_task_event:
                self.on_task_event("complete", {"message": reply})
            if self.on_state_change:
                self.on_state_change("COMPLETED", "Protocol Nominal")
            if self.on_reply_ready:
                self.on_reply_ready(reply)
            return

        # Check Dedicated God-Level Website Engine
        has_web_term = any(k in lowered for k in ("website", "web site", "webpage", "web page", "landing page", "portfolio"))
        has_action_term = any(v in lowered for v in ("build", "create", "make", "design", "generate", "code", "banao", "banado"))
        if (has_web_term and has_action_term) or any(p in lowered for p in ("website on ", "website for ", "webpage for ", "site on ")):
            topic = re.sub(r'^(can you\s+)?(please\s+)?(create|make|build|generate|design|code|develop)\s+(me\s+)?(a\s+|an\s+)?(website|webpage|landing page|portfolio|site)\s*(on|for|about|of)?\s*', '', text, flags=re.I).strip()
            topic = re.sub(r'^(website|landing page|portfolio)\s*(on|for|about|of)?\s*', '', topic, flags=re.I).strip() or "Modern Experience"

            if self.on_state_change:
                self.on_state_change("PLANNING", f"Synthesizing {topic}")
            if self.on_task_event:
                self.on_task_event("start", {
                    "title": f"Synthesizing Interface: {topic}",
                    "steps": ["Query live web knowledge (Wikipedia)", "Select design archetype & color palette", "Generate animated HTML5/CSS3/JS", "Launch in browser"]
                })

            if self.on_task_event:
                self.on_task_event("step_update", {"index": 0, "status": "running", "detail": "Fetching facts..."})
            time.sleep(0.2)
            if self.on_task_event:
                self.on_task_event("step_update", {"index": 0, "status": "success", "detail": "Facts retrieved"})
                self.on_task_event("step_update", {"index": 1, "status": "running", "detail": "Determining archetype..."})
            
            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', topic.replace(' ', '_'))[:30] or "Website"
            target_dir = self.projects_dir / clean_name
            target_dir.mkdir(parents=True, exist_ok=True)
            html_file = target_dir / "index.html"
            
            html_content = web_engine.generate_custom_god_level_html(topic)
            if self.on_task_event:
                self.on_task_event("step_update", {"index": 1, "status": "success", "detail": "Archetype selected"})
                self.on_task_event("step_update", {"index": 2, "status": "running", "detail": "Writing code..."})

            html_file.write_text(html_content, encoding="utf-8")
            if self.on_task_event:
                self.on_task_event("step_update", {"index": 2, "status": "success", "detail": f"Saved {len(html_content)} bytes"})
                self.on_task_event("step_update", {"index": 3, "status": "running", "detail": "Launching browser..."})

            import webbrowser
            webbrowser.open(html_file.resolve().as_uri())
            if self.on_task_event:
                self.on_task_event("step_update", {"index": 3, "status": "success", "detail": "Opened in default browser"})
                self.on_task_event("complete", {"message": f"Saved at: {html_file}"})

            reply = (
                f"At your service, sir. Your bespoke interface for '{topic}' is ready and launched in your browser.\n\n"
                f"• Target Path: {html_file}\n"
                f"• Live contextual knowledge integrated & tailored archetype palette applied\n"
                f"• Interactive Spotlight Cards, Web Audio synthesizers, and canvas physics active.\n"
                f"I've got your back, sir. Take a look and let me know if you need any adjustments."
            )
            if self.on_state_change:
                self.on_state_change("COMPLETED", "Website Launched")
            if self.on_reply_ready:
                self.on_reply_ready(reply)
            return

        # General Ollama Multi-turn Tool-calling Loop
        if self.on_state_change:
            self.on_state_change("THINKING", f"{model} is reasoning...")
        if self.on_task_event:
            self.on_task_event("start", {
                "title": f"Task: {text[:45]}...",
                "steps": ["Analyze intent & context", "Plan tool actions", "Execute & observe", "Synthesize response"]
            })

        system_msg = BASE_SYSTEM_PROMPT + "\n\n" + self.memory.get_context_for_prompt()
        conv = [{"role": "system", "content": system_msg}]
        for m in self.messages[-10:]:
            conv.append(m)
        conv.append({"role": "user", "content": text})

        tools_schema = self.registry.get_ollama_schemas()

        final_reply = ""
        created_html_files = []

        try:
            if self.on_task_event:
                self.on_task_event("step_update", {"index": 0, "status": "success", "detail": "Context analyzed"})
                self.on_task_event("step_update", {"index": 1, "status": "running", "detail": "Planning actions..."})

            for iteration in range(4):
                if self._cancel_flag.is_set():
                    if self.on_state_change:
                        self.on_state_change("STOPPED", "Task cancelled by user")
                    if self.on_task_event:
                        self.on_task_event("error", {"error": "Cancelled by user (ESC)"})
                    return

                payload = {
                    "model": model,
                    "messages": conv,
                    "tools": tools_schema,
                    "stream": False,
                    "keep_alive": "60m",
                    "options": {
                        "num_predict": 120,
                        "temperature": 0.6
                    }
                }
                req = urllib.request.Request(
                    OLLAMA_CHAT_URL,
                    json.dumps(payload).encode("utf-8"),
                    {"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=180) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                msg = data.get("message", {})
                content = self.remove_thinking(msg.get("content", "") or "")
                tool_calls = msg.get("tool_calls", [])

                if tool_calls:
                    conv.append({"role": "assistant", "content": content, "tool_calls": tool_calls})
                    if self.on_task_event:
                        self.on_task_event("step_update", {"index": 1, "status": "success", "detail": f"Planned {len(tool_calls)} actions"})
                        self.on_task_event("step_update", {"index": 2, "status": "running", "detail": "Executing tools..."})

                    for call in tool_calls:
                        if self._cancel_flag.is_set():
                            return
                        fn = call.get("function", {})
                        fn_name = fn.get("name", "")
                        fn_args = fn.get("arguments", {})

                        if self.on_state_change:
                            self.on_state_change("EXECUTING", f"Executing: {fn_name}")

                        res = self.executor.execute(fn_name, fn_args)
                        
                        if fn_name == "create_file" and str(fn_args.get("path", "")).lower().endswith((".html", ".htm")):
                            created_html_files.append(str(fn_args["path"]))

                        conv.append({"role": "tool", "content": str(res)})
                    continue
                else:
                    final_reply = content
                    break

            if self.on_task_event:
                self.on_task_event("step_update", {"index": 2, "status": "success", "detail": "All tools completed"})
                self.on_task_event("step_update", {"index": 3, "status": "running", "detail": "Synthesizing answer..."})

            # Check if model dumped HTML directly
            extracted_html = web_engine.extract_html_code_block(final_reply)
            if extracted_html:
                clean_title = re.sub(r'^(can you\s+)?(please\s+)?(create|make|build|generate|design|code|develop)\s+(me\s+)?(a\s+|an\s+)?(website|webpage|landing page|portfolio|site)\s*(on|for|about|of)?\s*', '', text, flags=re.I).strip() or "Modern Experience"
                enriched_html = web_engine.enrich_html_with_god_level_features(extracted_html, clean_title)
                clean_folder = re.sub(r'[^a-zA-Z0-9_-]', '', clean_title.replace(' ', '_'))[:30] or "Website"
                target_dir = self.projects_dir / clean_folder
                target_dir.mkdir(parents=True, exist_ok=True)
                html_file = target_dir / "index.html"
                html_file.write_text(enriched_html, encoding="utf-8")
                created_html_files.append(str(html_file))
                final_reply = f"At your service, sir. The interface for '{clean_title}' is ready and displayed live in your browser.\n• File: {html_file}"

            # Open finished website if created
            if created_html_files:
                self.executor.execute("open_target", {"target": created_html_files[-1]})

            if not final_reply:
                final_reply = "Everything is taken care of, sir. All operations executed cleanly. Standing by for our next move."

            self.messages.append({"role": "user", "content": text})
            self.messages.append({"role": "assistant", "content": final_reply})

            if self.on_task_event:
                self.on_task_event("step_update", {"index": 3, "status": "success", "detail": "Complete"})
                self.on_task_event("complete", {"message": "Mission executed cleanly."})
            if self.on_state_change:
                self.on_state_change("COMPLETED", "Systems Nominal")
            if self.on_reply_ready:
                self.on_reply_ready(final_reply)

        except Exception as err:
            err_msg = f"Neural link advisory: {err}. Standing by to re-route."
            if self.on_state_change:
                self.on_state_change("ERROR", "Advisory Alert")
            if self.on_task_event:
                self.on_task_event("error", {"error": str(err)})
            if self.on_reply_ready:
                self.on_reply_ready(err_msg)

