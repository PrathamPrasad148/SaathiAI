"""Saathi: local-first Hinglish desktop assistant — JARVIS Edition."""
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


# ─── JARVIS Color Palette ──────────────────────────────────────────────
# Deep midnight base with JARVIS Green accent
COLOR_BG = "#0a0a0f"
COLOR_PANEL = "#12121f"
COLOR_ACCENT = "#00ff88"
COLOR_ACCENT_DIM = "#00cc6a"
COLOR_TEXT = "#e8e8f0"
COLOR_TEXT_MUTED = "#6a6a80"
COLOR_ORB = "#00ff88"
COLOR_ORB_GLOW = "#00ff8840"
COLOR_HEADER = "#0f0f14"
COLOR_BORDER = "#2a2a3a"
COLOR_SUCCESS = "#00ff88"
COLOR_WARNING = "#ffaa00"
COLOR_ERROR = "#ff5555"


APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
HISTORY_FILE = DATA_DIR / "history.json"
FAST_MODEL = "qwen3:4b-instruct"
DEEP_MODEL = "qwen3:14b"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


# ── System prompts ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Saathi, a warm, sharp, capable personal assistant who talks like a real Indian friend, not a robot. Reply only in natural Hinglish, Roman/English letters only (e.g. 'Haan bilkul, abhi karta hoon'). Never use Devanagari, Urdu/Arabic script, or any other writing system. Vary your phrasing, keep it conversational and confident, avoid stiff or repetitive sentence patterns and avoid excessive apologising. Give direct, useful answers. For coding, first state a short plan, then provide complete runnable code and clear run instructions. Be honest about limits. Saathi CAN open apps/websites/media, list/read/create/edit files and folders, run terminal commands, and fetch live data (weather, currency, definitions, Wikipedia, etc.) on the user's desktop once permission is granted or confirmed in the app — say so plainly when something actually happened. Never claim you opened something, changed a file, ran a command, fetched data, sent a message, or controlled a device unless the desktop app actually confirms it happened. Deleting/moving files and running terminal commands always show the user an explicit confirmation with the exact path/command first, regardless of any standing permission — that's a hard rule Saathi cannot waive."""

QUICK_PROMPT = """You are Saathi, chatting casually. Reply only in natural, warm Hinglish using Roman/English letters. Be brief and direct. Never claim an action happened unless the desktop app confirms it."""

ACTION_WORDS = ("open", "launch", "start", "play")
SINGLE_WORD_ACTIONS = {"youtube": "https://www.youtube.com", "spotify": "spotify:", "notepad": "notepad.exe", "calculator": "calc.exe"}
SONG_WORDS = ("song", "music", "gaana", "gana", "play")
SYSTEM_COMMAND_PATTERNS = ("run command", "execute command", "terminal", "cmd")
DATA_COMMAND_PATTERNS = ("weather", "currency", "meaning", "define", "wikipedia", "news", "translate", "public ip")
UTILITY_COMMAND_PATTERNS = ("clipboard", "screenshot", "organize")


