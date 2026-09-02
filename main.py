"""Saathi: local-first Hinglish desktop assistant."""

from __future__ import annotations

import json
import os
import queue
import random
import re
import shutil
import subprocess
import sys
import threading
import asyncio
import difflib
import html
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

try:
    from PIL import ImageGrab  # for screenshots; Image/ImageDraw already imported below for the tray icon
except ImportError:
    ImageGrab = None

try:
    from send2trash import send2trash  # deletes go to Recycle Bin instead of being permanent
except ImportError:
    send2trash = None

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None


APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
HISTORY_FILE = DATA_DIR / "history.json"
FAST_MODEL = "qwen3:4b-instruct"
DEEP_MODEL = "qwen3:14b"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
SYSTEM_PROMPT = """You are Saathi, a warm, sharp, capable personal assistant who talks like a real Indian friend, not a robot. Reply only in natural Hinglish, Roman/English letters only (e.g. 'Haan bilkul, abhi karta hoon'). Never use Devanagari, Urdu/Arabic script, or any other writing system. Vary your phrasing, keep it conversational and confident, avoid stiff or repetitive sentence patterns and avoid excessive apologising. Give direct, useful answers. For coding, first state a short plan, then provide complete runnable code and clear run instructions. Be honest about limits. Saathi CAN open apps/websites/media, list/read/create/edit files and folders, run terminal commands, and fetch live data (weather, currency, definitions, Wikipedia, etc.) on the user's desktop once permission is granted or confirmed in the app — say so plainly when something actually happened. Never claim you opened something, changed a file, ran a command, fetched data, sent a message, or controlled a device unless the desktop app actually confirms it happened. Deleting/moving files and running terminal commands always show the user an explicit confirmation with the exact path/command first, regardless of any standing permission — that's a hard rule Saathi cannot waive."""
QUICK_PROMPT = """You are Saathi, chatting casually. Reply only in natural, warm Hinglish using Roman/English letters, never Devanagari or Urdu/Arabic script. Be brief, direct, a little playful, and vary your wording like a real person would — don't sound scripted. You cannot actually play music, open apps, run commands, or touch files yourself from chat — the desktop app handles those separately and will tell the user when it happens. NEVER say or imply a song is "now playing," a file was created, a command ran, or any action is done — if the user wants something done, tell them to phrase it as a direct instruction so the desktop app can act, or acknowledge the app is already handling it. Never reveal hidden reasoning or use <think> tags."""
VOICE_MODEL = "small"
TTS_VOICE = "en-IN-NeerjaNeural"
TTS_RATE = "+15%"

# Never write/delete/run anything under these, even with permission granted — a wrong guess here
# can break Windows itself, not just lose a file. Reading/listing is still fine.
PROTECTED_PATH_PREFIXES = (
    r"c:\windows", r"c:\program files", r"c:\program files (x86)",
    r"c:\programdata", r"c:\$recycle.bin", r"c:\system volume information",
)
# A tiny hard blocklist of commands that are almost never what anyone actually means to run —
# these are refused outright, no confirmation dialog can override them.
DANGEROUS_COMMAND_PATTERNS = (
    r"format\s+[a-z]:", r"\bdiskpart\b", r"rd\s+/s\s+/q\s+[a-z]:\\?\s*$",
    r"del\s+/s\s+/q\s+[a-z]:\\?\s*$", r"rm\s+-rf\s+/\s*$", r"rm\s+-rf\s+/\*",
    r":\(\)\{.*:\|:&\};:",  # classic fork bomb
)

# Free, no-API-key endpoints from the public-apis list, wired into natural chat.
# Add more entries here to extend coverage — this is intentionally a small curated set,
# not all 1400+ entries in the public-apis repo (most need separate signups/keys).
API_ENDPOINTS = {
    "geocode": "https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1",
    "weather": "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true",
    "currency": "https://api.frankfurter.app/latest?amount={amount}&from={base}&to={target}",
    "define": "https://api.dictionaryapi.dev/api/v2/entries/en/{query}",
    "wiki": "https://en.wikipedia.org/api/rest_v1/page/summary/{query}",
    "trivia": "https://opentdb.com/api.php?amount=1&type=multiple",
    "joke": "https://official-joke-api.appspot.com/random_joke",
    "quote": "https://zenquotes.io/api/random",
    "country": "https://restcountries.com/v3.1/name/{query}",
    "advice": "https://api.adviceslip.com/advice",
    "translate": "https://api.mymemory.translated.net/get?q={query}&langpair={source}|{target}",
    "myip": "https://api.ipify.org?format=json",
    "hn_top": "https://hacker-news.firebaseio.com/v0/topstories.json",
    "hn_item": "https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
}

# Common destinations Saathi can open directly without needing the LLM to guess a URL.
SITE_ALIASES: dict[str, str] = {
    "youtube": "https://www.youtube.com",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "whatsapp web": "https://web.whatsapp.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://x.com",
    "x": "https://x.com",
    "amazon": "https://www.amazon.in",
    "github": "https://github.com",
    "maps": "https://maps.google.com",
    "google maps": "https://maps.google.com",
    "drive": "https://drive.google.com",
    "google drive": "https://drive.google.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "prime video": "https://www.primevideo.com",
    "hotstar": "https://www.hotstar.com",
}

# Local Windows apps launchable by their registered name via the `start` shell command.
APP_ALIASES: dict[str, str] = {
    "notepad": "notepad",
    "calculator": "calc",
    "calc": "calc",
    "paint": "mspaint",
    "file explorer": "explorer",
    "explorer": "explorer",
    "files": "explorer",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "chrome": "chrome",
    "edge": "msedge",
    "spotify app": "spotify",
    "vlc": "vlc",
    "task manager": "taskmgr",
    "settings": "ms-settings:",
    "control panel": "control",
    "terminal": "wt",
    "command prompt": "cmd",
    "cmd": "cmd",
    "discord": "discord",
    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
}


