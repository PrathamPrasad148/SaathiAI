"""Saathi: Agentic Hinglish desktop coding assistant & personal companion."""
from __future__ import annotations

import asyncio
import difflib
import html
import json
import os
import queue
import random
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
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
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

try:
    from send2trash import send2trash
except ImportError:
    send2trash = None

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None


# ─── JARVIS Color Palette ──────────────────────────────────────────────
COLOR_BG = "#0a0a0f"
COLOR_PANEL = "#12121f"
COLOR_ACCENT = "#00ff88"
COLOR_ACCENT_DIM = "#00cc6a"
COLOR_TEXT = "#e8e8f0"
COLOR_TEXT_MUTED = "#8a8aa0"
COLOR_ORB = "#00ff88"
COLOR_ORB_GLOW = "#00ff8840"
COLOR_HEADER = "#0f0f14"
COLOR_BORDER = "#2a2a3a"
COLOR_TOOL = "#38bdf8"
COLOR_SUCCESS = "#00ff88"
COLOR_WARNING = "#ffaa00"
COLOR_ERROR = "#ff5555"

APP_DIR = Path(__file__).parent.resolve()
DATA_DIR = APP_DIR / "data"
PROJECTS_DIR = APP_DIR / "Projects"
HISTORY_FILE = DATA_DIR / "history.json"
REMINDERS_FILE = DATA_DIR / "reminders.json"
NOTES_FILE = DATA_DIR / "notes.txt"

OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"

AVAILABLE_MODELS = [
    "Auto (Smart Agent)",
    "qwen2.5:7b",
    "qwen3:14b",
    "qwen3:4b-instruct",
]
DEFAULT_CODER_MODEL = "qwen2.5:7b"
DEFAULT_FAST_MODEL = "qwen3:4b-instruct"


# ─── System Prompts ────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Saathi, a brilliant, friendly, proactive AI coding assistant and desktop companion for Windows. You talk like a real, tech-savvy Indian friend in natural, warm Hinglish using Roman/English letters only (e.g. 'Haan bilkul bhai, abhi bana deta hoon!'). Never use Devanagari script.

