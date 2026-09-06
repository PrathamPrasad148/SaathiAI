import tkinter as tk
from .theme import COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_HEADING

class SettingsView(tk.Frame):
    def __init__(self, parent, permission_manager, **kwargs):
        super().__init__(parent, bg=COLOR_BG, padx=24, pady=20, **kwargs)
        self.permissions = permission_manager

        # Header
        tk.Label(self, text="⚙ CONFIGURATION & TRUST MODEL", font=FONT_HEADING, bg=COLOR_BG, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 16))

        # Master Full System Control Card
        box_master = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=14, highlightthickness=1, highlightbackground=COLOR_BORDER)
        box_master.pack(fill="x", pady=(0, 16))

        master_top = tk.Frame(box_master, bg=COLOR_CARD)
        master_top.pack(fill="x", pady=(0, 8))

        tk.Label(master_top, text="⚡ AUTONOMOUS FULL SYSTEM CONTROL", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg=COLOR_CYAN).pack(side="left")
        
        self.lbl_master_status = tk.Label(master_top, text="", font=("Segoe UI", 9, "bold"), padx=8, pady=2)
        self.lbl_master_status.pack(side="right")

        tk.Label(
            box_master,
            text="When authorized, Saathi AI operates with complete sovereign control over your mouse, keyboard,\n"
                 "open application windows, system volume, process termination, and PowerShell execution.\n"
                 "Requires only one permission — no repeated confirmation popups during autonomous operation.",
            font=("Segoe UI", 9),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            justify="left"
        ).pack(anchor="w", pady=(0, 10))

        master_actions = tk.Frame(box_master, bg=COLOR_CARD)
        master_actions.pack(fill="x")

        self.btn_master_toggle = tk.Button(
            master_actions,
            text="",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self._toggle_master_permission
        )
        self.btn_master_toggle.pack(side="left")

        # Permissions box
        box_perm = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=14, highlightthickness=1, highlightbackground=COLOR_BORDER)
        box_perm.pack(fill="x", pady=(0, 16))

        tk.Label(box_perm, text="INDIVIDUAL ACTION RISK POLICY", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_EMERALD).pack(anchor="w", pady=(0, 8))
        tk.Label(
            box_perm,
            text="• Routine Safe Actions (reading files, opening websites, creating code): ALWAYS ALLOWED\n"
                 "• Modifying Operations (terminal execution, sending to recycle bin): ASK ONCE PER SESSION\n"
                 "• Destructive / High Risk Actions (process kill, PC power): REQUIRE CONFIRMATION UNLESS MASTER CONTROL IS ACTIVE",
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

        # Register listener and set initial UI state
        if hasattr(self.permissions, "add_listener"):
            self.permissions.add_listener(self._on_permission_change)
        self._update_master_ui(getattr(self.permissions, "master_system_control", False))

    def _on_permission_change(self, is_authorized: bool):
        self._update_master_ui(is_authorized)

    def _update_master_ui(self, authorized: bool):
        if authorized:
            self.lbl_master_status.configure(
                text="AUTHORIZED // FULL AUTONOMY",
                bg="#064e3b",
                fg="#34d399"
            )
            self.btn_master_toggle.configure(
                text="REVOKE SYSTEM CONTROL",
                bg="#7f1d1d",
                fg="#fca5a5",
                activebackground="#991b1b",
                activeforeground="#fef2f2"
            )
        else:
            self.lbl_master_status.configure(
                text="RESTRICTED // STANDBY",
                bg="#1e293b",
                fg="#94a3b8"
            )
            self.btn_master_toggle.configure(
                text="GRANT FULL SYSTEM CONTROL (SINGLE PERMISSION)",
                bg="#065f46",
                fg="#6ee7b7",
                activebackground="#047857",
                activeforeground="#a7f3d0"
            )

    def _toggle_master_permission(self):
        if hasattr(self.permissions, "toggle_master_control"):
            self.permissions.toggle_master_control(persist=True)

