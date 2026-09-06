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
    STARK EXPO 2010 // HYPER-ADVANCED IRON MAN JARVIS HOLOGRAPHIC COMMAND CENTER HUD
    All English, ultra-dense, military-grade Stark Industries telemetry:
    1. Top 30-Day Matrix Ribbon (01..30) with active day highlighted in glowing cyan
    2. Grid Location: 'Stark Tower // New Delhi, India // Sector 07 // Secure'
    3. Media Player Header: Frequency oscilloscope & live acoustic stream ('Laichzeit // Edge TTS')
    4. Circular Chronometer Dial (02:40) with outer progress calibration arc
    5. Top-Left Giant Date Dial (SEPTEMBER 21 // THURSDAY // 01:06:39 // SECONDS CHRONOMETER)
    6. Upper-Left RAM (15%) & SWAP (49%) dual concentric telemetry gauge
    7. Multi-Core CPU Gauge (0.74 / 1.57 GHz) + 8-Core Thread Load Equalizer (C0..C7)
    8. Storage Volume Monitor (Total: 512 GB // Free: 184 GB // NVMe RAID 0)
    9. Stark Expo 2010 Atom Hologram with 3 rotating 3D orbital electron rings
    10. Artificial Horizon & Flight Pitch Ladder (Pitch +20 to -20 with roll angle)
    11. Reactor Energy Meter (100% // Peak Output // Magnetic Containment 14.8 T)
    12. Trash Repository & System Uptime Telemetry (0 Objects // Uptime: 0d 4h 18m)
    13. Dual Concentric Network I/O Dial (0.0k / 1.6k)
    14. Bottom-Left Windows OS Orb, Power Controls (Power Down / Reboot Core) & IP Address
    15. THE GRAND MASTER ARC REACTOR CORE:
        - Outer vernier compass degree ring (72 micro-ticks, degree labels 000..330)
        - Orbital application nodes: Dead Space, Limbo, Cyber Engine, AIMP 2, Sprint Layout, Arduino, Control Panel, Neural Core
        - Iconic RED ACCENT ARC (35 deg) rotating alongside cyan laser telemetry segments
        - Dual-layer stator turbine teeth (64 inner teeth + 32 outer counter-rotating cogs)
        - 12 magnetic induction coils with animated electric corona filaments
        - 360-degree rotating diagnostic sweep ray with phosphor fade trail
        - Multi-layered glowing plasma iris with live microphone & TTS audio RMS reactivity
        - Real-time 48-channel audio spectrum equalizer with peak-hold bars
        - Floating hex memory address stream (0x7F // 0xA9 // ADDR_CORE // FLUX_OK)
        - Bottom launcher nodes: ● Games, ● Programs, ● Cloud Drive, ● Electronics
        - STARK INDUSTRIES tactical forward-slash badge
    16. 3D Rotating Holographic Gyroscope Wireframe Cube in right HUD preview frame
    17. Tactical Radar Scope with 360° sweeping line and 4 active pulsing target blips
    18. Real-Time Tactical Intel Stream (Kinopoisk, Defense Grid, Neural Sync, Satellite Patrol)
    19. Live Network Traffic Sparkline Waveforms (Download 25.4 kb/s, Upload 282.0 kb/s, Packet Loss 0.00%)
    20. Full Satellite Meteorological & Moon Phase Station (13°C, Detailed Moon Vector, Atmospheric Metrics, 7-Day Forecast)
    """
    def __init__(self, parent, width=1380, height=760, on_node_click=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg="#01040a", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.on_node_click = on_node_click

        # State & Status
        self.state = "IDLE"
        self.status_detail = "All Systems Nominal • Standby"

        # Procedural Rotation Angles
        self.angle_outer = 0.0
        self.angle_inner = 0.0
        self.angle_sweep = 0.0
        self.angle_coils = 0.0
        self.angle_orbit = 0.0
        self.angle_radar = 0.0
        self.angle_3d_x = 0.0
        self.angle_3d_y = 0.0
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
        self.core_temp = 42.0
        self.gpu_load = 28.0
        self.start_time = time.time()
        self.local_ip = self._detect_local_ip()

        # Multi-Core CPU Simulation (8 Cores)
        self.core_loads = [random.uniform(10, 35) for _ in range(8)]

        # Network Traffic Sparklines (40 samples)
        self.net_down_history = [22.0 + random.uniform(-4, 4) for _ in range(40)]
        self.net_up_history = [14.0 + random.uniform(-3, 3) for _ in range(40)]
        self.cur_down_kb = 25.4
        self.cur_up_kb = 18.2

        # 3D Cube Vertices (Centered at 0, size 26)
        self.cube_vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1]
        ]
        self.cube_edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]

        # Radar Blips (r, angle_rad, intensity)
        self.radar_blips = [
            [22, 0.8, 1.0],
            [34, 2.4, 0.6],
            [15, 4.1, 0.8],
            [28, 5.5, 0.4]
        ]

        # Telemetry Background Thread
        self._running = True
        self._start_telemetry_thread()

        # Events
        self.bind("<Configure>", self._on_resize)
        self.bind("<Button-1>", self._on_click)

        # Main Animation Loop (~40-60 FPS)
        self.after(30, self._render_frame)

    def _detect_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "192.168.1.104"

    def _on_resize(self, event):
        if event.width > 300 and event.height > 200:
            self.width = event.width
            self.height = event.height

    def _on_click(self, event):
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

                    # Update core loads
                    base_cpu = self.cpu_pct
                    self.core_loads = [max(5.0, min(100.0, base_cpu + random.uniform(-12, 14))) for _ in range(8)]

                    # Update network sparklines
                    d_val = max(2.0, min(98.0, self.cur_down_kb + random.uniform(-8.0, 8.0)))
                    u_val = max(1.0, min(85.0, self.cur_up_kb + random.uniform(-5.0, 5.0)))
                    self.cur_down_kb = d_val
                    self.cur_up_kb = u_val
                    self.net_down_history.pop(0)
                    self.net_down_history.append(d_val)
                    self.net_up_history.pop(0)
                    self.net_up_history.append(u_val)

                    self.core_temp = 38.0 + (self.cpu_pct * 0.25)
                    self.gpu_load = max(10.0, min(95.0, self.gpu_load + random.uniform(-4, 4)))
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
            self.status_detail = "All Systems Nominal • Standby"
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

        # Smooth audio level
        self.audio_level += (self.target_audio_level - self.audio_level) * 0.35

        # Speed scaling per agent state
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
        self.angle_radar = (self.angle_radar + speed * 2.2) % (2 * math.pi)
        self.angle_3d_x = (self.angle_3d_x + 0.035) % (2 * math.pi)
        self.angle_3d_y = (self.angle_3d_y + 0.045) % (2 * math.pi)
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)

        # Dynamic color styling
        core_cyan = "#00f0ff"
        glow_blue = "#0088ff"
        accent_red = "#ff3344"     # Distinct red accent arc segment
        if self.state == "EXECUTING":
            core_cyan = "#00ffaa"
        elif self.state in ("THINKING", "PLANNING"):
            core_cyan = "#8b5cf6"
        elif self.state == "ERROR":
            core_cyan = "#ef4444"

        # --- 0. BACKGROUND HOLOGRAPHIC CIRCUIT NETWORK ---
        self._draw_laser_circuit_bus(cx, cy, w, h, core_cyan)

        # --- 1. TOP 30-DAY MATRIX CALENDAR RIBBON ---
        self._draw_top_calendar_matrix(w)

        # --- 2. TOP LOCATION & AUDIO MEDIA TICKER ---
        self._draw_top_location_media(w, cx)

        # --- 3. CIRCULAR CHRONOMETER DIAL (02:40) ---
        self._draw_chronometer_dial(cx + 175, 78)

        # --- 4. TOP-LEFT GIANT DATE & TIME DIAL ---
        self._draw_giant_date_dial(145, 120)

        # --- 5. UPPER-LEFT RAM & SWAP CONCENTRIC GAUGE ---
        self._draw_ram_swap_gauge(340, 75)

        # --- 6. MID-LEFT CPU GAUGE & 8-CORE THREAD EQUALIZER ---
        self._draw_cpu_and_multicore_cluster(275, 145)

        # --- 7. MID-LEFT DISK STORAGE & NVMe MONITOR ---
        self._draw_storage_volume_monitor(125, 260)

        # --- 8. STARK EXPO 2010 ATOM HOLOGRAM ---
        self._draw_stark_expo_atom_hologram(275, 275)

        # --- 9. FLIGHT ATTITUDE / ARTIFICIAL HORIZON PITCH LADDER ---
        self._draw_pitch_horizon_ladder(275, 385)

        # --- 10. REACTOR ENERGY GAUGE (100% // PEAK) ---
        self._draw_reactor_energy_gauge(130, 380)

        # --- 11. RECYCLE REPOSITORY & SYSTEM UPTIME TELEMETRY ---
        self._draw_trash_uptime_telemetry(130, 475)

        # --- 12. LOWER-LEFT DUAL CONCENTRIC NETWORK METER (0.0k / 1.6k) ---
        self._draw_dual_network_dial(285, 520)

        # --- 13. BOTTOM-LEFT WINDOWS CONTROLS & IP ADDRESS ---
        self._draw_windows_system_controls(40, h - 35)

        # --- 14. THE GRAND MASTER ARC REACTOR CORE ---
        self._draw_grand_arc_reactor(cx, cy, core_cyan, glow_blue, accent_red)

        # --- 15. BOTTOM LAUNCHER NODES & STARK INDUSTRIES BADGE ---
        self._draw_bottom_launchers(cx, cy + 185)

        # --- 16. MID-RIGHT 3D ROTATING GYROSCOPE CUBE & RADAR SCOPE ---
        self._draw_3d_cube_and_radar(cx + 295, cy - 30)

        # --- 17. MID-RIGHT TACTICAL INTEL STREAM ---
        self._draw_tactical_intel_stream(cx + 275, cy - 145)

        # --- 18. LOWER-RIGHT LIVE NETWORK TRAFFIC SPARKLINES ---
        self._draw_network_sparklines(cx + 295, cy + 175)

        # --- 19. FAR-RIGHT SATELLITE METEOROLOGICAL & MOON STATION ---
        self._draw_weather_moon_station(w - 195, 35, h)

        self.after(33, self._render_frame)

    # -------------------------------------------------------------
    # 0. BACKGROUND HOLOGRAPHIC CIRCUIT NETWORK
    # -------------------------------------------------------------
    def _draw_laser_circuit_bus(self, cx, cy, w, h, color):
        line_color = "#071c36"
        node_color = "#0d3a6c"

        # Radiating bus traces from reactor core to peripheral dials
        traces = [
            [(cx - 150, cy - 40), (cx - 240, cy - 40), (cx - 270, cy - 100)],
            [(cx - 150, cy + 30), (cx - 220, cy + 30), (cx - 250, cy + 120)],
            [(cx + 60, cy - 140), (cx + 120, cy - 190), (cx + 175, cy - 190)],
            [(cx + 150, cy - 20), (cx + 220, cy - 20), (cx + 270, cy - 60)],
            [(cx + 150, cy + 50), (cx + 240, cy + 50), (cx + 270, cy + 120)],
            [(cx - 140, cy + 140), (cx - 190, cy + 190), (cx - 240, cy + 190)],
        ]
        for poly in traces:
            flat = [coord for pt in poly for coord in pt]
            self.create_line(flat, fill=line_color, width=1)
            # Glowing junction dot
            end_x, end_y = poly[1]
            self.create_oval(end_x - 2, end_y - 2, end_x + 2, end_y + 2, fill=node_color, outline="")

        # Subtle tactical coordinate grid markings
        for gy in (60, 200, 360, 520, 680):
            self.create_line(20, gy, w - 210, gy, fill="#020d1c", width=1, dash=(2, 8))

    # -------------------------------------------------------------
    # 1. TOP 30-DAY MATRIX CALENDAR RIBBON
    # -------------------------------------------------------------
    def _draw_top_calendar_matrix(self, w):
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
                # Active illuminated cyan indicator badge
                self.create_rectangle(bx - 3, y - 2, bx + 19, y + 12, fill="#00f0ff", outline="")
                self.create_text(bx + 8, y + 5, text=day_str, font=("Consolas", 8, "bold"), fill="#01040a")
            else:
                self.create_text(bx + 8, y + 5, text=day_str, font=("Consolas", 7), fill="#1e3a5f")

    # -------------------------------------------------------------
    # 2. TOP LOCATION & AUDIO MEDIA TICKER
    # -------------------------------------------------------------
    def _draw_top_location_media(self, w, cx):
        # Grid Coordinates & Location
        self.create_text(
            w - 230, 26,
            text="STARK TOWER // NEW DELHI // SECTOR 07 // GRID SECURE",
            font=FONT_HUD_TINY,
            fill="#38bdf8",
            anchor="e"
        )

        # Media Player Stream Header
        media_x = cx + 75
        media_y = 34
        # Speaker Icon
        self.create_polygon(
            media_x, media_y, media_x + 4, media_y, media_x + 8, media_y - 4,
            media_x + 8, media_y + 8, media_x + 4, media_y + 4, media_x, media_y + 4,
            fill="#00f0ff", outline=""
        )
        # Real-time frequency bars beside speaker
        for b in range(8):
            bh = 2 + (self.audio_level * 12 * math.sin(self.pulse * 2 + b * 0.7))
            bx = media_x + 12 + b * 4
            self.create_line(bx, media_y + 2 - bh, bx, media_y + 2 + bh, fill="#00f0ff", width=2)

        track_title = "Laichzeit // FLAC 96kHz"
        artist = "Rammstein • Acoustic Matrix"
        if self.state == "SPEAKING":
            track_title = "Neural Audio Synthesizer"
            artist = "Edge TTS // Saathi Voice Stream"
        elif self.state == "LISTENING":
            track_title = "Acoustic Sensor Stream"
            artist = "Whisper Neural Decryption Active"

        self.create_text(media_x + 50, media_y - 4, text=track_title, font=("Segoe UI", 9, "bold"), fill="#f8fafc", anchor="w")
        self.create_text(media_x + 50, media_y + 8, text=f"• {artist} •", font=FONT_HUD_TINY, fill="#00f0ff", anchor="w")

    # -------------------------------------------------------------
    # 3. CIRCULAR CHRONOMETER DIAL (02:40)
    # -------------------------------------------------------------
    def _draw_chronometer_dial(self, x, y):
        radius = 38
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        self.create_arc(x - radius + 3, y - radius + 3, x + radius - 3, y + radius - 3, start=40, extent=-280, style="arc", outline="#00f0ff", width=2)

        # Degree calibration ticks
        for deg in range(0, 360, 30):
            rad = math.radians(deg)
            x1 = x + (radius - 5) * math.cos(rad)
            y1 = y + (radius - 5) * math.sin(rad)
            x2 = x + radius * math.cos(rad)
            y2 = y + radius * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill="#00a8ff", width=1)

        now = datetime.datetime.now()
        self.create_text(x, y, text=now.strftime("%H:%M"), font=("Segoe UI", 13, "bold"), fill="#ffffff")

    # -------------------------------------------------------------
    # 4. TOP-LEFT GIANT DATE & TIME DIAL
    # -------------------------------------------------------------
    def _draw_giant_date_dial(self, x, y):
        radius = 56
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#0c3058", width=1)
        self.create_oval(x - (radius - 5), y - (radius - 5), x + (radius - 5), y + (radius - 5), outline="#00f0ff", width=2)

        # Outer segmented brackets
        self.create_arc(x - (radius + 6), y - (radius + 6), x + (radius + 6), y + (radius + 6), start=110, extent=60, style="arc", outline="#00a8ff", width=2)
        self.create_arc(x - (radius + 6), y - (radius + 6), x + (radius + 6), y + (radius + 6), start=290, extent=60, style="arc", outline="#00a8ff", width=2)

        now = datetime.datetime.now()
        month_str = now.strftime("%B").upper()
        day_num = f"{now.day:02d}"
        weekday_str = now.strftime("%A").upper()
        sec_clock = now.strftime("%H : %M : %S")

        self.create_text(x, y - 22, text=month_str, font=("Segoe UI", 9, "bold"), fill="#38bdf8")
        self.create_text(x, y + 2, text=day_num, font=("Segoe UI", 26, "bold"), fill="#ffffff")
        self.create_text(x, y + 26, text=weekday_str, font=FONT_HUD_TINY, fill="#00ffaa")
        self.create_text(x, y + radius + 12, text=sec_clock, font=FONT_HUD_TINY, fill="#00f0ff")

    # -------------------------------------------------------------
    # 5. UPPER-LEFT RAM & SWAP CONCENTRIC GAUGE
    # -------------------------------------------------------------
    def _draw_ram_swap_gauge(self, x, y):
        radius = 34
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#0a2544", width=1)
        # RAM progress arc
        self.create_arc(x - radius, y - radius, x + radius, y + radius, start=90, extent=-(self.ram_pct * 3.6), style="arc", outline="#00f0ff", width=4)
        # Inner SWAP arc
        r_inner = radius - 8
        self.create_oval(x - r_inner, y - r_inner, x + r_inner, y + r_inner, outline="#081b33", width=1)
        self.create_arc(x - r_inner, y - r_inner, x + r_inner, y + r_inner, start=180, extent=-176, style="arc", outline="#0088ff", width=2)

        self.create_text(x, y - 7, text=f"RAM: {int(self.ram_pct)}%", font=("Segoe UI", 8, "bold"), fill="#ffffff")
        self.create_text(x, y + 7, text="SWAP: 49%", font=("Segoe UI", 8), fill="#38bdf8")

    # -------------------------------------------------------------
    # 6. MID-LEFT CPU GAUGE & 8-CORE THREAD EQUALIZER
    # -------------------------------------------------------------
    def _draw_cpu_and_multicore_cluster(self, x, y):
        radius = 38
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        cpu_ext = min(300.0, max(20.0, self.cpu_pct * 3.0))
        self.create_arc(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, start=210, extent=-cpu_ext, style="arc", outline="#00f0ff", width=4)

        self.create_text(x, y - 10, text="CPU CLOCK", font=FONT_HUD_TINY, fill="#38bdf8")
        self.create_text(x, y + 2, text=f"{self.cpu_pct/100 * 3.2:.2f} GHz", font=("Segoe UI", 9, "bold"), fill="#ffffff")
        self.create_text(x, y + 14, text=f"{int(self.cpu_pct)}% LOAD", font=FONT_HUD_TINY, fill="#00ffaa")

        # 8-Core Thread Load Equalizer directly below
        eq_x = x - 34
        eq_y = y + radius + 12
        for core_i in range(8):
            ch = (self.core_loads[core_i] / 100.0) * 16
            bx = eq_x + core_i * 9
            self.create_rectangle(bx, eq_y - ch, bx + 6, eq_y, fill="#00f0ff" if core_i % 2 == 0 else "#0088ff", outline="")
        self.create_text(x, eq_y + 10, text="CORES: C0 - C7 ACTIVE", font=("Consolas", 6), fill="#64748b")

    # -------------------------------------------------------------
    # 7. MID-LEFT STORAGE VOLUME MONITOR
    # -------------------------------------------------------------
    def _draw_storage_volume_monitor(self, x, y):
        self.create_text(x, y, text="TOTAL STORAGE: 512 GB", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x, y + 14, text="NVMe RAID 0 (SYSTEM C:)", font=FONT_HUD_TINY, fill="#64748b", anchor="w")
        # Progress bar
        bar_w = 90
        self.create_rectangle(x, y + 24, x + bar_w, y + 29, fill="#06182e", outline="#0a2a50")
        filled_w = bar_w * (self.disk_pct / 100.0)
        self.create_rectangle(x, y + 24, x + filled_w, y + 29, fill="#00f0ff", outline="")
        free_gb = int(512 * (1 - self.disk_pct / 100.0))
        self.create_text(x, y + 38, text=f"FREE SPACE: {free_gb} GB", font=FONT_HUD_TINY, fill="#00ffaa", anchor="w")

    # -------------------------------------------------------------
    # 8. STARK EXPO 2010 ATOM HOLOGRAM
    # -------------------------------------------------------------
    def _draw_stark_expo_atom_hologram(self, x, y):
        rx = 48
        ry = 16
        for idx, base_angle in enumerate((0, math.pi / 3, 2 * math.pi / 3)):
            rot = base_angle + self.angle_orbit
            pts = []
            steps = 24
            for s in range(steps):
                t = s * (2 * math.pi / steps)
                ex = rx * math.cos(t)
                ey = ry * math.sin(t)
                px = x + ex * math.cos(rot) - ey * math.sin(rot)
                py = y + ex * math.sin(rot) + ey * math.cos(rot)
                pts.extend([px, py])
            self.create_polygon(pts, fill="", outline="#0e3a6c", width=1)

            # Rotating electron particle
            t_elec = self.pulse * 2 + idx * 2.1
            ex_e = rx * math.cos(t_elec)
            ey_e = ry * math.sin(t_elec)
            px_e = x + ex_e * math.cos(rot) - ey_e * math.sin(rot)
            py_e = y + ex_e * math.sin(rot) + ey_e * math.cos(rot)
            self.create_oval(px_e - 2, py_e - 2, px_e + 2, py_e + 2, fill="#00f0ff", outline="")

        self.create_text(x, y - 8, text="STARK", font=("Segoe UI", 9, "bold"), fill="#38bdf8")
        self.create_text(x, y + 6, text="EXPO", font=("Segoe UI", 13, "bold"), fill="#ffffff")
        self.create_text(x, y + 18, text="2010", font=("Segoe UI", 7, "bold"), fill="#00f0ff")

    # -------------------------------------------------------------
    # 9. FLIGHT ATTITUDE / ARTIFICIAL HORIZON PITCH LADDER
    # -------------------------------------------------------------
    def _draw_pitch_horizon_ladder(self, x, y):
        # Center boresight reticle
        self.create_line(x - 14, y, x - 5, y, fill="#00f0ff", width=1)
        self.create_line(x + 5, y, x + 14, y, fill="#00f0ff", width=1)
        self.create_oval(x - 2, y - 2, x + 2, y + 2, fill="#00f0ff", outline="")

        # Pitch rungs
        ladder_offset = math.sin(self.pulse * 0.5) * 4
        # Pitch +10
        self.create_line(x - 18, y - 16 + ladder_offset, x - 8, y - 16 + ladder_offset, fill="#0088ff", width=1)
        self.create_line(x + 8, y - 16 + ladder_offset, x + 18, y - 16 + ladder_offset, fill="#0088ff", width=1)
        self.create_text(x - 24, y - 16 + ladder_offset, text="+10", font=("Consolas", 6), fill="#38bdf8")

        # Pitch -10
        self.create_line(x - 18, y + 16 + ladder_offset, x - 8, y + 16 + ladder_offset, fill="#0088ff", width=1)
        self.create_line(x + 8, y + 16 + ladder_offset, x + 18, y + 16 + ladder_offset, fill="#0088ff", width=1)
        self.create_text(x - 24, y + 16 + ladder_offset, text="-10", font=("Consolas", 6), fill="#38bdf8")

        self.create_text(x, y + 30, text="ATTITUDE // PITCH 0.0°", font=("Consolas", 6), fill="#64748b")

    # -------------------------------------------------------------
    # 10. REACTOR ENERGY GAUGE (100% // PEAK)
    # -------------------------------------------------------------
    def _draw_reactor_energy_gauge(self, x, y):
        radius = 34
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        self.create_arc(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, start=0, extent=360, style="arc", outline="#00f0ff", width=3)
        self.create_text(x, y - 6, text="REACTOR FLUX", font=FONT_HUD_TINY, fill="#38bdf8")
        self.create_text(x, y + 6, text="100%", font=("Segoe UI", 9, "bold"), fill="#ffffff")
        self.create_text(x, y + 18, text="PEAK OUTPUT", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # 11. RECYCLE REPOSITORY & SYSTEM UPTIME TELEMETRY
    # -------------------------------------------------------------
    def _draw_trash_uptime_telemetry(self, x, y):
        self.create_text(x, y, text="♺ TRASH REPOSITORY: 0 OBJECTS", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")

        elapsed = int(time.time() - self.start_time)
        hrs = elapsed // 3600
        mins = (elapsed % 3600) // 60
        secs = elapsed % 60
        self.create_text(x, y + 16, text=f"SYSTEM UPTIME: 0d {hrs}h {mins}m {secs}s", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        self.create_text(x, y + 32, text="COMMS: 0 PENDING PACKETS // SECURE", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        for i in range(3):
            self.create_oval(x + i * 14, y + 46, x + i * 14 + 6, y + 46 + 6, fill="#00f0ff" if i == 0 else "#0a264a", outline="")

    # -------------------------------------------------------------
    # 12. LOWER-LEFT DUAL CONCENTRIC NETWORK METER (0.0k / 1.6k)
    # -------------------------------------------------------------
    def _draw_dual_network_dial(self, x, y):
        r_out = 44
        r_in = 30
        self.create_arc(x - r_out, y - r_out, x + r_out, y + r_out, start=220, extent=-240, style="arc", outline="#00f0ff", width=5)
        self.create_arc(x - r_in, y - r_in, x + r_in, y + r_in, start=200, extent=-200, style="arc", outline="#0088ff", width=4)

        self.create_text(x, y - 6, text="0.0k", font=FONT_HUD_TINY, fill="#ffffff")
        self.create_text(x, y + 6, text="1.6k", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # 13. BOTTOM-LEFT WINDOWS CONTROLS & IP ADDRESS
    # -------------------------------------------------------------
    def _draw_windows_system_controls(self, x, y):
        # Windows Logo Orb
        self.create_oval(x - 14, y - 14, x + 14, y + 14, fill="#061f3d", outline="#00f0ff", width=1)
        self.create_rectangle(x - 8, y - 8, x - 2, y - 2, fill="#00f0ff", outline="")
        self.create_rectangle(x + 2, y - 8, x + 8, y - 2, fill="#38bdf8", outline="")
        self.create_rectangle(x - 8, y + 2, x - 2, y + 8, fill="#0088ff", outline="")
        self.create_rectangle(x + 2, y + 2, x + 8, y + 8, fill="#00ffaa", outline="")

        # Power Controls
        self.create_text(x + 24, y - 5, text="⏻ POWER DOWN", font=FONT_HUD_TINY, fill="#64748b", anchor="w")
        self.create_text(x + 24, y + 7, text="⟳ REBOOT CORE", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        # Local IP Address
        self.create_text(x + 130, y + 2, text=f"IP: {self.local_ip}", font=FONT_MONO, fill="#00f0ff", anchor="w")

    # -------------------------------------------------------------
    # 14. THE GRAND MASTER ARC REACTOR CORE
    # -------------------------------------------------------------
    def _draw_grand_arc_reactor(self, cx, cy, core_cyan, glow_blue, accent_red):
        """Draw the hyper-intricate Stark Industries Arc Reactor assembly."""
        # --- Ring 0: Outer Vernier Compass Calibration Ring (R = 175) ---
        r_compass = 172
        self.create_oval(cx - r_compass, cy - r_compass, cx + r_compass, cy + r_compass, outline="#0c3058", width=1)

        # 72 Micro Degree Ticks (every 5 degrees)
        for deg in range(0, 360, 5):
            rad = math.radians(deg)
            is_maj = (deg % 30 == 0)
            is_mid = (deg % 10 == 0)
            t_len = 9 if is_maj else (5 if is_mid else 3)
            x1 = cx + (r_compass - t_len) * math.cos(rad)
            y1 = cy + (r_compass - t_len) * math.sin(rad)
            x2 = cx + r_compass * math.cos(rad)
            y2 = cy + r_compass * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill="#00f0ff" if is_maj else "#082547", width=1)

            if is_maj and deg % 60 == 0:
                tx = cx + (r_compass - 18) * math.cos(rad)
                ty = cy + (r_compass - 18) * math.sin(rad)
                self.create_text(tx, ty, text=f"{deg:03d}", font=("Consolas", 6), fill="#38bdf8")

        # --- Orbital Application Nodes around the perimeter ---
        orbital_nodes = [
            ("Dead Space", -75),
            ("Limbo", -50),
            ("Cyber Engine", -25),
            ("AIMP 2", 15),
            ("Sprint Layout 5.0", 40),
            ("Arduino", 65),
            ("Control Panel", 115),
            ("Neural Core", 200)
        ]
        r_labels = 188
        for name, deg_off in orbital_nodes:
            ang = math.radians(deg_off)
            lx = cx + r_labels * math.cos(ang)
            ly = cy + r_labels * math.sin(ang)
            dot_x = cx + r_compass * math.cos(ang)
            dot_y = cy + r_compass * math.sin(ang)
            self.create_line(dot_x, dot_y, lx, ly, fill="#0a325c", width=1)
            self.create_oval(dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2, fill="#00f0ff", outline="")
            anchor_dir = "w" if math.cos(ang) >= 0 else "e"
            self.create_text(lx, ly, text=name, font=FONT_HUD_TINY, fill="#38bdf8", anchor=anchor_dir)

        # --- Ring 1: Rotating Segmented Cyan Telemetry Arcs & THE RED ACCENT ARC ---
        r_outer_arcs = 148
        num_segs = 6
        span = 0.26 * math.pi
        for i in range(num_segs):
            s_ang = self.angle_outer + i * (2 * math.pi / num_segs)
            self.create_arc(
                cx - r_outer_arcs, cy - r_outer_arcs, cx + r_outer_arcs, cy + r_outer_arcs,
                start=math.degrees(s_ang), extent=math.degrees(span),
                style="arc", outline=core_cyan, width=3
            )

        # THE ICONIC RED ACCENT ARC (Upper-Left Quadrant)
        red_start = math.degrees(self.angle_outer + math.pi * 0.75)
        self.create_arc(
            cx - r_outer_arcs - 2, cy - r_outer_arcs - 2, cx + r_outer_arcs + 2, cy + r_outer_arcs + 2,
            start=red_start, extent=48, style="arc", outline=accent_red, width=5
        )

        # --- Ring 2: Dual-Layer Stator Turbine Gears (64 teeth + 32 outer cogs) ---
        r_stator = 124
        teeth_count = 64
        for t in range(teeth_count):
            t_rad = self.angle_inner + t * (2 * math.pi / teeth_count)
            t1_x = cx + (r_stator - 6) * math.cos(t_rad)
            t1_y = cy + (r_stator - 6) * math.sin(t_rad)
            t2_x = cx + (r_stator + 6) * math.cos(t_rad)
            t2_y = cy + (r_stator + 6) * math.sin(t_rad)
            is_accent = (t % 8 == 0)
            self.create_line(t1_x, t1_y, t2_x, t2_y, fill="#00f0ff" if is_accent else "#0c3058", width=2 if is_accent else 1)

        self.create_oval(cx - r_stator, cy - r_stator, cx + r_stator, cy + r_stator, outline="#0a2a50", width=1, dash=(2, 4))

        # --- Ring 3: 12 Magnetic Induction Coils with Corona Filaments ---
        num_coils = 12
        r_c_in = 84
        r_c_out = 108
        for c in range(num_coils):
            c_ang = self.angle_coils + c * (2 * math.pi / num_coils)
            c1_x = cx + r_c_in * math.cos(c_ang)
            c1_y = cy + r_c_in * math.sin(c_ang)
            c2_x = cx + r_c_out * math.cos(c_ang)
            c2_y = cy + r_c_out * math.sin(c_ang)

            coil_col = COLOR_COPPER if math.sin(self.pulse * 2 + c) < 0 else core_cyan
            self.create_line(c1_x, c1_y, c2_x, c2_y, fill=coil_col, width=4)

            # Animated electrical flux arc toward center
            if c % 3 == 0:
                f_mid_x = cx + (r_c_in - 14) * math.cos(c_ang + 0.1)
                f_mid_y = cy + (r_c_in - 14) * math.sin(c_ang + 0.1)
                self.create_line(c1_x, c1_y, f_mid_x, f_mid_y, fill="#00f0ff", width=1)

        # --- Ring 4: Holographic Sweeping Radar Diagnostic Beam ---
        sweep_rad = self.angle_sweep
        self.create_line(cx, cy, cx + 162 * math.cos(sweep_rad), cy + 162 * math.sin(sweep_rad), fill=glow_blue, width=1)
        self.create_line(cx, cy, cx + 158 * math.cos(sweep_rad - 0.08), cy + 158 * math.sin(sweep_rad - 0.08), fill="#051c36", width=1)

        # --- Ring 5: Multi-Depth Glowing Plasma Iris Core ---
        r_iris = 42 + math.sin(self.pulse) * 4 + (self.audio_level * 24)

        # Outer containment ring
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

        # Floating Hex Memory Stream (Bottom of Reactor)
        hex_str = f"0x7F // 0xA9 // ADDR_CORE: 0x{int(self.pulse*100):02X} // FLUX_OK // T: {self.core_temp:.1f}C"
        self.create_text(cx, cy + r_compass + 10, text=hex_str, font=("Consolas", 6), fill="#38bdf8")

        # 48-Channel Audio Spectrum Equalizer (Beneath core)
        bars = 36
        bar_w = 4
        gap = 3
        total_w = bars * (bar_w + gap)
        start_x = cx - (total_w / 2)
        eq_base_y = cy + r_compass + 24

        for b in range(bars):
            dist_norm = 1.0 - abs(b - (bars / 2)) / (bars / 2)
            wave_h = 2 + (self.audio_level * 18 * dist_norm * math.sin(b * 0.5 + self.pulse * 3))
            bx = start_x + b * (bar_w + gap)
            self.create_rectangle(bx, eq_base_y - wave_h, bx + bar_w, eq_base_y + wave_h, fill=core_cyan, outline="")

    # -------------------------------------------------------------
    # 15. BOTTOM LAUNCHER NODES & STARK INDUSTRIES BADGE
    # -------------------------------------------------------------
    def _draw_bottom_launchers(self, cx, base_y):
        launchers = ["Games", "Programs", "Cloud Drive", "Electronics"]
        for idx, item in enumerate(launchers):
            ly = base_y + idx * 16
            self.create_oval(cx - 70, ly, cx - 64, ly + 6, fill="#00f0ff", outline="")
            self.create_text(cx - 56, ly + 3, text=item, font=FONT_HUD_TINY, fill="#ffffff", anchor="w")

        # Tactical toggle switch
        self.create_rectangle(cx + 20, base_y + 8, cx + 42, base_y + 24, outline="#00f0ff", fill="#061a33")
        self.create_oval(cx + 28, base_y + 13, cx + 34, base_y + 19, fill="#00f0ff", outline="")

        # STARK INDUSTRIES Tactical Slash Banner
        banner_y = base_y + 72
        self.create_polygon(
            cx - 130, banner_y + 8, cx - 118, banner_y - 8, cx + 118, banner_y - 8,
            cx + 130, banner_y + 8, fill="", outline="#0e3a6c", width=1
        )
        self.create_text(cx, banner_y, text="STARK INDUSTRIES", font=("Segoe UI", 11, "bold"), fill="#00f0ff")

    # -------------------------------------------------------------
    # 16. 3D ROTATING GYROSCOPE CUBE & RADAR SCOPE
    # -------------------------------------------------------------
    def _draw_3d_cube_and_radar(self, x, y):
        # Frame 1: 3D Holographic Rotating Gyroscope Cube
        r_box = 42
        self.create_oval(x - r_box, y - r_box, x + r_box, y + r_box, outline="#00f0ff", width=1)
        self.create_arc(x - r_box + 2, y - r_box + 2, x + r_box - 2, y + r_box - 2, start=30, extent=-120, style="arc", outline="#0088ff", width=3)

        # 3D Math Projection
        d = 60
        scale_size = 18
        ax = self.angle_3d_x
        ay = self.angle_3d_y
        cos_x = math.cos(ax); sin_x = math.sin(ax)
        cos_y = math.cos(ay); sin_y = math.sin(ay)

        proj = []
        for vx, vy, vz in self.cube_vertices:
            # Rotate around Y
            x1 = vx * cos_y + vz * sin_y
            z1 = -vx * sin_y + vz * cos_y
            # Rotate around X
            y1 = vy * cos_x - z1 * sin_x
            z2 = vy * sin_x + z1 * cos_x
            # Perspective
            dist = d / (d + z2 * 0.4)
            px = x + (x1 * scale_size) * dist
            py = y + (y1 * scale_size) * dist
            proj.append((px, py))

        for p1, p2 in self.cube_edges:
            self.create_line(proj[p1][0], proj[p1][1], proj[p2][0], proj[p2][1], fill="#00f0ff", width=1)

        self.create_text(x, y + r_box + 10, text="3D GIMBAL CORE", font=FONT_HUD_TINY, fill="#38bdf8")

        # Frame 2: Tactical Radar Scope with Sweeping Blips
        r_rad = x + 95
        self.create_oval(r_rad - r_box, y - r_box, r_rad + r_box, y + r_box, outline="#00f0ff", width=1)
        self.create_oval(r_rad - 24, y - 24, r_rad + 24, y + 24, outline="#082547", width=1)
        self.create_line(r_rad - r_box, y, r_rad + r_box, y, fill="#082547", width=1)
        self.create_line(r_rad, y - r_box, r_rad, y + r_box, fill="#082547", width=1)

        # Radar sweep ray
        sw_ang = self.angle_radar
        self.create_line(r_rad, y, r_rad + r_box * math.cos(sw_ang), y + r_box * math.sin(sw_ang), fill="#00ffaa", width=1)

        # Radar blips
        for b_r, b_ang, b_int in self.radar_blips:
            # Blip pulses when sweep passes
            diff = (sw_ang - b_ang) % (2 * math.pi)
            if diff < 0.8:
                col = "#00ffaa"
            else:
                col = "#005533"
            bx = r_rad + b_r * math.cos(b_ang)
            by = y + b_r * math.sin(b_ang)
            self.create_oval(bx - 2, by - 2, bx + 2, by + 2, fill=col, outline="")

        self.create_text(r_rad, y + r_box + 10, text="RADAR // 360° SCOPE", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # 17. MID-RIGHT TACTICAL INTEL STREAM
    # -------------------------------------------------------------
    def _draw_tactical_intel_stream(self, x, y):
        self.create_text(x, y, text="TACTICAL INTEL STREAM // SATELLITE", font=("Segoe UI", 9, "bold"), fill="#00f0ff", anchor="w")

        intel_items = [
            "Kinopoisk • High-Bandwidth Autonomous Link Active",
            "Battleship Protocol • Defense Grid Nominal (Grade 1)",
            "Crimson Snowfall • Threat Interception Ready",
            "Harmonic Link • Acoustic Signal Synchronized",
            "Le Havre Hub • Local Cache Integrity 100%",
            "Vanguard Co-Pilot • Full Operational Capability"
        ]
        for idx, item in enumerate(intel_items):
            iy = y + 16 + idx * 14
            self.create_text(x, iy, text=f"— {item}", font=FONT_HUD_TINY, fill="#38bdf8" if idx == 0 else "#64748b", anchor="w")

    # -------------------------------------------------------------
    # 18. LOWER-RIGHT ROLLING NETWORK SPARKLINES
    # -------------------------------------------------------------
    def _draw_network_sparklines(self, x, y):
        # Inflow / Download
        self.create_text(x - 10, y, text=f"NET INFLOW: {self.cur_down_kb:.1f} KB/S", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x + 130, y, text="169.39 GB", font=FONT_HUD_TINY, fill="#00ffaa", anchor="e")

        pts_down = []
        graph_w = 140
        graph_h = 18
        for i, val in enumerate(self.net_down_history):
            gx = (x - 10) + i * (graph_w / len(self.net_down_history))
            gy = (y + 22) - (val / 100.0) * graph_h
            pts_down.extend([gx, gy])
        if len(pts_down) >= 4:
            self.create_line(pts_down, fill="#00f0ff", width=1)

        # Outflow / Upload
        up_y = y + 36
        self.create_text(x - 10, up_y, text=f"NET OUTFLOW: {self.cur_up_kb:.1f} KB/S", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x + 130, up_y, text="32.95 GB", font=FONT_HUD_TINY, fill="#0088ff", anchor="e")

        pts_up = []
        for i, val in enumerate(self.net_up_history):
            gx = (x - 10) + i * (graph_w / len(self.net_up_history))
            gy = (up_y + 22) - (val / 100.0) * graph_h
            pts_up.extend([gx, gy])
        if len(pts_up) >= 4:
            self.create_line(pts_up, fill="#0088ff", width=1)

        # Media Control Strip
        strip_y = up_y + 36
        self.create_rectangle(x - 10, strip_y, x + 130, strip_y + 14, outline="#0a2a50", fill="#030d1c")
        self.create_text(x + 60, strip_y + 7, text="⏮   ▶   ⏸   ⏭   🔊 [━━━━●━━]", font=FONT_HUD_TINY, fill="#00f0ff")

    # -------------------------------------------------------------
    # 19. FAR-RIGHT SATELLITE METEOROLOGICAL & MOON STATION
    # -------------------------------------------------------------
    def _draw_weather_moon_station(self, x, start_y, total_h):
        # Vertical tactical boundary
        self.create_line(x - 15, start_y, x - 15, total_h - 20, fill="#081e3a", width=1)

        now = datetime.datetime.now()
        self.create_text(x, start_y, text=f"SYNCED {now.strftime('%m/%d/%y %H:%M')}", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        # Temperature
        self.create_text(x, start_y + 28, text="24°C", font=("Segoe UI", 24, "bold"), fill="#ffffff", anchor="w")

        # Glowing Moon Graphic
        m_x = x + 110
        m_y = start_y + 28
        self.create_oval(m_x - 20, m_y - 20, m_x + 20, m_y + 20, fill="#1c3a60", outline="#00f0ff", width=1)
        self.create_oval(m_x - 8, m_y - 6, m_x - 2, m_y, fill="#0d1f36", outline="")
        self.create_oval(m_x + 2, m_y + 4, m_x + 9, m_y + 11, fill="#0d1f36", outline="")
        self.create_oval(m_x - 4, m_y + 8, m_x - 1, m_y + 11, fill="#0d1f36", outline="")

        self.create_text(x, start_y + 54, text="ATMOSPHERE: CLEAR // OPTIMAL", font=("Segoe UI", 8, "bold"), fill="#00ffaa", anchor="w")

        # Atmospheric Metrics in English
        specs = [
            ("HUMIDITY", "77%"),
            ("FEELS LIKE", "24°C"),
            ("PRECIPITATION", "0%"),
            ("VISIBILITY", "10.0 KM"),
            ("WIND VELOCITY", "3 KM/H (NNW)"),
            ("SOLAR DAWN", "05:42 AM"),
            ("SOLAR DUSK", "06:38 PM")
        ]
        for idx, (lbl, val) in enumerate(specs):
            sy = start_y + 72 + idx * 14
            self.create_text(x, sy, text=f"{lbl}: {val}", font=FONT_HUD_TINY, fill="#38bdf8" if idx == 0 else "#64748b", anchor="w")

        # 7-Day Meteorological Trajectory
        fc_start_y = start_y + 185
        self.create_text(x, fc_start_y, text="7-DAY TRAJECTORY:", font=("Segoe UI", 8, "bold"), fill="#00f0ff", anchor="w")

        forecast = [
            ("TONIGHT", "18°C", "☁ PARTLY CLOUDY", "#38bdf8"),
            ("TOMORROW", "26° / 18°", "☀ SUNNY / CLEAR", "#ffaa00"),
            ("FRIDAY", "27° / 19°", "☀ CLEAR SKY", "#ffaa00"),
            ("SATURDAY", "23° / 17°", "☁ OVERCAST", "#38bdf8"),
            ("SUNDAY", "21° / 16°", "🌧 PRECIPITATION", "#00f0ff"),
            ("MONDAY", "22° / 16°", "☁ PARTLY CLOUDY", "#38bdf8"),
            ("TUESDAY", "24° / 17°", "🌧 LIGHT SHOWER", "#00f0ff"),
            ("WEDNESDAY", "25° / 18°", "🌧 PRECIP / RAIN", "#00f0ff")
        ]
        for f_idx, (day, temp, cond, c_col) in enumerate(forecast):
            fy = fc_start_y + 18 + f_idx * 28
            if fy + 24 > total_h - 10:
                break
            self.create_text(x, fy, text=day, font=("Segoe UI", 8, "bold"), fill="#ffffff", anchor="w")
            self.create_text(x + 130, fy, text=temp, font=("Segoe UI", 8, "bold"), fill="#00ffaa", anchor="e")
            self.create_text(x, fy + 12, text=cond, font=FONT_HUD_TINY, fill=c_col, anchor="w")
