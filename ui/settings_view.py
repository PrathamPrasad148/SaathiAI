import tkinter as tk
from .theme import COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_HEADING

class SettingsView(tk.Frame):
    def __init__(self, parent, permission_manager, **kwargs):
        super().__init__(parent, bg=COLOR_BG, padx=24, pady=20, **kwargs)
        self.permissions = permission_manager

        # Header
        tk.Label(self, text="⚙ CONFIGURATION & TRUST MODEL", font=FONT_HEADING, bg=COLOR_BG, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 16))

        # Permissions box
        box_perm = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=14, highlightthickness=1, highlightbackground=COLOR_BORDER)
        box_perm.pack(fill="x", pady=(0, 16))

        tk.Label(box_perm, text="AUTHORIZATION & RISK POLICY", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_EMERALD).pack(anchor="w", pady=(0, 8))
        tk.Label(
            box_perm,
            text="• Routine Safe Actions (reading files, opening websites, creating code): ALWAYS ALLOWED\n"
                 "• Modifying Operations (terminal execution, sending to recycle bin): ASK ONCE PER SESSION\n"
                 "• Destructive / High Risk Actions (process kill): REQUIRE CONFIRMATION",
            font=("Segoe UI", 9),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            justify="left"
        ).pack(anchor="w")

        # Keyboard shortcuts box
        box_keys = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=14, highlightthickness=1, highlightbackground=COLOR_BORDER)
        box_keys.pack(fill="x", pady=(0, 16))

        tk.Label(box_keys, text="KEYBOARD SHORTCUTS", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 8))
        tk.Label(
            box_keys,
            text="• Enter          ❯ Send message or direct command\n"
                 "• Esc            ❯ Immediately STOP active task & voice synthesis\n"
                 "• Space (Focus)  ❯ Push-to-Talk voice capture\n"
                 "• Ctrl + L       ❯ Clear conversation stream",
            font=("Consolas", 9),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            justify="left"
        ).pack(anchor="w")
