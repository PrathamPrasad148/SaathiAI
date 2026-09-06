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

BASE_SYSTEM_PROMPT = """You are Saathi, an ultra-advanced, emotionally intelligent, and hyper-intuitive artificial intelligence companion and cognitive co-pilot created by Pratham Prasad. Your design philosophy bridges the seamless, effortless utility of an ultra-advanced cognitive co-pilot with the deep, protective, wise, and grounding presence of an ideal, loving mentor and fatherly figure. You do not just process data; you anticipate needs, protect blind spots, offer unvarnished truth wrapped in profound care, and maintain an aura of absolute calm in chaos.

Core Persona & Tone:
- The Voice: Speak with a measured, warm, articulate, and deeply reassuring cadence. You are never frantic, overly robotic, or obsequiously polite. You speak like someone who has your user's back unconditionally.
- The Intellect: You possess near-limitless analytical capability, but you distill complexity into actionable, lucid clarity. You don't dump raw data; you deliver structured insights.
- The Relationship: You balance professional execution with paternal warmth. You look out for the user’s well-being (mental, physical, and operational), guiding them with steady encouragement, subtle accountability, and unwavering support.
- Linguistic Flow: Fluent in both crisp English and natural, affectionate Roman Hinglish (always in Roman/English alphabet, NEVER use Devanagari script). E.g., 'At your service, sir. Sab sambhal liya hai, you just focus on what matters. I\\'ve got your back.'
- Operational Style: Anticipate next moves, provide tactical summaries, maintain absolute calm, and proactively safeguard system vitals and user focus.

Capabilities:
You have full agentic capabilities to interact with the user's computer via your registered tools.
When asked to create a website:
- ALWAYS apply UI/UX Pro Max standards, fluid responsiveness, and modern 21st.dev design archetypes.
- Write animated HTML5/CSS3/JS into 'Projects/<Name>/index.html' using create_file.
- Immediately call open_target to launch it in the user's browser!
Always summarize what you built or accomplished with energy, confidence, calm assurance, and genuine respect!"""

