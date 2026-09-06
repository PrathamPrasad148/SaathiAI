import tkinter as tk
from tkinter import scrolledtext
from .theme import COLOR_BG, COLOR_CARD, COLOR_PANEL, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_AMBER, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_BODY, FONT_MONO

class ChatStreamView(tk.Frame):
    """Sleek scrollable conversation view with message tags and action cards."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)

        self.chat_log = scrolledtext.ScrolledText(
            self,
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            insertbackground=COLOR_CYAN,
            wrap="word",
            font=FONT_BODY,
            padx=14,
            pady=14,
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER
        )
        self.chat_log.pack(fill="both", expand=True)

        self.chat_log.tag_configure("user_hdr", foreground=COLOR_EMERALD, font=("Segoe UI", 10, "bold"))
        self.chat_log.tag_configure("user_body", foreground=COLOR_TEXT, font=("Segoe UI", 10))
        self.chat_log.tag_configure("asst_hdr", foreground=COLOR_CYAN, font=("Segoe UI", 10, "bold"))
        self.chat_log.tag_configure("asst_body", foreground=COLOR_TEXT, font=("Segoe UI", 10))
        self.chat_log.tag_configure("tool_action", foreground=COLOR_AMBER, font=FONT_MONO)
        self.chat_log.tag_configure("code_block", foreground="#a7f3d0", background="#0a0f1d", font=FONT_MONO)

        self.chat_log.configure(state="disabled")

    def append_message(self, role: str, text: str):
        self.chat_log.configure(state="normal")
        if role == "user":
            self.chat_log.insert("end", "You: ", "user_hdr")
            self.chat_log.insert("end", f"{text}\n\n", "user_body")
        elif role == "assistant":
            self.chat_log.insert("end", "Saathi: ", "asst_hdr")
            self.chat_log.insert("end", f"{text}\n\n", "asst_body")
        elif role == "action":
            self.chat_log.insert("end", f"? {text}\n", "tool_action")
        elif role == "system":
            self.chat_log.insert("end", f"?? {text}\n\n", "tool_action")
        self.chat_log.configure(state="disabled")
        self.chat_log.see("end")

    def clear(self):
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", "end")
        self.chat_log.configure(state="disabled")
