import tkinter as tk
from tkinter import scrolledtext
from typing import Dict, Any, List
from .theme import COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_AMBER, COLOR_ERROR, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_BOLD, FONT_MONO

class TaskObserverPanel(tk.Frame):
    """
    Dedicated Task Observer HUD.
    Displays active mission title, real-time step checklist,
    execution timeline checkmarks, and active tool indicators.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_PANEL, width=280, padx=14, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER, **kwargs)
        self.pack_propagate(False)

        # Header
        hdr = tk.Frame(self, bg=COLOR_PANEL)
        hdr.pack(fill="x", pady=(0, 10))

        tk.Label(hdr, text="? TASK OBSERVER", font=("Segoe UI", 11, "bold"), bg=COLOR_PANEL, fg=COLOR_CYAN).pack(side="left")
        self.badge_status = tk.Label(hdr, text="IDLE", font=("Segoe UI", 8, "bold"), bg="#1e293b", fg=COLOR_EMERALD, padx=6, pady=2)
        self.badge_status.pack(side="right")

        # Current Mission Box
        self.box_mission = tk.Frame(self, bg=COLOR_CARD, padx=10, pady=8, highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.box_mission.pack(fill="x", pady=(0, 10))

        self.lbl_mission_title = tk.Label(self.box_mission, text="No active task.", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT, wraplength=240, justify="left")
        self.lbl_mission_title.pack(anchor="w")

        # Steps Checklist Frame
        tk.Label(self, text="MISSION WORKFLOW", font=("Segoe UI", 8, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(6, 4))
        self.steps_container = tk.Frame(self, bg=COLOR_PANEL)
        self.steps_container.pack(fill="x", pady=(0, 10))

        # Real-time Tool Activity Feed
        tk.Label(self, text="OBSERVATION FEED", font=("Segoe UI", 8, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(6, 4))
        self.feed_log = scrolledtext.ScrolledText(
            self, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, font=FONT_MONO,
            wrap="word", height=8, relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER
        )
        self.feed_log.pack(fill="both", expand=True)
        self.feed_log.configure(state="disabled")

        self.step_labels = []

    def set_mission(self, title: str, steps: List[str]):
        self.lbl_mission_title.configure(text=title)
        self.badge_status.configure(text="RUNNING", fg=COLOR_CYAN, bg="#1e293b")

        # Clear existing step labels
        for w in self.steps_container.winfo_children():
            w.destroy()
        self.step_labels.clear()

        for idx, step_desc in enumerate(steps):
            f = tk.Frame(self.steps_container, bg=COLOR_PANEL)
            f.pack(fill="x", pady=2)
            icon = tk.Label(f, text="?", font=("Segoe UI", 9, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED, width=2)
            icon.pack(side="left")
            desc = tk.Label(f, text=step_desc, font=("Segoe UI", 9), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED, wraplength=220, justify="left")
            desc.pack(side="left", padx=4)
            self.step_labels.append((icon, desc))

    def update_step(self, index: int, status: str, detail: str = ""):
        if index < len(self.step_labels):
            icon_lbl, desc_lbl = self.step_labels[index]
            if status == "running":
                icon_lbl.configure(text="?", fg=COLOR_CYAN)
                desc_lbl.configure(fg=COLOR_TEXT)
            elif status == "success":
                icon_lbl.configure(text="?", fg=COLOR_EMERALD)
                desc_lbl.configure(fg=COLOR_EMERALD)
            elif status == "error":
                icon_lbl.configure(text="?", fg=COLOR_ERROR)
                desc_lbl.configure(fg=COLOR_ERROR)

        if detail:
            self.log_event(f"[{status.upper()}] {detail}")

    def complete_mission(self, message: str = "Mission Complete"):
        self.badge_status.configure(text="COMPLETED", fg=COLOR_EMERALD, bg="#064e3b")
        self.log_event(f"? {message}")

    def fail_mission(self, error: str):
        self.badge_status.configure(text="FAILED", fg=COLOR_ERROR, bg="#7f1d1d")
        self.log_event(f"? Error: {error}")

    def log_event(self, text: str):
        self.feed_log.configure(state="normal")
        self.feed_log.insert("end", f"{text}\n")
        self.feed_log.see("end")
        self.feed_log.configure(state="disabled")
