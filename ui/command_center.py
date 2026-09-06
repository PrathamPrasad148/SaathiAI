import tkinter as tk
from typing import Callable, Optional
from .theme import (
    COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_BORDER_GLOW,
    COLOR_CYAN, COLOR_EMERALD, COLOR_AMBER, COLOR_ERROR, COLOR_TEXT,
    COLOR_TEXT_MUTED, FONT_BOLD, FONT_HUD_TINY, FONT_HUD_LABEL
)
from .ai_core import AICoreVisualizer
from .chat_view import ChatStreamView

class CommandCenterView(tk.Frame):
    """
    Stark Industries Master Command Center Console.
    Unifies:
    - Master Mark VII Arc Reactor & Telemetry Visualizer Core
    - Tactical Protocol Launchers (Websites, Workflows, Memory, System)
    - High-Tech Chat Stream
    - Tactical Command Deck with Voice PTT and Emergency Abort
    """
    def __init__(self, parent,
                 on_send_command: Callable[[str], None],
                 on_toggle_voice: Callable[[], None],
                 on_stop_task: Callable[[], None],
                 **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self.on_send_command = on_send_command
        self.on_toggle_voice = on_toggle_voice
        self.on_stop_task = on_stop_task

        # 1. Top Section: Panoramic Stark Arc Reactor HUD
        self.core_frame = tk.Frame(self, bg=COLOR_BG, pady=2)
        self.core_frame.pack(fill="x")

        self.visualizer = AICoreVisualizer(self.core_frame, width=860, height=265)
        self.visualizer.pack(fill="x", expand=True, padx=6)

        # 2. Tactical Protocol Ribbon (Direct Protocol Launchers like the image)
        self.proto_ribbon = tk.Frame(self, bg=COLOR_PANEL, padx=8, pady=4, highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.proto_ribbon.pack(fill="x", padx=10, pady=(2, 6))

        tk.Label(
            self.proto_ribbon,
            text="TACTICAL PROTOCOLS:",
            font=FONT_HUD_TINY,
            bg=COLOR_PANEL,
            fg="#38bdf8"
        ).pack(side="left", padx=(4, 10))

        protocols = [
            ("🌐 GOD-MODE WEB", "Create a futuristic AI dashboard website"),
            ("⚡ RUN WORKFLOW", "Run workflow Morning Routine"),
            ("🧠 RECALL MEMORY", "What do you know about my preferences?"),
            ("💻 SYS HEALTH", "Check system resources and running processes"),
            ("🛡️ DIAGNOSTICS", "Run complete diagnostic check on all tools")
        ]

        for label, cmd in protocols:
            b = tk.Button(
                self.proto_ribbon,
                text=label,
                font=FONT_HUD_TINY,
                bg="#08182f",
                fg=COLOR_TEXT_MUTED,
                activebackground="#0e345e",
                activeforeground=COLOR_CYAN,
                relief="flat",
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda c=cmd: self.on_send_command(c)
            )
            b.pack(side="left", padx=3)

        # 3. Middle: Chat Stream View
        self.chat_view = ChatStreamView(self)
        self.chat_view.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        # 4. Bottom: Tactical Command Deck
        deck = tk.Frame(self, bg=COLOR_PANEL, padx=12, pady=8, highlightthickness=1, highlightbackground=COLOR_BORDER)
        deck.pack(fill="x", side="bottom", padx=10, pady=(0, 8))

        # Acoustic Sensors / Voice Button
        self.btn_mic = tk.Button(
            deck,
            text="🎙️ LISTEN",
            font=FONT_BOLD,
            bg="#091c36",
            fg=COLOR_CYAN,
            activebackground=COLOR_CYAN,
            activeforeground="#04060c",
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
            command=self.on_toggle_voice
        )
        self.btn_mic.pack(side="left", padx=(0, 10))

        # Tactical Input Entry
        self.input_entry = tk.Entry(
            deck,
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            insertbackground=COLOR_CYAN,
            font=("Segoe UI", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER
        )
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self._submit())

        # Transmit / Send Directive Button
        btn_send = tk.Button(
            deck,
            text="TRANSMIT ❯",
            font=FONT_BOLD,
            bg=COLOR_CYAN,
            fg="#02050e",
            activebackground="#38bdf8",
            activeforeground="#02050e",
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._submit
        )
        btn_send.pack(side="left", padx=(0, 8))

        # Emergency Abort Button
        btn_stop = tk.Button(
            deck,
            text="🛑 ABORT",
            font=FONT_BOLD,
            bg="#2a0d14",
            fg=COLOR_ERROR,
            activebackground=COLOR_ERROR,
            activeforeground="#ffffff",
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2",
            command=self.on_stop_task
        )
        btn_stop.pack(side="left")

    def _submit(self):
        txt = self.input_entry.get().strip()
        if txt:
            self.input_entry.delete(0, "end")
            self.on_send_command(txt)
