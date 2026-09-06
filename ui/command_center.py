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
    Pratham Prasad Master Command Console.
    Unifies:
    - Master Saathi Holographic HUD Engine (Panoramic Canvas)
    - Interactive HUD Nodes (Clicking on Games, Programs, News, Weather triggers directives)
    - Collapsible Holographic HUD Chat Feed
    - Tactical Command Deck with Voice PTT and Emergency Abort
    """
    def __init__(self, parent,
                 on_send_command: Callable[[str], None],
                 on_toggle_voice: Callable[[], None],
                 on_stop_task: Callable[[], None],
                 **kwargs):
        super().__init__(parent, bg="#01040a", **kwargs)
        self.on_send_command = on_send_command
        self.on_toggle_voice = on_toggle_voice
        self.on_stop_task = on_stop_task
        self.chat_visible = False

        # 1. Master Panoramic Saathi HUD Canvas
        self.hud_container = tk.Frame(self, bg="#01040a")
        self.hud_container.pack(fill="both", expand=True)

        self.visualizer = AICoreVisualizer(
            self.hud_container,
            width=1380,
            height=660,
            on_node_click=self._handle_hud_click
        )
        self.visualizer.pack(fill="both", expand=True)

        # 2. Collapsible Holographic HUD Chat Feed (Glass Terminal)
        self.chat_frame = tk.Frame(self, bg="#040b1a", height=180, highlightthickness=1, highlightbackground="#0c2847")
        self.chat_view = ChatStreamView(self.chat_frame)
        self.chat_view.pack(fill="both", expand=True, padx=8, pady=4)
        # By default, keep collapsed to display 100% pure Pratham Prasad Cognitive HUD, but readily toggleable

        # 3. Bottom Tactical Directive Deck
        self.deck = tk.Frame(self, bg="#040b1a", padx=12, pady=8, highlightthickness=1, highlightbackground="#0c2847")
        self.deck.pack(fill="x", side="bottom")

        # Acoustic Voice Sensor Button
        self.btn_mic = tk.Button(
            self.deck,
            text="🎙️ LISTEN",
            font=FONT_BOLD,
            bg="#081e3a",
            fg=COLOR_CYAN,
            activebackground=COLOR_CYAN,
            activeforeground="#01040a",
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
            command=self.on_toggle_voice
        )
        self.btn_mic.pack(side="left", padx=(0, 10))

        # Directive Input Entry
        self.input_entry = tk.Entry(
            self.deck,
            bg="#061326",
            fg=COLOR_TEXT,
            insertbackground=COLOR_CYAN,
            font=("Segoe UI", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#0e3a6c"
        )
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self._submit())

        # Transmit Directive Button
        btn_send = tk.Button(
            self.deck,
            text="TRANSMIT ❯",
            font=FONT_BOLD,
            bg=COLOR_CYAN,
            fg="#01040a",
            activebackground="#38bdf8",
            activeforeground="#01040a",
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._submit
        )
        btn_send.pack(side="left", padx=(0, 8))

        # Toggle HUD Chat Stream Button
        self.btn_toggle_chat = tk.Button(
            self.deck,
            text="💬 HUD LOG",
            font=FONT_HUD_LABEL,
            bg="#082240",
            fg="#38bdf8",
            activebackground="#0e3a6c",
            activeforeground="#00f0ff",
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2",
            command=self.toggle_chat_drawer
        )
        self.btn_toggle_chat.pack(side="left", padx=(0, 8))

        # Emergency Abort Button
        btn_stop = tk.Button(
            self.deck,
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

    def toggle_chat_drawer(self):
        if self.chat_visible:
            self.chat_frame.pack_forget()
            self.chat_visible = False
            self.btn_toggle_chat.configure(text="💬 HUD LOG", bg="#082240", fg="#38bdf8")
        else:
            self.chat_frame.pack(fill="x", side="bottom", before=self.deck)
            self.chat_visible = True
            self.btn_toggle_chat.configure(text="▲ HIDE LOG", bg="#00f0ff", fg="#01040a")

    def _submit(self):
        txt = self.input_entry.get().strip()
        if txt:
            self.input_entry.delete(0, "end")
            # Automatically show chat drawer when user transmits so they see response
            if not self.chat_visible:
                self.toggle_chat_drawer()
            self.on_send_command(txt)

    def _handle_hud_click(self, x: int, y: int):
        """Handle interactive clicks on HUD widgets."""
        w = self.visualizer.width
        h = self.visualizer.height
        cx = w * 0.47
        cy = h * 0.46

        # Check click near Bottom Launchers (Games, Programs, Skydrive, Electronics)
        if cx - 80 <= x <= cx + 60 and cy + 180 <= y <= cy + 250:
            rel_y = y - (cy + 180)
            if rel_y < 18:
                self.on_send_command("List installed games and launch gaming protocol")
            elif rel_y < 36:
                self.on_send_command("List open windows and running programs")
            elif rel_y < 54:
                self.on_send_command("Open Projects and documents folder")
            else:
                self.on_send_command("Check system hardware and CPU diagnostics")

        # Check click near Weather station (Far Right)
        elif x >= w - 210 and y <= 350:
            self.on_send_command("Give me a detailed weather report and atmospheric conditions")

        # Check click near News Feed (Mid Right)
        elif cx + 250 <= x <= w - 220 and cy - 140 <= y <= cy:
            self.on_send_command("Summarize today's latest tech news and active protocols")
