import time
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from .theme import COLOR_PANEL, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_BOLD, FONT_MONO_BOLD
from automation.system import get_system_telemetry

class TopTelemetryBar(tk.Frame):
    def __init__(self, parent, on_model_change: Optional[Callable[[str], None]] = None, **kwargs):
        super().__init__(parent, bg=COLOR_PANEL, height=46, padx=16, pady=8, highlightthickness=1, highlightbackground=COLOR_BORDER, **kwargs)
        self.on_model_change = on_model_change

        # Left: Identity & Core Status
        left_frame = tk.Frame(self, bg=COLOR_PANEL)
        left_frame.pack(side="left")

        tk.Label(left_frame, text="SAATHI", font=("Segoe UI", 16, "bold"), bg=COLOR_PANEL, fg=COLOR_EMERALD).pack(side="left")
        tk.Label(left_frame, text="OS 2.0", font=("Segoe UI", 8, "bold"), bg="#1e293b", fg=COLOR_CYAN, padx=6, pady=1).pack(side="left", padx=8)

        # Center Telemetry: CPU, RAM, Disk Gauges
        center_frame = tk.Frame(self, bg=COLOR_PANEL)
        center_frame.pack(side="left", padx=24)

        self.lbl_cpu = tk.Label(center_frame, text="CPU: --%", font=FONT_MONO_BOLD, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
        self.lbl_cpu.pack(side="left", padx=10)

        self.lbl_ram = tk.Label(center_frame, text="RAM: --%", font=FONT_MONO_BOLD, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
        self.lbl_ram.pack(side="left", padx=10)

        self.lbl_mic = tk.Label(center_frame, text="MIC: READY", font=FONT_MONO_BOLD, bg=COLOR_PANEL, fg=COLOR_EMERALD)
        self.lbl_mic.pack(side="left", padx=10)

        # Right: Model Selector & Clock
        right_frame = tk.Frame(self, bg=COLOR_PANEL)
        right_frame.pack(side="right")

        tk.Label(right_frame, text="MODEL:", font=("Segoe UI", 8, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 6))

        self.selected_model = tk.StringVar(value="Auto (Smart Agent)")
        models = ["Auto (Smart Agent)", "qwen2.5:7b", "qwen3:14b", "qwen3:4b-instruct"]
        self.combo_model = ttk.Combobox(right_frame, textvariable=self.selected_model, values=models, state="readonly", width=18)
        self.combo_model.pack(side="left", padx=(0, 14))
        self.combo_model.bind("<<ComboboxSelected>>", self._handle_model_change)

        self.lbl_clock = tk.Label(right_frame, text="--:-- IST", font=FONT_MONO_BOLD, bg=COLOR_PANEL, fg=COLOR_CYAN)
        self.lbl_clock.pack(side="left")

        self.after(500, self._update_telemetry)

    def _handle_model_change(self, event=None):
        if self.on_model_change:
            self.on_model_change(self.selected_model.get())

    def set_mic_status(self, text: str, is_active: bool = False):
        self.lbl_mic.configure(
            text=f"MIC: {text.upper()}",
            fg=COLOR_CYAN if is_active else COLOR_EMERALD
        )

    def _update_telemetry(self):
        try:
            info = get_system_telemetry()
            cpu = info.get("cpu_percent", 0.0)
            ram = info.get("ram_percent", 0.0)
            self.lbl_cpu.configure(text=f"CPU: {cpu}%")
            self.lbl_ram.configure(text=f"RAM: {ram}%")
            self.lbl_clock.configure(text=time.strftime("%H:%M:%S IST"))
        except Exception:
            pass
        self.after(1500, self._update_telemetry)
