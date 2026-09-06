import tkinter as tk
from typing import Callable
from .theme import COLOR_PANEL, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_TEXT, COLOR_TEXT_MUTED

class NavigationRail(tk.Frame):
    """
    Futuristic Left Navigation Rail for Saathi Operating Console.
    Allows switching between Command Center, Tasks, Projects, Automations, Memory, System, and Settings.
    """
    def __init__(self, parent, on_navigate: Callable[[str], None], **kwargs):
        super().__init__(parent, bg=COLOR_PANEL, width=190, padx=8, pady=16, highlightthickness=1, highlightbackground=COLOR_BORDER, **kwargs)
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.active_tab = "core"
        self.buttons = {}

        nav_items = [
            ("core", "⬡ COMMAND CENTER"),
            ("tasks", "◈ TASK OBSERVER"),
            ("projects", "🌐 PROJECTS & WEB"),
            ("automations", "⚡ AUTOMATIONS"),
            ("memory", "🧠 NEURAL MEMORY"),
            ("system", "💻 SYSTEM & APPS"),
            ("settings", "⚙ CONFIGURATION")
        ]

        tk.Label(self, text="NAVIGATION", font=("Segoe UI", 8, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=10, pady=(0, 10))

        for key, label in nav_items:
            btn = tk.Button(
                self,
                text=label,
                font=("Segoe UI", 9, "bold"),
                bg=COLOR_PANEL,
                fg=COLOR_TEXT_MUTED,
                activebackground="#1e293b",
                activeforeground=COLOR_CYAN,
                relief="flat",
                anchor="w",
                padx=12,
                pady=9,
                cursor="hand2",
                command=lambda k=key: self.select(k)
            )
            btn.pack(fill="x", pady=2)
            self.buttons[key] = btn

        self.select("core", notify=False)

    def select(self, key: str, notify: bool = True):
        self.active_tab = key
        for k, btn in self.buttons.items():
            if k == key:
                btn.configure(bg="#13172b", fg=COLOR_CYAN)
            else:
                btn.configure(bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
        if notify:
            self.on_navigate(key)