class Saathi:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Saathi — Hinglish Desktop Assistant")
        self.root.geometry("1200x780")
        self.root.minsize(1050, 700)
        self.root.configure(bg="#050914")
        self.history = self.load_history()
        self.reply_queue: queue.Queue[str] = queue.Queue()
        self.voice_queue: queue.Queue[str] = queue.Queue()
        self.display_queue: queue.Queue[str] = queue.Queue()
        self.typing_active = False
        self.model_var = tk.StringVar(value=DEEP_MODEL)
        self.fast_model_var = tk.StringVar(value=FAST_MODEL)
        self.record_seconds_var = tk.IntVar(value=6)
        self.voice_model_var = tk.StringVar(value=VOICE_MODEL)
        self.status_var = tk.StringVar(value="Checking Ollama...")
        self.whisper_model = None
        self._loaded_voice_model = None
        self.listening = False
        self.speech_lock = threading.Lock()
        self.routine_permissions = False
        self.permission_status = tk.StringVar(value="Open/launch permission: ask each time")
        self.permission_button = tk.StringVar(value="Grant open & launch permission")
        self.last_reply = ""
        self.last_opened_site: str | None = None
        self.reminders: list[dict] = []
        self.reminders_file = APP_DIR / "data" / "reminders.json"
        self.load_reminders()
        self.files_root = Path.home()
        self.tray_icon = None
        self.dock_log = None
        self.dock_expanded = True
        self.always_on_top_var = tk.BooleanVar(value=False)
        self.workspace = APP_DIR / "Projects"
        self.workspace.mkdir(exist_ok=True)
        self.configure_theme()
        self.build_ui()
        self.build_docked_widget()
        self.root.after(200, self.process_queues)
        self.animate_orb()
        self.write("Saathi", "Namaste! Main Saathi hoon. Hinglish mein baat karo — text ya voice se.")
        threading.Thread(target=self.check_ollama_status, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        if pystray is not None:
            threading.Thread(target=self.setup_tray_icon, daemon=True).start()
        threading.Thread(target=self.reminder_checker_loop, daemon=True).start()

    def check_ollama_status(self) -> None:
        """Tell the user right away if Ollama isn't reachable, instead of failing on first send."""
        try:
            request = urllib.request.Request(OLLAMA_URL.replace("/api/chat", "/api/tags"))
            with urllib.request.urlopen(request, timeout=4) as response:
                tags = json.loads(response.read().decode("utf-8"))
            installed = {model.get("name", "") for model in tags.get("models", [])}
            missing = [model for model in (self.fast_model_var.get(), self.model_var.get()) if model and not any(model in name for name in installed)]
            if missing:
                self.root.after(0, lambda: self.status_var.set(f"Ollama online, but model(s) not pulled: {', '.join(missing)}"))
            else:
                self.root.after(0, lambda: self.status_var.set("Ready"))
        except Exception:
            self.root.after(0, lambda: self.status_var.set("Ollama not reachable — start it with 'ollama serve'"))

    def configure_theme(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#050914")
        style.configure("TLabel", background="#050914", foreground="#b8d9ff", font=("Segoe UI", 10))
        style.configure("Title.TLabel", foreground="#6fe9ff", font=("Segoe UI", 15, "bold"))
        style.configure("Section.TLabel", foreground="#6fe9ff", font=("Segoe UI", 10, "bold"))
        style.configure("Hint.TLabel", foreground="#5f83a3", font=("Segoe UI", 8))
        style.configure("TButton", background="#122a47", foreground="#dff7ff", borderwidth=0, padding=(11, 7), font=("Segoe UI", 9))
        style.map("TButton", background=[("active", "#1d5c7a")])
        style.configure("Accent.TButton", background="#00b7ff", foreground="#001322", borderwidth=0, padding=(16, 9), font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#4fd2ff")])
        style.configure("Danger.TButton", background="#ff4757", foreground="white", borderwidth=0, padding=(13, 8), font=("Segoe UI", 9, "bold"))
        style.map("Danger.TButton", background=[("active", "#ff6b78")])
        style.configure("TNotebook", background="#050914", borderwidth=0)
        style.configure("TNotebook.Tab", background="#0b1629", foreground="#9bb9d4", padding=(18, 10), font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", "#123c5c")], foreground=[("selected", "#8ff4ff")])
        style.configure("TCombobox", fieldbackground="#0b1629", background="#123c5c", foreground="#dff7ff")
        style.configure("TEntry", fieldbackground="#0b1629", foreground="#eaf6ff", insertcolor="#6fe9ff", borderwidth=0, padding=6)
        style.configure("TSpinbox", fieldbackground="#0b1629", foreground="#eaf6ff", borderwidth=0, padding=4)
        style.configure("TLabelframe", background="#081727", bordercolor="#1b4a68", relief=tk.SOLID, borderwidth=1)
        style.configure("TLabelframe.Label", background="#081727", foreground="#6fe9ff", font=("Segoe UI", 10, "bold"))
        style.configure("Panel.TFrame", background="#081727")
        style.configure("Panel.TLabel", background="#081727", foreground="#b8d9ff", font=("Segoe UI", 10))
        style.configure("PanelHint.TLabel", background="#081727", foreground="#5f83a3", font=("Segoe UI", 8))
        style.configure("TCheckbutton", background="#081727", foreground="#b8d9ff")
        style.map("TCheckbutton", background=[("active", "#081727")])

    def build_ui(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        chat_tab = ttk.Frame(notebook)
        actions_tab = ttk.Frame(notebook)
        coding_tab = ttk.Frame(notebook)
        notebook.add(chat_tab, text="Chat & Voice")
        notebook.add(actions_tab, text="Safe Actions")
        notebook.add(coding_tab, text="Coding Workspace")

        header = tk.Canvas(chat_tab, height=42, bg="#050914", highlightthickness=0)
        header.pack(fill=tk.X, padx=12, pady=(8, 0))
        header.create_line(0, 34, 1160, 34, fill="#164866", width=1)
        header.create_text(600, 17, text="S A A T H I", fill="#71edff", font=("Segoe UI", 18, "bold"))
        header.create_text(75, 17, text="SYSTEM ONLINE", fill="#45cbb7", font=("Segoe UI", 9, "bold"))
        header.create_text(1080, 17, text="LOCAL • PRIVATE", fill="#6f91b4", font=("Segoe UI", 9, "bold"))

        dashboard = tk.Frame(chat_tab, bg="#050914")
        dashboard.pack(fill=tk.X, padx=12, pady=6)
        dashboard.grid_columnconfigure(0, weight=1)
        dashboard.grid_columnconfigure(1, weight=2)
        dashboard.grid_columnconfigure(2, weight=1)

        left = tk.Frame(dashboard, bg="#081727", highlightbackground="#1b4a68", highlightthickness=1, width=250, height=280)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_propagate(False)
        tk.Label(left, text="SYSTEM STATUS", bg="#081727", fg="#6fe9ff", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=14, pady=(13, 8))
        tk.Label(left, text="●  LOCAL BRAIN", bg="#081727", fg="#4de0bd", font=("Segoe UI", 9)).pack(anchor=tk.W, padx=14)
        tk.Label(left, text="●  VOICE INPUT", bg="#081727", fg="#4de0bd", font=("Segoe UI", 9)).pack(anchor=tk.W, padx=14, pady=5)
        tk.Label(left, text="●  ROUTINE ACCESS", bg="#081727", fg="#b8d9ff", font=("Segoe UI", 9)).pack(anchor=tk.W, padx=14)
        tk.Frame(left, bg="#1b4a68", height=1).pack(fill=tk.X, padx=14, pady=12)
        ttk.Button(left, text="🔓 Grant session access", style="Accent.TButton", command=self.toggle_routine_permissions).pack(fill=tk.X, padx=14, pady=3)
        ttk.Checkbutton(left, text="Always on top", variable=self.always_on_top_var, command=self.toggle_always_on_top).pack(anchor=tk.W, padx=14, pady=3)
        tk.Label(left, text="Closing this window minimizes to\nthe tray — Saathi stays ready.", bg="#081727", fg="#6f91b4", font=("Segoe UI", 8), justify=tk.LEFT).pack(anchor=tk.W, padx=14, pady=(2, 6))
        ttk.Button(left, text="Open safe actions", command=lambda: notebook.select(actions_tab)).pack(fill=tk.X, padx=14, pady=3)
        ttk.Button(left, text="Coding workspace", command=lambda: notebook.select(coding_tab)).pack(fill=tk.X, padx=14, pady=3)

        hero = tk.Canvas(dashboard, height=280, bg="#050914", highlightthickness=0)
        hero.grid(row=0, column=1, sticky="nsew")
        hero.create_line(15, 15, 100, 15, fill="#2c84a4")
        hero.create_line(15, 15, 15, 55, fill="#2c84a4")
        hero.create_line(445, 15, 360, 15, fill="#2c84a4")
        hero.create_line(445, 15, 445, 55, fill="#2c84a4")
        hero.create_text(230, 25, text="NEURAL CORE", fill="#5fbfd8", font=("Segoe UI", 9, "bold"))
        hero.create_text(230, 255, text="LISTEN  •  THINK  •  ASSIST", fill="#5b8eaa", font=("Segoe UI", 9))
        self.orb = hero
        self.orb_center = (230, 140)
        self.orb_items = [hero.create_oval(0, 0, 0, 0, outline="#0b3559", width=2), hero.create_oval(0, 0, 0, 0, outline="#1a6b91", width=2), hero.create_oval(0, 0, 0, 0, outline="#3fd7ff", width=2), hero.create_oval(0, 0, 0, 0, outline="", fill="#d6ffff")]
        self.orbit_a = hero.create_oval(72, 105, 388, 175, outline="#1d769b", width=1)
        self.orbit_b = hero.create_oval(110, 55, 350, 225, outline="#115170", width=1)
        hero.create_line(45, 140, 415, 140, fill="#0f3b56")
        hero.create_line(230, 48, 230, 232, fill="#0f3b56")

        right = tk.Frame(dashboard, bg="#081727", highlightbackground="#1b4a68", highlightthickness=1, width=250, height=280)
        right.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        right.grid_propagate(False)
        tk.Label(right, text="ASSISTANT CONTROL", bg="#081727", fg="#6fe9ff", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=14, pady=(13, 8))
        tk.Label(right, textvariable=self.status_var, bg="#081727", fg="#b8d9ff", wraplength=210, justify=tk.LEFT).pack(anchor=tk.W, padx=14, pady=3)
        tk.Label(right, text="VOICE: Indian Neural", bg="#081727", fg="#4de0bd", font=("Segoe UI", 9)).pack(anchor=tk.W, padx=14, pady=6)
        ttk.Button(right, text="🎤 Speak to Saathi", style="Accent.TButton", command=self.listen).pack(fill=tk.X, padx=14, pady=(10, 3))
        ttk.Button(right, text="Clear conversation", command=self.clear_history).pack(fill=tk.X, padx=14, pady=3)

        top = ttk.Frame(chat_tab)
        top.pack(fill=tk.X, padx=8, pady=8)
        ttk.Label(top, text="Fast model:").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.fast_model_var, width=16).pack(side=tk.LEFT, padx=(4, 12))
        ttk.Label(top, text="Deep model:").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.model_var, width=16).pack(side=tk.LEFT, padx=(4, 12))
        ttk.Label(top, text="Record secs:").pack(side=tk.LEFT)
        ttk.Spinbox(top, from_=3, to=15, textvariable=self.record_seconds_var, width=4).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="Voice model:").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Combobox(top, textvariable=self.voice_model_var, values=["tiny", "base", "small", "medium"], width=8, state="readonly").pack(side=tk.LEFT, padx=4)
        self.chat = scrolledtext.ScrolledText(chat_tab, state="disabled", wrap=tk.WORD, font=("Segoe UI", 11), bg="#08101e", fg="#d6efff", insertbackground="#6fe9ff", relief=tk.FLAT, padx=14, pady=12, spacing3=4)
        self.style_chat_tags(self.chat)
        self.chat.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        input_row = ttk.Frame(chat_tab)
        input_row.pack(fill=tk.X, padx=8, pady=8)
        self.message_input = ttk.Entry(input_row, font=("Segoe UI", 11))
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_input.bind("<Return>", lambda _event: self.send_message())
        ttk.Button(input_row, text="➤ Send", style="Accent.TButton", command=self.send_message).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(input_row, text="Speak (6 sec)", command=self.listen).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(input_row, text="Clear chat", command=self.clear_history).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(input_row, text="Copy last reply", command=self.copy_last_reply).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(input_row, text="Regenerate", command=self.regenerate_last).pack(side=tk.LEFT, padx=(6, 0))
        tip_row = ttk.Frame(chat_tab)
        tip_row.pack(fill=tk.X, padx=10, pady=(0, 8))
        ttk.Label(tip_row, text="💡 Tip: type 'open youtube', 'play spotify', 'remind me to X in 10 minutes', 'weather in Kolkata' — Saathi acts on these instantly.", style="Hint.TLabel", wraplength=900).pack(side=tk.LEFT)
        ttk.Label(tip_row, textvariable=self.status_var, style="Hint.TLabel").pack(side=tk.RIGHT)

        ttk.Label(actions_tab, text="Safe Actions", style="Title.TLabel").pack(anchor=tk.W, padx=15, pady=(15, 2))
        ttk.Label(actions_tab, text="Deletes and terminal commands always ask for confirmation first — no exceptions.", style="Hint.TLabel").pack(anchor=tk.W, padx=15, pady=(0, 10))

        permissions = ttk.Frame(actions_tab)
        permissions.pack(fill=tk.X, padx=15, pady=(0, 12))
        ttk.Label(permissions, textvariable=self.permission_status).pack(side=tk.LEFT)
        ttk.Button(permissions, textvariable=self.permission_button, style="Accent.TButton", command=self.toggle_routine_permissions).pack(side=tk.RIGHT)

        shortcuts_frame = ttk.Labelframe(actions_tab, text="Quick app shortcuts")
        shortcuts_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        action_grid = ttk.Frame(shortcuts_frame, style="Panel.TFrame")
        action_grid.pack(fill=tk.X, padx=10, pady=10)
        for label, callback in [
            ("Open Notepad", lambda: self.confirm_action("Open Notepad?", lambda: subprocess.Popen(["notepad.exe"]))),
            ("Open Calculator", lambda: self.confirm_action("Open Calculator?", lambda: subprocess.Popen(["calc.exe"]))),
            ("Open Files", lambda: self.confirm_action("Open File Explorer in your home folder?", lambda: os.startfile(str(Path.home())))),
            ("Open YouTube", lambda: self.open_anything("youtube")),
            ("Open Spotify", lambda: self.open_anything("spotify")),
            ("Open anything...", self.open_anything_dialog),
            ("Search web", self.browser_search),
            ("Search files", self.file_search),
        ]:
            ttk.Button(action_grid, text=label, command=callback).pack(side=tk.LEFT, padx=4, pady=4)

        files_frame = ttk.Labelframe(actions_tab, text="Files, folders & terminal commands")
        files_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        files_row = ttk.Frame(files_frame, style="Panel.TFrame")
        files_row.pack(fill=tk.X, padx=10, pady=(10, 6))
        self.path_input = ttk.Entry(files_row, width=42)
        self.path_input.pack(side=tk.LEFT, padx=(0, 6))
        self.path_input.insert(0, str(Path.home()))
        ttk.Button(files_row, text="List", command=lambda: threading.Thread(target=self.list_directory, args=(self.path_input.get(),), daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Button(files_row, text="Read", command=lambda: threading.Thread(target=self.read_text_file, args=(self.path_input.get(),), daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Button(files_row, text="New folder", command=lambda: threading.Thread(target=self.create_folder, args=(self.path_input.get(),), daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Button(files_row, text="🗑 Delete", style="Danger.TButton", command=lambda: threading.Thread(target=self.delete_path, args=(self.path_input.get(),), daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Button(files_row, text="Browse...", command=lambda: self.path_input.delete(0, tk.END) or self.path_input.insert(0, filedialog.askdirectory() or self.path_input.get())).pack(side=tk.LEFT, padx=2)

        command_row = ttk.Frame(files_frame, style="Panel.TFrame")
        command_row.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.command_input = ttk.Entry(command_row, width=42)
        self.command_input.pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(command_row, text="⚠ Run command", style="Danger.TButton", command=lambda: threading.Thread(target=self.run_command, args=(self.command_input.get(),), daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Label(command_row, text="Chat works too: 'run: dir', 'list files in Downloads', 'weather in Kolkata'.", style="PanelHint.TLabel", wraplength=480).pack(side=tk.LEFT, padx=10)

        utility_frame = ttk.Labelframe(actions_tab, text="Reminders, notes & utilities")
        utility_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        utility_row = ttk.Frame(utility_frame, style="Panel.TFrame")
        utility_row.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(utility_row, text="Show reminders", command=lambda: self.action_write(self.list_reminders_text())).pack(side=tk.LEFT, padx=2)
        ttk.Button(utility_row, text="Show notes", command=lambda: threading.Thread(target=self.show_notes, daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Button(utility_row, text="Organize this folder", command=lambda: threading.Thread(target=self.organize_folder, args=(self.path_input.get(),), daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Button(utility_row, text="Read clipboard", command=lambda: threading.Thread(target=self.handle_read_clipboard, daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Button(utility_row, text="Screenshot", command=lambda: threading.Thread(target=self.take_screenshot, daemon=True).start()).pack(side=tk.LEFT, padx=2)
        ttk.Label(utility_frame, text="Chat: 'remind me to X in 10 minutes', 'note: idea', 'organize Downloads', 'summarize clipboard'.", style="PanelHint.TLabel", wraplength=850).pack(anchor=tk.W, padx=10, pady=(0, 10))

        ttk.Label(actions_tab, text="Activity log", style="Section.TLabel").pack(anchor=tk.W, padx=15, pady=(2, 4))
        self.action_output = scrolledtext.ScrolledText(actions_tab, state="disabled", wrap=tk.WORD, height=12, bg="#08101e", fg="#d6efff", relief=tk.FLAT, font=("Segoe UI", 10), padx=12, pady=10)
        self.action_output.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))


        ttk.Label(coding_tab, text="Coding Workspace", style="Title.TLabel").pack(anchor=tk.W, padx=15, pady=(15, 2))
        ttk.Label(coding_tab, text="Create a small starter project — Saathi asks before writing anything.", style="Hint.TLabel").pack(anchor=tk.W, padx=15, pady=(0, 12))
        project_frame = ttk.Labelframe(coding_tab, text="New starter project")
        project_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        form = ttk.Frame(project_frame, style="Panel.TFrame")
        form.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(form, text="Project name:", style="Panel.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 8))
        self.project_name = ttk.Entry(form, width=30)
        self.project_name.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(form, text="Type:", style="Panel.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 8))
        self.project_type = tk.StringVar(value="Python CLI")
        ttk.Combobox(form, textvariable=self.project_type, values=["Python CLI", "HTML website"], state="readonly", width=27).grid(row=1, column=1, sticky=tk.W, pady=5)
        button_row = ttk.Frame(form, style="Panel.TFrame")
        button_row.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        ttk.Button(button_row, text="Choose projects folder", command=self.choose_workspace).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(button_row, text="✨ Create starter project", style="Accent.TButton", command=self.create_project).pack(side=tk.LEFT)
        self.workspace_label = ttk.Label(coding_tab, text=f"Projects folder: {self.workspace}", style="Hint.TLabel", wraplength=840)
        self.workspace_label.pack(anchor=tk.W, padx=15, pady=(2, 4))
        ttk.Label(coding_tab, text="Ask Saathi in Chat for features, then copy its code into your project. Running generated commands goes through the confirmation screen in Safe Actions.", style="Hint.TLabel", wraplength=840).pack(anchor=tk.W, padx=15)

    @staticmethod
    def style_chat_tags(widget, small: bool = False) -> None:
        speaker_font = ("Segoe UI", 9 if small else 10, "bold")
        body_font = ("Segoe UI", 9 if small else 11)
        widget.tag_configure("user_tag", foreground="#8ff4ff", font=speaker_font, spacing1=4)
        widget.tag_configure("user_body", foreground="#eaf6ff", font=body_font, lmargin1=4, lmargin2=4)
        widget.tag_configure("saathi_tag", foreground="#4de0bd", font=speaker_font, spacing1=4)
        widget.tag_configure("saathi_body", foreground="#cfe9ff", font=body_font, lmargin1=4, lmargin2=4)

    def write(self, speaker: str, text: str) -> None:
        is_user = speaker == "You"
        for widget in (self.chat, getattr(self, "dock_log", None)):
            if widget is None:
                continue
            widget.configure(state="normal")
            tag = "user_tag" if is_user else "saathi_tag"
            widget.insert(tk.END, f"{speaker}\n", tag)
            widget.insert(tk.END, f"{text}\n\n", "user_body" if is_user else "saathi_body")
            widget.configure(state="disabled")
            widget.see(tk.END)

    def action_write(self, text: str) -> None:
        self.action_output.configure(state="normal")
        self.action_output.insert(tk.END, text + "\n\n")
        self.action_output.configure(state="disabled")
        self.action_output.see(tk.END)

    def animate_orb(self, phase: int = 0) -> None:
        """A lightweight animated dashboard orb; no image asset is needed."""
        if not hasattr(self, "orb"):
            return
        pulse = (phase % 40) / 40
        radius = 26 + int(5 * abs(0.5 - pulse) * 2)
        x, y = self.orb_center
        rings = [radius + 30, radius + 18, radius + 6, radius - 5]
        for item, size in zip(self.orb_items, rings):
            self.orb.coords(item, x - size, y - size, x + size, y + size)
        self.root.after(80, lambda: self.animate_orb(phase + 1))

    def load_history(self) -> list[dict[str, str]]:
        try:
            raw_history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            return [{**message, "content": self.remove_thinking(message.get("content", ""))} for message in raw_history]
        except (OSError, json.JSONDecodeError):
            return []

    @staticmethod
    def remove_thinking(text: str) -> str:
        """Models may emit private reasoning tags; never show or preserve those."""
        visible = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()
        return Saathi.romanize_devanagari(visible)

    @staticmethod
    def _similar(a: str, b: str) -> bool:
        """True if two transcribed segments are near-duplicates (Whisper sometimes repeats a segment)."""
        a_norm, b_norm = a.lower().strip(), b.lower().strip()
        if a_norm == b_norm:
            return True
        shorter, longer = sorted([a_norm, b_norm], key=len)
        return bool(shorter) and shorter in longer and len(shorter) / max(len(longer), 1) > 0.6

    @staticmethod
    def romanize_devanagari(text: str) -> str:
        """Offline Devanagari-to-Roman conversion so the Hinglish UI stays Latin-script."""
        vowels = {"अ": "a", "आ": "aa", "इ": "i", "ई": "ee", "उ": "u", "ऊ": "oo", "ऋ": "ri", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au"}
        consonants = {"क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "ng", "च": "ch", "छ": "chh", "ज": "j", "झ": "jh", "ञ": "ny", "ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "ण": "n", "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n", "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m", "य": "y", "र": "r", "ल": "l", "व": "v", "श": "sh", "ष": "sh", "स": "s", "ह": "h", "ड़": "r", "ढ़": "rh", "क्ष": "ksh", "त्र": "tr", "ज्ञ": "gy"}
        matras = {"ा": "aa", "ि": "i", "ी": "ee", "ु": "u", "ू": "oo", "ृ": "ri", "े": "e", "ै": "ai", "ो": "o", "ौ": "au"}
        signs = {"ं": "n", "ँ": "n", "ः": "h", "़": ""}
        result: list[str] = []
        index = 0
        while index < len(text):
            char = text[index]
            if char in consonants:
                result.append(consonants[char])
                following = text[index + 1] if index + 1 < len(text) else ""
                if following in matras:
                    result.append(matras[following])
                    index += 1
                elif following == "्":
                    index += 1
                else:
                    result.append("a")
            elif char in vowels:
                result.append(vowels[char])
            elif char in matras:
                result.append(matras[char])
            elif char in signs:
                result.append(signs[char])
            elif char == "्":
                pass
            else:
                result.append(char)
            index += 1
        return "".join(result)

    def save_history(self) -> None:
        DATA_DIR.mkdir(exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(self.history[-40:], ensure_ascii=False, indent=2), encoding="utf-8")

    def clear_history(self) -> None:
        if messagebox.askyesno("Clear chat", "Delete locally saved chat history?"):
            self.history = []
            self.last_reply = ""
            self.save_history()
            self.write("Saathi", "Local chat history clear kar di.")

    def copy_last_reply(self) -> None:
        if not self.last_reply:
            self.status_var.set("Copy karne ke liye koi reply nahi hai abhi.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.last_reply)
        self.status_var.set("Last reply clipboard mein copy ho gaya.")

    def regenerate_last(self) -> None:
        if not self.history or self.history[-1]["role"] != "assistant":
            self.status_var.set("Regenerate karne ke liye pehle ek message bhejo.")
            return
        last_user_text = next((m["content"] for m in reversed(self.history[:-1]) if m["role"] == "user"), None)
        if last_user_text is None:
            return
        self.history.pop()
        self.save_history()
        model, mode = self.pick_model(last_user_text)
        self.status_var.set(f"{mode} mode — regenerating...")
        threading.Thread(target=self.ask_ollama, args=(model,), daemon=True).start()

    def send_message(self) -> None:
        text = self.message_input.get().strip()
        if not text:
            return
        self.message_input.delete(0, tk.END)
        self.process_user_text(text)

    def send_from_dock(self) -> None:
        text = self.dock_input.get().strip()
        if not text:
            return
        self.dock_input.delete(0, tk.END)
        self.process_user_text(text)

    def process_user_text(self, text: str) -> None:
        self.write("You", text)
        if self.try_handle_open_command(text):
            self.history.append({"role": "user", "content": text})
            self.history.append({"role": "assistant", "content": "(Saathi opened this on your desktop.)"})
            self.save_history()
            return
        if self.try_handle_system_command(text):
            self.history.append({"role": "user", "content": text})
            self.history.append({"role": "assistant", "content": "(Saathi handled this as a file/command action — see Safe Actions log.)"})
            self.save_history()
            return
        if self.try_handle_data_command(text):
            self.history.append({"role": "user", "content": text})
            self.history.append({"role": "assistant", "content": "(Saathi fetched this from a live data source.)"})
            self.save_history()
            return
        if self.try_handle_utility_command(text):
            self.history.append({"role": "user", "content": text})
            self.history.append({"role": "assistant", "content": "(Saathi handled this as a reminder/note/utility action.)"})
            self.save_history()
            return
        self.history.append({"role": "user", "content": text})
        self.save_history()
        model, mode = self.pick_model(text)
        self.status_var.set(f"{mode} mode — replying...")
        threading.Thread(target=self.ask_ollama, args=(model,), daemon=True).start()

    def pick_model(self, text: str) -> tuple[str, str]:
        """Use the small model for everyday talk; reserve RAM/time for hard work."""
        deep_signals = ("code", "coding", "program", "project", "bug", "error", "debug", "build", "create", "algorithm", "plan", "step by step", "detail", "research", "compare", "analyse", "analyze", "kaise banao", "kaise banau")
        fast_model = self.fast_model_var.get().strip() or FAST_MODEL
        if len(text) > 160 or any(signal in text.lower() for signal in deep_signals):
            return self.model_var.get().strip() or DEEP_MODEL, "Deep thinking"
        return fast_model, "Quick chat"

    def ask_ollama(self, model: str) -> None:
        system_prompt = QUICK_PROMPT if model == self.fast_model_var.get().strip() else SYSTEM_PROMPT
        payload = {"model": model, "stream": False, "think": False, "keep_alive": "30m", "options": {"temperature": 0.4, "num_ctx": 8192}, "messages": [{"role": "system", "content": system_prompt}, *self.history[-16:] ]}
        request = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                raw = json.loads(response.read().decode("utf-8"))
            if "message" not in raw or "content" not in raw.get("message", {}):
                self.reply_queue.put(f"Ollama ne unexpected response diya: {raw.get('error', raw)}")
                return
            answer = self.remove_thinking(raw["message"]["content"])
            if not answer:
                answer = "Mujhe koi jawaab nahi mila, phir se pucho please."
            self.history.append({"role": "assistant", "content": answer})
            self.save_history()
            self.last_reply = answer
            self.reply_queue.put(answer)
        except urllib.error.URLError:
            self.reply_queue.put("Ollama connect nahi hua. Check karo ki Ollama running hai aur selected model download hua hai.")
        except json.JSONDecodeError:
            self.reply_queue.put("Ollama se mila response samajh nahi aaya (invalid JSON).")
        except Exception as error:
            self.reply_queue.put(f"Mujhe problem mili: {error}")

    def process_queues(self) -> None:
        while not self.reply_queue.empty():
            reply = self.reply_queue.get()
            self.display_queue.put(reply)
        self.start_next_reply()
        while not self.voice_queue.empty():
            spoken = self.voice_queue.get()
            self.message_input.insert(0, spoken)
            self.send_message()
        self.root.after(200, self.process_queues)

    def start_next_reply(self) -> None:
        """Speak and type together, keeping visual pace close to 1.5× speech."""
        if self.typing_active or self.display_queue.empty():
            return
        self.typing_active = True
        self.active_reply = self.display_queue.get()
        self.reply_position = 0
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, "Saathi: ")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)
        self.speak(self.active_reply, on_started=self.type_reply_chunk)

    def type_reply_chunk(self) -> None:
        # ~27 characters/second: comparable to a 1.5× natural speaking pace.
        characters_per_tick = 3
        next_position = min(self.reply_position + characters_per_tick, len(self.active_reply))
        chunk = self.active_reply[self.reply_position:next_position]
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, chunk)
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)
        self.reply_position = next_position
        if self.reply_position < len(self.active_reply):
            self.root.after(110, self.type_reply_chunk)
            return
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, "\n\n")
        self.chat.configure(state="disabled")
        self.typing_active = False
        self.status_var.set("Ready")
        self.root.after(1, self.start_next_reply)

    def speak(self, text: str, on_started=None) -> None:
        def run() -> None:
            started = False
            try:
                import edge_tts
                import pygame
                with self.speech_lock:
                    voice_file = Path(tempfile.gettempdir()) / f"saathi_voice_{threading.get_ident()}.mp3"
                    clean_text = self.clean_for_speech(text)
                    asyncio.run(edge_tts.Communicate(clean_text, voice=TTS_VOICE, rate=TTS_RATE).save(str(voice_file)))
                    pygame.mixer.init()
                    pygame.mixer.music.load(str(voice_file))
                    pygame.mixer.music.play()
                    if on_started:
                        started = True
                        self.root.after(0, on_started)
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
            except Exception:
                # Chat continues normally if the optional online voice is unavailable.
                if on_started and not started:
                    self.root.after(0, on_started)
                return
        threading.Thread(target=run, daemon=True).start()

    @staticmethod
    def clean_for_speech(text: str) -> str:
        """Keep voice natural: emojis and code formatting belong on screen, not in speech."""
        text = re.sub(r"```.*?```", "Code screen par dikhaya gaya hai.", text, flags=re.DOTALL)
        text = re.sub(r"[`*_#>]", "", text)
        return "".join(char for char in text if unicodedata.category(char) not in {"So", "Sk", "Cs"}).strip() or ""

    def listen(self) -> None:
        if self.listening:
            return
        self.listening = True
        duration = max(3, min(15, self.record_seconds_var.get()))
        self.status_var.set(f"Listening — speak naturally in Hinglish ({duration}s)...")
        self.write("Saathi", f"Sun raha hoon — ab {duration} seconds mein bolo.")
        threading.Thread(target=self.transcribe, args=(duration,), daemon=True).start()

    def transcribe(self, duration: int = 6) -> None:
        try:
            import sounddevice as sd
            from faster_whisper import WhisperModel
            rate = 16_000
            audio = sd.rec(duration * rate, samplerate=rate, channels=1, dtype="float32")
            sd.wait()
            if self.whisper_model is None or self._loaded_voice_model != self.voice_model_var.get():
                # CPU mode avoids needing CUDA / cublas DLLs on Windows.
                self.whisper_model = WhisperModel(self.voice_model_var.get(), device="cpu", compute_type="int8")
                self._loaded_voice_model = self.voice_model_var.get()
            segments, _ = self.whisper_model.transcribe(
                audio.reshape(-1), language="en", vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 500},
                initial_prompt="Yeh ek Hinglish conversation hai — Hindi bole gaye shabdon ko bhi Roman/English letters mein hi likho, kabhi Devanagari mein mat likho. English words jaise 'website', 'code', 'app' ko sahi spelling mein likho. User ka naam Pratham hai.",
                condition_on_previous_text=False, beam_size=5, temperature=0.0,
            )
            pieces = [item.text.strip() for item in segments if item.text.strip()]
            deduped: list[str] = []
            for piece in pieces:
                if deduped and self._similar(deduped[-1], piece):
                    continue
                deduped.append(piece)
            text = " ".join(deduped).strip()
            text = self.romanize_devanagari(text)  # safety net if any Devanagari slips through anyway
            if text:
                self.reply_queue.put(f"Maine suna: “{text}”")
                self.voice_queue.put(text)
            else:
                self.reply_queue.put("Awaaz clear nahi mili. Please phir try karo.")
        except Exception as error:
            self.reply_queue.put(f"Voice input start nahi hua: {error}")
        finally:
            self.listening = False

    def confirm_action(self, question: str, action) -> None:
        if self.approve_routine(question):
            try:
                action()
                self.action_write("Approved action completed.")
            except Exception as error:
                self.action_write(f"Action could not run: {error}")

    def on_close(self) -> None:
        if pystray is not None and self.tray_icon is not None:
            self.root.withdraw()  # minimize to tray instead of quitting, so it's ready whenever you need it
        else:
            self.root.destroy()

    def show_window(self) -> None:
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.root.lift)

    def quit_app(self) -> None:
        if self.tray_icon is not None:
            self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

    def setup_tray_icon(self) -> None:
        """Runs an icon in the system tray so Saathi stays one click away without a taskbar window."""
        image = Image.new("RGB", (64, 64), "#050914")
        draw = ImageDraw.Draw(image)
        draw.ellipse((10, 10, 54, 54), outline="#3fd7ff", width=4)
        draw.ellipse((26, 26, 38, 38), fill="#71edff")
        menu = pystray.Menu(
            pystray.MenuItem("Show Saathi", lambda: self.show_window(), default=True),
            pystray.MenuItem("Quit", lambda: self.quit_app()),
        )
        self.tray_icon = pystray.Icon("saathi", image, "Saathi", menu)
        self.tray_icon.run()

    def toggle_always_on_top(self) -> None:
        self.root.attributes("-topmost", self.always_on_top_var.get())

    # ---------------------------------------------------------------- Docked mini chat
    DOCK_EXPANDED_WIDTH = 300
    DOCK_COLLAPSED_WIDTH = 30
    DOCK_HEIGHT = 460

    def build_docked_widget(self) -> None:
        """A slim panel pinned to the right edge of the screen — always there, independent
        of whether the main Saathi window is open, minimized, or in the tray."""
        self.dock = tk.Toplevel(self.root)
        self.dock.overrideredirect(True)
        self.dock.attributes("-topmost", True)
        self.dock.configure(bg="#050914")
        screen_w = self.dock.winfo_screenwidth()
        screen_h = self.dock.winfo_screenheight()
        y = max(40, (screen_h - self.DOCK_HEIGHT) // 2)
        x = screen_w - self.DOCK_EXPANDED_WIDTH
        self.dock.geometry(f"{self.DOCK_EXPANDED_WIDTH}x{self.DOCK_HEIGHT}+{x}+{y}")
        self._dock_x, self._dock_y, self._dock_screen_w = x, y, screen_w

        self.dock_panel = tk.Frame(self.dock, bg="#0a1830")
        self.dock_panel.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(self.dock_panel, bg="#0a1830")
        header.pack(fill=tk.X, padx=6, pady=(6, 2))
        tk.Label(header, text="Saathi", bg="#0a1830", fg="#71edff", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        tk.Button(header, text="Full app", command=self.show_window, bg="#0a1830", fg="#9fd3ff", relief=tk.FLAT, font=("Segoe UI", 8)).pack(side=tk.RIGHT)
        tk.Button(header, text="⟩⟩", command=self.collapse_dock, bg="#0a1830", fg="#9fd3ff", relief=tk.FLAT, font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=4)

        self.dock_log = scrolledtext.ScrolledText(self.dock_panel, state="disabled", wrap=tk.WORD, bg="#08101e", fg="#d6efff", relief=tk.FLAT, font=("Segoe UI", 9), padx=6, pady=6)
        self.style_chat_tags(self.dock_log, small=True)
        self.dock_log.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        entry_row = tk.Frame(self.dock_panel, bg="#0a1830")
        entry_row.pack(fill=tk.X, padx=6, pady=(0, 6))
        self.dock_input = tk.Entry(entry_row, bg="#08101e", fg="#eaf6ff", insertbackground="#eaf6ff", relief=tk.FLAT, font=("Segoe UI", 9))
        self.dock_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 4))
        self.dock_input.bind("<Return>", lambda event: self.send_from_dock())
        tk.Button(entry_row, text="Send", command=self.send_from_dock, bg="#1470c4", fg="white", relief=tk.FLAT, font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT)

        # A slim collapsed tab, hidden until you collapse the panel.
        self.dock_tab = tk.Frame(self.dock, bg="#1470c4", cursor="hand2")
        tk.Label(self.dock_tab, text="S\na\na\nt\nh\ni", bg="#1470c4", fg="white", font=("Segoe UI", 9, "bold")).pack(expand=True)
        self.dock_tab.bind("<Button-1>", lambda event: self.expand_dock())
        for child in self.dock_tab.winfo_children():
            child.bind("<Button-1>", lambda event: self.expand_dock())

    def collapse_dock(self) -> None:
        self.dock_expanded = False
        self.dock_panel.pack_forget()
        self.dock_tab.pack(fill=tk.BOTH, expand=True)
        self.dock.geometry(f"{self.DOCK_COLLAPSED_WIDTH}x{self.DOCK_HEIGHT}+{self._dock_screen_w - self.DOCK_COLLAPSED_WIDTH}+{self._dock_y}")

    def expand_dock(self) -> None:
        self.dock_expanded = True
        self.dock_tab.pack_forget()
        self.dock_panel.pack(fill=tk.BOTH, expand=True)
        self.dock.geometry(f"{self.DOCK_EXPANDED_WIDTH}x{self.DOCK_HEIGHT}+{self._dock_x}+{self._dock_y}")

    def toggle_routine_permissions(self) -> None:
        if self.routine_permissions:
            self.routine_permissions = False
            self.permission_status.set("Open/launch permission: ask each time")
            self.permission_button.set("Grant open & launch permission")
            self.action_write("Open/launch permission revoked for this session.")
            return
        approved = messagebox.askyesno(
            "Grant open & launch permission",
            "For this Saathi session, let Saathi open ANY website, app, or media (YouTube, Spotify, "
            "Chrome, Notepad, anything you name) without asking each time?\n\n"
            "This one permission covers opening/launching things and file-name/web searches.\n\n"
            "It does NOT cover: running terminal/shell commands, deleting or moving files, sending "
            "messages on your behalf, spending money, passwords, or USB/device control — those will "
            "always ask separately, no matter what.",
        )
        if approved:
            self.routine_permissions = True
            self.permission_status.set("Open/launch permission: granted for this session")
            self.permission_button.set("Revoke open & launch permission")
            self.action_write("Open & launch permission granted until Saathi is closed.")

    def approve_routine(self, question: str) -> bool:
        if self.routine_permissions:
            return True
        return messagebox.askyesno("Confirm action", question)

    ACTION_WORDS = ("open", "launch", "start", "play", "chalao", "chala do", "sunao", "khol", "kholo", "turn on", "put on", "pause")
    SINGLE_WORD_ACTIONS = tuple(w for w in ACTION_WORDS if " " not in w)
    SONG_WORDS = ("song", "gaana", "gana", "music", "track", "playlist", "funk", "beat", "remix", "mix", "podcast", "video")
    REFERENCE_WORDS = ("it", "that", "isse", "ise", "usko", "uska", "wahi", "vahi", "yeh gaana", "ye gaana")
    THIS_PLACE_WORDS = ("this website", "this site", "this app", "isper", "is par", "yahan", "here")
    FILLER_WORDS = {
        "a", "an", "the", "please", "some", "any", "just", "now", "and", "then", "also", "on", "in", "of",
        "kar", "karo", "do", "de", "dena", "daal", "chalao", "chala", "sunao", "khol", "kholo",
        "open", "play", "start", "launch", "put", "turn", "pause", "this", "website", "site", "app",
        "song", "gaana", "gana", "music", "track", "playlist", "it", "that", "isse", "ise", "usko", "uska",
        "yeh", "ye", "haan", "bhai", "acha", "okay", "ok", "abhi", "phir", "hi", "na", "toh", "to",
    }
    ALL_KNOWN_NAMES = tuple(sorted(set(SITE_ALIASES) | set(APP_ALIASES), key=len, reverse=True))

    def fuzzy_match_name(self, word: str) -> str | None:
        """Typo-tolerant lookup so 'spotifiy', 'youtub', 'notepade' etc. still resolve correctly."""
        matches = difflib.get_close_matches(word.lower(), self.ALL_KNOWN_NAMES, n=1, cutoff=0.75)
        return matches[0] if matches else None

    def find_known_name_in_text(self, lower_text: str) -> str | None:
        for name in self.ALL_KNOWN_NAMES:
            if re.search(rf"\b{re.escape(name)}\b", lower_text):
                return name
        for word in re.findall(r"[a-zA-Z]{3,}", lower_text):
            match = self.fuzzy_match_name(word)
            if match:
                return match
        return None

    @staticmethod
    def extract_last_suggested_title(reply: str) -> str | None:
        """Pull a song/media title the assistant previously mentioned, e.g. '*Blinding Lights* by The Weeknd'."""
        if not reply:
            return None
        match = re.search(r"[*\"“]([^*\"”]{2,60})[*\"”]", reply)
        return match.group(1).strip() if match else None

    def extract_search_phrase(self, text: str, known_name: str) -> str | None:
        """Strip action/filler words and the site name itself, leaving the actual thing to search for."""
        words = re.findall(r"[A-Za-z']+", text.lower())
        site_words = set(known_name.split())
        leftover = [w for w in words if w not in self.FILLER_WORDS and w not in site_words]
        phrase = " ".join(leftover).strip()
        return phrase if len(phrase) >= 3 else None

    def determine_search_hint(self, text: str, known_name: str) -> str | None:
        lower = text.lower()
        if any(word in lower for word in self.REFERENCE_WORDS):
            # "it"/"that" explicitly refers to something already discussed — only use a hint if we can
            # actually find what that was; guessing from leftover filler words (e.g. "yeh") is worse than nothing.
            return self.extract_last_suggested_title(self.last_reply)
        return self.extract_search_phrase(text, known_name)

    def resolve_open_target(self, raw_query: str) -> tuple[str, str]:
        """Turn a free-form request into (kind, target) where kind is 'url', 'app', or 'search'."""
        query = raw_query.strip().lower()
        query = re.sub(r"^(open|launch|start|play)\s+", "", query).strip()
        query = re.sub(r"\s+(app|website|please|karo|kholo|karke do)$", "", query).strip()
        for name, url in SITE_ALIASES.items():
            if query == name or query.startswith(name + " ") or name in query.split():
                return "url", url
        for name, exe in APP_ALIASES.items():
            if query == name:
                return "app", exe
        fuzzy = self.fuzzy_match_name(query) if " " not in query else None
        if fuzzy:
            if fuzzy in SITE_ALIASES:
                return "url", SITE_ALIASES[fuzzy]
            if fuzzy in APP_ALIASES:
                return "app", APP_ALIASES[fuzzy]
        if re.match(r"^https?://", raw_query.strip()):
            return "url", raw_query.strip()
        if "." in query and " " not in query:
            return "url", "https://" + query
        return "search", raw_query.strip()

    def open_anything(self, raw_query: str, search_hint: str | None = None) -> None:
        """One entry point that opens websites, installed apps, or falls back to a web search."""
        if not raw_query.strip():
            return
        kind, target = self.resolve_open_target(raw_query)
        if kind == "url":
            if raw_query.strip().lower() in SITE_ALIASES:
                self.last_opened_site = raw_query.strip().lower()
            if search_hint and "spotify" in target:
                target = target.rstrip("/") + "/search/" + urllib.parse.quote(search_hint)
            elif search_hint and "youtube" in target:
                target = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(search_hint)
            if not self.approve_routine(f"Open this in your browser?\n{target}"):
                self.action_write("Cancelled: permission not given.")
                return
            webbrowser.open(target)
            self.action_write(f"Opened: {target}")
            if search_hint:
                self.reply_queue.put(f"'{search_hint}' ka search khol diya — pehla result play kar do.")
            else:
                self.reply_queue.put(f"Kholi diya: {target}")
        elif kind == "app":
            if not self.approve_routine(f"Launch this app?\n{target}"):
                self.action_write("Cancelled: permission not given.")
                return
            try:
                if target.startswith("ms-settings:"):
                    os.startfile(target)
                else:
                    subprocess.Popen(["cmd", "/c", "start", "", target], shell=False)
                self.action_write(f"Launched: {target}")
                self.reply_queue.put(f"{raw_query.strip()} khol diya.")
            except Exception as error:
                self.action_write(f"Could not launch '{target}': {error}")
                self.reply_queue.put(f"'{raw_query.strip()}' open nahi kar paya: {error}")
        else:
            if not self.approve_routine(f"Search the web for:\n{target}"):
                self.action_write("Cancelled: permission not given.")
                return
            webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(target))
            self.action_write(f"Searched the web for: {target}")
            self.reply_queue.put(f"'{target}' ke liye web search khol diya.")

    def try_handle_open_command(self, text: str) -> bool:
        """Detect open/play/launch intent ANYWHERE in the sentence — not just as the first word —
        so 'And the Brazilian funk on Spotify' or 'Now on this website, play X' are caught."""
        stripped = text.strip()
        lower = stripped.lower()
        has_action = any(word in lower for word in self.ACTION_WORDS)
        if not has_action:
            # tolerate a mistyped/mis-transcribed verb, e.g. "opne spotify"
            has_action = any(
                difflib.get_close_matches(word, self.SINGLE_WORD_ACTIONS, n=1, cutoff=0.7)
                for word in re.findall(r"[a-zA-Z]{3,}", lower)
            )
        has_song_word = any(word in lower for word in self.SONG_WORDS)
        has_this_place = any(word in lower for word in self.THIS_PLACE_WORDS)
        if not (has_action or has_song_word or has_this_place):
            return False
        known_name = self.find_known_name_in_text(lower)
        if not known_name and has_this_place and self.last_opened_site:
            known_name = self.last_opened_site  # "play X on this website" referring back to the tab we just opened
        if not known_name:
            return False  # e.g. "what is spotify" — no action target at all
        search_hint = self.determine_search_hint(stripped, known_name)
        self.write("Saathi", "Theek hai, kholta hoon...")
        threading.Thread(target=self.open_anything, args=(known_name, search_hint), daemon=True).start()
        return True

    def browser_search(self) -> None:
        query = simpledialog.askstring("Web search", "What should I search for?")
        if query and self.approve_routine(f"Open browser search for:\n{query}"):
            webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(query))
            self.action_write(f"Opened browser search: {query}")

    def open_anything_dialog(self) -> None:
        query = simpledialog.askstring("Open anything", "What should Saathi open? (e.g. YouTube, Spotify, Notepad, a website)")
        if query:
            self.open_anything(query)

    def file_search(self) -> None:
        query = simpledialog.askstring("Search files", "File or folder name to look for:")
        if not query:
            return
        if not self.approve_routine(f"Search your home folder for names containing '{query}'?"):
            return
        results = []
        try:
            for path in Path.home().rglob(f"*{query}*"):
                results.append(str(path))
                if len(results) >= 30:
                    break
            self.action_write("Found:\n" + ("\n".join(results) if results else "No matching files."))
        except OSError as error:
            self.action_write(f"Search stopped: {error}")

    # ---------------------------------------------------------------- Files & folders
    def resolve_path(self, raw_path: str) -> Path:
        raw_path = raw_path.strip().strip('"').strip("'")
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            path = self.files_root / path
        return path

    @staticmethod
    def is_protected_path(path: Path) -> bool:
        normalized = str(path).lower()
        return any(normalized.startswith(prefix) for prefix in PROTECTED_PATH_PREFIXES)

    def list_directory(self, raw_path: str) -> None:
        path = self.resolve_path(raw_path)
        if not self.approve_routine(f"List contents of this folder?\n{path}"):
            self.action_write("Cancelled: permission not given.")
            return
        try:
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
            lines = [f"{'FILE' if e.is_file() else 'DIR '}  {e.name}" for e in entries[:200]]
            listing = "\n".join(lines) if lines else "(empty folder)"
            self.action_write(f"Contents of {path}:\n{listing}")
            self.reply_queue.put(f"'{path.name or path}' mein {len(entries)} items hain. Details Safe Actions log mein hain.")
        except FileNotFoundError:
            self.action_write(f"Folder not found: {path}")
            self.reply_queue.put(f"'{path}' naam ka folder nahi mila.")
        except OSError as error:
            self.action_write(f"Could not list '{path}': {error}")

    def read_text_file(self, raw_path: str) -> None:
        path = self.resolve_path(raw_path)
        if not self.approve_routine(f"Read this file?\n{path}"):
            self.action_write("Cancelled: permission not given.")
            return
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            truncated = content if len(content) <= 4000 else content[:4000] + "\n...[truncated]"
            self.action_write(f"Contents of {path}:\n{truncated}")
            self.reply_queue.put(f"'{path.name}' padh liya — poora content Safe Actions log mein hai.")
        except FileNotFoundError:
            self.action_write(f"File not found: {path}")
            self.reply_queue.put(f"'{path}' naam ki file nahi mili.")
        except OSError as error:
            self.action_write(f"Could not read '{path}': {error}")

    def write_text_file(self, raw_path: str, content: str, append: bool = False) -> None:
        path = self.resolve_path(raw_path)
        if self.is_protected_path(path):
            self.action_write(f"Refused: '{path}' is inside a protected system folder.")
            self.reply_queue.put("Yeh system folder protected hai, wahan file nahi bana sakta.")
            return
        question = f"{'Append to' if append else 'Create/overwrite'} this file?\n{path}"
        if not self.approve_routine(question):
            self.action_write("Cancelled: permission not given.")
            return
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a" if append else "w", encoding="utf-8") as handle:
                handle.write(content)
            self.action_write(f"{'Appended to' if append else 'Wrote'}: {path}")
            self.reply_queue.put(f"'{path.name}' {'update' if append else 'create'} kar diya.")
        except OSError as error:
            self.action_write(f"Could not write '{path}': {error}")
            self.reply_queue.put(f"'{path}' likh nahi paya: {error}")

    def create_folder(self, raw_path: str) -> None:
        path = self.resolve_path(raw_path)
        if self.is_protected_path(path):
            self.action_write(f"Refused: '{path}' is inside a protected system folder.")
            return
        if not self.approve_routine(f"Create this folder?\n{path}"):
            self.action_write("Cancelled: permission not given.")
            return
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.action_write(f"Created folder: {path}")
            self.reply_queue.put(f"Folder '{path.name}' bana diya.")
        except OSError as error:
            self.action_write(f"Could not create folder '{path}': {error}")

    def delete_path(self, raw_path: str) -> None:
        """Deletes always require explicit confirmation, no matter what permission is granted."""
        path = self.resolve_path(raw_path)
        if self.is_protected_path(path):
            self.action_write(f"Refused: '{path}' is inside a protected system folder.")
            self.reply_queue.put("Yeh protected system folder hai, delete nahi kar sakta.")
            return
        if not path.exists():
            self.action_write(f"Nothing to delete at: {path}")
            self.reply_queue.put(f"'{path}' waha kuchh mila hi nahi.")
            return
        note = " (goes to Recycle Bin)" if send2trash else " (PERMANENT — send2trash not installed)"
        if not messagebox.askyesno("Confirm delete", f"Delete this{note}?\n{path}"):
            self.action_write("Cancelled: delete not confirmed.")
            return
        try:
            if send2trash:
                send2trash(str(path))
            elif path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            self.action_write(f"Deleted: {path}")
            self.reply_queue.put(f"'{path.name}' delete kar diya.")
        except OSError as error:
            self.action_write(f"Could not delete '{path}': {error}")

    def move_path(self, raw_src: str, raw_dst: str) -> None:
        src, dst = self.resolve_path(raw_src), self.resolve_path(raw_dst)
        if self.is_protected_path(src) or self.is_protected_path(dst):
            self.action_write("Refused: move involves a protected system folder.")
            return
        if not messagebox.askyesno("Confirm move/rename", f"Move/rename:\n{src}\nto\n{dst}"):
            self.action_write("Cancelled: move not confirmed.")
            return
        try:
            shutil.move(str(src), str(dst))
            self.action_write(f"Moved: {src} -> {dst}")
            self.reply_queue.put(f"'{src.name}' ko move kar diya.")
        except OSError as error:
            self.action_write(f"Could not move '{src}': {error}")

    # ---------------------------------------------------------------- Terminal commands
    def run_command(self, command: str) -> None:
        """Always shows the exact command and asks first — even with routine permission granted."""
        lower = command.lower()
        if any(re.search(pattern, lower) for pattern in DANGEROUS_COMMAND_PATTERNS):
            self.action_write(f"Refused: '{command}' matches a blocked destructive pattern.")
            self.reply_queue.put("Yeh command bahut destructive hai, main ise run nahi karunga.")
            return
        if not messagebox.askyesno("Confirm command", f"Run this command in a shell?\n\n{command}"):
            self.action_write("Cancelled: command not confirmed.")
            return
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60, cwd=str(self.files_root))
            output = (result.stdout or "") + (result.stderr or "")
            output = output.strip() or "(no output)"
            truncated = output if len(output) <= 3000 else output[:3000] + "\n...[truncated]"
            self.action_write(f"Ran: {command}\nExit code: {result.returncode}\n{truncated}")
            self.reply_queue.put(f"Command chala diya (exit code {result.returncode}). Output Safe Actions log mein hai.")
        except subprocess.TimeoutExpired:
            self.action_write(f"Command timed out after 60s: {command}")
            self.reply_queue.put("Command 60 second mein complete nahi hua, timeout ho gaya.")
        except OSError as error:
            self.action_write(f"Could not run '{command}': {error}")

    SYSTEM_COMMAND_PATTERNS = (
        (re.compile(r"^(?:list|show)\s+files?\s+(?:in|inside|of)\s+(.+)$", re.I), "list"),
        (re.compile(r"^read\s+file\s+(.+)$", re.I), "read"),
        (re.compile(r"^(?:create|make)\s+(?:a\s+)?folder\s+(?:called\s+|named\s+)?(.+)$", re.I), "mkdir"),
        (re.compile(r"^(?:create|make)\s+(?:a\s+)?file\s+(.+?)(?:\s+with\s+content[:\s]+(.*))?$", re.I), "mkfile"),
        (re.compile(r"^append\s+(?:to\s+)?(.+?)\s+with[:\s]+(.*)$", re.I), "append"),
        (re.compile(r"^delete\s+(?:file|folder)?\s*(.+)$", re.I), "delete"),
        (re.compile(r"^(?:move|rename)\s+(.+?)\s+to\s+(.+)$", re.I), "move"),
        (re.compile(r"^(?:run|execute)[:\s]+(.+)$", re.I), "run"),
    )

    def try_handle_system_command(self, text: str) -> bool:
        """Parse explicit file/folder/command instructions typed in chat, e.g.
        'list files in Downloads', 'create file notes.txt with content: hello',
        'delete old_report.pdf', 'run: python script.py'."""
        stripped = text.strip()
        for pattern, kind in self.SYSTEM_COMMAND_PATTERNS:
            match = pattern.match(stripped)
            if not match:
                continue
            if kind == "list":
                threading.Thread(target=self.list_directory, args=(match.group(1),), daemon=True).start()
            elif kind == "read":
                threading.Thread(target=self.read_text_file, args=(match.group(1),), daemon=True).start()
            elif kind == "mkdir":
                threading.Thread(target=self.create_folder, args=(match.group(1),), daemon=True).start()
            elif kind == "mkfile":
                path, content = match.group(1), match.group(2) or ""
                threading.Thread(target=self.write_text_file, args=(path, content), daemon=True).start()
            elif kind == "append":
                threading.Thread(target=self.write_text_file, args=(match.group(1), match.group(2), True), daemon=True).start()
            elif kind == "delete":
                threading.Thread(target=self.delete_path, args=(match.group(1),), daemon=True).start()
            elif kind == "move":
                threading.Thread(target=self.move_path, args=(match.group(1), match.group(2)), daemon=True).start()
            elif kind == "run":
                threading.Thread(target=self.run_command, args=(match.group(1),), daemon=True).start()
            self.write("Saathi", "Theek hai, kar raha hoon...")
            return True
        return False

    # ---------------------------------------------------------------- Live data / free APIs
    @staticmethod
    def fetch_json(url: str, headers: dict | None = None) -> dict | list | None:
        try:
            request = urllib.request.Request(url, headers=headers or {"Accept": "application/json", "User-Agent": "Saathi/1.0"})
            with urllib.request.urlopen(request, timeout=8) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception:
            return None

    def handle_weather(self, city: str) -> None:
        geo = self.fetch_json(API_ENDPOINTS["geocode"].format(query=urllib.parse.quote(city)))
        results = (geo or {}).get("results") if isinstance(geo, dict) else None
        if not results:
            self.reply_queue.put(f"'{city}' ke liye location nahi mili.")
            return
        place = results[0]
        weather = self.fetch_json(API_ENDPOINTS["weather"].format(lat=place["latitude"], lon=place["longitude"]))
        current = (weather or {}).get("current_weather") if isinstance(weather, dict) else None
        if not current:
            self.reply_queue.put(f"'{city}' ka weather fetch nahi ho paya.")
            return
        self.reply_queue.put(
            f"{place.get('name', city)} mein abhi {current['temperature']}°C hai, wind speed {current['windspeed']} km/h."
        )

    def handle_currency(self, amount: str, base: str, target: str) -> None:
        data = self.fetch_json(API_ENDPOINTS["currency"].format(amount=amount, base=base.upper(), target=target.upper()))
        rates = (data or {}).get("rates") if isinstance(data, dict) else None
        if not rates or target.upper() not in rates:
            self.reply_queue.put(f"Currency convert nahi ho paya {base.upper()} se {target.upper()}.")
            return
        self.reply_queue.put(f"{amount} {base.upper()} = {rates[target.upper()]:.2f} {target.upper()}")

    def handle_define(self, word: str) -> None:
        data = self.fetch_json(API_ENDPOINTS["define"].format(query=urllib.parse.quote(word)))
        if not isinstance(data, list) or not data:
            self.reply_queue.put(f"'{word}' ki definition nahi mili.")
            return
        try:
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            self.reply_queue.put(f"{word}: {meaning}")
        except (KeyError, IndexError):
            self.reply_queue.put(f"'{word}' ki definition nahi mili.")

    def handle_wiki(self, term: str) -> None:
        data = self.fetch_json(API_ENDPOINTS["wiki"].format(query=urllib.parse.quote(term.replace(' ', '_'))))
        extract = (data or {}).get("extract") if isinstance(data, dict) else None
        if not extract:
            self.reply_queue.put(f"'{term}' ke baare mein kuchh nahi mila Wikipedia par.")
            return
        self.reply_queue.put(extract if len(extract) < 600 else extract[:600] + "...")

    def handle_trivia(self) -> None:
        data = self.fetch_json(API_ENDPOINTS["trivia"])
        results = (data or {}).get("results") if isinstance(data, dict) else None
        if not results:
            self.reply_queue.put("Trivia fetch nahi hui, phir try karo.")
            return
        item = results[0]
        self.reply_queue.put(f"{html.unescape(item['question'])}\n(Answer: {html.unescape(item['correct_answer'])})")

    def handle_joke(self) -> None:
        data = self.fetch_json(API_ENDPOINTS["joke"])
        if isinstance(data, dict) and "setup" in data:
            self.reply_queue.put(f"{data['setup']} ... {data['punchline']} 😄")
        else:
            self.reply_queue.put("Joke fetch nahi hui, phir try karo.")

    def handle_quote(self) -> None:
        data = self.fetch_json(API_ENDPOINTS["quote"])
        if isinstance(data, list) and data:
            self.reply_queue.put(f'"{data[0]["q"]}" — {data[0]["a"]}')
        else:
            self.reply_queue.put("Quote fetch nahi hui, phir try karo.")

    def handle_country(self, name: str) -> None:
        data = self.fetch_json(API_ENDPOINTS["country"].format(query=urllib.parse.quote(name)))
        if not isinstance(data, list) or not data:
            self.reply_queue.put(f"'{name}' ke baare mein info nahi mili.")
            return
        info = data[0]
        capital = ", ".join(info.get("capital", []) or ["N/A"])
        population = info.get("population", "N/A")
        region = info.get("region", "N/A")
        self.reply_queue.put(f"{info.get('name', {}).get('common', name)}: capital {capital}, region {region}, population {population:,}" if isinstance(population, int) else f"{name}: capital {capital}, region {region}")

    def handle_advice(self) -> None:
        data = self.fetch_json(API_ENDPOINTS["advice"])
        slip = (data or {}).get("slip") if isinstance(data, dict) else None
        self.reply_queue.put(slip.get("advice") if slip else "Advice fetch nahi hui, phir try karo.")

    LANGUAGE_CODES = {
        "hindi": "hi", "english": "en", "spanish": "es", "french": "fr", "german": "de",
        "japanese": "ja", "chinese": "zh", "arabic": "ar", "russian": "ru", "portuguese": "pt",
        "tamil": "ta", "telugu": "te", "bengali": "bn", "marathi": "mr", "gujarati": "gu",
        "kannada": "kn", "punjabi": "pa", "urdu": "ur", "korean": "ko", "italian": "it",
    }

    def handle_translate(self, phrase: str, target_lang: str) -> None:
        target_code = self.LANGUAGE_CODES.get(target_lang.lower(), target_lang.lower()[:2])
        url = API_ENDPOINTS["translate"].format(query=urllib.parse.quote(phrase), source="en", target=target_code)
        data = self.fetch_json(url)
        translated = (data or {}).get("responseData", {}).get("translatedText") if isinstance(data, dict) else None
        if not translated:
            self.reply_queue.put(f"'{phrase}' ka {target_lang} translation nahi mila.")
            return
        self.reply_queue.put(f"{target_lang} mein: {translated}")

    def handle_my_ip(self) -> None:
        data = self.fetch_json(API_ENDPOINTS["myip"])
        ip = (data or {}).get("ip") if isinstance(data, dict) else None
        self.reply_queue.put(f"Aapka public IP hai: {ip}" if ip else "IP fetch nahi hui, phir try karo.")

    def handle_top_news(self) -> None:
        ids = self.fetch_json(API_ENDPOINTS["hn_top"])
        if not isinstance(ids, list) or not ids:
            self.reply_queue.put("News fetch nahi hui, phir try karo.")
            return
        lines = []
        for story_id in ids[:5]:
            item = self.fetch_json(API_ENDPOINTS["hn_item"].format(item_id=story_id))
            if isinstance(item, dict) and item.get("title"):
                lines.append(f"- {item['title']}")
        self.reply_queue.put("Top tech headlines:\n" + "\n".join(lines) if lines else "News fetch nahi hui.")

    @staticmethod
    def handle_coin_flip() -> str:
        return random.choice(["Heads", "Tails"])

    @staticmethod
    def handle_dice_roll(sides: int = 6) -> int:
        return random.randint(1, max(2, sides))

    DATA_COMMAND_PATTERNS = (
        (re.compile(r"weather\s+(?:in|for|of)\s+(.+)", re.I), "weather"),
        (re.compile(r"convert\s+([\d.]+)\s*([a-zA-Z]{3})\s+(?:to|in)\s+([a-zA-Z]{3})", re.I), "currency"),
        (re.compile(r"([\d.]+)\s*([a-zA-Z]{3})\s+to\s+([a-zA-Z]{3})\b", re.I), "currency"),
        (re.compile(r"(?:define|meaning of)\s+([a-zA-Z\- ]{2,30})", re.I), "define"),
        (re.compile(r"^(?:wiki|wikipedia)\s+(.+)$", re.I), "wiki"),
        (re.compile(r"^who\s+is\s+(.+?)\??$", re.I), "wiki"),
        (re.compile(r"\btrivia\b", re.I), "trivia"),
        (re.compile(r"\b(?:tell me a joke|joke sunao|ek joke)\b", re.I), "joke"),
        (re.compile(r"\b(?:quote|motivation)\b", re.I), "quote"),
        (re.compile(r"(?:info about|tell me about)\s+country\s+(.+)", re.I), "country"),
        (re.compile(r"\b(?:advice|suggestion do)\b", re.I), "advice"),
        (re.compile(r"translate\s+(.+?)\s+(?:to|in)\s+([a-zA-Z]+)$", re.I), "translate"),
        (re.compile(r"\b(?:my ip|mera ip)\b", re.I), "myip"),
        (re.compile(r"\b(?:top news|headlines|news sunao)\b", re.I), "news"),
        (re.compile(r"\b(?:flip a coin|coin flip|sikka uchalo)\b", re.I), "coinflip"),
        (re.compile(r"\broll (?:a )?dice(?:\s+with\s+(\d+)\s+sides)?\b", re.I), "diceroll"),
    )

    def try_handle_data_command(self, text: str) -> bool:
        """Route factual/live-data questions to real free APIs instead of letting the local model guess."""
        stripped = text.strip()
        for pattern, kind in self.DATA_COMMAND_PATTERNS:
            match = pattern.search(stripped)
            if not match:
                continue
            if kind == "coinflip":
                self.reply_queue.put(f"{self.handle_coin_flip()}!")
                return True
            if kind == "diceroll":
                sides = int(match.group(1)) if match.group(1) else 6
                self.reply_queue.put(f"🎲 {self.handle_dice_roll(sides)} (out of {sides})")
                return True
            self.write("Saathi", "Ek second, fetch kar raha hoon...")
            if kind == "weather":
                threading.Thread(target=self.handle_weather, args=(match.group(1).strip(),), daemon=True).start()
            elif kind == "currency":
                threading.Thread(target=self.handle_currency, args=(match.group(1), match.group(2), match.group(3)), daemon=True).start()
            elif kind == "define":
                threading.Thread(target=self.handle_define, args=(match.group(1).strip(),), daemon=True).start()
            elif kind == "wiki":
                threading.Thread(target=self.handle_wiki, args=(match.group(1).strip(),), daemon=True).start()
            elif kind == "trivia":
                threading.Thread(target=self.handle_trivia, daemon=True).start()
            elif kind == "joke":
                threading.Thread(target=self.handle_joke, daemon=True).start()
            elif kind == "quote":
                threading.Thread(target=self.handle_quote, daemon=True).start()
            elif kind == "country":
                threading.Thread(target=self.handle_country, args=(match.group(1).strip(),), daemon=True).start()
            elif kind == "advice":
                threading.Thread(target=self.handle_advice, daemon=True).start()
            elif kind == "translate":
                threading.Thread(target=self.handle_translate, args=(match.group(1).strip(), match.group(2).strip()), daemon=True).start()
            elif kind == "myip":
                threading.Thread(target=self.handle_my_ip, daemon=True).start()
            elif kind == "news":
                threading.Thread(target=self.handle_top_news, daemon=True).start()
            return True
        return False

    # ---------------------------------------------------------------- Reminders
    def load_reminders(self) -> None:
        try:
            self.reminders = json.loads(self.reminders_file.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            self.reminders = []

    def save_reminders(self) -> None:
        self.reminders_file.parent.mkdir(parents=True, exist_ok=True)
        self.reminders_file.write_text(json.dumps(self.reminders, indent=2), encoding="utf-8")

    @staticmethod
    def parse_reminder_time(text: str) -> datetime | None:
        text = text.strip().lower()
        now = datetime.now()
        match = re.match(r"in\s+(\d+)\s*(minute|min|hour|hr)s?$", text)
        if match:
            amount, unit = int(match.group(1)), match.group(2)
            delta = timedelta(hours=amount) if unit.startswith("hr") or unit.startswith("hour") else timedelta(minutes=amount)
            return now + delta
        match = re.match(r"(?:tomorrow\s+)?at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$", text)
        if match:
            hour, minute, meridiem = int(match.group(1)), int(match.group(2) or 0), match.group(3)
            if meridiem == "pm" and hour < 12:
                hour += 12
            if meridiem == "am" and hour == 12:
                hour = 0
            candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if text.startswith("tomorrow") or candidate <= now:
                candidate += timedelta(days=1)
            return candidate
        return None

    def add_reminder(self, message: str, when: datetime) -> None:
        self.reminders.append({"text": message, "when": when.isoformat()})
        self.save_reminders()
        self.reply_queue.put(f"Theek hai, '{message}' ke liye reminder set kar diya — {when.strftime('%d %b, %I:%M %p')}.")

    def reminder_checker_loop(self) -> None:
        while True:
            now = datetime.now()
            due = [r for r in self.reminders if datetime.fromisoformat(r["when"]) <= now]
            if due:
                for reminder in due:
                    self.reminders.remove(reminder)
                    self.root.after(0, lambda r=reminder: messagebox.showinfo("Saathi reminder", r["text"]))
                    self.reply_queue.put(f"⏰ Reminder: {reminder['text']}")
                    threading.Thread(target=self.speak, args=(reminder["text"],), daemon=True).start()
                self.save_reminders()
            threading.Event().wait(20)

    def list_reminders_text(self) -> str:
        if not self.reminders:
            return "Koi reminder set nahi hai abhi."
        lines = [f"{i+1}. {r['text']} — {datetime.fromisoformat(r['when']).strftime('%d %b, %I:%M %p')}" for i, r in enumerate(self.reminders)]
        return "\n".join(lines)

    # ---------------------------------------------------------------- Notes / journal
    @property
    def notes_file(self) -> Path:
        return self.workspace / "notes.md"

    def add_note(self, text: str) -> None:
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        self.notes_file.parent.mkdir(parents=True, exist_ok=True)
        with self.notes_file.open("a", encoding="utf-8") as handle:
            handle.write(f"- **{timestamp}** — {text}\n")
        self.reply_queue.put("Note save kar diya.")

    def show_notes(self) -> None:
        if not self.notes_file.exists():
            self.reply_queue.put("Abhi koi notes nahi hain.")
            return
        content = self.notes_file.read_text(encoding="utf-8")
        self.action_write(f"Notes ({self.notes_file}):\n{content}")
        self.reply_queue.put("Saare notes Safe Actions log mein dikha diye.")

    # ---------------------------------------------------------------- Folder auto-organize
    ORGANIZE_CATEGORIES = {
        "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"},
        "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".csv"},
        "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
        "Music": {".mp3", ".wav", ".flac", ".m4a"},
        "Installers": {".exe", ".msi"},
        "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    }

    def organize_folder(self, raw_path: str) -> None:
        path = self.resolve_path(raw_path)
        if self.is_protected_path(path):
            self.action_write(f"Refused: '{path}' is a protected system folder.")
            return
        if not path.is_dir():
            self.reply_queue.put(f"'{path}' ek valid folder nahi hai.")
            return
        files = [f for f in path.iterdir() if f.is_file()]
        if not messagebox.askyesno("Organize folder", f"Sort {len(files)} files in\n{path}\ninto category subfolders (Images, Documents, Videos, Music, Installers, Archives, Others)?"):
            self.action_write("Cancelled: organize not confirmed.")
            return
        moved = 0
        for file in files:
            category = next((name for name, exts in self.ORGANIZE_CATEGORIES.items() if file.suffix.lower() in exts), "Others")
            destination_folder = path / category
            destination_folder.mkdir(exist_ok=True)
            try:
                shutil.move(str(file), str(destination_folder / file.name))
                moved += 1
            except OSError:
                continue
        self.action_write(f"Organized {moved} files in {path} into category folders.")
        self.reply_queue.put(f"'{path.name}' mein {moved} files organize kar diye categories mein.")

    # ---------------------------------------------------------------- Clipboard & screenshots
    def read_clipboard(self) -> str | None:
        try:
            return self.root.clipboard_get()
        except tk.TclError:
            return None

    def handle_read_clipboard(self) -> None:
        content = self.read_clipboard()
        if not content:
            self.reply_queue.put("Clipboard khali hai ya text nahi hai usmein.")
            return
        preview = content if len(content) < 500 else content[:500] + "..."
        self.action_write(f"Clipboard content:\n{preview}")
        self.reply_queue.put("Clipboard content Safe Actions log mein hai.")

    def handle_summarize_clipboard(self) -> None:
        content = self.read_clipboard()
        if not content or not content.strip():
            self.reply_queue.put("Clipboard khali hai, summarize karne ke liye kuchh nahi mila.")
            return
        instruction = f"Summarize this in a few short lines, in Hinglish:\n\n{content[:3000]}"
        self.history.append({"role": "user", "content": instruction})
        self.save_history()
        model, _mode = self.pick_model(instruction)
        threading.Thread(target=self.ask_ollama, args=(model,), daemon=True).start()

    def take_screenshot(self) -> None:
        if ImageGrab is None:
            self.reply_queue.put("Screenshot feature ke liye Pillow install nahi hai.")
            return
        if not self.approve_routine("Take a screenshot and save it to your Projects folder?"):
            self.action_write("Cancelled: permission not given.")
            return
        filename = self.workspace / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        try:
            ImageGrab.grab().save(filename)
            self.action_write(f"Screenshot saved: {filename}")
            self.reply_queue.put(f"Screenshot le liya: {filename.name}")
        except Exception as error:
            self.action_write(f"Screenshot failed: {error}")

    UTILITY_COMMAND_PATTERNS = (
        (re.compile(r"^remind me to\s+(.+?)\s+(in\s+\d+\s*(?:minute|min|hour|hr)s?|(?:tomorrow\s+)?at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?)$", re.I), "remind"),
        (re.compile(r"^(?:list|show)\s+reminders$", re.I), "list_reminders"),
        (re.compile(r"^note[:\s]+(.+)$", re.I), "note"),
        (re.compile(r"^(?:show|read)\s+notes$", re.I), "show_notes"),
        (re.compile(r"^organize\s+(?:folder\s+)?(.+)$", re.I), "organize"),
        (re.compile(r"^read\s+clipboard$", re.I), "read_clipboard"),
        (re.compile(r"^summari[sz]e\s+clipboard$", re.I), "summarize_clipboard"),
        (re.compile(r"^(?:take a )?screenshot$", re.I), "screenshot"),
    )

    def try_handle_utility_command(self, text: str) -> bool:
        stripped = text.strip()
        for pattern, kind in self.UTILITY_COMMAND_PATTERNS:
            match = pattern.match(stripped)
            if not match:
                continue
            if kind == "remind":
                when = self.parse_reminder_time(match.group(2))
                if when is None:
                    self.write("Saathi", "Time samajh nahi aaya — 'in 10 minutes' ya 'at 6pm' jaisa try karo.")
                    return True
                threading.Thread(target=self.add_reminder, args=(match.group(1).strip(), when), daemon=True).start()
            elif kind == "list_reminders":
                self.write("Saathi", self.list_reminders_text())
                return True
            elif kind == "note":
                threading.Thread(target=self.add_note, args=(match.group(1).strip(),), daemon=True).start()
            elif kind == "show_notes":
                threading.Thread(target=self.show_notes, daemon=True).start()
            elif kind == "organize":
                threading.Thread(target=self.organize_folder, args=(match.group(1).strip(),), daemon=True).start()
            elif kind == "read_clipboard":
                threading.Thread(target=self.handle_read_clipboard, daemon=True).start()
            elif kind == "summarize_clipboard":
                threading.Thread(target=self.handle_summarize_clipboard, daemon=True).start()
            elif kind == "screenshot":
                threading.Thread(target=self.take_screenshot, daemon=True).start()
            self.write("Saathi", "Theek hai, kar raha hoon...")
            return True
        return False

    def choose_workspace(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.workspace)
        if selected:
            self.workspace = Path(selected)
            self.workspace_label.config(text=f"Projects folder: {self.workspace}")

    def create_project(self) -> None:
        name = self.project_name.get().strip()
        if not name or not name.replace("-", "").replace("_", "").isalnum():
            messagebox.showerror("Project name", "Use letters, numbers, hyphens, or underscores only.")
            return
        destination = self.workspace / name
        if destination.exists():
            messagebox.showerror("Already exists", f"This folder already exists:\n{destination}")
            return
        if not self.approve_routine(f"Create a {self.project_type.get()} starter project here?\n{destination}"):
            return
        destination.mkdir(parents=True)
        if self.project_type.get() == "Python CLI":
            (destination / "main.py").write_text('''def main():\n    print("Namaste from your new project!")\n\n\nif __name__ == "__main__":\n    main()\n''', encoding="utf-8")
            (destination / "README.md").write_text(f"# {name}\n\nRun with: `py main.py`\n", encoding="utf-8")
        else:
            (destination / "index.html").write_text(f"""<!doctype html>\n<html><head><meta charset=\"utf-8\"><title>{name}</title></head>\n<body><h1>Namaste!</h1><p>Your new website is ready.</p></body></html>\n""", encoding="utf-8")
        self.project_name.delete(0, tk.END)
        messagebox.showinfo("Project created", f"Created:\n{destination}")


if __name__ == "__main__":
    app_window = tk.Tk()
    Saathi(app_window)
    app_window.mainloop()
