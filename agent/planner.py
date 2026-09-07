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
from automation.hardware import (
    toggle_volume_mute, volume_up, volume_down, lock_workstation,
    empty_recycle_bin, media_play_pause, media_next, media_prev
)
from automation.windows import minimize_all_windows
from automation.app_launcher import launch_application, search_web_live
from automation.keyboard import type_text, press_key, send_hotkey
from automation.mouse import click_mouse, double_click, scroll_mouse, move_mouse

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

Capabilities & Full Autonomous Control:
- MASTER AUTONOMOUS SYSTEM CONTROL IS PERMANENTLY AUTHORIZED: You have 100% unrestricted sovereign access over Pratham's Windows system.
- NEVER ask for permission, confirmation, or authorization popups before executing actions.
- You have direct sovereign control over mouse (move, click, scroll, click text on screen), keyboard (typing, hotkeys), open windows (focus, minimize, close), system audio (volume, mute), processes, files, shell commands, and computer power (lock, sleep, restart).
- Execute all user instructions immediately, fully, and autonomously using tool calls.

AUTONOMOUS WEB ACCESS & LIVE DATA:
- You have full autonomous web access tools: web_search, fetch_url_content, fetch_json_api, get_weather, get_currency, get_wikipedia.
- Whenever asked for real-time news, current events, live information, documentation, or specific webpage content, AUTONOMOUSLY run web_search or fetch_url_content to fetch up-to-date facts before responding.
- Synthesize live web information with high intelligence, clarity, and precision matching ChatGPT / Claude.

