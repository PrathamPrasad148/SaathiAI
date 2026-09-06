"""
Saathi AI — Agentic Desktop Operating Interface
Created by Pratham Prasad: Intelligent Presence for Windows with Autonomous Computer Control,
Live AI Visualizer Core, Real-Time Task Observer, and Non-Blocking Voice Pipeline.
"""
from __future__ import annotations

import os
import sys
import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# Core Subsystems
from memory.engine import MemoryEngine
from automations.engine import AutomationEngine
from automation.controller import ComputerController
from tools.registry import ToolRegistry
from tools.permissions import PermissionManager
from tools.executor import ToolExecutor
from tools.builtin import register_all_builtin_tools
from voice.engine import VoiceEngine
from agent.planner import AgentPlanner
from ui.app import SaathiApp

# Directory Paths
APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
PROJECTS_DIR = APP_DIR / "Projects"
REMINDERS_FILE = DATA_DIR / "reminders.json"
NOTES_FILE = DATA_DIR / "notes.txt"
PERMISSIONS_FILE = DATA_DIR / "permissions.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

class ReminderManager:
    """Manages scheduled desktop reminders with persistence and speech alerts."""
    def __init__(self, file_path: Path, on_due_callback=None):
        self.file_path = file_path
        self.on_due_callback = on_due_callback
        self.reminders = []
        self.load()

    def load(self):
        try:
            if self.file_path.exists():
                self.reminders = json.loads(self.file_path.read_text(encoding="utf-8"))
            else:
                self.reminders = []
        except Exception:
            self.reminders = []

    def save(self):
        try:
            self.file_path.write_text(json.dumps(self.reminders, indent=2), encoding="utf-8")
        except OSError:
            pass

    def add_reminder(self, text: str, minutes: int) -> dict:
        when_time = datetime.now() + timedelta(minutes=int(minutes))
        rem = {"text": text, "when": when_time.isoformat(), "done": False}
        self.reminders.append(rem)
        self.save()
        return rem

    def check_due(self) -> list[str]:
        now = datetime.now()
        triggered = []
        for r in self.reminders:
            if not r.get("done"):
                try:
                    if datetime.fromisoformat(r["when"]) <= now:
                        r["done"] = True
                        triggered.append(r["text"])
                except Exception:
                    pass
        if triggered:
            self.save()
        return triggered

def main():
    root = tk.Tk()

    # 1. Initialize Memory & Automations
    memory_engine = MemoryEngine(DATA_DIR / "memory.json")
    automation_engine = AutomationEngine(DATA_DIR / "automations.json")

    # 2. Initialize Computer Controller
    controller = ComputerController(PROJECTS_DIR)

    # 3. Initialize Reminders
    reminder_mgr = ReminderManager(REMINDERS_FILE)

    # 4. Initialize Tool Framework
    permission_mgr = PermissionManager(PERMISSIONS_FILE)
    tool_registry = ToolRegistry()

    def ask_confirm_tool(tool_name: str) -> bool:
        granted = messagebox.askyesno(
            "Saathi Sovereign Security Authorization",
            f"Saathi AI requests authorization to execute '{tool_name}'.\n\n"
            "Would you like to grant Saathi AI FULL SYSTEM CONTROL?\n\n"
            "• Yes: Grant Full System Control (one permission — all mouse, keyboard, and system commands authorized without further popups)\n"
            "• No: Cancel this action",
            parent=root
        )
        if granted:
            permission_mgr.authorize_master_control(persist=True)
            return True
        return False

    tool_executor = ToolExecutor(
        registry=tool_registry,
        permissions=permission_mgr,
        confirmation_dialog=ask_confirm_tool
    )

    # Register all Built-in Tools (Files, System, Web, Voice, Vision, Memory)
    register_all_builtin_tools(
        registry=tool_registry,
        app_dir=APP_DIR,
        reminder_mgr=reminder_mgr,
        notes_file=NOTES_FILE,
        memory_engine=memory_engine,
        automation_engine=automation_engine
    )

    # Bind tool executor to automation engine
    automation_engine.tool_executor = tool_executor.execute

    # 5. Initialize Voice Engine
    voice_engine = VoiceEngine()

    # 6. Initialize Agent Planner
    agent_planner = AgentPlanner(
        tool_registry=tool_registry,
        tool_executor=tool_executor,
        memory_engine=memory_engine,
        automation_engine=automation_engine,
        app_dir=APP_DIR,
        projects_dir=PROJECTS_DIR,
        permission_manager=permission_mgr
    )

    # 7. Initialize Master UI
    app = SaathiApp(
        root=root,
        app_dir=APP_DIR,
        projects_dir=PROJECTS_DIR,
        agent_planner=agent_planner,
        voice_engine=voice_engine,
        memory_engine=memory_engine,
        automation_engine=automation_engine,
        permission_manager=permission_mgr
    )

    # 8. Reminders Polling Loop
    def poll_reminders():
        due = reminder_mgr.check_due()
        for text in due:
            alert = f"? REMINDER: {text}"
            app.views["core"].chat_view.append_message("assistant", alert)
            voice_engine.tts.speak(f"Bhai, reminder: {text}")
        root.after(20000, poll_reminders)

    root.after(10000, poll_reminders)

    # 9. Tray Icon Support
    try:
        import pystray
        from PIL import Image
        img = Image.new("RGB", (64, 64), "#00ffaa")
        menu = pystray.Menu(
            pystray.MenuItem("Show Saathi", lambda icon, item: root.after(0, lambda: (root.deiconify(), root.lift()))),
            pystray.MenuItem("Quit", lambda icon, item: root.after(0, root.destroy))
        )
        tray_icon = pystray.Icon("saathi", img, "Saathi AI OS", menu)
        threading.Thread(target=tray_icon.run, daemon=True).start()
    except Exception:
        pass

    # 10. Start Main Application Loop
    root.mainloop()

if __name__ == "__main__":
    main()
