import tkinter as tk
from typing import Callable
from .theme import COLOR_PANEL, COLOR_BORDER, COLOR_CYAN, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_ASTRAL_VIOLET, COLOR_QUANTUM_TEAL

class NavigationRail(tk.Frame):
    """
    4th Civilization Left Navigation Rail for Saathi Operating Console.
    Features glowing active tab indicator and consciousness-tier color transitions.
    """
    def __init__(self, parent, on_navigate: Callable[[str], None], **kwargs):
        super().__init__(parent, bg=COLOR_PANEL, width=190, padx=0, pady=16, highlightthickness=1, highlightbackground=COLOR_BORDER, **kwargs)
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.active_tab = "core"
        self.buttons = {}
        self.glow_bars = {}

        nav_items = [
            ("core", "⬡ COMMAND CENTER"),
            ("chat", "💬 CHAT INTERFACE"),
            ("projects", "🌐 PROJECTS & WEB"),
            ("automations", "⚡ AUTOMATIONS"),
            ("memory", "🧠 NEURAL MEMORY"),
            ("system", "💻 SYSTEM & APPS"),
            ("settings", "⚙ CONFIGURATION")
        ]

        tk.Label(self, text="NAVIGATION", font=("Segoe UI", 8, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=14, pady=(0, 10))

        for key, label in nav_items:
            row = tk.Frame(self, bg=COLOR_PANEL)
            row.pack(fill="x", pady=2)

            # Left edge glow bar (3px astral violet stripe for active tab)
            glow = tk.Frame(row, bg=COLOR_PANEL, width=3)
            glow.pack(side="left", fill="y")
            self.glow_bars[key] = glow

            btn = tk.Button(
                row,
                text=label,
                font=("Segoe UI", 9, "bold"),
                bg=COLOR_PANEL,
                fg=COLOR_TEXT_MUTED,
                activebackground="#1a1040",
                activeforeground=COLOR_QUANTUM_TEAL,
                relief="flat",
                anchor="w",
                padx=10,
                pady=9,
                cursor="hand2",
                command=lambda k=key: self.select(k)
            )
            btn.pack(side="left", fill="x", expand=True)
            self.buttons[key] = btn

        self.select("core", notify=False)

    def select(self, key: str, notify: bool = True):
        self.active_tab = key
        for k, btn in self.buttons.items():
            if k == key:
                btn.configure(bg="#0f0a2a", fg=COLOR_CYAN)
                self.glow_bars[k].configure(bg=COLOR_ASTRAL_VIOLET)
            else:
                btn.configure(bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
                self.glow_bars[k].configure(bg=COLOR_PANEL)
        if notify:
            self.on_navigate(key)