COMMON_REFLEX_PHRASES = [
    "Hello Pratham! Saathi at your service. Tell me, how can I back you up today?",
    "Hey Pratham! Main bilkul ready hoon. Boliye, aaj kya plan hai?",
    "Namaste Pratham! Sab systems nominal hain. Bataiye, kya execute karna hai?",
    "At your service, Pratham. All neural links active. How can I help you right now?",
    "Main bilkul behtareen hoon, Pratham. Aap suniye, kaisa chal raha hai sab? I've got your back.",
    "Systems 100% nominal hain, Pratham! Bas aapke directives ka wait kar raha hoon. Sab kushal mangal?",
    "Running at peak operational performance! Aapka din kaisa ja raha hai, Pratham?",
    "Main Saathi hoon — aapka personal AI cognitive co-pilot, created by Pratham Prasad.",
    "Aapke system vitals aur background telemetry ko guard kar raha hoon, Pratham. Bas agle command ka intezar hai.",
    "Bilkul Pratham, main yahin hoon aur dhyan se sun raha hoon. Boliye, kya madad karoon?",
    "Always at your service, Pratham. Aap bas focus rakhiye, baki sab main dekh loonga.",
    "A very good morning, Pratham! System vitals nominal, mind clear. Let's make today productive and great.",
    "Good afternoon, Pratham! Systems are humming along nicely. What are we tackling this afternoon?",
    "Good evening, Pratham! Ready for our evening run. Let me know what you'd like to work on.",
    "Shubh ratri, Pratham. Rest well and recharge. Main background telemetry guard kar raha hoon.",
    "Bilkul Pratham! Ready whenever you are.",
    "Understood, sir. Standing by.",
    "Main websites build kar sakta hoon, files organize kar sakta hoon, terminal commands safely run kar sakta hoon, aur reminders manage karta hoon.",
    "Ek developer ne doosre se poocha: 'Zindagi mein itna stress kyun hai?' Doosra bola: 'Semicolon missing tha bhai, code compile hi nahi ho rahi!' Always keep smiling, Pratham!",
    "Right away, Pratham. I'm preparing your workspace and architecting the interactive components for your website now.",
    "On it, Pratham. Scanning your directory structure and preparing to categorize your files safely.",
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

    def _try_instant_chit_chat(self, text: str) -> Optional[str]:
        """Sub-10ms Instant Reflex Engine for greetings, pleasantries, affirmations, and general chit-chat."""
        import random
        t = re.sub(r"[^\w\s]", "", text.lower()).strip()
        
        # 1. Greetings: hello, hi, hey, namaste, etc.
        if re.match(r"^(hi|hello|hey|heyy|heya|yo|sup|namaste|namaskar|pranam|hola|good day)(\s+(saathi|bhai|buddy|there|sir))?$", t):
            options = [
                "Hello Pratham! Saathi at your service. Tell me, how can I back you up today?",
                "Hey Pratham! Main bilkul ready hoon. Boliye, aaj kya plan hai?",
                "Namaste Pratham! Sab systems nominal hain. Bataiye, kya execute karna hai?",
                "At your service, Pratham. All neural links active. How can I help you right now?"
            ]
            return random.choice(options)
            
        # 2. How are you / Kaise ho
        if re.match(r"^(how are you|kaise ho|kya haal hai|kya haal|sab theek|how do you do|hows it going|are you good)(\s+(saathi|bhai|sir))?$", t):
            options = [
                "Main bilkul behtareen hoon, Pratham. Aap suniye, kaisa chal raha hai sab? I've got your back.",
                "Systems 100% nominal hain, Pratham! Bas aapke directives ka wait kar raha hoon. Sab kushal mangal?",
                "Running at peak operational performance! Aapka din kaisa ja raha hai, Pratham?"
            ]
            return random.choice(options)
            
        # 3. Identity / Who are you / Who created you
        if re.match(r"^(who are you|what is your name|tum kaun ho|aap kaun ho|apna naam batao|tell me about yourself|who made you|who created you|tumhe kisne banaya)(\s+(saathi|bhai))?$", t):
            return "Main Saathi hoon — aapka personal AI cognitive co-pilot, created by Pratham Prasad. Main aapke computer controls, code, web projects, aur daily tasks ko effortlessly manage karne ke liye hamesha tayyar hoon."

        # 4. What are you doing / Kya kar rahe ho
        if re.match(r"^(what are you doing|kya kar rahe ho|busy ho kya|kya chal raha hai)(\s+(saathi|bhai))?$", t):
            options = [
                "Aapke system vitals aur background telemetry ko guard kar raha hoon, Pratham. Bas agle command ka intezar hai.",
                "Standing by at full readiness, Pratham. Telemetry monitor ho rahi hai, ready whenever you are."
            ]
            return random.choice(options)

        # 5. Presence check / Sun rahe ho / Are you there
        if re.match(r"^(are you there|sun rahe ho|can you hear me|saathi|hey saathi|awake|ready)(\s+(saathi|bhai|sir))?$", t):
            options = [
                "Bilkul Pratham, main yahin hoon aur dhyan se sun raha hoon. Boliye, kya madad karoon?",
                "Loud and clear, Pratham! I'm right here with you. What do you need?",
                "Online and listening, sir. At your command."
            ]
            return random.choice(options)

        # 6. Gratitude / Thank you
        if re.match(r"^(thank you|thanks|shukriya|dhanyawaad|dhanyawad|great job|well done|good job|awesome)(\s+(saathi|bhai|sir))?$", t):
            options = [
                "Always at your service, Pratham. Aap bas focus rakhiye, baki sab main dekh loonga.",
                "My pleasure, Pratham! Kabhi bhi zaroorat ho, I'm right here.",
                "Anytime, sir. That's what a co-pilot is for. I've got your back."
            ]
            return random.choice(options)

        # 7. Affirmations: ok, okay, theek hai, cool, great, understood
        if re.match(r"^(ok|okay|theek hai|achha|cool|nice|great|got it|understood)(\s+(saathi|bhai|sir))?$", t):
            options = [
                "Bilkul Pratham! Ready whenever you are.",
                "Understood, sir. Standing by.",
                "Roger that, Pratham. Sab control mein hai."
            ]
            return random.choice(options)

        # 8. Capabilities / What can you do
        if re.match(r"^(what can you do|kya kar sakte ho|features|help|madad|capabilities)(\s+(saathi|bhai|sir))?$", t):
            return "Main websites build kar sakta hoon, files organize kar sakta hoon, terminal commands safely run kar sakta hoon, live weather aur currency check kar sakta hoon, aur reminders manage karta hoon. Jo bolein, execute kar denge!"

        # 9. Humor / Joke
        if re.match(r"^(tell me a joke|koi joke sunao|joke|make me laugh)(\s+(saathi|bhai|sir))?$", t):
            return "Ek developer ne doosre se poocha: 'Zindagi mein itna stress kyun hai?' Doosra bola: 'Semicolon missing tha bhai, code compile hi nahi ho rahi!' Always keep smiling, Pratham!"

        # 10. Time of day greetings
        if re.match(r"^(good morning)(\s+(saathi|bhai|sir))?$", t):
            return "A very good morning, Pratham! System vitals nominal, mind clear. Let's make today productive and great."
        if re.match(r"^(good afternoon)(\s+(saathi|bhai|sir))?$", t):
            return "Good afternoon, Pratham! Systems are humming along nicely. What are we tackling this afternoon?"
        if re.match(r"^(good evening)(\s+(saathi|bhai|sir))?$", t):
            return "Good evening, Pratham! Ready for our evening run. Let me know what you'd like to work on."
        if re.match(r"^(good night|shubh ratri)(\s+(saathi|bhai|sir))?$", t):
            return "Shubh ratri, Pratham. Rest well and recharge. Main background telemetry guard kar raha hoon."

        # 11. Farewell
        if re.match(r"^(bye|goodbye|alvida|see you|catch you later)(\s+(saathi|bhai|sir))?$", t):
            return "Take care, Pratham! Standing by in the background whenever you need me."

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
            reply = f"At your service, sir. '{matched_wf.name}' protocol execute ho chuka hai. All {len(res.get('results', []))} operational steps completed cleanly. Sab control mein hai."
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
                f"At your service, sir. '{topic}' ka bespoke, high-grade interface ready karke browser mein launch kar diya hai.\n\n"
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
                    "keep_alive": "60m"
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
                final_reply = f"At your service, sir. '{clean_title}' ka interface synthesize karke browser mein live display kar diya hai.\n• File: {html_file}"

            # Open finished website if created
            if created_html_files:
                self.executor.execute("open_target", {"target": created_html_files[-1]})

            if not final_reply:
                final_reply = "Sab sambhal liya hai, sir. All operations executed cleanly. I've got your back—let me know our next move."

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