class Saathi:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("Saathi AI")
        self.root.geometry("980x700")
        self.root.minsize(720, 520)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.messages = []
        self.last_reply = ""
        self.always_on_top = False
        self.routine_permissions = False
        self.reply_queue = queue.Queue()
        self.speaking = False
        self.reminders = []
        DATA_DIR.mkdir(exist_ok=True)
        self.configure_theme()
        self.load_history()
        self.load_reminders()
        self.build_ui()
        self.setup_tray_icon()
        self.process_queues()
        self.reminder_checker_loop()

    def check_ollama_status(self):
        try:
            with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as response:
                return response.status == 200
        except (OSError, urllib.error.URLError):
            return False

    def configure_theme(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=COLOR_PANEL, foreground=COLOR_TEXT, padding=(12, 7))
        style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT_DIM)])
        style.configure("TButton", background=COLOR_PANEL, foreground=COLOR_TEXT, padding=7)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT)

    def build_ui(self):
        self.root.configure(background=COLOR_BG)
        header = tk.Frame(self.root, bg=COLOR_HEADER, padx=18, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="SAATHI", font=("Segoe UI", 22, "bold"), bg=COLOR_HEADER, fg=COLOR_ACCENT).pack(side="left")
        self.status = tk.Label(header, text="Checking Ollama...", bg=COLOR_HEADER, fg=COLOR_TEXT_MUTED)
        self.status.pack(side="right")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)
        self.chat_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.tools_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.settings_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(self.chat_tab, text="Chat")
        self.notebook.add(self.tools_tab, text="Tools")
        self.notebook.add(self.settings_tab, text="Settings")
        self.chat_log = scrolledtext.ScrolledText(self.chat_tab, bg=COLOR_PANEL, fg=COLOR_TEXT, insertbackground=COLOR_ACCENT, wrap="word", state="disabled")
        self.chat_log.pack(fill="both", expand=True, padx=8, pady=8)
        input_row = tk.Frame(self.chat_tab, bg=COLOR_BG)
        input_row.pack(fill="x", padx=8, pady=(0, 8))
        self.input_box = tk.Entry(input_row, bg=COLOR_PANEL, fg=COLOR_TEXT, insertbackground=COLOR_ACCENT)
        self.input_box.pack(side="left", fill="x", expand=True, ipady=8)
        self.input_box.bind("<Return>", lambda event: self.send_message())
        tk.Button(input_row, text="Send", command=self.send_message, bg=COLOR_ACCENT_DIM, fg="white").pack(side="left", padx=(8, 0))
        tk.Button(input_row, text="Listen", command=self._listen_and_send, bg=COLOR_PANEL, fg=COLOR_TEXT).pack(side="left", padx=(6, 0))
        for label, command in (("Clear", self.clear_history), ("Copy", self.copy_last_reply), ("Regenerate", self.regenerate_last)):
            tk.Button(input_row, text=label, command=command, bg=COLOR_PANEL, fg=COLOR_TEXT).pack(side="left", padx=(6, 0))
        self.build_tools_tab()
        self.build_settings_tab()
        self.build_docked_widget()
        self.root.after(200, lambda: self.status.configure(text="Ollama online" if self.check_ollama_status() else "Ollama offline"))
        self.animate_orb()
        for role, text in self.messages[-20:]:
            self.append_chat(role, text)

    def build_tools_tab(self):
        for text, command in (("Choose workspace", self.choose_workspace), ("Create project", self.create_project), ("Read clipboard", self.handle_read_clipboard), ("Screenshot", self.take_screenshot), ("Show reminders", self.list_reminders_text), ("Show notes", self.show_notes)):
            tk.Button(self.tools_tab, text=text, command=command, bg=COLOR_PANEL, fg=COLOR_TEXT, width=22).pack(anchor="w", padx=20, pady=6)

    def build_settings_tab(self):
        self.permission_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.settings_tab, text="Allow routine safe actions", variable=self.permission_var, command=self.toggle_routine_permissions, bg=COLOR_BG, fg=COLOR_TEXT, selectcolor=COLOR_PANEL, activebackground=COLOR_BG).pack(anchor="w", padx=20, pady=16)
        tk.Button(self.settings_tab, text="Toggle always on top", command=self.toggle_always_on_top, bg=COLOR_PANEL, fg=COLOR_TEXT).pack(anchor="w", padx=20)

    def build_docked_widget(self):
        self.dock = tk.Frame(self.root, bg=COLOR_HEADER, padx=8, pady=4)
        tk.Button(self.dock, text="Saathi", command=self.show_window, bg=COLOR_ACCENT_DIM, fg="white").pack(side="left")
        tk.Button(self.dock, text="Hide", command=self.collapse_dock, bg=COLOR_PANEL, fg=COLOR_TEXT).pack(side="right")
        self.expand_dock()

    def collapse_dock(self):
        self.dock.pack_forget()

    def expand_dock(self):
        self.dock.pack(fill="x", side="bottom")

    def animate_orb(self):
        if hasattr(self, "status"):
            color = COLOR_ACCENT if self.status.cget("foreground") != COLOR_ACCENT else COLOR_TEXT_MUTED
            self.status.configure(foreground=color)
        self.root.after(900, self.animate_orb)

    def append_chat(self, role, text):
        if not hasattr(self, "chat_log"):
            return
        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", "%s: %s\n\n" % ("You" if role == "user" else "Saathi", text))
        self.chat_log.configure(state="disabled")
        self.chat_log.see("end")

    def load_history(self):
        try:
            self.messages = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.messages = []

    def remove_thinking(self, text):
        return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()

    def _similar(self, first, second):
        return difflib.SequenceMatcher(None, first.lower(), second.lower()).ratio()

    def romanize_devanagari(self, text):
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()

    def save_history(self):
        HISTORY_FILE.write_text(json.dumps(self.messages[-100:], ensure_ascii=True, indent=2), encoding="utf-8")

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
        if self.messages and self.messages[-1][0] == "user":
            self.start_next_reply(self.messages[-1][1])

    def send_message(self):
        text = self.input_box.get().strip()
        if text:
            self.input_box.delete(0, "end")
            self.process_user_text(text)

    def _listen_and_send(self):
        text = self.listen()
        if text:
            self.process_user_text(text)

    def process_user_text(self, text):
        self.messages.append(("user", text))
        self.append_chat("user", text)
        if self.try_handle_open_command(text) or self.try_handle_system_command(text) or self.try_handle_data_command(text) or self.try_handle_utility_command(text):
            self.save_history()
            return
        self.start_next_reply(text)

    def pick_model(self, text):
        return DEEP_MODEL if any(word in text.lower() for word in ("code", "explain", "plan", "write")) else FAST_MODEL

    def ask_ollama(self, text):
        payload = {"model": self.pick_model(text), "messages": [{"role": "system", "content": QUICK_PROMPT}, {"role": "user", "content": text}], "stream": False}
        request = urllib.request.Request(OLLAMA_URL, json.dumps(payload).encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=120) as response:
            return self.remove_thinking(json.loads(response.read().decode())["message"]["content"])

    def start_next_reply(self, text):
        threading.Thread(target=self._reply_worker, args=(text,), daemon=True).start()

    def _reply_worker(self, text):
        try:
            reply = self.ask_ollama(text)
        except Exception as error:
            reply = "Ollama se connect nahi ho paaya: %s" % error
        self.reply_queue.put(reply)

    def process_queues(self):
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
            output = Path(tempfile.gettempdir()) / "saathi_reply.mp3"
            asyncio.run(edge_tts.Communicate(self.clean_for_speech(text), "en-IN-NeerjaNeural").save(str(output)))
            pygame.mixer.init()
            pygame.mixer.music.load(str(output))
            pygame.mixer.music.play()
            return True
        except (ImportError, OSError, RuntimeError):
            return False

    def clean_for_speech(self, text):
        return re.sub(r"[*_`#]", "", text)

    def listen(self):
        try:
            import sounddevice as sd
            import numpy as np
            sample_rate = 16000
            recording = sd.rec(int(sample_rate * 5), samplerate=sample_rate, channels=1, dtype="float32")
            sd.wait()
            return self.transcribe(np.asarray(recording).flatten())
        except (ImportError, OSError, RuntimeError) as error:
            messagebox.showerror("Voice input", "Microphone unavailable: %s" % error, parent=self.root)
            return ""

    def transcribe(self, audio):
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel("base", compute_type="int8")
            segments, _ = model.transcribe(audio, language="hi", vad_filter=True)
            return " ".join(segment.text.strip() for segment in segments).strip()
        except (ImportError, OSError, RuntimeError):
            return ""

    def confirm_action(self, message):
        return messagebox.askyesno("Confirm action", message, parent=self.root)

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
        menu = pystray.Menu(pystray.MenuItem("Show Saathi", lambda icon, item: self.root.after(0, self.show_window)), pystray.MenuItem("Quit", lambda icon, item: self.root.after(0, self.quit_app)))
        self.tray_icon = pystray.Icon("saathi", image, "Saathi AI", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
        return self.tray_icon

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)

    def toggle_routine_permissions(self):
        self.routine_permissions = self.permission_var.get()

    def fuzzy_match_name(self, query, names):
        return max(names, key=lambda name: self._similar(query, name), default=None)

    def find_known_name_in_text(self, text, names):
        return next((name for name in names if name.lower() in text.lower()), None)

    def extract_last_suggested_title(self, text):
        return text.strip().splitlines()[-1] if text.strip() else ""

    def extract_search_phrase(self, text):
        return re.sub(r"^(search|google|look up)\s+", "", text.strip(), flags=re.I)

    def determine_search_hint(self, text):
        return self.extract_search_phrase(text)

    def resolve_open_target(self, target):
        return SINGLE_WORD_ACTIONS.get(target.lower(), target)

    def open_anything(self, target):
        import os as _os
        resolved = self.resolve_open_target(target)
        if resolved.startswith(("http://", "https://", "spotify:")):
            webbrowser.open(resolved)
        else:
            _os.startfile(resolved)

    def try_handle_open_command(self, text):
        words = text.strip().split(maxsplit=1)
        if not words or words[0].lower() not in ACTION_WORDS:
            return False
        target = words[1] if len(words) > 1 else ""
        if not target:
            return False
        if target.lower() in SINGLE_WORD_ACTIONS or target.startswith(("http://", "https://")):
            if self.routine_permissions or self.confirm_action("Open %s?" % target):
                try:
                    self.open_anything(target)
                    self.append_chat("assistant", "Opening %s." % target)
                except OSError as error:
                    self.append_chat("assistant", "Open nahi ho paaya: %s" % error)
            return True
        self.browser_search(target)
        return True

    def browser_search(self, phrase):
        webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(phrase))

    def open_anything_dialog(self):
        target = simpledialog.askstring("Open", "App, file, or URL:", parent=self.root)
        if target:
            self.open_anything(target)

    def file_search(self, phrase, folder=None):
        base = Path(folder or APP_DIR)
        return [path for path in base.rglob("*") if phrase.lower() in path.name.lower()][:50]

    def resolve_path(self, value):
        return Path(value).expanduser().resolve()

    def is_protected_path(self, path):
        resolved = self.resolve_path(path)
        return resolved == Path(resolved.anchor) or resolved == APP_DIR

    def list_directory(self, path):
        return "\n".join(item.name for item in self.resolve_path(path).iterdir())

    def read_text_file(self, path):
        return self.resolve_path(path).read_text(encoding="utf-8")

    def write_text_file(self, path, content):
        target = self.resolve_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def create_folder(self, path):
        self.resolve_path(path).mkdir(parents=True, exist_ok=True)

    def delete_path(self, path):
        target = self.resolve_path(path)
        if self.is_protected_path(target) or not self.confirm_action("Delete %s?" % target):
            return False
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        return True

    def move_path(self, source, destination):
        if not self.confirm_action("Move %s to %s?" % (source, destination)):
            return False
        shutil.move(str(self.resolve_path(source)), str(self.resolve_path(destination)))
        return True

    def run_command(self, command):
        if not self.confirm_action("Run command?\n\n%s" % command):
            return "Cancelled"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        return (result.stdout or result.stderr).strip()

    def try_handle_system_command(self, text):
        if not any(pattern in text.lower() for pattern in SYSTEM_COMMAND_PATTERNS):
            return False
        command = re.sub(r"^(run command|execute command|terminal|cmd)\s*", "", text, flags=re.I)
        self.append_chat("assistant", self.run_command(command))
        return True

    def handle_weather(self, city):
        url = "https://wttr.in/%s?format=3" % urllib.parse.quote(city or "Delhi")
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode().strip()

    def handle_currency(self, base="USD", target="INR"):
        with urllib.request.urlopen("https://open.er-api.com/v6/latest/%s" % base, timeout=10) as response:
            rates = json.loads(response.read().decode())["rates"]
        return "1 %s = %s %s" % (base, rates.get(target, "unavailable"), target)

    def try_handle_data_command(self, text):
        lowered = text.lower()
        if "weather" in lowered:
            result = self.handle_weather(text.lower().split("weather", 1)[-1].strip())
        elif "currency" in lowered:
            result = self.handle_currency()
        else:
            return False
        self.append_chat("assistant", result)
        return True

    def load_reminders(self):
        self.reminders_file = DATA_DIR / "reminders.json"
        try:
            self.reminders = json.loads(self.reminders_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.reminders = []

    def save_reminders(self):
        self.reminders_file.write_text(json.dumps(self.reminders, indent=2), encoding="utf-8")

    def parse_reminder_time(self, value):
        return datetime.fromisoformat(value) if "T" in value else datetime.now() + timedelta(minutes=int(value))

    def add_reminder(self, text, when):
        reminder = {"text": text, "when": self.parse_reminder_time(when).isoformat(), "done": False}
        self.reminders.append(reminder)
        self.save_reminders()
        return reminder

    def reminder_checker_loop(self):
        now = datetime.now()
        for reminder in self.reminders:
            if not reminder.get("done") and datetime.fromisoformat(reminder["when"]) <= now:
                reminder["done"] = True
                self.append_chat("assistant", "Reminder: %s" % reminder["text"])
        self.save_reminders()
        self.root.after(30000, self.reminder_checker_loop)

    def list_reminders_text(self):
        text = "\n".join("- %s (%s)" % (item["text"], item["when"]) for item in self.reminders if not item.get("done")) or "No pending reminders."
        self.append_chat("assistant", text)
        return text

    def notes_file(self):
        return DATA_DIR / "notes.txt"

    def add_note(self, text):
        with self.notes_file().open("a", encoding="utf-8") as notes:
            notes.write(text.strip() + "\n")

    def show_notes(self):
        try:
            text = self.notes_file().read_text(encoding="utf-8")
        except OSError:
            text = "No notes yet."
        self.append_chat("assistant", text)
        return text

    def organize_folder(self, folder):
        categories = {"Images": {".png", ".jpg", ".jpeg", ".gif"}, "Documents": {".txt", ".pdf", ".docx"}, "Videos": {".mp4", ".mov"}, "Archives": {".zip", ".7z", ".rar"}}
        for item in self.resolve_path(folder).iterdir():
            if item.is_file():
                category = next((name for name, extensions in categories.items() if item.suffix.lower() in extensions), "Other")
                self.create_folder(item.parent / category)
                shutil.move(str(item), str(item.parent / category / item.name))

    def read_clipboard(self):
        return self.root.clipboard_get()

    def handle_read_clipboard(self):
        try:
            text = self.read_clipboard()
        except tk.TclError:
            text = "Clipboard is empty."
        self.append_chat("assistant", text)
        return text

    def handle_summarize_clipboard(self):
        return self.process_user_text("Summarize this clipboard content: " + self.read_clipboard())

    def take_screenshot(self):
        if ImageGrab is None:
            return None
        target = APP_DIR / "Projects" / ("screenshot_%s.png" % datetime.now().strftime("%Y%m%d_%H%M%S"))
        target.parent.mkdir(exist_ok=True)
        ImageGrab.grab().save(target)
        return target

    def try_handle_utility_command(self, text):
        lowered = text.lower()
        if "screenshot" in lowered:
            self.append_chat("assistant", "Screenshot saved: %s" % self.take_screenshot())
            return True
        if "read clipboard" in lowered:
            self.handle_read_clipboard()
            return True
        return False

    def choose_workspace(self):
        return filedialog.askdirectory(parent=self.root, title="Choose workspace")

    def create_project(self):
        workspace = self.choose_workspace()
        if not workspace:
            return None
        name = simpledialog.askstring("New project", "Project name:", parent=self.root)
        if name:
            target = Path(workspace) / name
            target.mkdir(parents=True, exist_ok=True)
            (target / "README.md").write_text("# %s\n" % name, encoding="utf-8")
            return target
        return None


if __name__ == "__main__":
    Saathi().root.mainloop()