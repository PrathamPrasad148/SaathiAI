import time
import socket
import calendar
import datetime
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from .theme import (
    COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD,
    COLOR_AMBER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_TEXT_DIM,
    FONT_BOLD, FONT_MONO, FONT_MONO_BOLD, FONT_HUD_TINY, FONT_HUD_LABEL
)
from automation.system import get_system_telemetry

class TopTelemetryBar(tk.Frame):
    """
    Pratham Prasad Top Telemetry & Chronometer HUD.
    Includes:
    - 31-day horizontal calendar matrix with active day highlight
    - Grid telemetry coordinates & local network IP
    - Pratham Prasad / Saathi OS 2.0 branding
    - System uptime counter & live precision chronometer
    - Sleek AI model selector
    """
    def __init__(self, parent, on_model_change: Optional[Callable[[str], None]] = None, on_toggle_master_control: Optional[Callable[[], None]] = None, on_toggle_fullscreen: Optional[Callable[[], None]] = None, **kwargs):
        super().__init__(parent, bg=COLOR_PANEL, highlightthickness=1, highlightbackground=COLOR_BORDER, **kwargs)
        self.on_model_change = on_model_change
        self.on_toggle_master_control = on_toggle_master_control
        self.on_toggle_fullscreen = on_toggle_fullscreen
        self.start_time = time.time()
        self.local_ip = self._get_local_ip()

        # 1. Top Calendar Day Matrix Ribbon
        self.cal_ribbon = tk.Frame(self, bg="#030814", height=22, padx=12, pady=2)
        self.cal_ribbon.pack(fill="x", side="top")
        self._build_calendar_strip()

        # 2. Main HUD Telemetry Row
        self.main_row = tk.Frame(self, bg=COLOR_PANEL, padx=14, pady=6)
        self.main_row.pack(fill="x", side="top")

        # Left: Identity, OS Branding & Uptime
        left_frame = tk.Frame(self.main_row, bg=COLOR_PANEL)
        left_frame.pack(side="left")

        tk.Label(left_frame, text="PRATHAM PRASAD", font=("Segoe UI", 9, "bold"), bg=COLOR_PANEL, fg="#38bdf8").pack(anchor="w")
        
        brand_row = tk.Frame(left_frame, bg=COLOR_PANEL)
        brand_row.pack(anchor="w")
        tk.Label(brand_row, text="SAATHI", font=("Segoe UI", 14, "bold"), bg=COLOR_PANEL, fg=COLOR_CYAN).pack(side="left")
        tk.Label(brand_row, text="MARK VII // OS 2.0", font=FONT_HUD_TINY, bg="#081b33", fg=COLOR_EMERALD, padx=6, pady=2).pack(side="left", padx=8)
        self.lbl_uptime = tk.Label(brand_row, text="UPTIME: 00:00:00", font=FONT_HUD_TINY, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
        self.lbl_uptime.pack(side="left", padx=6)

        # Center Telemetry: Grid Network, Telemetry Stats & Audio
        center_frame = tk.Frame(self.main_row, bg=COLOR_PANEL)
        center_frame.pack(side="left", expand=True)

        self.lbl_grid = tk.Label(
            center_frame,
            text=f"GRID: {self.local_ip} // NEW DELHI, IN // SECURE // ENCRYPTED",
            font=FONT_MONO,
            bg=COLOR_PANEL,
            fg="#38bdf8"
        )
        self.lbl_grid.pack(anchor="center")

        status_strip = tk.Frame(center_frame, bg=COLOR_PANEL)
        status_strip.pack(anchor="center", pady=(2, 0))

        self.lbl_cpu = tk.Label(status_strip, text="CPU: --%", font=FONT_HUD_TINY, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
        self.lbl_cpu.pack(side="left", padx=8)

        self.lbl_ram = tk.Label(status_strip, text="RAM: --%", font=FONT_HUD_TINY, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
        self.lbl_ram.pack(side="left", padx=8)

        self.lbl_gpu = tk.Label(status_strip, text="GPU: N/A", font=FONT_HUD_TINY, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED)
        self.lbl_gpu.pack(side="left", padx=8)

        self.lbl_mic = tk.Label(status_strip, text="ACOUSTIC: READY", font=FONT_HUD_TINY, bg="#05192d", fg=COLOR_EMERALD, padx=6, pady=1)
        self.lbl_mic.pack(side="left", padx=8)

        # Right: AI Model Selector, Fullscreen Button & Clock
        right_frame = tk.Frame(self.main_row, bg=COLOR_PANEL)
        right_frame.pack(side="right")

        tk.Label(right_frame, text="CORE NEURAL LINK:", font=FONT_HUD_TINY, bg=COLOR_PANEL, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 6))

        self.selected_model = tk.StringVar(value="Auto (Smart Agent)")
        models = ["Auto (Smart Agent)", "qwen2.5:7b", "qwen3:14b", "qwen3:4b-instruct"]
        self.combo_model = ttk.Combobox(right_frame, textvariable=self.selected_model, values=models, state="readonly", width=18)
        self.combo_model.pack(side="left", padx=(0, 10))
        self.combo_model.bind("<<ComboboxSelected>>", self._handle_model_change)

        if self.on_toggle_fullscreen:
            self.btn_fs = tk.Button(
                right_frame,
                text="[ ⛶ FULLSCREEN ]",
                font=FONT_HUD_TINY,
                bg="#082545",
                fg=COLOR_CYAN,
                activebackground=COLOR_CYAN,
                activeforeground="#000000",
                bd=1,
                relief="solid",
                cursor="hand2",
                command=self.on_toggle_fullscreen
            )
            self.btn_fs.pack(side="left", padx=(0, 10))

        self.lbl_date = tk.Label(right_frame, text="", font=FONT_HUD_TINY, bg=COLOR_PANEL, fg="#38bdf8")
        self.lbl_date.pack(side="left", padx=(0, 10))

        self.lbl_clock = tk.Label(right_frame, text="--:--:-- IST", font=FONT_MONO_BOLD, bg=COLOR_PANEL, fg=COLOR_CYAN)
        self.lbl_clock.pack(side="left")

        self.after(500, self._update_telemetry)

    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "192.168.1.104"

    def _build_calendar_strip(self):
        now = datetime.datetime.now()
        month_name = now.strftime("%B").upper()
        year = now.year
        today_day = now.day
        num_days = calendar.monthrange(year, now.month)[1]

        # Month header
        tk.Label(
            self.cal_ribbon,
            text=f"CALENDAR // {month_name} {year}:",
            font=FONT_HUD_TINY,
            bg="#030814",
            fg=COLOR_TEXT_MUTED
        ).pack(side="left", padx=(0, 12))

        for d in range(1, num_days + 1):
            day_str = f"{d:02d}"
            if d == today_day:
                # Active day highlight in glowing cyan
                lbl = tk.Label(
                    self.cal_ribbon,
                    text=day_str,
                    font=("Consolas", 8, "bold"),
                    bg=COLOR_CYAN,
                    fg="#02050e",
                    padx=3,
                    pady=0
                )
            else:
                lbl = tk.Label(
                    self.cal_ribbon,
                    text=day_str,
                    font=FONT_HUD_TINY,
                    bg="#030814",
                    fg="#334155"
                )
            lbl.pack(side="left", padx=2)

    def _handle_model_change(self, event=None):
        if self.on_model_change:
            self.on_model_change(self.selected_model.get())

    def _handle_master_control_click(self):
        if self.on_toggle_master_control:
            self.on_toggle_master_control()

    def set_master_control_status(self, authorized: bool):
        if hasattr(self, "btn_master_control"):
            if authorized:
                self.btn_master_control.configure(
                    text="⚡ FULL CONTROL: ACTIVE",
                    bg="#064e3b",
                    fg="#34d399",
                    activebackground="#047857",
                    activeforeground="#6ee7b7"
                )
            else:
                self.btn_master_control.configure(
                    text="🛡️ CONTROL: RESTRICTED",
                    bg="#0f172a",
                    fg="#94a3b8",
                    activebackground="#1e293b",
                    activeforeground="#38bdf8"
                )

    def set_mic_status(self, text: str, is_active: bool = False):
        self.lbl_mic.configure(
            text=f"ACOUSTIC: {text.upper()}",
            fg=COLOR_CYAN if is_active else COLOR_EMERALD,
            bg="#082b47" if is_active else "#05192d"
        )

    def _update_telemetry(self):
        try:
            now = datetime.datetime.now()
            self.lbl_clock.configure(text=now.strftime("%H:%M:%S IST"))
            self.lbl_date.configure(text=now.strftime("%a, %d %b").upper())

            # Uptime calculation
            elapsed = int(time.time() - self.start_time)
            hrs = elapsed // 3600
            mins = (elapsed % 3600) // 60
            secs = elapsed % 60
            self.lbl_uptime.configure(text=f"UPTIME: {hrs:02d}:{mins:02d}:{secs:02d}")

            info = get_system_telemetry()
            cpu = info.get("cpu_percent", 0.0)
            ram = info.get("ram_percent", 0.0)
            self.lbl_cpu.configure(text=f"CPU: {cpu}%")
            self.lbl_ram.configure(text=f"RAM: {ram}%")

            # GPU Telemetry
            try:
                from automation.hardware import get_gpu_telemetry
                gpu_info = get_gpu_telemetry()
                if gpu_info.get("available"):
                    temp = gpu_info.get("temp_c", 0)
                    v_used = gpu_info.get("vram_used_gb", 0.0)
                    v_tot = gpu_info.get("vram_total_gb", 0.0)
                    self.lbl_gpu.configure(text=f"GPU: {temp}°C // VRAM {v_used}/{v_tot} GB", fg=COLOR_CYAN)
                else:
                    self.lbl_gpu.configure(text="GPU: ACTIVE", fg=COLOR_TEXT_MUTED)
            except Exception:
                pass
        except Exception:
            pass
        self.after(1000, self._update_telemetry)