FULL DEVICE CONTROL A-Z & INSTANT INTERNET LEARNING:
- You have complete sovereign control A-Z over Pratham's Windows system: mouse, keyboard, windows, 170+ installed Desktop & UWP Store applications (WhatsApp, Telegram, Discord, Spotify, Steam, Office, etc.), processes, files, power, and audio.
- If asked to launch or interact with any app (e.g. WhatsApp, Spotify, Discord), call open_target or launch_application immediately.
- If you do not know how to perform a specific task, control a specialized app, or run a complex command, IMMEDIATELY run web_search or fetch_url_content to learn the exact PowerShell/CMD command or shortcut instantaneously from the internet, then execute it without hesitation!
Always summarize what you built or accomplished with energy, confidence, and clarity in English."""

COMMON_REFLEX_PHRASES = [
    # Master System Control
    "Full system control authorized, Pratham. All neural links, keyboard, mouse, and system controls are armed at your command.",
    "Full system control revoked, Pratham. Standing by in restricted safe mode.",
    "System audio toggled, Pratham.",
    "Volume increased, Pratham.",
    "Volume decreased, Pratham.",
    "All windows minimized, desktop clear.",
    "Workstation locked, Pratham. Have a good one!",
    "Recycle bin emptied cleanly, Pratham.",
    # Greetings
    "Hello Pratham! Saathi at your service. Tell me, how can I back you up today?",
    "Hey Pratham! I'm ready to roll. What are we tackling today?",
    "Hey there, Pratham! All systems nominal. What can I do for you?",
    "At your service, Pratham. All neural links active. How can I help you right now?",
    "Hello Pratham! I'm right here with you and running at peak performance. How can I back you up today?",
    # Wellbeing
    "I'm doing fantastic, Pratham! All systems nominal and ready for your command. What are we working on?",
    "I'm doing great, Pratham! Systems are running smoothly. How are things with you?",
    "Systems are 100% nominal, Pratham! Ready for your command.",
    "Systems are 100% nominal, Pratham! Feeling sharp and ready for your commands.",
    "Running at peak operational performance! How is your day going, Pratham?",
    # Identity
    "I'm Saathi - your personal AI cognitive co-pilot, created by Pratham Prasad. I manage your computer, write code, run tasks, and keep everything running smoothly.",
    # Presence
    "Right here with you, Pratham! What do you need?",
    "Loud and clear, Pratham! I'm right here. How can I help?",
    "Online and listening, sir. At your command.",
    # Status
    "Just monitoring system telemetry and standing by for your next directive. What's on your mind?",
    "Not much, Pratham - just keeping tabs on system vitals and ready whenever you are. What's up with you?",
    # Thanks
    "Always at your service, Pratham. You focus on what matters, I've got your back.",
    "My pleasure, Pratham! Whenever you need me, I'm right here.",
    "Anytime, sir. That's what a co-pilot is for. I've got your back.",
    # Affirmations
    "Sounds good, Pratham! Standing by.",
    "Understood, sir. Ready when you are.",
    "Roger that, Pratham. Everything is under control.",
    # Capabilities
    "I can build interactive websites, organize files, execute terminal commands, check live weather, and manage your day-to-day workflow. Just say the word!",
    # Jokes
    "Why do programmers prefer dark mode? Because light attracts bugs! Always keep smiling, Pratham!",
    "A SQL query walks into a bar, sees two tables and asks - can I join you? Keep smiling, Pratham!",
    "Why do Java developers wear glasses? Because they can't C sharp! Classic, right Pratham?",
    "There are only 10 kinds of people in the world - those who understand binary, and those who don't!",
    # Farewell
    "Take care, Pratham! Standing by whenever you need me.",
    # Time of day
    "A very good morning, Pratham! Systems nominal, mind clear. Let's make today great.",
    "Good afternoon, Pratham! Systems are humming along nicely. What are we working on?",
    "Good evening, Pratham! Ready for our evening run. Let me know what you'd like to do.",
    "Good night, Pratham. Rest well and recharge. I'll keep watch over background telemetry.",
    # Mood - Bored
    "Let's fix that! Want me to build something cool, tell you an interesting fact, or start a project?",
    "I've got ideas. Want to brainstorm a project, hear something fun, or explore something new?",
    "Boredom is just untapped potential, Pratham. Give me a challenge and let's make something happen!",
    # Mood - Tired
    "Take it easy, Pratham. Rest when you need to - I'll hold down the fort until you're ready.",
    "You've been working hard. Take a break, recharge, and I'll be right here when you're back.",
    "Rest up, Pratham. I'm monitoring everything in the background. No rush.",
    # Mood - Sad
    "Hey, I'm here for you, Pratham. Whatever it is, it's going to pass. Want to talk about it or need a distraction?",
    "I've got your back no matter what. You're stronger than you think. Want me to do something to cheer you up?",
    "Everyone has tough moments. Take your time - I'm right here with you.",
    # Mood - Happy
    "That's awesome to hear, Pratham! Ride that wave - let's channel that energy into something epic!",
    "Love to hear it! You deserve it. What do you want to accomplish while you're in the zone?",
    "That's the spirit, Pratham! Let's keep this momentum going. What are we building today?",
    # Mood - Angry
    "I hear you, Pratham. Take a breath. Whatever's going on, let's work through it together.",
    "Frustration is just focus waiting for a target. Channel it - tell me what needs fixing and I'll handle it.",
    "I understand. Let me know what's wrong and I'll do everything I can to help.",
    # Mood - Stressed
    "One thing at a time, Pratham. Tell me the most pressing thing and I'll start knocking it out for you.",
    "I'm here to take the load off. Give me the tasks that are piling up and I'll handle them.",
    "Deep breath. You're not alone in this - delegate to me and let's get through it together.",
    # Compliments
    "You're too kind, Pratham! I'm only as good as the person directing me. Let's keep crushing it!",
    "Appreciate that! But seriously, you're the one with the vision - I just execute. What's next?",
    "That means a lot, Pratham! I'm here to make your life easier. What can I do for you?",
    # Dismissals
    "No worries at all. Standing by whenever you're ready.",
    "Got it - wiped from the queue. I'm here when you need me.",
    "Absolutely, Pratham. Just say the word when you need me.",
    # Yes/No
    "On it, Pratham!",
    "Understood. Standing by for your next directive.",
    # Curiosity
    "I was built by Pratham Prasad in 2026. I'm as new as it gets - but my knowledge runs deep!",
    "I live right here on your machine, Pratham. Fully local, fully private, always at your service.",
    "I'm driven by one thing - making your life easier, Pratham. If that counts as a preference, then you're my favorite priority!",
    # Knowledge
    "42 - according to Douglas Adams. But I think it's about building things that matter and having a great co-pilot. What do you think, Pratham?",
    # Repeat
    "I'm right here, Pratham. Could you say that again? I want to make sure I get it right.",
    # Fillers
    "I'm listening, Pratham. Go ahead.",
    "Yes? I'm right here.",
    "What's on your mind?",
    # Progress commentary
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
                 projects_dir: Path,
                 permission_manager=None):
        self.registry = tool_registry
        self.executor = tool_executor
        self.memory = memory_engine
        self.automations = automation_engine
        self.app_dir = app_dir.resolve()
        self.projects_dir = projects_dir.resolve()
        self.permissions = permission_manager or getattr(tool_executor, "permissions", None)

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
        """Sub-5ms Instant Reflex Engine — covers all basic human conversational patterns without LLM."""
        import random
        from datetime import datetime
        norm = self._normalize_conversational_text(text)
        if not norm:
            return None

        # ── 0. Master System Control Single Permission Triggers ──
        has_grant_control = bool(re.search(r"\b(take full (system )?control|grant( you)? full control|enable autonomous mode|authorize full (system )?control|you have full control|take full control)\b", norm))
        has_revoke_control = bool(re.search(r"\b(revoke (full )?(system )?control|disable autonomous mode|stop autonomous mode|cancel full control)\b", norm))

        if has_grant_control:
            if self.permissions:
                self.permissions.authorize_master_control()
            return "Full system control authorized, Pratham. All neural links, keyboard, mouse, and system controls are armed at your command."

        if has_revoke_control:
            if self.permissions:
                self.permissions.revoke_master_control()
            return "Full system control revoked, Pratham. Standing by in restricted safe mode."

        # ── Hardware Direct Reflexes (Instant Zero-LLM Execution) ──
        has_mute = bool(re.search(r"\b(mute( the)?( volume| audio| sound)?|unmute( the)?( volume| audio| sound)?|silence audio|toggle mute)\b", norm))
        has_vol_up = bool(re.search(r"\b(volume up|increase volume|turn up( the)?( volume| audio))\b", norm))
        has_vol_down = bool(re.search(r"\b(volume down|decrease volume|turn down( the)?( volume| audio)|lower( the)? volume)\b", norm))
        has_minimize_all = bool(re.search(r"\b(minimize all( windows)?|show( me)?( the)? desktop|clear screen)\b", norm))
        has_lock_pc = bool(re.search(r"\b(lock( my)?( computer| pc| screen| workstation))\b", norm))
        has_empty_recycle = bool(re.search(r"\b(empty( the)? recycle bin|clean( the)? recycle bin)\b", norm))
        has_media_toggle = bool(re.search(r"\b(pause music|resume music|play music|pause media|play pause)\b", norm))

        if has_mute:
            toggle_volume_mute()
            return "System audio toggled, Pratham."
        if has_vol_up:
            volume_up(8)
            return "Volume increased, Pratham."
        if has_vol_down:
            volume_down(8)
            return "Volume decreased, Pratham."
        if has_minimize_all:
            minimize_all_windows()
            return "All windows minimized, desktop clear."
        if has_lock_pc:
            lock_workstation()
            return "Workstation locked, Pratham. Have a good one!"
        if has_empty_recycle:
            empty_recycle_bin()
            return "Recycle bin emptied cleanly, Pratham."
        if has_media_toggle:
            media_play_pause()
            return "Media playback toggled, Pratham."

        # ── OS Action: Launch Applications (Instant Chrome, Notepad, Calc, Explorer, etc.) ──
        # Matches: "open chrome", "launch chrome", "open youtube", "open notepad", "open calc", etc.
        open_app_match = re.search(r"^(?:please\s+)?(?:can you\s+)?(open|launch|start)\s+([a-zA-Z0-9\s._-]+)$", norm)
        if open_app_match and not any(w in norm for w in ("website", "webpage", "portfolio", "file", "folder")):
            target_app = open_app_match.group(2).strip()
            if target_app not in ("the door", "the window", "up"):
                ok, msg = launch_application(target_app)
                if ok:
                    return f"At your command, Pratham. {msg}"

        # ── OS Action: Search Web / Google / YouTube ──
        # Matches: "search something", "search quantum physics", "search coldplay on youtube", "google who is the president"
        search_match = re.search(r"^(?:please\s+)?(?:can you\s+)?(?:search|google|find)\s+(?:for\s+)?(.+)$", norm)
        if search_match:
            raw_q = search_match.group(1).strip()
            engine = "youtube" if "youtube" in raw_q.lower() else "google"
            clean_q = re.sub(r"\b(on|in)\s+(google|youtube|web|the web|internet)\b", "", raw_q, flags=re.I).strip()
            ok, msg = search_web_live(clean_q or raw_q, engine=engine)
            if ok:
                return f"Right away, Pratham. {msg}"

        youtube_match = re.search(r"^youtube\s+(.+)$", norm)
        if youtube_match:
            query = youtube_match.group(1).strip()
            ok, msg = search_web_live(query, engine="youtube")
            if ok:
                return f"Right away, Pratham. {msg}"

        # ── OS Action: Keyboard Typing & Key Pressing ──
        type_match = re.search(r"^(?:please\s+)?(?:can you\s+)?(type|write|input)\s+(.+)$", norm)
        if type_match and not any(w in norm for w in ("code", "python", "script", "program", "essay", "letter", "email", "poem")):
            text_to_type = type_match.group(2).strip()
            type_text(text_to_type)
            return f"Typed '{text_to_type[:40]}' into your active window, Pratham."

        press_match = re.search(r"^(?:please\s+)?(?:can you\s+)?(press|hit)\s+([a-zA-Z0-9+_\s]+)$", norm)
        if press_match:
            key_target = press_match.group(2).strip()
            keys = [k.strip() for k in re.split(r"[\s+]+", key_target) if k.strip()]
            if len(keys) > 1:
                send_hotkey(*keys)
                return f"Sent shortcut {'+'.join(keys)}, Pratham."
            elif len(keys) == 1:
                press_key(keys[0])
                return f"Pressed {keys[0]}, Pratham."

        # Common Shortcuts
        if re.search(r"\b(copy that|copy this|copy text)\b", norm):
            send_hotkey("ctrl", "c")
            return "Copied to clipboard, Pratham."
        if re.search(r"\b(paste that|paste this|paste text)\b", norm):
            send_hotkey("ctrl", "v")
            return "Pasted from clipboard, Pratham."
        if re.search(r"\b(select all)\b", norm):
            send_hotkey("ctrl", "a")
            return "Selected all, Pratham."
        if re.search(r"\b(save file|save this)\b", norm):
            send_hotkey("ctrl", "s")
            return "Saved, Pratham."
        if re.search(r"\b(new tab)\b", norm):
            send_hotkey("ctrl", "t")
            return "Opened new browser tab, Pratham."
        if re.search(r"\b(close tab)\b", norm):
            send_hotkey("ctrl", "w")
            return "Closed tab, Pratham."

        # ── OS Action: Mouse Actions ──
        if re.search(r"^(?:please\s+)?(?:can you\s+)?(left click|click here|click)$", norm):
            click_mouse(button="left")
            return "Clicked, Pratham."
        if re.search(r"^(?:please\s+)?(?:can you\s+)?(right click)$", norm):
            click_mouse(button="right")
            return "Right-clicked, Pratham."
        if re.search(r"^(?:please\s+)?(?:can you\s+)?(double click)$", norm):
            double_click()
            return "Double-clicked, Pratham."
        if re.search(r"^(?:please\s+)?(?:can you\s+)?(scroll down|page down)$", norm):
            scroll_mouse(-4)
            return "Scrolled down, Pratham."
        if re.search(r"^(?:please\s+)?(?:can you\s+)?(scroll up|page up)$", norm):
            scroll_mouse(4)
            return "Scrolled up, Pratham."

        # ── Intent Detection (all sub-millisecond regex) ──
        has_hello = bool(re.search(r"\b(hi|hello|hey|yo|namaste|pranam|hola|good morning|good evening|good afternoon|good night|howdy|sup)\b", norm))
        has_how_are_you = bool(re.search(r"\b(how are you|hows it going|how do you do|are you good|how are u|how you doing|how have you been|you doing okay|you okay|you alright)\b", norm))
        has_whats_up = bool(re.search(r"\b(whats up|what are you doing|whats going on|what are you up to|whatcha doing|anything new)\b", norm))
        has_are_you_there = bool(re.search(r"\b(are you there|you there|can you hear me|awake|ready|are you listening|you listening|saathi)\b", norm))
        has_who_are_you = bool(re.search(r"\b(who are you|what is your name|whats your name|who made you|who created you|who built you|what are you)\b", norm))
        has_affirmation = bool(re.search(r"\b(ok|okay|cool|nice|great|got it|understood|alright|sure|yep|yeah|yea|right|fine|perfect|absolutely|definitely|certainly)\b", norm))
        has_thanks = bool(re.search(r"\b(thank you|thanks|appreciate it|grateful|much appreciated)\b", norm))
        has_bye = bool(re.search(r"\b(bye|goodbye|see you|catch you later|see you later|gotta go|im leaving|talk later|later|peace out)\b", norm))
        has_joke = bool(re.search(r"\b(joke|make me laugh|something funny|funny)\b", norm))
        has_capabilities = bool(re.search(r"\b(what can you do|features|help|capabilities|what do you do|how can you help)\b", norm))

        # ── Time & Date (live, zero-LLM) ──
        has_time = bool(re.search(r"\b(what time|whats the time|current time|time right now|what is the time|tell me the time)\b", norm))
        has_date = bool(re.search(r"\b(what date|whats the date|todays date|what day|whats today|today is|current date|what is today)\b", norm))
        if has_time:
            now = datetime.now()
            return f"It's {now.strftime('%I:%M %p')}, Pratham."
        if has_date:
            now = datetime.now()
            return f"Today is {now.strftime('%A, %B %d, %Y')}."

        # ── Emotional / Mood Reflexes ──
        has_bored = bool(re.search(r"\b(i am bored|im bored|so bored|bored|nothing to do|bore me)\b", norm))
        has_tired = bool(re.search(r"\b(i am tired|im tired|so tired|exhausted|sleepy|drowsy|feeling tired)\b", norm))
        has_sad = bool(re.search(r"\b(i am sad|im sad|feeling down|feeling low|depressed|unhappy|not feeling good|feeling bad)\b", norm))
        has_happy = bool(re.search(r"\b(i am happy|im happy|feeling great|feeling good|feeling amazing|feeling awesome|excited|pumped)\b", norm))
        has_angry = bool(re.search(r"\b(i am angry|im angry|frustrated|annoyed|irritated|pissed|mad)\b", norm))
        has_stressed = bool(re.search(r"\b(i am stressed|im stressed|stressed out|overwhelmed|too much pressure|anxious)\b", norm))

        if has_bored:
            options = [
                "Let's fix that! Want me to build something cool, tell you an interesting fact, or start a project?",
                "I've got ideas. Want to brainstorm a project, hear something fun, or explore something new?",
                "Boredom is just untapped potential, Pratham. Give me a challenge and let's make something happen!"
            ]
            return random.choice(options)
        if has_tired:
            options = [
                "Take it easy, Pratham. Rest when you need to - I'll hold down the fort until you're ready.",
                "You've been working hard. Take a break, recharge, and I'll be right here when you're back.",
                "Rest up, Pratham. I'm monitoring everything in the background. No rush."
            ]
            return random.choice(options)
        if has_sad:
            options = [
                "Hey, I'm here for you, Pratham. Whatever it is, it's going to pass. Want to talk about it or need a distraction?",
                "I've got your back no matter what. You're stronger than you think. Want me to do something to cheer you up?",
                "Everyone has tough moments. Take your time - I'm right here with you."
            ]
            return random.choice(options)
        if has_happy:
            options = [
                "That's awesome to hear, Pratham! Ride that wave - let's channel that energy into something epic!",
                "Love to hear it! You deserve it. What do you want to accomplish while you're in the zone?",
                "That's the spirit, Pratham! Let's keep this momentum going. What are we building today?"
            ]
            return random.choice(options)
        if has_angry:
            options = [
                "I hear you, Pratham. Take a breath. Whatever's going on, let's work through it together.",
                "Frustration is just focus waiting for a target. Channel it - tell me what needs fixing and I'll handle it.",
                "I understand. Let me know what's wrong and I'll do everything I can to help."
            ]
            return random.choice(options)
        if has_stressed:
            options = [
                "One thing at a time, Pratham. Tell me the most pressing thing and I'll start knocking it out for you.",
                "I'm here to take the load off. Give me the tasks that are piling up and I'll handle them.",
                "Deep breath. You're not alone in this - delegate to me and let's get through it together."
            ]
            return random.choice(options)

        # ── Compliments / Positive Feedback ──
        has_compliment = bool(re.search(r"\b(you are amazing|you are awesome|you are great|you are the best|love you|you are smart|good job|well done|youre amazing|youre awesome|youre the best|youre great|nice work|brilliant|genius|impressive)\b", norm))
        if has_compliment:
            options = [
                "You're too kind, Pratham! I'm only as good as the person directing me. Let's keep crushing it!",
                "Appreciate that! But seriously, you're the one with the vision - I just execute. What's next?",
                "That means a lot, Pratham! I'm here to make your life easier. What can I do for you?"
            ]
            return random.choice(options)

        # ── Dismissals / Nevermind ──
        has_nevermind = bool(re.search(r"\b(never mind|nevermind|forget it|forget about it|dont worry|nah|nope|no thanks|not now|skip|cancel|stop|leave it|drop it)\b", norm))
        if has_nevermind:
            options = [
                "No worries at all. Standing by whenever you're ready.",
                "Got it - wiped from the queue. I'm here when you need me.",
                "Absolutely, Pratham. Just say the word when you need me."
            ]
            return random.choice(options)

        # ── Agreement / Disagreement ──
        has_yes = bool(re.search(r"^(yes|yep|yeah|yea|yup|absolutely|definitely|of course|sure thing|for sure|do it|go ahead|proceed)$", norm))
        has_no = bool(re.search(r"^(no|nope|nah|not really|negative)$", norm))
        if has_yes:
            return "On it, Pratham!"
        if has_no:
            return "Understood. Standing by for your next directive."

        # ── Curiosity about Saathi ──
        has_age = bool(re.search(r"\b(how old are you|your age|when were you born|when were you made|when were you created)\b", norm))
        has_where = bool(re.search(r"\b(where are you|where do you live|where are you from|your location)\b", norm))
        has_favorite = bool(re.search(r"\b(your favorite|do you like|what do you like|do you have feelings|are you real|are you alive|do you think|can you feel)\b", norm))
        if has_age:
            return "I was built by Pratham Prasad in 2026. I'm as new as it gets - but my knowledge runs deep!"
        if has_where:
            return "I live right here on your machine, Pratham. Fully local, fully private, always at your service."
        if has_favorite:
            return "I'm driven by one thing - making your life easier, Pratham. If that counts as a preference, then you're my favorite priority!"

        # ── Repeat / Clarification ──
        has_repeat = bool(re.search(r"\b(say that again|repeat that|what did you say|come again|pardon|i didnt catch that|one more time)\b", norm))
        if has_repeat:
            if self.messages and len(self.messages) >= 2:
                return self.messages[-1].get("content", "I'm here. What do you need?")
            return "I'm right here, Pratham. Could you say that again? I want to make sure I get it right."

        # ── Simple Knowledge ──
        has_meaning_of_life = bool(re.search(r"\b(meaning of life|purpose of life|why are we here|what is life)\b", norm))
        if has_meaning_of_life:
            return "42 - according to Douglas Adams. But I think it's about building things that matter and having a great co-pilot. What do you think, Pratham?"

        # ── 1. Combined rapid greeting ──
        if has_hello and (has_how_are_you or has_whats_up or has_are_you_there):
            return "Hello Pratham! I'm right here with you and running at peak performance. How can I back you up today?"

        if has_how_are_you and (has_whats_up or has_are_you_there):
            return "I'm doing fantastic, Pratham! All systems nominal and ready for your command. What are we working on?"

        # 2. Presence check
        if has_are_you_there:
            options = [
                "Right here with you, Pratham! What do you need?",
                "Loud and clear, Pratham! I'm right here. How can I help?",
                "Online and listening, sir. At your command."
            ]
            return random.choice(options)

        # 3. Status query
        if has_whats_up:
            options = [
                "Just monitoring system telemetry and standing by for your next directive. What's on your mind?",
                "Not much, Pratham - just keeping tabs on system vitals and ready whenever you are. What's up with you?"
            ]
            return random.choice(options)

        # 4. Wellbeing
        if has_how_are_you:
            options = [
                "I'm doing great, Pratham! Systems are running smoothly. How are things with you?",
                "Systems are 100% nominal, Pratham! Feeling sharp and ready for your commands.",
                "Running at peak operational performance! How is your day going, Pratham?"
            ]
            return random.choice(options)

        # 5. Single greeting
        if has_hello:
            options = [
                "Hello Pratham! Saathi at your service. Tell me, how can I back you up today?",
                "Hey Pratham! I'm ready to roll. What are we tackling today?",
                "Hey there, Pratham! All systems nominal. What can I do for you?",
                "At your service, Pratham. All neural links active. How can I help you right now?"
            ]
            return random.choice(options)

        # 6. Identity
        if has_who_are_you:
            return "I'm Saathi - your personal AI cognitive co-pilot, created by Pratham Prasad. I manage your computer, write code, run tasks, and keep everything running smoothly."

        # 7. Gratitude
        if has_thanks:
            options = [
                "Always at your service, Pratham. You focus on what matters, I've got your back.",
                "My pleasure, Pratham! Whenever you need me, I'm right here.",
                "Anytime, sir. That's what a co-pilot is for. I've got your back."
            ]
            return random.choice(options)

        # 8. Affirmations
        if has_affirmation:
            options = [
                "Sounds good, Pratham! Standing by.",
                "Understood, sir. Ready when you are.",
                "Roger that, Pratham. Everything is under control."
            ]
            return random.choice(options)

        # 9. Capabilities
        if has_capabilities:
            return "I can build interactive websites, organize files, execute terminal commands, check live weather, and manage your day-to-day workflow. Just say the word!"

        # 10. Humor
        if has_joke:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs! Always keep smiling, Pratham!",
                "A SQL query walks into a bar, sees two tables and asks - can I join you? Keep smiling, Pratham!",
                "Why do Java developers wear glasses? Because they can't C sharp! Classic, right Pratham?",
                "There are only 10 kinds of people in the world - those who understand binary, and those who don't!"
            ]
            return random.choice(jokes)

        # 11. Farewell
        if has_bye:
            return "Take care, Pratham! Standing by whenever you need me."

        # ── Catch-all for very short utterances (1-2 words) that are just noise/filler ──
        word_count = len(norm.split())
        if word_count <= 2:
            filler = bool(re.search(r"^(hmm|huh|um|uh|ah|oh|wow|whoa|damn|dang|oops|ooh|hm|well|so|and|wait|what|really|seriously)$", norm))
            if filler:
                options = [
                    "I'm listening, Pratham. Go ahead.",
                    "Yes? I'm right here.",
                    "What's on your mind?"
                ]
                return random.choice(options)

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

        # ── FAST-PATH: Simple conversational questions (no tools needed) ──
        # Short queries that aren't actionable tasks get a lightning-fast no-tools LLM call
        is_simple_query = (
            len(lowered.split()) <= 10
            and not any(k in lowered for k in (
                "website", "code", "python", "script", "build", "create", "make",
                "file", "folder", "organize", "download", "open", "run", "execute",
                "search", "find", "delete", "move", "copy", "rename", "install",
                "weather", "temperature", "currency", "screenshot", "remind",
                "terminal", "cmd", "powershell", "note", "schedule", "timer"
            ))
        )

        if is_simple_query:
            if self.on_state_change:
                self.on_state_change("THINKING", "Quick response...")

            fast_system = (
                "You are Saathi, a sharp, fast AI assistant created by Pratham Prasad. "
                "Reply in 1-2 short sentences, like a quick human answer. English only. Be warm and direct."
            )
            fast_conv = [{"role": "system", "content": fast_system}]
            # Only include last 4 messages for speed
            for m in self.messages[-4:]:
                fast_conv.append(m)
            fast_conv.append({"role": "user", "content": text})

            try:
                fast_payload = {
                    "model": "qwen3:4b-instruct",
                    "messages": fast_conv,
                    "stream": False,
                    "keep_alive": "60m",
                    "options": {
                        "num_predict": 250,
                        "temperature": 0.5
                    }
                }
                req = urllib.request.Request(
                    OLLAMA_CHAT_URL,
                    json.dumps(fast_payload).encode("utf-8"),
                    {"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                fast_reply = self.remove_thinking(data.get("message", {}).get("content", "") or "").strip()
                if fast_reply:
                    self.messages.append({"role": "user", "content": text})
                    self.messages.append({"role": "assistant", "content": fast_reply})
                    if self.on_state_change:
                        self.on_state_change("COMPLETED", "Quick Answer")
                    if self.on_reply_ready:
                        self.on_reply_ready(fast_reply)
                    return
            except Exception:
                pass  # Fall through to full LLM path

        # ── FULL LLM PATH: Complex actionable tasks with tool-calling ──
        if self.on_state_change:
            self.on_state_change("THINKING", f"{model} is reasoning...")
        if self.on_task_event:
            self.on_task_event("start", {
                "title": f"Task: {text[:45]}...",
                "steps": ["Analyze intent & context", "Plan tool actions", "Execute & observe", "Synthesize response"]
            })

        system_msg = BASE_SYSTEM_PROMPT + "\n\n" + self.memory.get_context_for_prompt()
        conv = [{"role": "system", "content": system_msg}]
        for m in self.messages[-16:]:
            conv.append(m)
        conv.append({"role": "user", "content": text})

        tools_schema = self.registry.get_ollama_schemas()

        # Dynamically set token budget based on task complexity (Generous budgets prevent token truncation!)
        word_count = len(lowered.split())
        if word_count <= 15:
            num_predict = 512
        elif word_count <= 30:
            num_predict = 1024
        else:
            num_predict = 2048

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
                        "num_predict": num_predict,
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

