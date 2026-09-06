import tkinter as tk
from typing import Callable, Optional
from .theme import (
    COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_BORDER_GLOW,
    COLOR_CYAN, COLOR_EMERALD, COLOR_AMBER, COLOR_ERROR, COLOR_TEXT,
    COLOR_TEXT_MUTED, FONT_TITLE, FONT_HEADING, FONT_BODY, FONT_BOLD, FONT_MONO
)
from .chat_view import ChatStreamView

class ChatTabView(tk.Frame):
    """
    Dedicated Full-Screen Cognitive Chat Interface for Saathi AI.
    Conceived and designed by Pratham Prasad.
    Provides panoramic conversation stream, quick action chips, real-time voice feedback, and directive input.
    """
    def __init__(self, parent,
                 on_send_command: Callable[[str], None],
                 on_toggle_voice: Callable[[], None],
                 **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self.on_send_command = on_send_command
        self.on_toggle_voice = on_toggle_voice

        # 1. Header Bar
        self.header = tk.Frame(self, bg=COLOR_PANEL, padx=20, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.header.pack(fill="x", side="top")

        title_frame = tk.Frame(self.header, bg=COLOR_PANEL)
        title_frame.pack(side="left")

        tk.Label(
            title_frame,
            text="SAATHI AI // COGNITIVE DIALOGUE MATRIX",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_CYAN
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="PRATHAM PRASAD LABS // CONTINUOUS AURAL PERCEPTION & DUAL-CHANNEL COGNITION",
            font=("Segoe UI", 8),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT_MUTED
        ).pack(anchor="w")

        # Status Pills on Right
        status_frame = tk.Frame(self.header, bg=COLOR_PANEL)
        status_frame.pack(side="right")

        self.pill_model = tk.Label(
            status_frame,
            text="● LOCAL LLM ACTIVE",
            font=("Segoe UI", 8, "bold"),
            bg="#082240",
            fg="#38bdf8",
            padx=10,
            pady=4
        )
        self.pill_model.pack(side="left", padx=4)

        self.pill_voice = tk.Label(
            status_frame,
            text="🎙️ ALWAYS-ON VOICE: ACTIVE",
            font=("Segoe UI", 8, "bold"),
            bg="#062e20",
            fg=COLOR_EMERALD,
            padx=10,
            pady=4
        )
        self.pill_voice.pack(side="left", padx=4)

        # 2. Main Scrollable Chat Stream Container
        self.chat_container = tk.Frame(self, bg=COLOR_BG, padx=20, pady=12)
        self.chat_container.pack(fill="both", expand=True)

        self.chat_view = ChatStreamView(self.chat_container)
        self.chat_view.pack(fill="both", expand=True)

        # 3. Interactive Quick Suggestion Chips Row
        self.chips_frame = tk.Frame(self, bg=COLOR_BG, padx=20, pady=4)
        self.chips_frame.pack(fill="x", side="top")

        chips = [
            ("👋 Hello Saathi", "Hello Saathi! How are you doing today?"),
            ("🌐 Build Portfolio", "Build a futuristic portfolio website for an aerospace engineer"),
            ("📁 Organize Downloads", "Organize my Downloads folder"),
            ("🌦️ Weather Telemetry", "What is the current weather in New Delhi?"),
            ("💻 System Diagnostics", "Check system hardware and CPU diagnostics")
        ]

        tk.Label(self.chips_frame, text="QUICK DIRECTIVES ❯", font=("Segoe UI", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 8))

        for label, cmd in chips:
            btn = tk.Button(
                self.chips_frame,
                text=label,
                font=("Segoe UI", 8),
                bg="#061830",
                fg="#7dd3fc",
                activebackground="#0e3a6c",
                activeforeground="#ffffff",
                relief="flat",
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda c=cmd: self._send_quick_chip(c)
            )
            btn.pack(side="left", padx=3)

        # 4. Directive Input Bar & Controls (Bottom Deck)
        self.input_deck = tk.Frame(self, bg=COLOR_PANEL, padx=20, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.input_deck.pack(fill="x", side="bottom")

        # Voice Listening Toggle
        self.btn_voice = tk.Button(
            self.input_deck,
            text="🎙️ VOICE: ON",
            font=FONT_BOLD,
            bg="#062e20",
            fg=COLOR_EMERALD,
            activebackground=COLOR_EMERALD,
            activeforeground="#01040a",
            relief="flat",
            padx=14,
            pady=8,
            cursor="hand2",
            command=self._on_toggle_voice_click
        )
        self.btn_voice.pack(side="left", padx=(0, 10))

        # Main Text Directive Entry
        self.entry_input = tk.Entry(
            self.input_deck,
            bg="#040b1a",
            fg=COLOR_TEXT,
            insertbackground=COLOR_CYAN,
            font=("Segoe UI", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#0e3a6c"
        )
        self.entry_input.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.entry_input.bind("<Return>", lambda e: self._submit())

        # Transmit Directive Button
        self.btn_send = tk.Button(
            self.input_deck,
            text="TRANSMIT ❯",
            font=FONT_BOLD,
            bg=COLOR_CYAN,
            fg="#01040a",
            activebackground="#38bdf8",
            activeforeground="#01040a",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self._submit
        )
        self.btn_send.pack(side="left", padx=(0, 8))

        # Clear Chat Button
        self.btn_clear = tk.Button(
            self.input_deck,
            text="🗑️ CLEAR",
            font=("Segoe UI", 9, "bold"),
            bg="#181e2e",
            fg=COLOR_TEXT_MUTED,
            activebackground="#2a324b",
            activeforeground="#ffffff",
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.clear_chat
        )
        self.btn_clear.pack(side="left")

        # Initial Welcome in Chat
        self.append_message("system", "Saathi AI Cognitive Matrix Initialized. Continuous voice perception is active. Speak anytime or type your directive below.")

    def _submit(self):
        text = self.entry_input.get().strip()
        if text:
            self.entry_input.delete(0, "end")
            self.on_send_command(text)

    def _send_quick_chip(self, cmd: str):
        self.on_send_command(cmd)

    def _on_toggle_voice_click(self):
        self.on_toggle_voice()

    def set_voice_active(self, is_listening: bool):
        if is_listening:
            self.btn_voice.configure(text="🎙️ VOICE: ON", bg="#062e20", fg=COLOR_EMERALD)
            self.pill_voice.configure(text="🎙️ ALWAYS-ON VOICE: ACTIVE", bg="#062e20", fg=COLOR_EMERALD)
        else:
            self.btn_voice.configure(text="🎙️ VOICE: MUTED", bg="#2a1215", fg=COLOR_ERROR)
            self.pill_voice.configure(text="🎙️ VOICE: MUTED", bg="#2a1215", fg=COLOR_ERROR)

    def append_message(self, role: str, text: str):
        self.chat_view.append_message(role, text)

    def clear_chat(self):
        self.chat_view.clear()
        self.append_message("system", "Chat history cleared. Saathi AI standing by.")
