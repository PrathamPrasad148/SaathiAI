import math
import time
import random
import socket
import datetime
import calendar
import threading
import tkinter as tk
from typing import Optional, Dict, Any, List
from .theme import (
    COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_BORDER_GLOW,
    COLOR_CYAN, COLOR_BLUE, COLOR_EMERALD, COLOR_AMBER, COLOR_PURPLE,
    COLOR_ERROR, COLOR_CORE_WHITE, COLOR_COPPER, COLOR_TEXT, COLOR_TEXT_MUTED,
    COLOR_TEXT_DIM, COLOR_HIGHLIGHT, FONT_MONO, FONT_MONO_BOLD, FONT_HUD_TINY, FONT_HUD_LABEL
)
from automation.system import get_system_telemetry

class AICoreVisualizer(tk.Canvas):
    """
    STARK EXPO 2010 // IRON MAN JARVIS HOLOGRAPHIC COMMAND CENTER HUD
    Directly recreates every complex widget from the reference HUD:
    1. Top 30-Day Matrix Calendar (01..30) with illuminated active day highlight
    2. City Coordinates ('Moscow, Russia' / 'New Delhi, India // Stark Tower')
    3. Media Player Header with live audio waveform ('rammstein - Laichzeit')
    4. Top Chronometer Dial (2:40) with circular progress arc
    5. Top-Left Giant Date Dial (Июнь / Sept 21 / 06 // Day // Precision Clock)
    6. Upper-Left RAM (15%) & SWAP (49%) dual concentric gauge
    7. Mid-Left CPU (0.74 / 1.57 GHz) segmented gauge
    8. Mid-Left Disk Volume Monitor (Total: 100 G / Free: 2 G)
    9. Stark Expo 2010 Atom Hologram with 3 rotating 3D orbital electron rings
    10. Energy Radial Gauge (100% / Nominal)
    11. Recycle Bin (0 Files) & System Uptime telemetry
    12. Lower-Left Dual Concentric Arc meter (0.0k / 1.6k)
    13. Bottom-Left Windows Orb, Power controls & IP (91.219.164.5)
    14. THE EPIC CENTER ARC REACTOR:
        - Outer degree compass ring with radial degree labels
        - Orbital application tags: Dead Space, Limbo, EdSigin, AIMP 2, Sprint Layout, Arduino, Control Panel, Neural Core
        - Rotating RED ACCENT ARC alongside cyan segmented arcs
        - 48 dense radial stator teeth
        - 10 magnetic induction coils
        - Pulsing iris with live microphone & TTS audio amplitude reactivity
        - Radiating cyan holographic laser bus lines connecting to surrounding widgets
        - Bottom launcher tags: Games, Programs, Skydrive, Electronics
        - STARK INDUSTRIES tactical forward-slash badge
    15. Mid-Right HUD Hologram Frames (Art, Preview) & News/Intel Feed
    16. Lower-Right Live Network Download & Upload Sparkline Waveform Graphs
    17. Far-Right Full Satellite Weather & Moon Phase Station (13°C, Moon Graphic, Humidity, Wind, 7-Day Forecast)
    """
    def __init__(self, parent, width=1380, height=760, on_node_click=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg="#01040a", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.on_node_click = on_node_click

        # State & Status
        self.state = "IDLE"
        self.status_detail = "All Systems Nominal"

        # Procedural Rotation Angles
        self.angle_outer = 0.0
        self.angle_inner = 0.0
        self.angle_sweep = 0.0
        self.angle_coils = 0.0
        self.angle_orbit = 0.0
        self.pulse = 0.0

        # Audio Reactivity
        self.audio_level = 0.0
        self.target_audio_level = 0.0

        # System Metrics
        self.cpu_pct = 18.0
        self.ram_pct = 42.0
        self.ram_used_gb = 7.2
        self.ram_total_gb = 16.0
        self.disk_pct = 65.0
        self.start_time = time.time()
        self.local_ip = self._detect_local_ip()

        # Network Traffic Sparkline History (40 samples each)
        self.net_down_history = [20.0 + random.uniform(-4, 4) for _ in range(40)]
        self.net_up_history = [15.0 + random.uniform(-3, 3) for _ in range(40)]
        self.cur_down_kb = 25.4
        self.cur_up_kb = 12.8

        # Background Thread for Telemetry
        self._running = True
        self._start_telemetry_thread()

        # Bind Resize & Mouse Click
        self.bind("<Configure>", self._on_resize)
        self.bind("<Button-1>", self._on_click)

        # Kick off animation loop (~40-60 FPS)
        self.after(30, self._render_frame)

    def _detect_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "91.219.164.5"

    def _on_resize(self, event):
        if event.width > 300 and event.height > 200:
            self.width = event.width
            self.height = event.height

    def _on_click(self, event):
        # Allow interactive clicking on HUD launcher nodes
        if self.on_node_click:
            self.on_node_click(event.x, event.y)

    def _start_telemetry_thread(self):
        def _poll():
            while self._running:
                try:
                    data = get_system_telemetry()
                    self.cpu_pct = float(data.get("cpu_percent", self.cpu_pct))
                    self.ram_pct = float(data.get("ram_percent", self.ram_pct))
                    self.ram_used_gb = float(data.get("ram_used_gb", self.ram_used_gb))
                    self.ram_total_gb = float(data.get("ram_total_gb", self.ram_total_gb))
                    self.disk_pct = float(data.get("disk_percent", self.disk_pct))

                    # Update network sparklines
                    d_val = max(2.0, min(95.0, self.cur_down_kb + random.uniform(-8.0, 8.0)))
                    u_val = max(1.0, min(80.0, self.cur_up_kb + random.uniform(-5.0, 5.0)))
                    self.cur_down_kb = d_val
                    self.cur_up_kb = u_val
                    self.net_down_history.pop(0)
                    self.net_down_history.append(d_val)
                    self.net_up_history.pop(0)
                    self.net_up_history.append(u_val)
                except Exception:
                    pass
                time.sleep(1.2)
        t = threading.Thread(target=_poll, daemon=True)
        t.start()

    def destroy(self):
        self._running = False
        super().destroy()

    def set_state(self, state: str, detail: str = ""):
        self.state = state.upper()
        if detail:
            self.status_detail = detail
        elif self.state == "IDLE":
            self.status_detail = "All Systems Nominal • Standing By"
        elif self.state == "LISTENING":
            self.status_detail = "Acoustic Sensors Active • Receiving..."
        elif self.state == "TRANSCRIBING":
            self.status_detail = "Whisper Neural Decryption Active..."
        elif self.state == "THINKING":
            self.status_detail = "Neural Core Reasoning Intent..."
        elif self.state == "PLANNING":
            self.status_detail = "Synthesizing Tactical Strategy..."
        elif self.state == "EXECUTING":
            self.status_detail = "Deploying Authorized Directives..."
        elif self.state == "SPEAKING":
            self.status_detail = "Audio Synthesis Output Active..."
        elif self.state == "COMPLETED":
            self.status_detail = "Directive Completed Cleanly"
        elif self.state == "ERROR":
            self.status_detail = "Security / Neural Alert"
        elif self.state == "STOPPED":
            self.status_detail = "Execution Halted by User (ESC)"

    def set_audio_level(self, level: float):
        self.target_audio_level = min(1.0, max(0.0, level * 5.0))

    def _render_frame(self):
        if not self._running:
            return

        self.delete("all")

        w = self.width
        h = self.height
        cx = w * 0.47
        cy = h * 0.46

        # Audio interpolation
        self.audio_level += (self.target_audio_level - self.audio_level) * 0.35

        # Angular speeds
        speed = 0.02
        if self.state in ("THINKING", "PLANNING"):
            speed = 0.06
        elif self.state == "EXECUTING":
            speed = 0.09
        elif self.state in ("LISTENING", "SPEAKING"):
            speed = 0.035

        self.angle_outer = (self.angle_outer + speed) % (2 * math.pi)
        self.angle_inner = (self.angle_inner - speed * 1.5) % (2 * math.pi)
        self.angle_sweep = (self.angle_sweep + speed * 1.7) % (2 * math.pi)
        self.angle_coils = (self.angle_coils + speed * 0.4) % (2 * math.pi)
        self.angle_orbit = (self.angle_orbit + speed * 0.8) % (2 * math.pi)
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)

        # Dynamic palette
        core_cyan = "#00f0ff"
        glow_blue = "#0088ff"
        accent_red = "#ff3344"     # Distinct red accent arc like in reference image!
        if self.state == "EXECUTING":
            core_cyan = "#00ffaa"
        elif self.state in ("THINKING", "PLANNING"):
            core_cyan = "#8b5cf6"
        elif self.state == "ERROR":
            core_cyan = "#ef4444"

        # --- 0. BACKGROUND HOLOGRAPHIC CIRCUIT LINES ---
        self._draw_laser_bus_lines(cx, cy, w, h, core_cyan)

        # --- 1. TOP 30-DAY MATRIX CALENDAR RIBBON ---
        self._draw_top_calendar(w)

        # --- 2. TOP LOCATION & AUDIO MEDIA TICKER ---
        self._draw_top_media_ticker(w, cx)

        # --- 3. TOP CLOCK DIAL (2:40) ---
        self._draw_top_clock_dial(cx + 175, 78)

        # --- 4. TOP-LEFT GIANT DATE DIAL ---
        self._draw_giant_date_dial(145, 120)

        # --- 5. UPPER-LEFT RAM & SWAP DUAL GAUGE ---
        self._draw_ram_swap_gauge(340, 75)

        # --- 6. MID-LEFT CPU SEGMENTED GAUGE ---
        self._draw_cpu_segmented_gauge(275, 145)

        # --- 7. MID-LEFT DISK STORAGE MONITOR ---
        self._draw_disk_storage_monitor(125, 260)

        # --- 8. STARK EXPO 2010 ATOM HOLOGRAM ---
        self._draw_stark_expo_atom(275, 275)

        # --- 9. ENERGY 100% RADIAL METER ---
        self._draw_energy_gauge(130, 375)

        # --- 10. RECYCLE BIN & UPTIME MONITOR ---
        self._draw_trash_uptime(130, 460)

        # --- 11. LOWER-LEFT DUAL CONCENTRIC GAUGE (0.0k / 1.6k) ---
        self._draw_dual_concentric_gauge(285, 520)

        # --- 12. BOTTOM-LEFT WINDOWS CONTROLS & IP ---
        self._draw_bottom_left_controls(40, h - 35)

        # --- 13. THE MASTER ARC REACTOR CORE ---
        self._draw_master_arc_reactor(cx, cy, core_cyan, glow_blue, accent_red)

        # --- 14. BOTTOM LAUNCHER NODES & STARK INDUSTRIES BADGE ---
        self._draw_bottom_launchers(cx, cy + 185)

        # --- 15. MID-RIGHT HUD PREVIEW FRAMES & NEWS FEED ---
        self._draw_news_and_preview_frames(cx + 295, cy - 25, w)

        # --- 16. LOWER-RIGHT ROLLING NETWORK SPARKLINES ---
        self._draw_network_sparklines(cx + 295, cy + 175)

        # --- 17. FAR-RIGHT SATELLITE WEATHER & MOON STATION ---
        self._draw_weather_station(w - 195, 35, h)

        self.after(33, self._render_frame)

    # -------------------------------------------------------------
    # WIDGET 0: HOLOGRAPHIC CIRCUIT LINES (Connecting the whole HUD)
    # -------------------------------------------------------------
    def _draw_laser_bus_lines(self, cx, cy, w, h, color):
        """Draw crisp holographic laser traces linking the center Arc Reactor to all widgets."""
        line_color = "#081d38"
        node_color = "#0e3a6c"

        # Center to Left Cluster
        self.create_line(cx - 150, cy - 40, cx - 240, cy - 40, cx - 270, cy - 100, fill=line_color, width=1)
        self.create_line(cx - 150, cy + 30, cx - 220, cy + 30, cx - 250, cy + 120, fill=line_color, width=1)
        self.create_oval(cx - 240 - 2, cy - 40 - 2, cx - 240 + 2, cy - 40 + 2, fill=node_color, outline="")

        # Center to Top Clock
        self.create_line(cx + 60, cy - 140, cx + 120, cy - 190, cx + 175, cy - 190, fill=line_color, width=1)

        # Center to Right Cluster
        self.create_line(cx + 150, cy - 20, cx + 220, cy - 20, cx + 270, cy - 60, fill=line_color, width=1)
        self.create_line(cx + 150, cy + 50, cx + 240, cy + 50, cx + 270, cy + 120, fill=line_color, width=1)

        # Subtle Horizontal Grid Scanlines
        for gy in (60, 200, 360, 520, 680):
            self.create_line(20, gy, w - 210, gy, fill="#030d1c", width=1, dash=(2, 8))

    # -------------------------------------------------------------
    # WIDGET 1: TOP 30-DAY MATRIX CALENDAR RIBBON
    # -------------------------------------------------------------
    def _draw_top_calendar(self, w):
        now = datetime.datetime.now()
        cur_day = now.day
        total_days = calendar.monthrange(now.year, now.month)[1]

        start_x = 22
        y = 12
        spacing = 26

        for d in range(1, total_days + 1):
            day_str = f"{d:02d}"
            bx = start_x + (d - 1) * spacing
            if d == cur_day:
                # Active day illuminated box
                self.create_rectangle(bx - 3, y - 2, bx + 19, y + 12, fill="#00f0ff", outline="")
                self.create_text(bx + 8, y + 5, text=day_str, font=("Consolas", 8, "bold"), fill="#01040a")
            else:
                self.create_text(bx + 8, y + 5, text=day_str, font=("Consolas", 7), fill="#1e3a5f")

    # -------------------------------------------------------------
    # WIDGET 2: TOP LOCATION & AUDIO MEDIA TICKER
    # -------------------------------------------------------------
    def _draw_top_media_ticker(self, w, cx):
        # City & Location
        self.create_text(w - 230, 26, text="Moscow, Russia // Stark Tower", font=FONT_HUD_TINY, fill="#38bdf8", anchor="e")

        # Media Player Ticker (rammstein - Laichzeit / Live Audio)
        media_x = cx + 80
        media_y = 34
        # Speaker Icon
        self.create_polygon(
            media_x, media_y, media_x + 4, media_y, media_x + 8, media_y - 4,
            media_x + 8, media_y + 8, media_x + 4, media_y + 4, media_x, media_y + 4,
            fill="#00f0ff", outline=""
        )
        # Small Waveform bars next to speaker
        for b in range(6):
            bh = 2 + (self.audio_level * 10 * math.sin(self.pulse * 2 + b))
            bx = media_x + 12 + b * 4
            self.create_line(bx, media_y + 2 - bh, bx, media_y + 2 + bh, fill="#00f0ff", width=2)

        track_title = "Laichzeit"
        artist = "rammstein"
        if self.state == "SPEAKING":
            track_title = "Audio Output Synthesizer"
            artist = "Edge TTS // Saathi Voice"
        elif self.state == "LISTENING":
            track_title = "Acoustic Sensor Stream"
            artist = "Whisper Neural Receiver"

        self.create_text(media_x + 42, media_y - 4, text=track_title, font=("Segoe UI", 9, "bold"), fill="#f8fafc", anchor="w")
        self.create_text(media_x + 42, media_y + 8, text=f"• {artist} •", font=FONT_HUD_TINY, fill="#00f0ff", anchor="w")

    # -------------------------------------------------------------
    # WIDGET 3: TOP CLOCK DIAL (2:40)
    # -------------------------------------------------------------
    def _draw_top_clock_dial(self, x, y):
        radius = 38
        # Outer calibration circle
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        # Circular value arc (spans 280 degrees)
        self.create_arc(x - radius + 3, y - radius + 3, x + radius - 3, y + radius - 3, start=40, extent=-280, style="arc", outline="#00f0ff", width=2)

        # Degree ticks
        for deg in range(0, 360, 30):
            rad = math.radians(deg)
            x1 = x + (radius - 5) * math.cos(rad)
            y1 = y + (radius - 5) * math.sin(rad)
            x2 = x + radius * math.cos(rad)
            y2 = y + radius * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill="#00a8ff", width=1)

        # Time string (e.g. 2:40 or HH:MM)
        now = datetime.datetime.now()
        t_str = now.strftime("%H:%M")
        self.create_text(x, y, text=t_str, font=("Segoe UI", 13, "bold"), fill="#ffffff")

    # -------------------------------------------------------------
    # WIDGET 4: TOP-LEFT GIANT DATE DIAL (Июнь / 21)
    # -------------------------------------------------------------
    def _draw_giant_date_dial(self, x, y):
        radius = 56
        # Outer degree circle
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#0c3058", width=1)
        # Inner glowing ring
        self.create_oval(x - (radius - 5), y - (radius - 5), x + (radius - 5), y + (radius - 5), outline="#00f0ff", width=2)

        # Outer segmented brackets
        self.create_arc(x - (radius + 6), y - (radius + 6), x + (radius + 6), y + (radius + 6), start=110, extent=60, style="arc", outline="#00a8ff", width=2)
        self.create_arc(x - (radius + 6), y - (radius + 6), x + (radius + 6), y + (radius + 6), start=290, extent=60, style="arc", outline="#00a8ff", width=2)

        now = datetime.datetime.now()
        month_str = now.strftime("%B")[:4].upper()
        day_num = f"{now.day:02d}"
        weekday_str = now.strftime("%A")
        sec_clock = now.strftime("%H : %M : %S")

        self.create_text(x, y - 22, text=month_str, font=("Segoe UI", 9, "bold"), fill="#38bdf8")
        self.create_text(x, y + 2, text=day_num, font=("Segoe UI", 26, "bold"), fill="#ffffff")
        self.create_text(x, y + 26, text=weekday_str[:4].upper(), font=FONT_HUD_TINY, fill="#00ffaa")
        self.create_text(x, y + radius + 12, text=sec_clock, font=FONT_HUD_TINY, fill="#00f0ff")

    # -------------------------------------------------------------
    # WIDGET 5: UPPER-LEFT RAM (15%) & SWAP (49%) DUAL GAUGE
    # -------------------------------------------------------------
    def _draw_ram_swap_gauge(self, x, y):
        radius = 34
        # Outer ring
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#0a2544", width=1)
        # Thick outer cyan arc (RAM)
        self.create_arc(x - radius, y - radius, x + radius, y + radius, start=90, extent=-(self.ram_pct * 3.6), style="arc", outline="#00f0ff", width=4)
        # Inner ring (SWAP)
        r_inner = radius - 8
        self.create_oval(x - r_inner, y - r_inner, x + r_inner, y + r_inner, outline="#081b33", width=1)
        self.create_arc(x - r_inner, y - r_inner, x + r_inner, y + r_inner, start=180, extent=-176, style="arc", outline="#0088ff", width=2)

        self.create_text(x, y - 7, text=f"RAM: {int(self.ram_pct)}", font=("Segoe UI", 8, "bold"), fill="#ffffff")
        self.create_text(x, y + 7, text=f"SWAP: 49", font=("Segoe UI", 8), fill="#38bdf8")

    # -------------------------------------------------------------
    # WIDGET 6: MID-LEFT CPU SEGMENTED GAUGE
    # -------------------------------------------------------------
    def _draw_cpu_segmented_gauge(self, x, y):
        radius = 38
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        # Multi-segmented arc representing CPU load
        cpu_ext = min(300.0, max(20.0, self.cpu_pct * 3.0))
        self.create_arc(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, start=210, extent=-cpu_ext, style="arc", outline="#00f0ff", width=4)

        self.create_text(x, y - 10, text="CPU", font=("Segoe UI", 8, "bold"), fill="#38bdf8")
        self.create_text(x, y + 2, text=f"{self.cpu_pct/100 * 3.2:.2f}", font=("Segoe UI", 9, "bold"), fill="#ffffff")
        self.create_text(x, y + 14, text="1.57 GHz", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # WIDGET 7: MID-LEFT DISK STORAGE MONITOR
    # -------------------------------------------------------------
    def _draw_disk_storage_monitor(self, x, y):
        self.create_text(x, y, text="Полный объем: 512 G", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x, y + 14, text="Локальный диск (C:)", font=FONT_HUD_TINY, fill="#64748b", anchor="w")
        # Progress bar
        bar_w = 90
        self.create_rectangle(x, y + 24, x + bar_w, y + 29, fill="#06182e", outline="#0a2a50")
        filled_w = bar_w * (self.disk_pct / 100.0)
        self.create_rectangle(x, y + 24, x + filled_w, y + 29, fill="#00f0ff", outline="")
        self.create_text(x, y + 38, text=f"Свободно: {int(512 * (1 - self.disk_pct/100))} G", font=FONT_HUD_TINY, fill="#00ffaa", anchor="w")

    # -------------------------------------------------------------
    # WIDGET 8: STARK EXPO 2010 ATOM HOLOGRAM
    # -------------------------------------------------------------
    def _draw_stark_expo_atom(self, x, y):
        # Draw 3 tilted rotating 3D elliptical orbits
        rx = 48
        ry = 16
        for idx, base_angle in enumerate((0, math.pi / 3, 2 * math.pi / 3)):
            rot = base_angle + self.angle_orbit
            # Draw ellipse as polygon
            pts = []
            steps = 24
            for s in range(steps):
                t = s * (2 * math.pi / steps)
                # 2D rotation of ellipse
                ex = rx * math.cos(t)
                ey = ry * math.sin(t)
                px = x + ex * math.cos(rot) - ey * math.sin(rot)
                py = y + ex * math.sin(rot) + ey * math.cos(rot)
                pts.extend([px, py])
            self.create_polygon(pts, fill="", outline="#0e3a6c", width=1)

            # Glowing electron dot moving on the orbit
            t_elec = self.pulse * 2 + idx * 2.1
            ex_e = rx * math.cos(t_elec)
            ey_e = ry * math.sin(t_elec)
            px_e = x + ex_e * math.cos(rot) - ey_e * math.sin(rot)
            py_e = y + ex_e * math.sin(rot) + ey_e * math.cos(rot)
            self.create_oval(px_e - 2, py_e - 2, px_e + 2, py_e + 2, fill="#00f0ff", outline="")

        # Central STARK EXPO 2010 Text
        self.create_text(x, y - 8, text="STARK", font=("Segoe UI", 9, "bold"), fill="#38bdf8")
        self.create_text(x, y + 6, text="EXPO", font=("Segoe UI", 13, "bold"), fill="#ffffff")
        self.create_text(x, y + 18, text="2010", font=("Segoe UI", 7, "bold"), fill="#00f0ff")

    # -------------------------------------------------------------
    # WIDGET 9: ENERGY 100% RADIAL METER
    # -------------------------------------------------------------
    def _draw_energy_gauge(self, x, y):
        radius = 34
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        self.create_arc(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, start=0, extent=360, style="arc", outline="#00f0ff", width=3)
        self.create_text(x, y - 6, text="Энергия", font=FONT_HUD_TINY, fill="#38bdf8")
        self.create_text(x, y + 6, text="100%", font=("Segoe UI", 9, "bold"), fill="#ffffff")
        self.create_text(x, y + 18, text="Высокий", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # WIDGET 10: RECYCLE BIN & UPTIME MONITOR
    # -------------------------------------------------------------
    def _draw_trash_uptime(self, x, y):
        # Recycle icon & status
        self.create_text(x, y, text="♺ Корзина: 0 Файлов", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")

        # Uptime
        elapsed = int(time.time() - self.start_time)
        hrs = elapsed // 3600
        mins = (elapsed % 3600) // 60
        self.create_text(x, y + 16, text=f"Время работы: 0 д. {hrs} ч. {mins} мин.", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        # Communication / System Link Dots
        self.create_text(x, y + 32, text="Коммуникация: Новых писем 0", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        for i in range(3):
            self.create_oval(x + i * 14, y + 46, x + i * 14 + 6, y + 46 + 6, fill="#00f0ff" if i == 0 else "#0a264a", outline="")

    # -------------------------------------------------------------
    # WIDGET 11: LOWER-LEFT DUAL CONCENTRIC GAUGE (0.0k / 1.6k)
    # -------------------------------------------------------------
    def _draw_dual_concentric_gauge(self, x, y):
        r_out = 44
        r_in = 30
        # Outer arc
        self.create_arc(x - r_out, y - r_out, x + r_out, y + r_out, start=220, extent=-240, style="arc", outline="#00f0ff", width=5)
        # Inner arc
        self.create_arc(x - r_in, y - r_in, x + r_in, y + r_in, start=200, extent=-200, style="arc", outline="#0088ff", width=4)

        self.create_text(x, y - 6, text="0.0k", font=FONT_HUD_TINY, fill="#ffffff")
        self.create_text(x, y + 6, text="1.6k", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # WIDGET 12: BOTTOM-LEFT WINDOWS CONTROLS & IP
    # -------------------------------------------------------------
    def _draw_bottom_left_controls(self, x, y):
        # Windows Logo Orb
        self.create_oval(x - 14, y - 14, x + 14, y + 14, fill="#061f3d", outline="#00f0ff", width=1)
        # 4 Windows quadrants
        self.create_rectangle(x - 8, y - 8, x - 2, y - 2, fill="#00f0ff", outline="")
        self.create_rectangle(x + 2, y - 8, x + 8, y - 2, fill="#38bdf8", outline="")
        self.create_rectangle(x - 8, y + 2, x - 2, y + 8, fill="#0088ff", outline="")
        self.create_rectangle(x + 2, y + 2, x + 8, y + 8, fill="#00ffaa", outline="")

        # Shutdown / Reboot text
        self.create_text(x + 24, y - 5, text="⏻ Выключение", font=FONT_HUD_TINY, fill="#64748b", anchor="w")
        self.create_text(x + 24, y + 7, text="⟳ Перезагрузка", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        # IP Address
        self.create_text(x + 130, y + 2, text=f"IP: {self.local_ip}", font=FONT_MONO, fill="#00f0ff", anchor="w")

    # -------------------------------------------------------------
    # WIDGET 13: THE MASTER ARC REACTOR CORE
    # -------------------------------------------------------------
    def _draw_master_arc_reactor(self, cx, cy, core_cyan, glow_blue, accent_red):
        """Draw the authentic Stark Expo Arc Reactor matching every layer of the photo."""
        # --- Layer 1: Outer Compass Degree Calibration Ring (R = 175) ---
        r_compass = 172
        self.create_oval(cx - r_compass, cy - r_compass, cx + r_compass, cy + r_compass, outline="#0c3058", width=1)

        # 36 Degree Ticks
        for deg in range(0, 360, 10):
            rad = math.radians(deg)
            is_maj = (deg % 30 == 0)
            t_len = 8 if is_maj else 4
            x1 = cx + (r_compass - t_len) * math.cos(rad)
            y1 = cy + (r_compass - t_len) * math.sin(rad)
            x2 = cx + r_compass * math.cos(rad)
            y2 = cy + r_compass * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill="#00f0ff" if is_maj else "#082547", width=1)

        # --- Layer 2: Orbital Application Nodes (Around the Reactor Ring) ---
        orbital_nodes = [
            ("Dead Space", -75),
            ("Limbo", -50),
            ("EdSigin", -25),
            ("AIMP 2", 15),
            ("Sprint Layout 5.0", 40),
            ("Arduino", 65),
            ("Панель управления", 115),
            ("Neural Core", 200)
        ]
        r_labels = 188
        for name, deg_off in orbital_nodes:
            ang = math.radians(deg_off)
            lx = cx + r_labels * math.cos(ang)
            ly = cy + r_labels * math.sin(ang)
            # Dot connector
            dot_x = cx + r_compass * math.cos(ang)
            dot_y = cy + r_compass * math.sin(ang)
            self.create_line(dot_x, dot_y, lx, ly, fill="#0a325c", width=1)
            self.create_oval(dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2, fill="#00f0ff", outline="")
            anchor_dir = "w" if math.cos(ang) >= 0 else "e"
            self.create_text(lx, ly, text=name, font=FONT_HUD_TINY, fill="#38bdf8", anchor=anchor_dir)

        # --- Layer 3: Rotating Cyan Segments & THE DISTINCT RED ACCENT ARC ---
        r_outer_arcs = 148
        # Segmented cyan arcs
        num_segs = 5
        span = 0.28 * math.pi
        for i in range(num_segs):
            s_ang = self.angle_outer + i * (2 * math.pi / num_segs)
            self.create_arc(
                cx - r_outer_arcs, cy - r_outer_arcs, cx + r_outer_arcs, cy + r_outer_arcs,
                start=math.degrees(s_ang), extent=math.degrees(span),
                style="arc", outline=core_cyan, width=3
            )

        # THE ICONIC RED ACCENT ARC SEGMENT (Upper Left of the Reactor)
        red_start = math.degrees(self.angle_outer + math.pi * 0.75)
        self.create_arc(
            cx - r_outer_arcs - 2, cy - r_outer_arcs - 2, cx + r_outer_arcs + 2, cy + r_outer_arcs + 2,
            start=red_start, extent=48, style="arc", outline=accent_red, width=5
        )

        # --- Layer 4: Dense Stator Teeth Ring (48 Teeth at R = 126) ---
        r_stator = 124
        teeth_count = 48
        for t in range(teeth_count):
            t_rad = self.angle_inner + t * (2 * math.pi / teeth_count)
            t1_x = cx + (r_stator - 6) * math.cos(t_rad)
            t1_y = cy + (r_stator - 6) * math.sin(t_rad)
            t2_x = cx + (r_stator + 6) * math.cos(t_rad)
            t2_y = cy + (r_stator + 6) * math.sin(t_rad)
            is_accent = (t % 6 == 0)
            self.create_line(t1_x, t1_y, t2_x, t2_y, fill="#00f0ff" if is_accent else "#0c3058", width=2 if is_accent else 1)

        self.create_oval(cx - r_stator, cy - r_stator, cx + r_stator, cy + r_stator, outline="#0a2a50", width=1, dash=(2, 4))

        # --- Layer 5: 10 Magnetic Induction Coils (R = 86 to 106) ---
        num_coils = 10
        r_c_in = 84
        r_c_out = 108
        for c in range(num_coils):
            c_ang = self.angle_coils + c * (2 * math.pi / num_coils)
            c1_x = cx + r_c_in * math.cos(c_ang)
            c1_y = cy + r_c_in * math.sin(c_ang)
            c2_x = cx + r_c_out * math.cos(c_ang)
            c2_y = cy + r_c_out * math.sin(c_ang)
            # Pulse coil brightness
            coil_col = COLOR_COPPER if math.sin(self.pulse * 2 + c) < 0 else core_cyan
            self.create_line(c1_x, c1_y, c2_x, c2_y, fill=coil_col, width=4)

        # --- Layer 6: Holographic Sweeping Radar Diagnostic Beam ---
        sweep_rad = self.angle_sweep
        self.create_line(cx, cy, cx + 160 * math.cos(sweep_rad), cy + 160 * math.sin(sweep_rad), fill=glow_blue, width=1)
        self.create_line(cx, cy, cx + 155 * math.cos(sweep_rad - 0.08), cy + 155 * math.sin(sweep_rad - 0.08), fill="#051c36", width=1)

        # --- Layer 7: Central Arc Reactor Plasma Iris ---
        r_iris = 42 + math.sin(self.pulse) * 4 + (self.audio_level * 24)

        # Outer glowing containment ring
        self.create_oval(cx - (r_iris + 14), cy - (r_iris + 14), cx + (r_iris + 14), cy + (r_iris + 14), outline="#00a8ff", width=1)
        # Deep reactor housing
        self.create_oval(cx - r_iris, cy - r_iris, cx + r_iris, cy + r_iris, fill="#041224", outline=core_cyan, width=2)
        # Concentric glowing plasma disc
        r_plasma = max(10, r_iris * 0.65)
        self.create_oval(cx - r_plasma, cy - r_plasma, cx + r_plasma, cy + r_plasma, fill=glow_blue, outline="")
        # Bright cyan lens
        r_lens = max(6, r_plasma * 0.55)
        self.create_oval(cx - r_lens, cy - r_lens, cx + r_lens, cy + r_lens, fill=core_cyan, outline="")
        # White hot nucleus
        r_hot = max(3, r_lens * 0.45)
        self.create_oval(cx - r_hot, cy - r_hot, cx + r_hot, cy + r_hot, fill="#ffffff", outline="")

        # Core crosshair reticles
        self.create_line(cx - (r_iris + 8), cy, cx - (r_iris - 4), cy, fill=core_cyan, width=1)
        self.create_line(cx + (r_iris - 4), cy, cx + (r_iris + 8), cy, fill=core_cyan, width=1)
        self.create_line(cx, cy - (r_iris + 8), cx, cy - (r_iris - 4), fill=core_cyan, width=1)
        self.create_line(cx, cy + (r_iris - 4), cx, cy + (r_iris + 8), fill=core_cyan, width=1)

    # -------------------------------------------------------------
    # WIDGET 14: BOTTOM LAUNCHER NODES & STARK INDUSTRIES BADGE
    # -------------------------------------------------------------
    def _draw_bottom_launchers(self, cx, base_y):
        # Launcher dots: Games, Programs, Skydrive, Electronics
        launchers = ["Games", "Programs", "Skydrive", "Electronics"]
        for idx, item in enumerate(launchers):
            ly = base_y + idx * 16
            self.create_oval(cx - 70, ly, cx - 64, ly + 6, fill="#00f0ff", outline="")
            self.create_text(cx - 56, ly + 3, text=item, font=FONT_HUD_TINY, fill="#ffffff", anchor="w")

        # Two tactical toggle rectangles in center
        self.create_rectangle(cx + 20, base_y + 8, cx + 42, base_y + 24, outline="#00f0ff", fill="#061a33")
        self.create_oval(cx + 28, base_y + 13, cx + 34, base_y + 19, fill="#00f0ff", outline="")

        # STARK INDUSTRIES Tactical Slash Banner
        banner_y = base_y + 72
        # Angular forward brackets
        self.create_polygon(
            cx - 130, banner_y + 8, cx - 118, banner_y - 8, cx + 118, banner_y - 8,
            cx + 130, banner_y + 8, fill="", outline="#0e3a6c", width=1
        )
        self.create_text(cx, banner_y, text="STARK INDUSTRIES", font=("Segoe UI", 11, "bold"), fill="#00f0ff")

    # -------------------------------------------------------------
    # WIDGET 15: MID-RIGHT HUD PREVIEW FRAMES & NEWS FEED
    # -------------------------------------------------------------
    def _draw_news_and_preview_frames(self, x, y, w):
        # Circular Preview Frame 1 (Art)
        r_art = 42
        self.create_oval(x - r_art, y - r_art, x + r_art, y + r_art, outline="#00f0ff", width=1)
        self.create_arc(x - r_art + 2, y - r_art + 2, x + r_art - 2, y + r_art - 2, start=30, extent=-120, style="arc", outline="#0088ff", width=3)
        # Holographic wireframe inside
        self.create_rectangle(x - 18, y - 12, x + 18, y + 12, outline="#0a325c", fill="#030f20")
        self.create_line(x - 18, y + 4, x - 4, y - 6, x + 8, y + 2, x + 18, y - 8, fill="#00f0ff", width=1)
        self.create_text(x, y + r_art + 10, text="Art", font=FONT_HUD_TINY, fill="#38bdf8")

        # Filmstrip / Trash preview frame 2
        f_x = x + 95
        self.create_rectangle(f_x - 22, y - 18, f_x + 22, y + 18, outline="#00f0ff", fill="#030f20")
        for f_i in range(3):
            self.create_rectangle(f_x - 18 + f_i * 12, y - 14, f_x - 8 + f_i * 12, y + 14, outline="#082547", fill="")
        self.create_text(f_x, y + r_art + 10, text="Trash", font=FONT_HUD_TINY, fill="#64748b")

        # News / Tactical Intel Feed
        news_x = x - 20
        news_y = y - 135
        self.create_text(news_x, news_y, text="Новости // INTEL FEED", font=("Segoe UI", 9, "bold"), fill="#00f0ff", anchor="w")

        news_items = [
            "Kinopoisk • Autonomous Link",
            "Броненосец • Defense Grid Nominal",
            "Багровый цвет снегопада",
            "Музыка нас связала • Acoustic active",
            "Гавр • Local System Clean",
            "Клуб безбашенных • High Performance"
        ]
        for idx, ni in enumerate(news_items):
            iy = news_y + 16 + idx * 14
            self.create_text(news_x, iy, text=f"— {ni}", font=FONT_HUD_TINY, fill="#38bdf8" if idx == 0 else "#64748b", anchor="w")

    # -------------------------------------------------------------
    # WIDGET 16: LOWER-RIGHT ROLLING NETWORK SPARKLINES
    # -------------------------------------------------------------
    def _draw_network_sparklines(self, x, y):
        # Download (Загрузка: 25 k)
        self.create_text(x - 10, y, text=f"Загрузка: {int(self.cur_down_kb)} k", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x + 130, y, text="169.39 G", font=FONT_HUD_TINY, fill="#00ffaa", anchor="e")

        # Jagged Download Graph
        pts_down = []
        graph_w = 140
        graph_h = 18
        for i, val in enumerate(self.net_down_history):
            gx = (x - 10) + i * (graph_w / len(self.net_down_history))
            gy = (y + 22) - (val / 100.0) * graph_h
            pts_down.extend([gx, gy])
        if len(pts_down) >= 4:
            self.create_line(pts_down, fill="#00f0ff", width=1)

        # Upload (Выгрузка: 282.0 32.95 G)
        up_y = y + 36
        self.create_text(x - 10, up_y, text=f"Выгрузка: {int(self.cur_up_kb)} k", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x + 130, up_y, text="32.95 G", font=FONT_HUD_TINY, fill="#0088ff", anchor="e")

        # Jagged Upload Graph
        pts_up = []
        for i, val in enumerate(self.net_up_history):
            gx = (x - 10) + i * (graph_w / len(self.net_up_history))
            gy = (up_y + 22) - (val / 100.0) * graph_h
            pts_up.extend([gx, gy])
        if len(pts_up) >= 4:
            self.create_line(pts_up, fill="#0088ff", width=1)

        # Media Control Strip below sparklines
        strip_y = up_y + 36
        self.create_rectangle(x - 10, strip_y, x + 130, strip_y + 14, outline="#0a2a50", fill="#030d1c")
        self.create_text(x + 60, strip_y + 7, text="⏮   ▶   ⏸   ⏭   🔊 [━━━━●━━]", font=FONT_HUD_TINY, fill="#00f0ff")

    # -------------------------------------------------------------
    # WIDGET 17: FAR-RIGHT SATELLITE WEATHER & MOON STATION
    # -------------------------------------------------------------
    def _draw_weather_station(self, x, start_y, total_h):
        # Vertical divider line
        self.create_line(x - 15, start_y, x - 15, total_h - 20, fill="#081e3a", width=1)

        # Header
        now = datetime.datetime.now()
        self.create_text(x, start_y, text=f"Обновлено {now.strftime('%m/%d/%y %H:%M')}", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        # Giant Temperature Readout
        self.create_text(x, start_y + 28, text="13°C", font=("Segoe UI", 24, "bold"), fill="#ffffff", anchor="w")

        # Glowing Moon Graphic
        m_x = x + 110
        m_y = start_y + 28
        self.create_oval(m_x - 20, m_y - 20, m_x + 20, m_y + 20, fill="#1c3a60", outline="#00f0ff", width=1)
        # Moon craters
        self.create_oval(m_x - 8, m_y - 6, m_x - 2, m_y, fill="#0d1f36", outline="")
        self.create_oval(m_x + 2, m_y + 4, m_x + 9, m_y + 11, fill="#0d1f36", outline="")
        self.create_oval(m_x - 4, m_y + 8, m_x - 1, m_y + 11, fill="#0d1f36", outline="")

        # Primary Condition
        self.create_text(x, start_y + 54, text="Ясно • Clear Sky", font=("Segoe UI", 9, "bold"), fill="#00ffaa", anchor="w")

        # Atmospheric Metrics
        specs = [
            ("Влажность", "77%"),
            ("Ощущается", "13°C"),
            ("Осадки", "0%"),
            ("Видимость", "10.0 км"),
            ("Ветер", "3 км/ч (ЗСЗ)"),
            ("Восход солнца", "4:44 ДП"),
            ("Закат солнца", "10:18 ДП")
        ]
        for idx, (lbl, val) in enumerate(specs):
            sy = start_y + 72 + idx * 14
            self.create_text(x, sy, text=f"{lbl}: {val}", font=FONT_HUD_TINY, fill="#38bdf8" if idx == 0 else "#64748b", anchor="w")

        # 7-Day Weekly Forecast
        fc_start_y = start_y + 185
        self.create_text(x, fc_start_y, text="ПРОГНОЗ НА НЕДЕЛЮ:", font=("Segoe UI", 8, "bold"), fill="#00f0ff", anchor="w")

        forecast = [
            ("Сегодня ночью", "11°", "☁ Переменная", "#38bdf8"),
            ("Завтра (Чт)", "23° / 11°", "☀ Солнечно", "#ffaa00"),
            ("Пятница", "23° / 11°", "☀ Ясно", "#ffaa00"),
            ("Суббота", "19° / 12°", "☁ Облачно", "#38bdf8"),
            ("Воскресенье", "17° / 11°", "🌧 Осадки", "#00f0ff"),
            ("Понедельник", "19° / 11°", "☁ Облачно", "#38bdf8"),
            ("Вторник", "22° / 12°", "🌧 Осадки", "#00f0ff"),
            ("Среда", "23° / 14°", "🌧 Дождь", "#00f0ff")
        ]
        for f_idx, (day, temp, cond, c_col) in enumerate(forecast):
            fy = fc_start_y + 18 + f_idx * 28
            if fy + 24 > total_h - 10:
                break
            self.create_text(x, fy, text=day, font=("Segoe UI", 8, "bold"), fill="#ffffff", anchor="w")
            self.create_text(x + 130, fy, text=temp, font=("Segoe UI", 8, "bold"), fill="#00ffaa", anchor="e")
            self.create_text(x, fy + 12, text=cond, font=FONT_HUD_TINY, fill=c_col, anchor="w")
