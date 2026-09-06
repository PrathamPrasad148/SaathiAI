import tkinter as tk
from typing import Callable, Optional
from .theme import COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_ERROR, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_BOLD
from .ai_core import AICoreVisualizer
from .chat_view import ChatStreamView

class CommandCenterView(tk.Frame):
    """
    Primary Jarvis Operating Console.
    Unifies the Dynamic AI Visualizer Core, Conversation Stream,
    and Bottom Command Deck with Voice PTT and Emergency Stop.
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

        # Top Center: Dynamic AI Visualizer Core
        self.core_frame = tk.Frame(self, bg=COLOR_BG, pady=4)
        self.core_frame.pack(fill="x")

        self.visualizer = AICoreVisualizer(self.core_frame, width=420, height=180)
        self.visualizer.pack(anchor="center")

        # Middle: Chat Stream View
        self.chat_view = ChatStreamView(self)
        self.chat_view.pack(fill="both", expand=True, padx=12, pady=(2, 8))

        # Bottom: Futuristic Command Deck
        deck = tk.Frame(self, bg=COLOR_PANEL, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        deck.pack(fill="x", side="bottom")

        # 1. Voice Button
        self.btn_mic = tk.Button(
            deck,
            text="?? Listen",
            font=FONT_BOLD,
            bg="#10192e",
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

        # 2. Text Input Box
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
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self._submit())

        # 3. Send Button
        btn_send = tk.Button(
            deck,
            text="Send",
            font=FONT_BOLD,
            bg=COLOR_EMERALD,
            fg="#04060c",
            activebackground="#00cc88",
            activeforeground="#04060c",
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._submit
        )
        btn_send.pack(side="left", padx=(0, 8))

        # 4. Emergency Stop / Interrupt Button
        btn_stop = tk.Button(
            deck,
            text="? STOP",
            font=FONT_BOLD,
            bg="#2a0f0f",
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
