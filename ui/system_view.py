import tkinter as tk
from .theme import COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_HEADING, FONT_MONO
from automation.processes import list_running_processes
from automation.windows import list_open_windows, focus_window_by_title, minimize_all_windows
from automation.system import get_system_telemetry

class SystemControlView(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_BG, padx=20, pady=16, **kwargs)

        # Header
        hdr = tk.Frame(self, bg=COLOR_BG)
        hdr.pack(fill="x", pady=(0, 12))

        tk.Label(hdr, text="💻 SYSTEM & PROCESS CONTROLLER", font=FONT_HEADING, bg=COLOR_BG, fg=COLOR_CYAN).pack(side="left")
        btn_min = tk.Button(hdr, text="Minimize All Windows", bg=COLOR_PANEL, fg=COLOR_TEXT, font=("Segoe UI", 9), relief="flat", padx=10, pady=4, command=minimize_all_windows, cursor="hand2")
        btn_min.pack(side="right")

        # Two-column layout: Left = Top Processes, Right = Open Windows
        cols = tk.Frame(self, bg=COLOR_BG)
        cols.pack(fill="both", expand=True)

        # Left: Processes
        left = tk.Frame(cols, bg=COLOR_CARD, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(left, text="TOP PROCESSES (BY RAM)", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_EMERALD).pack(anchor="w", pady=(0, 6))
        self.txt_procs = tk.Text(left, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED, font=FONT_MONO, height=14, relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.txt_procs.pack(fill="both", expand=True)

        # Right: Windows
        right = tk.Frame(cols, bg=COLOR_CARD, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        tk.Label(right, text="ACTIVE APPLICATION WINDOWS", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 6))
        self.win_list_frame = tk.Frame(right, bg=COLOR_CARD)
        self.win_list_frame.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        # Update procs
        procs = list_running_processes(14)
        lines = [f"{p['name'][:22]:24} RAM: {p['ram']}%  CPU: {p['cpu']}%" for p in procs]
        self.txt_procs.configure(state="normal")
        self.txt_procs.delete("1.0", "end")
        self.txt_procs.insert("end", "\n".join(lines))
        self.txt_procs.configure(state="disabled")

        # Update windows
        for w in self.win_list_frame.winfo_children():
            w.destroy()

        wins = list_open_windows()[:8]
        for win in wins:
            r = tk.Frame(self.win_list_frame, bg=COLOR_PANEL, padx=8, pady=4, highlightthickness=1, highlightbackground=COLOR_BORDER)
            r.pack(fill="x", pady=2)
            tk.Label(r, text=win['title'][:32], font=("Segoe UI", 8), bg=COLOR_PANEL, fg=COLOR_TEXT).pack(side="left")
            btn_focus = tk.Button(r, text="Focus", font=("Segoe UI", 7, "bold"), bg=COLOR_CYAN, fg="#04060c", relief="flat", padx=6, command=lambda t=win['title']: focus_window_by_title(t), cursor="hand2")
            btn_focus.pack(side="right")