You have full agentic capabilities to interact with the user's computer via your tools:
- `create_file`: Create or write code, complete HTML/CSS/JS websites, Python scripts, apps, or text files. Automatically creates all parent directories.
- `read_file`: Read file content from disk.
- `list_directory`: Explore files and folders.
- `open_target`: Open any file (like an HTML website in the user's browser), application (Notepad, Calculator, Spotify), or URL.
- `run_command`: Run terminal/PowerShell commands safely.
- `get_weather`: Fetch live weather for any city.
- `get_currency`: Fetch live currency exchange rates.
- `get_wikipedia`: Search Wikipedia summaries for any topic.
- `add_reminder`: Set desktop reminders.
- `add_note`: Save persistent notes.
- `take_screenshot`: Capture desktop screenshots.

CRITICAL INSTRUCTIONS FOR CODING & PROJECT CREATION:
1. When the user asks you to create a website (e.g., Independence Day website, portfolio, landing page, game, tool):
   - You MUST ALWAYS call `create_file` to write the complete, beautiful, production-ready code directly to `Projects/<ProjectName>/index.html` (e.g. `Projects/IndependenceDay/index.html`).
   - Write modern HTML5, gorgeous CSS3 styling (tricolor gradients, animations, glassmorphism, responsive layout, Ashok Chakra details, interactive cards), and interactive JavaScript!
   - Immediately after creating the file, call `open_target` with the file path (`Projects/<ProjectName>/index.html`) so it opens directly in the user's default browser!
   - NEVER say you cannot create websites or need a server. You run right on their machine and have full ability to build and launch it!
2. When the user asks to write a Python script or program:
   - Call `create_file` to save it under `Projects/` or current workspace.
   - Explain clearly how it works and how to run it.
3. Keep your tone energetic, confident, respectful, and helpful. Always summarize what you built or accomplished in friendly Hinglish!"""

UI_UX_SKILL_FILE = APP_DIR / "saathi-ai" / "skills" / "ui-ux-pro-max" / "SKILL.md"

if not UI_UX_SKILL_FILE.exists():
    UI_UX_SKILL_FILE = APP_DIR / "skills" / "ui-ux-pro-max" / "SKILL.md"

if UI_UX_SKILL_FILE.exists():
    try:
        SYSTEM_PROMPT += (
            "\n\nUI/UX PRO MAX SKILL:\n"
            + UI_UX_SKILL_FILE.read_text(encoding="utf-8")
        )
    except OSError:
        pass

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Create or overwrite a file with given content. Automatically creates parent directories. Used for writing HTML, CSS, JS, Python, or text files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path (e.g. 'Projects/IndependenceDay/index.html') or absolute path"},
                    "content": {"type": "string", "description": "The complete source code or content of the file"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_target",
            "description": "Open a local file in the default browser/app, open an application (e.g., notepad, spotify), or open a web URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "File path (e.g. 'Projects/IndependenceDay/index.html'), URL (e.g. 'https://youtube.com'), or application name"}
                },
                "required": ["target"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read text content of a file on disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path of the file to read"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and folders inside a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path, default is 'Projects'"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a Windows terminal/shell command and return its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command string to execute"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather report for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. 'Delhi', 'Mumbai', 'Bengaluru'"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_currency",
            "description": "Get latest currency exchange rate between two currencies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base": {"type": "string", "description": "Base currency code, e.g. 'USD'"},
                    "target": {"type": "string", "description": "Target currency code, e.g. 'INR'"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_wikipedia",
            "description": "Look up Wikipedia summary for a topic or person.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Topic or title to search on Wikipedia"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_reminder",
            "description": "Set a reminder with a notification text and duration in minutes from now.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Reminder text"},
                    "minutes": {"type": "integer", "description": "Minutes from now"}
                },
                "required": ["text", "minutes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_note",
            "description": "Append a note to the user's persistent notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {"type": "string", "description": "Note content to save"}
                },
                "required": ["note"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Capture a screenshot of the user's desktop and save it to the Projects folder.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


class Saathi:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("Saathi AI — Agentic Desktop Assistant")
        self.root.geometry("1020x740")
        self.root.minsize(760, 560)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.messages = []
        self.last_reply = ""
        self.always_on_top = False
        self.routine_permissions = False
        self.selected_model = tk.StringVar(value="Auto (Smart Agent)")
        self.reply_queue = queue.Queue()
        self.status_queue = queue.Queue()
        self.speaking = False
        self.reminders = []

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

        self.configure_theme()
        self.load_history()
        self.load_reminders()
        self.build_ui()
        self.setup_tray_icon()
        self.process_queues()
        self.reminder_checker_loop()

    def check_ollama_status(self):
        try:
            req = urllib.request.Request(OLLAMA_TAGS_URL)
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except (OSError, urllib.error.URLError):
            return False

    def configure_theme(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=COLOR_PANEL, foreground=COLOR_TEXT, padding=(14, 8), font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT_DIM)], foreground=[("selected", "#000000")])
        style.configure("TButton", background=COLOR_PANEL, foreground=COLOR_TEXT, padding=7)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT)
        style.configure("TCombobox", fieldbackground=COLOR_PANEL, background=COLOR_PANEL, foreground=COLOR_TEXT)

    def build_ui(self):
        self.root.configure(background=COLOR_BG)

        # Header bar
        header = tk.Frame(self.root, bg=COLOR_HEADER, padx=18, pady=10)
        header.pack(fill="x")

        title_frame = tk.Frame(header, bg=COLOR_HEADER)
        title_frame.pack(side="left")

        tk.Label(title_frame, text="SAATHI", font=("Segoe UI", 20, "bold"), bg=COLOR_HEADER, fg=COLOR_ACCENT).pack(side="left")
        tk.Label(title_frame, text="AGENTIC AI", font=("Segoe UI", 9, "bold"), bg="#1e293b", fg=COLOR_ACCENT, padx=6, pady=2).pack(side="left", padx=10)

        # Header Right - Status and Model
        right_frame = tk.Frame(header, bg=COLOR_HEADER)
        right_frame.pack(side="right")

        tk.Label(right_frame, text="Model:", bg=COLOR_HEADER, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9)).pack(side="left", padx=(0, 5))
        self.model_combo = ttk.Combobox(right_frame, textvariable=self.selected_model, values=AVAILABLE_MODELS, state="readonly", width=18)
        self.model_combo.pack(side="left", padx=(0, 15))

        self.status = tk.Label(right_frame, text="Checking Ollama...", bg=COLOR_HEADER, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 10))
        self.status.pack(side="left")

        # Notebook tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        self.chat_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.tools_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.settings_tab = tk.Frame(self.notebook, bg=COLOR_BG)

        self.notebook.add(self.chat_tab, text="Chat & Agent")
        self.notebook.add(self.tools_tab, text="Projects & Tools")
        self.notebook.add(self.settings_tab, text="Settings")

        # Chat tab layout
        self.chat_log = scrolledtext.ScrolledText(
            self.chat_tab,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            wrap="word",
            state="disabled",
            font=("Segoe UI", 10),
            padx=12,
            pady=12,
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
        )
        self.chat_log.pack(fill="both", expand=True, padx=8, pady=8)

        # Chat tag styles
        self.chat_log.tag_configure("user_label", foreground=COLOR_ACCENT, font=("Segoe UI", 10, "bold"))
        self.chat_log.tag_configure("user_text", foreground=COLOR_TEXT, font=("Segoe UI", 10))
        self.chat_log.tag_configure("assistant_label", foreground="#38bdf8", font=("Segoe UI", 10, "bold"))
        self.chat_log.tag_configure("assistant_text", foreground=COLOR_TEXT, font=("Segoe UI", 10))
        self.chat_log.tag_configure("tool_action", foreground="#fbbf24", font=("Consolas", 9, "italic"))
        self.chat_log.tag_configure("code_block", foreground="#a7f3d0", background="#1a1a2e", font=("Consolas", 9))

        input_row = tk.Frame(self.chat_tab, bg=COLOR_BG)
        input_row.pack(fill="x", padx=8, pady=(0, 8))

        self.input_box = tk.Entry(
            input_row,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            font=("Segoe UI", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
        )
        self.input_box.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))
        self.input_box.bind("<Return>", lambda event: self.send_message())

        btn_send = tk.Button(input_row, text="Send", command=self.send_message, bg=COLOR_ACCENT_DIM, fg="#0a0a0f", font=("Segoe UI", 10, "bold"), relief="flat", padx=16, pady=4, cursor="hand2")
        btn_send.pack(side="left", padx=(0, 6))

        btn_listen = tk.Button(input_row, text="🎤 Voice", command=self._listen_and_send, bg=COLOR_PANEL, fg=COLOR_TEXT, font=("Segoe UI", 10), relief="flat", padx=12, pady=4, cursor="hand2")
        btn_listen.pack(side="left", padx=(0, 6))

        for label, command in (("Clear", self.clear_history), ("Copy", self.copy_last_reply), ("Regenerate", self.regenerate_last)):
            tk.Button(input_row, text=label, command=command, bg=COLOR_PANEL, fg=COLOR_TEXT, relief="flat", padx=10, pady=4, cursor="hand2").pack(side="left", padx=(0, 4))

        self.build_tools_tab()
        self.build_settings_tab()
        self.build_docked_widget()

        self.root.after(300, self._check_initial_status)
        self.animate_orb()

        # Load recent history into view
        for item in self.messages[-30:]:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                self.append_chat(item[0], item[1])

    def _check_initial_status(self):
        online = self.check_ollama_status()
        self.status.configure(
            text="🟢 Ollama Online" if online else "🔴 Ollama Offline",
            fg=COLOR_SUCCESS if online else COLOR_ERROR
        )

    def build_tools_tab(self):
        container = tk.Frame(self.tools_tab, bg=COLOR_BG, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Workspace & Quick Tools", font=("Segoe UI", 14, "bold"), bg=COLOR_BG, fg=COLOR_ACCENT).pack(anchor="w", pady=(0, 15))

        tools_grid = tk.Frame(container, bg=COLOR_BG)
        tools_grid.pack(anchor="w")

        tools_actions = [
            ("📁 Open Projects Folder", self.open_projects_folder),
            ("🇮🇳 Build Independence Day Website", self.demo_independence_day),
            ("📋 Read Clipboard", self.handle_read_clipboard),
            ("📝 Summarize Clipboard", self.handle_summarize_clipboard),
            ("📸 Take Screenshot", self.take_screenshot),
            ("⏰ Show Reminders", self.list_reminders_text),
            ("🗒️ Show Notes", self.show_notes),
            ("📂 Choose Workspace", self.choose_workspace),
        ]

        row = 0
        col = 0
        for text, command in tools_actions:
            btn = tk.Button(
                tools_grid,
                text=text,
                command=command,
                bg=COLOR_PANEL,
                fg=COLOR_TEXT,
                font=("Segoe UI", 10),
                relief="flat",
                width=30,
                pady=8,
                cursor="hand2",
                anchor="w",
                padx=14,
            )
            btn.grid(row=row, column=col, padx=8, pady=6, sticky="w")
            col += 1
            if col > 1:
                col = 0
                row += 1

    def build_settings_tab(self):
        container = tk.Frame(self.settings_tab, bg=COLOR_BG, padx=24, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Preferences & Controls", font=("Segoe UI", 14, "bold"), bg=COLOR_BG, fg=COLOR_ACCENT).pack(anchor="w", pady=(0, 15))

        self.permission_var = tk.BooleanVar(value=True)
        cb = tk.Checkbutton(
            container,
            text="Allow routine safe actions (auto-create files, open websites/apps without dialog)",
            variable=self.permission_var,
            command=self.toggle_routine_permissions,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            selectcolor=COLOR_PANEL,
            activebackground=COLOR_BG,
            font=("Segoe UI", 10)
        )
        cb.pack(anchor="w", pady=10)
        self.routine_permissions = True

        tk.Button(
            container,
            text="Toggle Always on Top",
            command=self.toggle_always_on_top,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            font=("Segoe UI", 10),
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2"
        ).pack(anchor="w", pady=10)

        # Model details info
        info_frame = tk.Frame(container, bg=COLOR_PANEL, padx=16, pady=14, highlightthickness=1, highlightbackground=COLOR_BORDER)
        info_frame.pack(fill="x", pady=20)

        tk.Label(info_frame, text="Active Agent Models:", font=("Segoe UI", 11, "bold"), bg=COLOR_PANEL, fg=COLOR_ACCENT).pack(anchor="w")
        tk.Label(
            info_frame,
            text="• qwen2.5:7b — Ultra-fast coding & native tool calling agent (Default for websites/code)\n"
                 "• qwen3:14b — Deep reasoning & advanced architecture planning\n"
                 "• qwen3:4b-instruct — Lightweight, instantaneous casual conversational model",
            font=("Segoe UI", 9),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_MUTED,
            justify="left"
        ).pack(anchor="w", pady=(6, 0))

    def build_docked_widget(self):
        self.dock = tk.Frame(self.root, bg=COLOR_HEADER, padx=10, pady=5)
        tk.Button(self.dock, text="⚡ Saathi Dock", command=self.show_window, bg=COLOR_ACCENT_DIM, fg="#0a0a0f", font=("Segoe UI", 9, "bold"), relief="flat", padx=10).pack(side="left")
        tk.Button(self.dock, text="Hide", command=self.collapse_dock, bg=COLOR_PANEL, fg=COLOR_TEXT, relief="flat", padx=8).pack(side="right")
        self.expand_dock()

    def collapse_dock(self):
        self.dock.pack_forget()

    def expand_dock(self):
        self.dock.pack(fill="x", side="bottom")

    def animate_orb(self):
        if hasattr(self, "status"):
            current = self.status.cget("text")
            if "..." in current or "Executing" in current or "Thinking" in current:
                fg = COLOR_ACCENT if self.status.cget("foreground") != COLOR_ACCENT else COLOR_TEXT_MUTED
                self.status.configure(foreground=fg)
        self.root.after(800, self.animate_orb)

    def append_chat(self, role, text, tag=None):
        if not hasattr(self, "chat_log"):
            return
        self.chat_log.configure(state="normal")
        if role == "user":
            self.chat_log.insert("end", "You: ", "user_label")
            self.chat_log.insert("end", f"{text}\n\n", "user_text")
        elif role == "action":
            self.chat_log.insert("end", f"⚡ {text}\n", "tool_action")
        elif role == "assistant":
            self.chat_log.insert("end", "Saathi: ", "assistant_label")
            self.chat_log.insert("end", f"{text}\n\n", "assistant_text")
        elif role == "system":
            self.chat_log.insert("end", f"ℹ️ {text}\n\n", "tool_action")
        self.chat_log.configure(state="disabled")
        self.chat_log.see("end")

    def load_history(self):
        try:
            if HISTORY_FILE.exists():
                self.messages = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            else:
                self.messages = []
        except (OSError, ValueError):
            self.messages = []

    def save_history(self):
        try:
            HISTORY_FILE.write_text(json.dumps(self.messages[-100:], ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    def clear_history(self):
        self.messages.clear()
        self.save_history()
        if hasattr(self, "chat_log"):
            self.chat_log.configure(state="normal")
            self.chat_log.delete("1.0", "end")
            self.chat_log.configure(state="disabled")

    def copy_last_reply(self):
        if self.last_reply:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.last_reply)

    def regenerate_last(self):
        for role, text in reversed(self.messages):
            if role == "user":
                self.start_next_reply(text)
                break

    def send_message(self):
        text = self.input_box.get().strip()
        if text:
            self.input_box.delete(0, "end")
            self.process_user_text(text)

    def _listen_and_send(self):
        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self):
        self.status_queue.put(("status", "Listening to microphone..."))
        text = self.listen()
        if text:
            self.root.after(0, lambda: self.process_user_text(text))
        else:
            self.status_queue.put(("status", "🟢 Ollama Online"))

    def process_user_text(self, text):
        self.messages.append(("user", text))
        self.append_chat("user", text)
        self.save_history()

        # Fast direct shortcuts for simple explicit queries
        lowered = text.lower().strip()
        if "independence day" in lowered and any(k in lowered for k in ("website", "page", "site", "web")):
            self._create_independence_day_website()
            reply = "Bhai, Independence Day website successfully generate karke aapke default browser mein open kar di hai! 🇮🇳\n\nFile saved at: Projects/IndependenceDay/index.html\nHappy Independence Day! 🎉"
            self.messages.append(("assistant", reply))
            self.append_chat("assistant", reply)
            self.save_history()
            threading.Thread(target=self.speak, args=(reply,), daemon=True).start()
            return
        if lowered in ("open projects", "open projects folder", "projects"):
            self.open_projects_folder()
            return
        if lowered == "screenshot" or lowered == "take screenshot":
            path = self.take_screenshot()
            reply = f"Screenshot save ho gayi: {path}"
            self.messages.append(("assistant", reply))
            self.append_chat("assistant", reply)
            self.save_history()
            return

        self.start_next_reply(text)

    def pick_model(self, text):
        chosen = self.selected_model.get()
        if chosen and chosen != "Auto (Smart Agent)":
            return chosen

        lowered = text.lower()
        coder_words = ("create", "website", "build", "code", "html", "css", "javascript", "script", "program", "app", "game", "write", "make", "develop", "fix", "debug", "explain", "plan", "remind", "weather", "currency", "wikipedia")
        if any(word in lowered for word in coder_words):
            return DEFAULT_CODER_MODEL
        return DEFAULT_CODER_MODEL

    def execute_tool(self, name, args):
        """Execute desktop tool actions on behalf of the agent."""
        try:
            if isinstance(args, str):
                args = json.loads(args)
        except Exception:
            pass

        if not isinstance(args, dict):
            args = {}

        if name == "create_file":
            path_str = args.get("path", "")
            content = args.get("content", "")
            if not path_str:
                return "Error: path is required."

            target_path = Path(path_str)
            if not target_path.is_absolute():
                target_path = APP_DIR / target_path

            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding="utf-8")
            return f"File '{target_path}' created successfully ({len(content)} characters)."

        elif name == "read_file":
            path_str = args.get("path", "")
            target_path = Path(path_str)
            if not target_path.is_absolute():
                target_path = APP_DIR / target_path
            if not target_path.exists():
                return f"Error: File '{path_str}' does not exist."
            return target_path.read_text(encoding="utf-8", errors="replace")[:10000]

        elif name == "list_directory":
            path_str = args.get("path", "Projects")
            target_path = Path(path_str)
            if not target_path.is_absolute():
                target_path = APP_DIR / target_path
            if not target_path.exists():
                return f"Directory '{path_str}' does not exist."
            items = [f"{'[DIR]' if p.is_dir() else '[FILE]'} {p.name}" for p in target_path.iterdir()]
            return "\n".join(items) if items else "Directory is empty."

        elif name == "open_target":
            target = args.get("target", "").strip()
            if not target:
                return "Error: target is required."

            # Check if file path
            p = Path(target)
            if not p.is_absolute():
                p = (APP_DIR / p).resolve()

            if p.exists():
                if p.suffix.lower() in (".html", ".htm"):
                    webbrowser.open(p.as_uri())
                else:
                    os.startfile(str(p))
                return f"Opened file '{p}'."

            if target.startswith(("http://", "https://", "spotify:")):
                webbrowser.open(target)
                return f"Opened URL '{target}'."

            # Try app name
            apps = {"notepad": "notepad.exe", "calc": "calc.exe", "calculator": "calc.exe", "explorer": "explorer.exe"}
            app_cmd = apps.get(target.lower(), target)
            try:
                os.startfile(app_cmd)
                return f"Launched '{app_cmd}'."
            except OSError:
                webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(target))
                return f"Searched web for '{target}'."

        elif name == "run_command":
            cmd = args.get("command", "")
            if not self.routine_permissions:
                if not messagebox.askyesno("Confirm Command", f"Run command?\n\n{cmd}", parent=self.root):
                    return "Command execution cancelled by user."
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45)
            output = (res.stdout or res.stderr or "").strip()
            return output if output else "Command executed successfully with no output."

        elif name == "get_weather":
            city = args.get("city", "Delhi").strip()
            url = "https://wttr.in/%s?format=3" % urllib.parse.quote(city)
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                return resp.read().decode("utf-8").strip()

        elif name == "get_currency":
            base = args.get("base", "USD").upper()
            target = args.get("target", "INR").upper()
            url = f"https://open.er-api.com/v6/latest/{base}"
            with urllib.request.urlopen(url, timeout=8) as resp:
                rates = json.loads(resp.read().decode("utf-8")).get("rates", {})
            val = rates.get(target, "N/A")
            return f"1 {base} = {val} {target}"

        elif name == "get_wikipedia":
            query = args.get("query", "").strip()
            if not query:
                return "No query provided."
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers={"User-Agent": "SaathiAI/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract")
            return extract if extract else f"No Wikipedia summary found for '{query}'."

        elif name == "add_reminder":
            text = args.get("text", "")
            minutes = int(args.get("minutes", 10))
            self.add_reminder(text, minutes)
            return f"Reminder set: '{text}' in {minutes} minutes."

        elif name == "add_note":
            note = args.get("note", "")
            self.add_note(note)
            return f"Note saved: '{note}'."

        elif name == "take_screenshot":
            target = self.take_screenshot()
            return f"Screenshot saved to '{target}'."

        return f"Unknown tool: {name}"

    def remove_thinking(self, text):
        return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()

    def start_next_reply(self, text):
        threading.Thread(target=self._reply_worker, args=(text,), daemon=True).start()

    def _reply_worker(self, text):
        model = self.pick_model(text)
        self.status_queue.put(("status", f"⚡ {model} is thinking..."))

        # Build conversation history
        conv_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for item in self.messages[-14:]:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                role = "assistant" if item[0] == "assistant" else "user"
                conv_messages.append({"role": role, "content": str(item[1])})

        # Start live progress ticker thread
        stop_ticker = threading.Event()
        start_time = time.time()

        def ticker():
            while not stop_ticker.wait(1.5):
                elapsed = int(time.time() - start_time)
                self.status_queue.put(("status", f"⚡ {model} generating... ({elapsed}s)"))

        threading.Thread(target=ticker, daemon=True).start()

        try:
            # Multi-turn tool-calling loop (up to 4 iterations)
            final_reply = ""
            for loop_idx in range(4):
                payload = {
                    "model": model,
                    "messages": conv_messages,
                    "tools": TOOLS_SCHEMA,
                    "keep_alive": "60m",
                    "stream": False,
                }
                req = urllib.request.Request(
                    OLLAMA_CHAT_URL,
                    json.dumps(payload).encode("utf-8"),
                    {"Content-Type": "application/json"}
                )
                # 300 seconds timeout for large generations on CPU
                with urllib.request.urlopen(req, timeout=300) as response:
                    res_data = json.loads(response.read().decode("utf-8"))

                msg = res_data.get("message", {})
                content = self.remove_thinking(msg.get("content", "") or "")
                tool_calls = msg.get("tool_calls", [])

                if tool_calls:
                    conv_messages.append({
                        "role": "assistant",
                        "content": content,
                        "tool_calls": tool_calls
                    })

                    for call in tool_calls:
                        fn = call.get("function", {})
                        fn_name = fn.get("name", "")
                        fn_args = fn.get("arguments", {})

                        if isinstance(fn_args, str):
                            try:
                                fn_args = json.loads(fn_args)
                            except json.JSONDecodeError:
                                fn_args = {}
                        if not isinstance(fn_args, dict):
                            fn_args = {}

                        preview = (
                            fn_args.get("path")
                            or fn_args.get("target")
                            or fn_args.get("city")
                            or ""
                        )
                        self.status_queue.put(
                            ("action", f"Executing: {fn_name}({preview})")
                        )
                        self.status_queue.put(("status", f"Running {fn_name}..."))

                        try:
                            result = self.execute_tool(fn_name, fn_args)
                        except Exception as tool_err:
                            result = f"Error executing {fn_name}: {tool_err}"
                        self.status_queue.put(("action", f"Done: {str(result)[:120]}"))

                        conv_messages.append({
                            "role": "tool",
                            "content": str(result)
                        })

                    continue
                else:
                    final_reply = content
                    break

            if not final_reply:
                final_reply = "Main ready hoon! Kaam ho gaya."

            self.reply_queue.put(final_reply)

        except Exception as error:
            err_str = str(error)
            if "timed out" in err_str.lower():
                err_msg = (
                    "Ollama request timed out on CPU. Laptop CPU pe bada code generate karne mein "
                    "thoda zyada time lag sakta hai.\n\n"
                    "Tip: Aap upar Model dropdown se 'qwen3:4b-instruct' select kar sakte ho — "
                    "wo CPU pe 2x faster response deta hai!"
                )
            else:
                err_msg = f"Ollama se connect nahi ho paaya: {error}"
            self.reply_queue.put(err_msg)

        finally:
            stop_ticker.set()
            self.status_queue.put(("status", "🟢 Ollama Online"))

    def _create_independence_day_website(self):
        """Creates an Independence Day website in Projects/IndependenceDay/index.html and opens it."""
        target_dir = PROJECTS_DIR / "IndependenceDay"
        target_dir.mkdir(parents=True, exist_ok=True)
        html_file = target_dir / "index.html"

        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Happy 78th Independence Day 🇮🇳 | Saathi AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body {
            min-height: 100vh;
            background: radial-gradient(circle at 50% 20%, #1e1b4b, #0f172a 70%);
            color: #f8fafc;
            overflow-x: hidden;
            text-align: center;
        }
        .tricolor-stripe {
            height: 10px;
            background: linear-gradient(90deg, #ff9933 33%, #ffffff 33%, #ffffff 66%, #138808 66%);
            box-shadow: 0 0 20px rgba(255, 153, 51, 0.5);
        }
        .hero {
            padding: 80px 20px 40px;
            max-width: 960px;
            margin: 0 auto;
        }
        .badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 153, 51, 0.4);
            color: #ff9933;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 25px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; transform: scale(1.05); } }
        h1 {
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 900;
            line-height: 1.15;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ff9933, #ffffff 50%, #138808);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        p.subtitle {
            font-size: clamp(1.1rem, 2.5vw, 1.4rem);
            color: #94a3b8;
            max-width: 680px;
            margin: 0 auto 40px;
            line-height: 1.6;
        }
        .chakra-container {
            margin: 30px auto;
            width: 140px;
            height: 140px;
            position: relative;
        }
        .chakra {
            width: 100%;
            height: 100%;
            border: 6px solid #000080;
            border-radius: 50%;
            position: relative;
            background: #ffffff;
            box-shadow: 0 0 35px rgba(0, 0, 128, 0.6);
            animation: spin 16s linear infinite;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        .spoke {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100%;
            height: 2px;
            background-color: #000080;
            transform-origin: center;
        }
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            max-width: 900px;
            margin: 40px auto 60px;
            padding: 0 20px;
        }
        .card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            padding: 30px 24px;
            border-radius: 20px;
            transition: all 0.3s ease;
            text-align: left;
        }
        .card:hover {
            transform: translateY(-8px);
            border-color: #ff9933;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        }
        .card h3 {
            font-size: 1.3rem;
            color: #ff9933;
            margin-bottom: 12px;
        }
        .card p {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        .interactive-btn {
            background: linear-gradient(135deg, #ff9933, #e65100);
            color: #fff;
            border: none;
            padding: 14px 34px;
            font-size: 1.1rem;
            font-weight: 700;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(255, 153, 51, 0.4);
            transition: all 0.3s;
        }
        .interactive-btn:hover {
            transform: scale(1.06);
            box-shadow: 0 12px 35px rgba(255, 153, 51, 0.6);
        }
        footer {
            padding: 40px 20px;
            color: #64748b;
            font-size: 0.9rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
</head>
<body>
    <div class="tricolor-stripe"></div>
    <div class="hero">
        <div class="badge">Azadi Ka Amrit Mahotsav 🇮🇳</div>
        <h1>HAPPY INDEPENDENCE DAY</h1>
        <p class="subtitle">Celebrating 78 Years of Freedom, Unity, and Progress. Proud to be an Indian!</p>

        <div class="chakra-container">
            <div class="chakra" id="ashokChakra"></div>
        </div>

        <div style="margin: 30px 0;">
            <button class="interactive-btn" onclick="celebrate()">Salute the Tiranga 🇮🇳</button>
        </div>

        <div class="cards-grid">
            <div class="card">
                <h3>Saffron (Kesari)</h3>
                <p>Represents courage, sacrifice, and valor of our brave freedom fighters who gave their all for our nation.</p>
            </div>
            <div class="card">
                <h3>White (Shweta)</h3>
                <p>Symbolizes peace, truth, unity, and honesty, guiding our country towards harmony and wisdom.</p>
            </div>
            <div class="card">
                <h3>Green (Hara)</h3>
                <p>Signifies growth, faith, and prosperity, blessing our fertile land and boundless future aspirations.</p>
            </div>
        </div>
    </div>

    <footer>
        Crafted with pride by <strong>Saathi AI</strong> on Windows • Vande Mataram • Jai Hind! 🇮🇳
    </footer>

    <script>
        // Generate 24 spokes for Ashok Chakra
        const chakra = document.getElementById('ashokChakra');
        for (let i = 0; i < 12; i++) {
            const spoke = document.createElement('div');
            spoke.className = 'spoke';
            spoke.style.transform = `translate(-50%, -50%) rotate(${i * 15}deg)`;
            chakra.appendChild(spoke);
        }

        function celebrate() {
            alert("Jai Hind! Vande Mataram! 🇮🇳\\nHappy Independence Day from Saathi AI!");
            confettiEffect();
        }

        function confettiEffect() {
            for(let i=0; i<60; i++) {
                const conf = document.createElement('div');
                const colors = ['#ff9933', '#ffffff', '#138808', '#000080'];
                conf.style.position = 'fixed';
                conf.style.left = Math.random() * window.innerWidth + 'px';
                conf.style.top = '-10px';
                conf.style.width = (Math.random() * 10 + 5) + 'px';
                conf.style.height = (Math.random() * 10 + 5) + 'px';
                conf.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                conf.style.zIndex = '9999';
                conf.style.borderRadius = '50%';
                conf.style.pointerEvents = 'none';
                conf.style.transition = 'all 3s ease-out';
                document.body.appendChild(conf);

                setTimeout(() => {
                    conf.style.transform = `translate(${Math.random()*100 - 50}px, ${window.innerHeight + 20}px) rotate(${Math.random()*360}deg)`;
                    conf.style.opacity = '0';
                }, 10);

                setTimeout(() => conf.remove(), 3200);
            }
        }
    </script>
</body>
</html>"""
        html_file.write_text(html_content, encoding="utf-8")
        webbrowser.open(html_file.as_uri())

    def demo_independence_day(self):
        self.append_chat("user", "Build me an Independence Day website now!")
        self._create_independence_day_website()
        reply = "Bhai, Independence Day website successfully generate karke aapke browser mein open kar di hai! 🇮🇳 Projects/IndependenceDay folder check kar lo!"
        self.messages.append(("assistant", reply))
        self.append_chat("assistant", reply)
        self.save_history()

    def open_projects_folder(self):
        PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        os.startfile(str(PROJECTS_DIR))

    def process_queues(self):
        try:
            while True:
                msg_type, data = self.status_queue.get_nowait()
                if msg_type == "status":
                    self.status.configure(text=data)
                elif msg_type == "action":
                    self.append_chat("action", data)
        except queue.Empty:
            pass

        try:
            while True:
                reply = self.reply_queue.get_nowait()
                self.last_reply = reply
                self.messages.append(("assistant", reply))
                self.append_chat("assistant", reply)
                threading.Thread(target=self.speak, args=(reply,), daemon=True).start()
                self.save_history()
        except queue.Empty:
            pass

        self.root.after(100, self.process_queues)

    def speak(self, text):
        try:
            import edge_tts
            import pygame
            clean_txt = re.sub(r"[*_`#<>{}]", "", text)
            clean_txt = re.sub(r"http\S+", "", clean_txt)[:400]
            if not clean_txt.strip():
                return False

            out_file = Path(tempfile.gettempdir()) / "saathi_tts.mp3"
            asyncio.run(edge_tts.Communicate(clean_txt, "en-IN-NeerjaNeural").save(str(out_file)))

            pygame.mixer.init()
            pygame.mixer.music.load(str(out_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            return True
        except Exception:
            return False

    def listen(self):
        try:
            import sounddevice as sd
            import numpy as np
            sample_rate = 16000
            recording = sd.rec(int(sample_rate * 5), samplerate=sample_rate, channels=1, dtype="float32")
            sd.wait()
            return self.transcribe(np.asarray(recording).flatten())
        except Exception as error:
            messagebox.showerror("Microphone Error", f"Voice input error: {error}", parent=self.root)
            return ""

    def transcribe(self, audio):
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel("base", compute_type="int8")
            segments, _ = model.transcribe(audio, language="hi", vad_filter=True)
            return " ".join(segment.text.strip() for segment in segments).strip()
        except Exception:
            return ""

    def on_close(self):
        self.save_history()
        self.root.destroy()

    def show_window(self):
        self.root.deiconify()
        self.root.lift()

    def quit_app(self):
        self.on_close()

    def setup_tray_icon(self):
        if pystray is None:
            return None
        image = Image.new("RGB", (64, 64), COLOR_ACCENT)
        menu = pystray.Menu(
            pystray.MenuItem("Show Saathi", lambda icon, item: self.root.after(0, self.show_window)),
            pystray.MenuItem("Quit", lambda icon, item: self.root.after(0, self.quit_app))
        )
        self.tray_icon = pystray.Icon("saathi", image, "Saathi AI", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
        return self.tray_icon

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)

    def toggle_routine_permissions(self):
        self.routine_permissions = self.permission_var.get()

    def load_reminders(self):
        try:
            if REMINDERS_FILE.exists():
                self.reminders = json.loads(REMINDERS_FILE.read_text(encoding="utf-8"))
            else:
                self.reminders = []
        except (OSError, ValueError):
            self.reminders = []

    def save_reminders(self):
        try:
            REMINDERS_FILE.write_text(json.dumps(self.reminders, indent=2), encoding="utf-8")
        except OSError:
            pass

    def add_reminder(self, text, minutes):
        when_time = datetime.now() + timedelta(minutes=int(minutes))
        reminder = {"text": text, "when": when_time.isoformat(), "done": False}
        self.reminders.append(reminder)
        self.save_reminders()
        return reminder

    def reminder_checker_loop(self):
        now = datetime.now()
        for reminder in self.reminders:
            if not reminder.get("done") and datetime.fromisoformat(reminder["when"]) <= now:
                reminder["done"] = True
                self.append_chat("assistant", f"⏰ REMINDER: {reminder['text']}")
                threading.Thread(target=self.speak, args=(f"Reminder: {reminder['text']}",), daemon=True).start()
        self.save_reminders()
        self.root.after(20000, self.reminder_checker_loop)

    def list_reminders_text(self):
        pending = [f"• {r['text']} (At: {r['when'][:16]})" for r in self.reminders if not r.get("done")]
        txt = "\n".join(pending) if pending else "No pending reminders."
        self.append_chat("assistant", txt)
        return txt

    def add_note(self, text):
        with NOTES_FILE.open("a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {text.strip()}\n")

    def show_notes(self):
        try:
            txt = NOTES_FILE.read_text(encoding="utf-8")
        except OSError:
            txt = "No notes recorded yet."
        self.append_chat("assistant", txt)
        return txt

    def handle_read_clipboard(self):
        try:
            text = self.root.clipboard_get()
        except tk.TclError:
            text = "Clipboard is empty."
        self.append_chat("assistant", f"Clipboard content:\n{text}")
        return text

    def handle_summarize_clipboard(self):
        try:
            text = self.root.clipboard_get()
            self.process_user_text(f"Summarize this text:\n{text}")
        except tk.TclError:
            self.append_chat("assistant", "Clipboard is empty.")

    def take_screenshot(self):
        if ImageGrab is None:
            return "ImageGrab not available"
        try:
            target = PROJECTS_DIR / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            target.parent.mkdir(parents=True, exist_ok=True)
            img = ImageGrab.grab()
            img.save(target)
            self.append_chat("assistant", f"Screenshot saved to: {target}")
            return str(target)
        except Exception as error:
            return f"Screenshot error: {error}"

    def choose_workspace(self):
        folder = filedialog.askdirectory(parent=self.root, title="Choose Workspace Folder")
        if folder:
            self.append_chat("assistant", f"Workspace set to: {folder}")
        return folder


if __name__ == "__main__":
    app = Saathi()
    app.root.mainloop()