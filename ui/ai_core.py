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
    PRATHAM EXPO // HYPER-ADVANCED SAATHI HOLOGRAPHIC COMMAND CENTER HUD
    All English, ultra-dense, military-grade Pratham Prasad telemetry:
    1. Top 30-Day Matrix Ribbon (01..30) with active day highlighted in glowing cyan
    2. Grid Location: 'Pratham Tower // New Delhi, India // Sector 07 // Secure'
    3. Media Player Header: Frequency oscilloscope & live acoustic stream ('Laichzeit // Edge TTS')
    4. Circular Chronometer Dial (02:40) with outer progress calibration arc
    5. Top-Left Giant Date Dial (SEPTEMBER 21 // THURSDAY // 01:06:39 // SECONDS CHRONOMETER)
    6. Upper-Left RAM (15%) & SWAP (49%) dual concentric telemetry gauge
    7. Multi-Core CPU Gauge (0.74 / 1.57 GHz) + 8-Core Thread Load Equalizer (C0..C7)
    8. Storage Volume Monitor (Total: 512 GB // Free: 184 GB // NVMe RAID 0)
    9. Pratham Expo Atom Hologram with 3 rotating 3D orbital electron rings
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
        - PRATHAM PRASAD tactical forward-slash badge
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

        # Neural Constellation Network (28 drifting synaptic nodes)
        self._init_neural_network()

        # Circuit Bus Streaming Packets
        self._init_circuit_packets()

        # Quantum Particle Field & 4D Tesseract Core
        self._init_quantum_particles()
        self._init_tesseract()

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

        # Airtight proportional columns: mathematically tuned for 1000px to 1920px widths
        weather_x = max(w - 165, 840)
        tactical_div_x = weather_x - 14
        mid_right_x = tactical_div_x - 165
        avail_left = 255
        avail_right = mid_right_x - 15
        cx = (avail_left + avail_right) / 2.0
        cy = max(310, min(int(h * 0.46), h - 330))

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

        # --- 0. BACKGROUND QUANTUM PARTICLE FIELD ---
        self._draw_quantum_particle_field(cx, cy, w, h)

        # --- 0A. BACKGROUND HOLOGRAPHIC CIRCUIT NETWORK ---
        self._draw_laser_circuit_bus(cx, cy, w, h, core_cyan)

        # --- 0B. HOLOGRAPHIC HONEYCOMB FORCEFIELD SHIELD ---
        self._draw_honeycomb_shield(cx, cy)

        # --- 0C. DYNAMIC NEURAL SYNAPSE PLEXUS & ACTION POTENTIALS ---
        self._update_and_draw_neural_plexus(cx, cy, w, h, core_cyan)

        # --- 0D. CIRCUIT BUS STREAMING DATA PACKETS ---
        self._update_and_draw_circuit_packets(cx, cy)

        # --- 0E. DYNAMIC 3D HOLOGRAPHIC THREAD RIBBONS (TECHIE VISUALS) ---
        self._draw_3d_holographic_threads(cx, cy)

        # --- 0F. HYPERDIMENSIONAL 4D TESSERACT CORE MATRIX ---
        self._draw_hyperdimensional_tesseract_core(cx, cy)

        # --- 0G. SWEEPING HOLOGRAPHIC SCANLINES & HEX DATA STREAM ---
        self._draw_tactical_holographic_scanlines(cx, cy, w, h)

        # --- 1. TACTICAL HUD HORIZON & TELEMETRY RETICLE ---
        self._draw_hud_horizon_line(w, cx)

        # --- 4. TOP-LEFT GIANT DATE DIAL ---
        self._draw_giant_date_dial(75, 75)

        # --- 5. UPPER-LEFT RAM & SWAP CONCENTRIC GAUGE ---
        self._draw_ram_swap_gauge(195, 60)

        # --- 6. MID-LEFT CPU GAUGE & 8-CORE THREAD EQUALIZER ---
        self._draw_cpu_and_multicore_cluster(195, 145)

        # --- 7. MID-LEFT DISK STORAGE & NVMe MONITOR ---
        self._draw_storage_volume_monitor(20, 175)

        # --- 8. QUANTUM NUCLEUS ATOM HOLOGRAM ---
        self._draw_pratham_expo_atom_hologram(195, 255)

        # --- 10. REACTOR ENERGY GAUGE (100% // PEAK) ---
        self._draw_reactor_energy_gauge(75, 270)

        # --- 9. FLIGHT ATTITUDE / ARTIFICIAL HORIZON PITCH LADDER ---
        self._draw_pitch_horizon_ladder(195, 345)

        # --- 11. RECYCLE REPOSITORY & SYSTEM STABILITY TELEMETRY ---
        self._draw_trash_uptime_telemetry(20, 365)

        # --- 12. LOWER-LEFT DUAL CONCENTRIC NETWORK METER (0.0k / 1.6k) ---
        self._draw_dual_network_dial(195, 435)

        # --- 13. BOTTOM-LEFT WINDOWS CONTROLS & OS KERNEL STATUS ---
        self._draw_windows_system_controls(20, h - 25)

        # --- 14. THE GRAND MASTER ARC REACTOR CORE ---
        self._draw_grand_arc_reactor(cx, cy, core_cyan, glow_blue, accent_red)

        # --- 14B. HIGH-VOLTAGE PLASMA LIGHTNING DISCHARGES ---
        self._draw_plasma_lightning(cx, cy, 42 + self.audio_level * 24, core_cyan)

        # --- 14C. TACTICAL RETICLE LOCK-ON SYSTEM ---
        self._draw_tactical_lock_reticle(cx, cy)

        # --- 15. BOTTOM LAUNCHER NODES & PRATHAM PRASAD BADGE ---
        self._draw_bottom_launchers(cx, cy + 185)

        # --- 16. MID-RIGHT 3D ROTATING GYROSCOPE CUBE & RADAR SCOPE ---
        self._draw_3d_cube_and_radar(mid_right_x + 18, cy)

        # --- 17. MID-RIGHT TACTICAL INTEL STREAM ---
        self._draw_tactical_intel_stream(mid_right_x, cy - 145)

        # --- 18. LOWER-RIGHT LIVE NETWORK TRAFFIC SPARKLINES ---
        self._draw_network_sparklines(mid_right_x, cy + 95)

        # --- 19. FAR-RIGHT SATELLITE METEOROLOGICAL & MOON STATION ---
        self._draw_weather_moon_station(weather_x, 35, h)

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
    # 1. TACTICAL HUD HORIZON BAR & TELEMETRY RETICLE
    # -------------------------------------------------------------
    def _draw_hud_horizon_line(self, w, cx):
        # Subtle military HUD horizon line across the upper viewport
        self.create_line(35, 18, w - 35, 18, fill="#072242", width=1)

        # Central azimuth notch
        self.create_line(cx - 36, 18, cx - 12, 18, fill="#00f0ff", width=2)
        self.create_line(cx + 12, 18, cx + 36, 18, fill="#00f0ff", width=2)
        self.create_oval(cx - 4, 14, cx + 4, 22, outline="#00f0ff", fill="#01040a", width=1)
        self.create_text(cx, 30, text="SAATHI HOLOGRAPHIC HUD // ONLINE", font=FONT_HUD_TINY, fill="#38bdf8")

        # Telemetry corner watermarks (non-duplicative)
        self.create_text(40, 10, text="AZM: 000° [NORAD]", font=("Consolas", 7), fill="#1e3a5f", anchor="w")
        self.create_text(w - 40, 10, text="COORD: 28.61° N // 77.20° E", font=("Consolas", 7), fill="#1e3a5f", anchor="e")

    # -------------------------------------------------------------
    # 4. TOP-LEFT GIANT DATE & TIME DIAL
    # -------------------------------------------------------------
    def _draw_giant_date_dial(self, x, y):
        radius = 42
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#0c3058", width=1)
        self.create_oval(x - (radius - 4), y - (radius - 4), x + (radius - 4), y + (radius - 4), outline="#00f0ff", width=2)

        # Outer segmented brackets
        self.create_arc(x - (radius + 5), y - (radius + 5), x + (radius + 5), y + (radius + 5), start=110, extent=60, style="arc", outline="#00a8ff", width=2)
        self.create_arc(x - (radius + 5), y - (radius + 5), x + (radius + 5), y + (radius + 5), start=290, extent=60, style="arc", outline="#00a8ff", width=2)

        now = datetime.datetime.now()
        month_str = now.strftime("%B").upper()
        day_num = f"{now.day:02d}"
        weekday_str = now.strftime("%A").upper()

        self.create_text(x, y - 16, text=month_str, font=("Segoe UI", 8, "bold"), fill="#38bdf8")
        self.create_text(x, y + 2, text=day_num, font=("Segoe UI", 20, "bold"), fill="#ffffff")
        self.create_text(x, y + 20, text=weekday_str, font=FONT_HUD_TINY, fill="#00ffaa")
        self.create_text(x, y + radius + 10, text="CALENDAR MATRIX", font=FONT_HUD_TINY, fill="#00f0ff")

    # -------------------------------------------------------------
    # 5. UPPER-LEFT RAM & SWAP CONCENTRIC GAUGE
    # -------------------------------------------------------------
    def _draw_ram_swap_gauge(self, x, y):
        radius = 28
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#0a2544", width=1)
        # RAM progress arc
        self.create_arc(x - radius, y - radius, x + radius, y + radius, start=90, extent=-(self.ram_pct * 3.6), style="arc", outline="#00f0ff", width=4)
        # Inner SWAP arc
        r_inner = radius - 7
        self.create_oval(x - r_inner, y - r_inner, x + r_inner, y + r_inner, outline="#081b33", width=1)
        self.create_arc(x - r_inner, y - r_inner, x + r_inner, y + r_inner, start=180, extent=-176, style="arc", outline="#0088ff", width=2)

        self.create_text(x, y - 6, text=f"RAM: {int(self.ram_pct)}%", font=("Segoe UI", 7, "bold"), fill="#ffffff")
        self.create_text(x, y + 6, text="SWAP: 49%", font=("Segoe UI", 7), fill="#38bdf8")

    # -------------------------------------------------------------
    # 6. MID-LEFT CPU GAUGE & 8-CORE THREAD EQUALIZER
    # -------------------------------------------------------------
    def _draw_cpu_and_multicore_cluster(self, x, y):
        radius = 30
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        cpu_ext = min(300.0, max(20.0, self.cpu_pct * 3.0))
        self.create_arc(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, start=210, extent=-cpu_ext, style="arc", outline="#00f0ff", width=3)

        self.create_text(x, y - 8, text="CPU CLOCK", font=FONT_HUD_TINY, fill="#38bdf8")
        self.create_text(x, y + 2, text=f"{self.cpu_pct/100 * 3.2:.2f} GHz", font=("Segoe UI", 8, "bold"), fill="#ffffff")
        self.create_text(x, y + 12, text=f"{int(self.cpu_pct)}% LOAD", font=FONT_HUD_TINY, fill="#00ffaa")

        # 8-Core Thread Load Equalizer directly below
        eq_x = x - 28
        eq_y = y + radius + 10
        for core_i in range(8):
            ch = (self.core_loads[core_i] / 100.0) * 14
            bx = eq_x + core_i * 7
            self.create_rectangle(bx, eq_y - ch, bx + 5, eq_y, fill="#00f0ff" if core_i % 2 == 0 else "#0088ff", outline="")
        self.create_text(x, eq_y + 8, text="CORES: C0 - C7", font=("Consolas", 6), fill="#64748b")

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
    # 8. QUANTUM NUCLEUS ATOM HOLOGRAM
    # -------------------------------------------------------------
    def _draw_pratham_expo_atom_hologram(self, x, y):
        rx = 36
        ry = 12
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

        self.create_text(x, y - 6, text="QUANTUM", font=("Segoe UI", 7, "bold"), fill="#38bdf8")
        self.create_text(x, y + 4, text="NUCLEUS", font=("Segoe UI", 10, "bold"), fill="#ffffff")
        self.create_text(x, y + 15, text="MARK VII CORE", font=("Segoe UI", 6, "bold"), fill="#00ffaa")

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

        self.create_text(x, y + 28, text="ATTITUDE // PITCH 0.0°", font=("Consolas", 6), fill="#64748b")

    # -------------------------------------------------------------
    # 10. REACTOR ENERGY GAUGE (100% // PEAK)
    # -------------------------------------------------------------
    def _draw_reactor_energy_gauge(self, x, y):
        radius = 30
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#082240", width=1)
        self.create_arc(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, start=0, extent=360, style="arc", outline="#00f0ff", width=3)
        self.create_text(x, y - 6, text="REACTOR FLUX", font=FONT_HUD_TINY, fill="#38bdf8")
        self.create_text(x, y + 5, text="100%", font=("Segoe UI", 8, "bold"), fill="#ffffff")
        self.create_text(x, y + 16, text="PEAK OUTPUT", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # 11. RECYCLE REPOSITORY & SYSTEM STABILITY TELEMETRY
    # -------------------------------------------------------------
    def _draw_trash_uptime_telemetry(self, x, y):
        self.create_text(x, y, text="♺ TRASH REPOSITORY: 0 OBJECTS", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x, y + 14, text="SYSTEM STABILITY: 99.9% // OK", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        self.create_text(x, y + 28, text="COMMS: 0 PENDING PACKETS // SECURE", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        for i in range(3):
            self.create_oval(x + i * 14, y + 40, x + i * 14 + 6, y + 40 + 6, fill="#00f0ff" if i == 0 else "#0a264a", outline="")

    # -------------------------------------------------------------
    # 12. LOWER-LEFT DUAL CONCENTRIC NETWORK METER (0.0k / 1.6k)
    # -------------------------------------------------------------
    def _draw_dual_network_dial(self, x, y):
        r_out = 36
        r_in = 24
        self.create_arc(x - r_out, y - r_out, x + r_out, y + r_out, start=220, extent=-240, style="arc", outline="#00f0ff", width=4)
        self.create_arc(x - r_in, y - r_in, x + r_in, y + r_in, start=200, extent=-200, style="arc", outline="#0088ff", width=3)

        self.create_text(x, y - 5, text="0.0k", font=FONT_HUD_TINY, fill="#ffffff")
        self.create_text(x, y + 5, text="1.6k", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # 13. BOTTOM-LEFT WINDOWS CONTROLS & OS KERNEL STATUS
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

        # OS Kernel Status
        self.create_text(x + 130, y + 2, text="OS KERNEL: ACTIVE", font=FONT_MONO, fill="#00ffaa", anchor="w")

    # -------------------------------------------------------------
    # 14. THE GRAND MASTER ARC REACTOR CORE
    # -------------------------------------------------------------
    def _draw_grand_arc_reactor(self, cx, cy, core_cyan, glow_blue, accent_red):
        """Draw the hyper-intricate Pratham Prasad Saathi Arc Reactor assembly."""
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
    # 15. BOTTOM LAUNCHER NODES & PRATHAM PRASAD BADGE
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

        # PRATHAM PRASAD Tactical Slash Banner
        banner_y = base_y + 72
        self.create_polygon(
            cx - 140, banner_y + 8, cx - 128, banner_y - 8, cx + 128, banner_y - 8,
            cx + 140, banner_y + 8, fill="", outline="#0e3a6c", width=1
        )
        self.create_text(cx, banner_y, text="SAATHI AI // COGNITIVE CORE MARK VII", font=("Segoe UI", 11, "bold"), fill="#00f0ff")

    # -------------------------------------------------------------
    # 16. 3D ROTATING GYROSCOPE CUBE & RADAR SCOPE
    # -------------------------------------------------------------
    def _draw_3d_cube_and_radar(self, x, y):
        # Frame 1: 3D Holographic Rotating Gyroscope Cube
        r_box = 30
        self.create_oval(x - r_box, y - r_box, x + r_box, y + r_box, outline="#00f0ff", width=1)
        self.create_arc(x - r_box + 2, y - r_box + 2, x + r_box - 2, y + r_box - 2, start=30, extent=-120, style="arc", outline="#0088ff", width=2)

        # 3D Math Projection
        d = 60
        scale_size = 13
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

        self.create_text(x, y + r_box + 9, text="3D GIMBAL", font=FONT_HUD_TINY, fill="#38bdf8")

        # Frame 2: Tactical Radar Scope with Sweeping Blips
        r_rad = x + 72
        self.create_oval(r_rad - r_box, y - r_box, r_rad + r_box, y + r_box, outline="#00f0ff", width=1)
        self.create_oval(r_rad - 18, y - 18, r_rad + 18, y + 18, outline="#082547", width=1)
        self.create_line(r_rad - r_box, y, r_rad + r_box, y, fill="#082547", width=1)
        self.create_line(r_rad, y - r_box, r_rad, y + r_box, fill="#082547", width=1)

        # Radar sweep ray
        sw_ang = self.angle_radar
        self.create_line(r_rad, y, r_rad + r_box * math.cos(sw_ang), y + r_box * math.sin(sw_ang), fill="#00ffaa", width=1)

        # Radar blips
        for b_r, b_ang, b_int in self.radar_blips:
            scaled_br = min(b_r * 0.72, r_box - 3)
            diff = (sw_ang - b_ang) % (2 * math.pi)
            if diff < 0.8:
                col = "#00ffaa"
            else:
                col = "#005533"
            bx = r_rad + scaled_br * math.cos(b_ang)
            by = y + scaled_br * math.sin(b_ang)
            self.create_oval(bx - 2, by - 2, bx + 2, by + 2, fill=col, outline="")

        self.create_text(r_rad, y + r_box + 9, text="360° RADAR", font=FONT_HUD_TINY, fill="#00ffaa")

    # -------------------------------------------------------------
    # 17. MID-RIGHT TACTICAL INTEL STREAM
    # -------------------------------------------------------------
    def _draw_tactical_intel_stream(self, x, y):
        self.create_text(x, y, text="TACTICAL INTEL STREAM", font=("Segoe UI", 8, "bold"), fill="#00f0ff", anchor="w")

        intel_items = [
            ("KINOPOISK", "LINK ACTIVE", "#00ffaa"),
            ("BATTLESHIP", "GRID NOMINAL", "#38bdf8"),
            ("CRIMSON", "THREAT RDY", "#ffaa00"),
            ("HARMONIC", "SYNCED OK", "#00ffaa"),
            ("LE HAVRE", "CACHE 100%", "#38bdf8"),
            ("VANGUARD", "FOC READY", "#8b5cf6")
        ]
        for idx, (label, status, scol) in enumerate(intel_items):
            iy = y + 16 + idx * 14
            self.create_text(x, iy, text=f"• {label}:", font=FONT_HUD_TINY, fill="#38bdf8" if idx == 0 else "#64748b", anchor="w")
            self.create_text(x + 145, iy, text=status, font=FONT_HUD_TINY, fill=scol, anchor="e")

    # -------------------------------------------------------------
    # 18. LOWER-RIGHT ROLLING NETWORK SPARKLINES
    # -------------------------------------------------------------
    def _draw_network_sparklines(self, x, y):
        # Inflow / Download
        self.create_text(x, y, text=f"NET IN: {self.cur_down_kb:.1f} KB/S", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x + 145, y, text="169.4 GB", font=FONT_HUD_TINY, fill="#00ffaa", anchor="e")

        pts_down = []
        graph_w = 145
        graph_h = 16
        for i, val in enumerate(self.net_down_history):
            gx = x + i * (graph_w / len(self.net_down_history))
            gy = (y + 20) - (val / 100.0) * graph_h
            pts_down.extend([gx, gy])
        if len(pts_down) >= 4:
            self.create_line(pts_down, fill="#00f0ff", width=1)

        # Outflow / Upload
        up_y = y + 28
        self.create_text(x, up_y, text=f"NET OUT: {self.cur_up_kb:.1f} KB/S", font=FONT_HUD_TINY, fill="#38bdf8", anchor="w")
        self.create_text(x + 145, up_y, text="32.9 GB", font=FONT_HUD_TINY, fill="#0088ff", anchor="e")

        pts_up = []
        for i, val in enumerate(self.net_up_history):
            gx = x + i * (graph_w / len(self.net_up_history))
            gy = (up_y + 20) - (val / 100.0) * graph_h
            pts_up.extend([gx, gy])
        if len(pts_up) >= 4:
            self.create_line(pts_up, fill="#0088ff", width=1)

        # Media Control Strip
        strip_y = up_y + 28
        self.create_rectangle(x, strip_y, x + 145, strip_y + 14, outline="#0a2a50", fill="#030d1c")
        self.create_text(x + 72, strip_y + 7, text="⏮   ▶   ⏸   ⏭   🔊 [━●━]", font=FONT_HUD_TINY, fill="#00f0ff")

    # -------------------------------------------------------------
    # 19. FAR-RIGHT SATELLITE METEOROLOGICAL & MOON STATION
    # -------------------------------------------------------------
    def _draw_weather_moon_station(self, x, start_y, total_h):
        now = datetime.datetime.now()
        self.create_text(x, start_y, text=f"SYNC {now.strftime('%m/%d %H:%M')}", font=FONT_HUD_TINY, fill="#64748b", anchor="w")

        # Temperature
        self.create_text(x, start_y + 26, text="24°C", font=("Segoe UI", 22, "bold"), fill="#ffffff", anchor="w")

        # Glowing Moon Graphic
        m_x = x + 115
        m_y = start_y + 26
        self.create_oval(m_x - 18, m_y - 18, m_x + 18, m_y + 18, fill="#1c3a60", outline="#00f0ff", width=1)
        self.create_oval(m_x - 7, m_y - 5, m_x - 2, m_y, fill="#0d1f36", outline="")
        self.create_oval(m_x + 2, m_y + 3, m_x + 8, m_y + 9, fill="#0d1f36", outline="")
        self.create_oval(m_x - 3, m_y + 7, m_x, m_y + 10, fill="#0d1f36", outline="")

        self.create_text(x, start_y + 50, text="ATMOSPHERE: CLEAR // OK", font=("Segoe UI", 8, "bold"), fill="#00ffaa", anchor="w")

        # Atmospheric Metrics in English
        specs = [
            ("HUMIDITY", "77%"),
            ("FEELS LIKE", "24°C"),
            ("PRECIPITATION", "0%"),
            ("VISIBILITY", "10.0 KM"),
            ("WIND VELOCITY", "3 KM/H"),
            ("SOLAR DAWN", "05:42 AM"),
            ("SOLAR DUSK", "06:38 PM")
        ]
        for idx, (lbl, val) in enumerate(specs):
            sy = start_y + 66 + idx * 13
            self.create_text(x, sy, text=f"{lbl}:", font=FONT_HUD_TINY, fill="#38bdf8" if idx == 0 else "#64748b", anchor="w")
            self.create_text(x + 130, sy, text=val, font=FONT_HUD_TINY, fill="#ffffff" if idx == 0 else "#94a3b8", anchor="e")

        # 7-Day Meteorological Trajectory
        fc_start_y = start_y + 165
        self.create_text(x, fc_start_y, text="7-DAY FORECAST:", font=("Segoe UI", 8, "bold"), fill="#00f0ff", anchor="w")

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
            fy = fc_start_y + 16 + f_idx * 26
            if fy + 22 > total_h - 10:
                break
            self.create_text(x, fy, text=day, font=("Segoe UI", 8, "bold"), fill="#ffffff", anchor="w")
            self.create_text(x + 130, fy, text=temp, font=("Segoe UI", 8, "bold"), fill="#00ffaa", anchor="e")
            self.create_text(x, fy + 11, text=cond, font=FONT_HUD_TINY, fill=c_col, anchor="w")

    # -------------------------------------------------------------
    # 20. NEURAL NETWORK INITIALIZATION & SYNAPTIC PLEXUS
    # -------------------------------------------------------------
    def _init_neural_network(self):
        """Initialize deep machinery neural nodes across the holographic workspace."""
        self.neural_nodes = []
        raw_nodes = [
            # Cognitive Cluster (Left Manifold)
            {"ox": -360, "oy": -150, "layer": "surface", "hub": True, "label": "SYN-A1"},
            {"ox": -320, "oy": -100, "layer": "surface", "hub": False, "label": ""},
            {"ox": -380, "oy": -50, "layer": "deep", "hub": False, "label": ""},
            {"ox": -420, "oy": -120, "layer": "surface", "hub": False, "label": ""},
            {"ox": -290, "oy": -170, "layer": "surface", "hub": False, "label": ""},
            {"ox": -440, "oy": 20, "layer": "deep", "hub": False, "label": ""},
            {"ox": -390, "oy": 80, "layer": "surface", "hub": True, "label": "AXON-4"},
            {"ox": -430, "oy": 160, "layer": "deep", "hub": False, "label": ""},
            {"ox": -360, "oy": 220, "layer": "surface", "hub": False, "label": ""},
            {"ox": -400, "oy": 290, "layer": "surface", "hub": False, "label": ""},

            # Deep Machinery Sub-Surface Lattice (Central Interior)
            {"ox": -220, "oy": -60, "layer": "deep", "hub": False, "label": ""},
            {"ox": -170, "oy": -90, "layer": "deep", "hub": False, "label": ""},
            {"ox": -110, "oy": -140, "layer": "deep", "hub": True, "label": "COR-01"},
            {"ox": -60, "oy": -180, "layer": "deep", "hub": False, "label": ""},
            {"ox": 60, "oy": -180, "layer": "deep", "hub": False, "label": ""},
            {"ox": 110, "oy": -140, "layer": "deep", "hub": True, "label": "COR-02"},
            {"ox": 170, "oy": -90, "layer": "deep", "hub": False, "label": ""},
            {"ox": 220, "oy": -60, "layer": "deep", "hub": False, "label": ""},

            # Central Core Orbit Halo
            {"ox": -195, "oy": -120, "layer": "surface", "hub": False, "label": ""},
            {"ox": -145, "oy": -180, "layer": "surface", "hub": False, "label": ""},
            {"ox": 0, "oy": -215, "layer": "surface", "hub": True, "label": "NEXUS-0"},
            {"ox": 145, "oy": -180, "layer": "surface", "hub": False, "label": ""},
            {"ox": 195, "oy": -120, "layer": "surface", "hub": False, "label": ""},
            {"ox": -205, "oy": 40, "layer": "surface", "hub": False, "label": ""},
            {"ox": -185, "oy": 120, "layer": "surface", "hub": False, "label": ""},
            {"ox": -125, "oy": 185, "layer": "surface", "hub": False, "label": ""},
            {"ox": 0, "oy": 220, "layer": "surface", "hub": True, "label": "NEXUS-B"},
            {"ox": 125, "oy": 185, "layer": "surface", "hub": False, "label": ""},
            {"ox": 185, "oy": 120, "layer": "surface", "hub": False, "label": ""},
            {"ox": 205, "oy": 40, "layer": "surface", "hub": False, "label": ""},

            # Conduit Bridges to Column 3
            {"ox": 235, "oy": 20, "layer": "deep", "hub": False, "label": ""},
            {"ox": 260, "oy": -80, "layer": "deep", "hub": False, "label": ""},
            {"ox": 250, "oy": 110, "layer": "deep", "hub": False, "label": ""},

            # Tactical Right Cluster
            {"ox": 285, "oy": -185, "layer": "surface", "hub": False, "label": ""},
            {"ox": 340, "oy": -155, "layer": "surface", "hub": True, "label": "SYN-R1"},
            {"ox": 390, "oy": -115, "layer": "deep", "hub": False, "label": ""},
            {"ox": 420, "oy": -45, "layer": "surface", "hub": False, "label": ""},
            {"ox": 340, "oy": 65, "layer": "surface", "hub": False, "label": ""},
            {"ox": 400, "oy": 115, "layer": "deep", "hub": False, "label": ""},
            {"ox": 360, "oy": 175, "layer": "surface", "hub": True, "label": "SYN-R2"}
        ]

        for idx, item in enumerate(raw_nodes):
            self.neural_nodes.append({
                "ox": item["ox"],
                "oy": item["oy"],
                "layer": item["layer"],
                "hub": item["hub"],
                "label": item["label"],
                "dx": random.uniform(-4, 4),
                "dy": random.uniform(-4, 4),
                "vx": random.uniform(-0.25, 0.25),
                "vy": random.uniform(-0.25, 0.25),
                "pulse": random.uniform(0, math.pi * 2),
                "color": "#00f0ff" if idx % 3 != 0 else "#8b5cf6",
                "flash": 0.0
            })

        self.synaptic_pulses = []
        self.random_synaptic_bridges = []
        self.synapse_rewire_counter = 0

    def _init_circuit_packets(self):
        """Initialize data packets flowing through laser circuit traces."""
        self.circuit_packets = []
        for i in range(6):
            self.circuit_packets.append({
                "trace_idx": i,
                "t": random.uniform(0.0, 1.0),
                "speed": random.uniform(0.015, 0.035),
                "color": "#00f0ff" if i % 2 == 0 else "#ffffff"
            })

    def _init_quantum_particles(self):
        """Initialize ambient floating 3D quantum light particles."""
        self.quantum_particles = []
        for _ in range(40):
            self.quantum_particles.append({
                "x": random.uniform(-500, 500),
                "y": random.uniform(-300, 300),
                "z": random.uniform(50, 250),
                "vx": random.uniform(-0.4, 0.4),
                "vy": random.uniform(-0.4, 0.4),
                "vz": random.uniform(-0.2, 0.2),
                "color": random.choice(["#00f0ff", "#8b5cf6", "#00ffaa", "#38bdf8"]),
                "size": random.uniform(1.2, 2.5)
            })

    def _init_tesseract(self):
        """Initialize 4D Hypercube / Tesseract 16 vertices and 32 edges."""
        self.tesseract_vertices = []
        for x in (-1, 1):
            for y in (-1, 1):
                for z in (-1, 1):
                    for w in (-1, 1):
                        self.tesseract_vertices.append([x, y, z, w])

        self.tesseract_edges = []
        for i in range(16):
            for j in range(i + 1, 16):
                diffs = sum(1 for k in range(4) if self.tesseract_vertices[i][k] != self.tesseract_vertices[j][k])
                if diffs == 1:
                    self.tesseract_edges.append((i, j))
        self.angle_4d_xw = 0.0
        self.angle_4d_yz = 0.0

    def _draw_quantum_particle_field(self, cx, cy, w, h):
        """Render drifting floating 3D quantum ambient light dust field across the background."""
        d = 200.0
        for p in self.quantum_particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["z"] += p["vz"]

            if abs(p["x"]) > 550: p["vx"] *= -1
            if abs(p["y"]) > 350: p["vy"] *= -1
            if p["z"] < 30 or p["z"] > 280: p["vz"] *= -1

            scale = d / (d + p["z"])
            px = cx + p["x"] * scale
            py = cy + p["y"] * scale

            r = p["size"] * scale
            self.create_oval(px - r, py - r, px + r, py + r, fill=p["color"], outline="")
            if random.random() < 0.05:
                self.create_oval(px - (r + 2), py - (r + 2), px + (r + 2), py + (r + 2), outline="#ffffff", width=1)

    def _draw_hyperdimensional_tesseract_core(self, cx, cy):
        """Render rotating 4D Tesseract hypercube matrix projected inside the central reactor core."""
        self.angle_4d_xw = (self.angle_4d_xw + 0.025) % (2 * math.pi)
        self.angle_4d_yz = (self.angle_4d_yz + 0.035) % (2 * math.pi)

        cos_xw = math.cos(self.angle_4d_xw); sin_xw = math.sin(self.angle_4d_xw)
        cos_yz = math.cos(self.angle_4d_yz); sin_yz = math.sin(self.angle_4d_yz)

        nodes_2d = []
        d4 = 3.5
        d3 = 180.0
        scale_size = 28 + self.audio_level * 18

        for vx, vy, vz, vw in self.tesseract_vertices:
            # 4D Rotation in X-W plane
            x1 = vx * cos_xw - vw * sin_xw
            w1 = vx * sin_xw + vw * cos_xw

            # 4D Rotation in Y-Z plane
            y1 = vy * cos_yz - vz * sin_yz
            z1 = vy * sin_yz + vz * cos_yz

            # 4D to 3D perspective projection
            w_scale = 1.0 / (d4 - w1 * 0.4)
            x3d = x1 * w_scale
            y3d = y1 * w_scale
            z3d = z1 * w_scale

            # 3D to 2D perspective projection
            z_scale = d3 / (d3 + z3d * 40.0)
            px = cx + (x3d * scale_size) * z_scale
            py = cy + (y3d * scale_size) * z_scale

            nodes_2d.append((px, py, z3d))

        # Render 32 Tesseract Edges with glowing depth colors
        for i, j in self.tesseract_edges:
            p1, p2 = nodes_2d[i], nodes_2d[j]
            avg_z = (p1[2] + p2[2]) / 2.0
            edge_col = "#ffffff" if avg_z < 0 else ("#00f0ff" if avg_z < 0.5 else "#062e54")
            lw = 2 if avg_z < 0 else 1
            self.create_line(p1[0], p1[1], p2[0], p2[1], fill=edge_col, width=lw)

    def _draw_tactical_holographic_scanlines(self, cx, cy, w, h):
        """Render sweeping holographic laser scanlines and cascading hex telemetry data streams."""
        # Sweeping horizontal laser scanline
        scan_y = (self.pulse * 140) % (h - 60) + 30
        self.create_line(25, scan_y, w - 25, scan_y, fill="#041f3d", width=1, dash=(8, 12))

        # Cascading Hex Addresses along central bus
        hex_samples = ["0x7F4A", "0x8B1C", "ADDR_CORE", "FLUX_NOMINAL", "0x3E9D", "SYN_GRID_OK"]
        for idx, sample in enumerate(hex_samples):
            hy = cy - 120 + idx * 42
            hx = cx + math.sin(self.pulse + idx) * 110
            self.create_text(hx, hy, text=sample, font=("Consolas", 6), fill="#00a8ff" if idx % 2 == 0 else "#00ffaa")

    # -------------------------------------------------------------
    # 20B. DYNAMIC 3D HOLOGRAPHIC THREAD RIBBONS (TECHIE VISUALS)
    # -------------------------------------------------------------
    def _draw_3d_holographic_threads(self, cx, cy):
        """Render multi-strand 3D helical ribbons and dynamic volumetric thread streams around the reactor core."""
        num_strands = 4
        points_per_strand = 28
        d = 160 # perspective distance

        for s_idx in range(num_strands):
            strand_phase = self.pulse * 1.6 + s_idx * (math.pi / 2)
            pts = []
            cols = ["#00f0ff", "#8b5cf6", "#00ffaa", "#38bdf8"]
            strand_col = cols[s_idx % len(cols)]

            for i in range(points_per_strand):
                t = i / points_per_strand
                angle = t * math.pi * 3.5 + strand_phase
                radius_3d = 150 + math.sin(t * math.pi + self.pulse) * 30

                # 3D Helix coordinates
                x3d = radius_3d * math.cos(angle)
                y3d = (t - 0.5) * 260
                z3d = radius_3d * math.sin(angle)

                # 3D Rotation around X & Y
                rx = self.angle_3d_x * 0.6
                ry = self.angle_3d_y * 0.6

                x1 = x3d * math.cos(ry) + z3d * math.sin(ry)
                z1 = -x3d * math.sin(ry) + z3d * math.cos(ry)
                y1 = y3d * math.cos(rx) - z1 * math.sin(rx)
                z2 = y3d * math.sin(rx) + z1 * math.cos(rx)

                scale = d / (d + z2 * 0.35)
                px = cx + x1 * scale
                py = cy + y1 * scale

                pts.append((px, py, z2))

            for i in range(len(pts) - 1):
                p1, p2 = pts[i], pts[i + 1]
                avg_z = (p1[2] + p2[2]) / 2.0

                if avg_z < -40:
                    l_col = "#ffffff"
                    lw = 2
                elif avg_z < 30:
                    l_col = strand_col
                    lw = 1
                else:
                    l_col = "#041a33"
                    lw = 1

                self.create_line(p1[0], p1[1], p2[0], p2[1], fill=l_col, width=lw)

                # Pulse packets along 3D threads
                if (i + int(self.pulse * 12)) % 7 == 0:
                    self.create_oval(p1[0] - 2, p1[1] - 2, p1[0] + 2, p1[1] + 2, fill="#ffffff", outline=strand_col)

    # -------------------------------------------------------------
    # 21. HOLOGRAPHIC HONEYCOMB FORCEFIELD SHIELD
    # -------------------------------------------------------------
    def _draw_honeycomb_shield(self, cx, cy):
        """Draw concentric hexagonal forcefield matrix with expanding energy ripple."""
        radii = [190, 215, 240]
        pulse_scale = math.sin(self.pulse * 1.5) * 3

        for idx, base_r in enumerate(radii):
            r = base_r + pulse_scale
            # 6 Hexagonal Vertices
            pts = []
            for h_i in range(6):
                ang = h_i * (math.pi / 3) + (self.pulse * 0.05 if idx % 2 == 0 else -self.pulse * 0.05)
                px = cx + r * math.cos(ang)
                py = cy + r * math.sin(ang)
                pts.extend([px, py])
                # Small corner junction diamond
                self.create_oval(px - 1.5, py - 1.5, px + 1.5, py + 1.5, fill="#00f0ff", outline="")

            # Close hexagon polygon
            pts.extend([pts[0], pts[1]])
            self.create_line(pts, fill="#072242", width=1, dash=(4, 6))

    # -------------------------------------------------------------
    # 22. DYNAMIC NEURAL SYNAPSE PLEXUS & ACTION POTENTIALS
    # -------------------------------------------------------------
    def _update_and_draw_neural_plexus(self, cx, cy, w, h, core_color):
        """Update and render interconnected neural nodes and streaming synaptic data packets."""
        node_coords = []
        num_nodes = len(self.neural_nodes)

        # 1. Update positions & draw node bodies
        for node in self.neural_nodes:
            # Drift within bounds
            node["dx"] += node["vx"]
            node["dy"] += node["vy"]
            if abs(node["dx"]) > 12:
                node["vx"] *= -1
            if abs(node["dy"]) > 12:
                node["vy"] *= -1

            node["pulse"] = (node["pulse"] + 0.07) % (math.pi * 2)
            if node["flash"] > 0:
                node["flash"] = max(0.0, node["flash"] - 0.08)

            nx = cx + node["ox"] + node["dx"]
            ny = cy + node["oy"] + node["dy"]
            node_coords.append((nx, ny))

        # 2. Manage Dynamic Randomized Neural Bridges (Deep Machinery Visuals)
        self.synapse_rewire_counter += 1
        alive_bridges = []
        for bridge in self.random_synaptic_bridges:
            bridge["life"] -= 1
            if bridge["life"] > 0:
                alive_bridges.append(bridge)
        self.random_synaptic_bridges = alive_bridges

        # Spawn new random neural links periodically or if pool is small
        if num_nodes >= 2 and (len(self.random_synaptic_bridges) < 7 or self.synapse_rewire_counter % 18 == 0):
            i = random.randrange(num_nodes)
            j = random.randrange(num_nodes)
            if i != j:
                bridge_colors = ["#00f0ff", "#8b5cf6", "#00ffaa", "#38bdf8", "#06b6d4"]
                b_col = random.choice(bridge_colors)
                self.random_synaptic_bridges.append({
                    "i": i,
                    "j": j,
                    "life": random.randint(45, 90),
                    "max_life": 90,
                    "color": b_col
                })

        # 3. Draw Proximity Filaments
        connected_pairs = []
        for i in range(num_nodes):
            x1, y1 = node_coords[i]
            for j in range(i + 1, num_nodes):
                x2, y2 = node_coords[j]
                dx = x1 - x2
                dy = y1 - y2
                dist_sq = dx * dx + dy * dy
                if dist_sq < 8100:  # < 90 pixels
                    dist = math.sqrt(dist_sq)
                    connected_pairs.append((i, j, x1, y1, x2, y2))
                    is_deep = (self.neural_nodes[i]["layer"] == "deep" and self.neural_nodes[j]["layer"] == "deep")
                    if is_deep:
                        fil_col = "#04182e" if dist > 55 else "#062242"
                        self.create_line(x1, y1, x2, y2, fill=fil_col, width=1, dash=(2, 4))
                    else:
                        fil_col = "#062242" if dist > 65 else "#0a3666"
                        self.create_line(x1, y1, x2, y2, fill=fil_col, width=1)

        # 4. Draw Randomized Futuristic Neural Bridges
        for bridge in self.random_synaptic_bridges:
            idx_a, idx_b = bridge["i"], bridge["j"]
            if idx_a < num_nodes and idx_b < num_nodes:
                bx1, by1 = node_coords[idx_a]
                bx2, by2 = node_coords[idx_b]
                fade_ratio = bridge["life"] / bridge["max_life"]
                # Cyber dash pattern for randomized deep machinery links
                self.create_line(bx1, by1, bx2, by2, fill=bridge["color"] if fade_ratio > 0.4 else "#0a3666", width=1, dash=(3, 5))

        # 5. Draw Node Bodies, Hub Halos & Labels
        for idx, node in enumerate(self.neural_nodes):
            nx, ny = node_coords[idx]
            base_r = 2.4 + math.sin(node["pulse"]) * 0.6

            if node["flash"] > 0:
                # Expanding high-energy ripple on arrival
                flash_r = base_r + node["flash"] * 7
                self.create_oval(nx - flash_r, ny - flash_r, nx + flash_r, ny + flash_r, outline="#ffffff", width=1)
                self.create_oval(nx - base_r, ny - base_r, nx + base_r, ny + base_r, fill="#ffffff", outline="")
            elif node["layer"] == "deep":
                # Deep machinery sub-surface junction (tiny diamond marker)
                self.create_rectangle(nx - 2, ny - 2, nx + 2, ny + 2, outline="#082c54", fill="#041428")
                self.create_oval(nx - 1, ny - 1, nx + 1, ny + 1, fill=node["color"], outline="")
            else:
                # Surface synaptic node
                self.create_oval(nx - (base_r + 2), ny - (base_r + 2), nx + (base_r + 2), ny + (base_r + 2), outline="#072445", width=1)
                self.create_oval(nx - base_r, ny - base_r, nx + base_r, ny + base_r, fill=node["color"], outline="")

            # Major Hub Tag & Ring
            if node["hub"]:
                hub_r = base_r + 5
                self.create_oval(nx - hub_r, ny - hub_r, nx + hub_r, ny + hub_r, outline="#00f0ff", width=1, dash=(2, 3))
                if node["label"]:
                    self.create_text(nx, ny - 10, text=node["label"], font=FONT_HUD_TINY, fill="#38bdf8")

        # 6. Spawn New Synaptic Pulses (Action Potentials)
        spawn_rate = 0.40 + self.audio_level * 0.8
        if self.state in ("THINKING", "PLANNING", "SPEAKING"):
            spawn_rate = 0.85

        if random.random() < spawn_rate:
            # Can spawn along standard proximity filament OR along random dynamic bridge
            if self.random_synaptic_bridges and random.random() < 0.45:
                br = random.choice(self.random_synaptic_bridges)
                i, j = br["i"], br["j"]
                speed = random.uniform(0.03, 0.07)
                self.synaptic_pulses.append([i, j, 0.0, speed, br["color"]])
            elif connected_pairs:
                pair = random.choice(connected_pairs)
                i, j = pair[0], pair[1]
                speed = random.uniform(0.04, 0.08)
                pulse_col = "#00f0ff" if random.random() < 0.65 else "#8b5cf6"
                self.synaptic_pulses.append([i, j, 0.0, speed, pulse_col])

        # 7. Advance & Render Active Synaptic Pulses
        alive_pulses = []
        for pulse in self.synaptic_pulses:
            i, j, t, spd, col = pulse
            t += spd
            if t >= 1.0:
                # Arrival flash on destination node
                if j < num_nodes:
                    self.neural_nodes[j]["flash"] = 1.0
                continue

            alive_pulses.append([i, j, t, spd, col])
            if i < num_nodes and j < num_nodes:
                x1, y1 = node_coords[i]
                x2, y2 = node_coords[j]
                px = x1 + (x2 - x1) * t
                py = y1 + (y2 - y1) * t

                # Glowing Action Potential Packet with Comet Spark Tail
                self.create_oval(px - 2.5, py - 2.5, px + 2.5, py + 2.5, fill="#ffffff", outline="")
                tail_t = max(0.0, t - 0.16)
                tx = x1 + (x2 - x1) * tail_t
                ty = y1 + (y2 - y1) * tail_t
                self.create_line(tx, ty, px, py, fill=col, width=2)

        self.synaptic_pulses = alive_pulses[:45]

    # -------------------------------------------------------------
    # 23. CIRCUIT BUS STREAMING DATA PACKETS
    # -------------------------------------------------------------
    def _update_and_draw_circuit_packets(self, cx, cy):
        """Render data packets traveling along the main laser circuit bus lines into the Arc Reactor."""
        traces = [
            [(cx - 270, cy - 100), (cx - 240, cy - 40), (cx - 150, cy - 40)],
            [(cx - 250, cy + 120), (cx - 220, cy + 30), (cx - 150, cy + 30)],
            [(cx + 175, cy - 190), (cx + 120, cy - 190), (cx + 60, cy - 140)],
            [(cx + 270, cy - 60), (cx + 220, cy - 20), (cx + 150, cy - 20)],
            [(cx + 270, cy + 120), (cx + 240, cy + 50), (cx + 150, cy + 50)],
            [(cx - 240, cy + 190), (cx - 190, cy + 190), (cx - 140, cy + 140)],
        ]

        for pkt in self.circuit_packets:
            pkt["t"] += pkt["speed"]
            if pkt["t"] >= 1.0:
                pkt["t"] = 0.0

            poly = traces[pkt["trace_idx"]]
            # 2 segments per polyline
            t_val = pkt["t"]
            if t_val < 0.5:
                # Segment 0 -> 1
                seg_t = t_val * 2.0
                p1, p2 = poly[0], poly[1]
            else:
                # Segment 1 -> 2
                seg_t = (t_val - 0.5) * 2.0
                p1, p2 = poly[1], poly[2]

            curr_x = p1[0] + (p2[0] - p1[0]) * seg_t
            curr_y = p1[1] + (p2[1] - p1[1]) * seg_t

            # Draw capsule packet
            self.create_oval(curr_x - 2.5, curr_y - 2.5, curr_x + 2.5, curr_y + 2.5, fill="#ffffff", outline=pkt["color"], width=1)

    # -------------------------------------------------------------
    # 24. HIGH-VOLTAGE PLASMA LIGHTNING DISCHARGES
    # -------------------------------------------------------------
    def _draw_plasma_lightning(self, cx, cy, r_iris, core_color):
        """Draw authentic high-voltage electric plasma sparks between coils and central iris."""
        # Determine number of lightning arcs based on audio & state
        num_arcs = 1
        if self.audio_level > 0.2:
            num_arcs = 2
        if self.state in ("THINKING", "PLANNING", "EXECUTING", "SPEAKING"):
            num_arcs = 3

        for a_i in range(num_arcs):
            # Pick a coil angle
            c_idx = (int(self.pulse * 4) + a_i * 4) % 12
            c_ang = self.angle_coils + c_idx * (2 * math.pi / 12)

            start_x = cx + 84 * math.cos(c_ang)
            start_y = cy + 84 * math.sin(c_ang)

            target_x = cx + r_iris * math.cos(c_ang + 0.15)
            target_y = cy + r_iris * math.sin(c_ang + 0.15)

            # Generate fractal jagged arc
            coords = [start_x, start_y]
            steps = 4
            for s in range(1, steps):
                f = s / steps
                lx = start_x + (target_x - start_x) * f
                ly = start_y + (target_y - start_y) * f
                # Perpendicular displacement
                nx = -(target_y - start_y)
                ny = (target_x - start_x)
                n_len = math.hypot(nx, ny) or 1.0
                nx /= n_len
                ny /= n_len
                offset = (random.random() - 0.5) * 12
                coords.extend([lx + nx * offset, ly + ny * offset])
            coords.extend([target_x, target_y])

            # Draw Cyan Lightning Halo & White Core Filament
            self.create_line(coords, fill="#00f0ff", width=2)
            self.create_line(coords, fill="#ffffff", width=1)

    # -------------------------------------------------------------
    # 25. TACTICAL RETICLE LOCK-ON SYSTEM
    # -------------------------------------------------------------
    def _draw_tactical_lock_reticle(self, cx, cy):
        """Draw an active targeting lock-on bracket circling orbital nodes."""
        # Lock onto node 'Cyber Engine' at angle 25 deg
        lock_ang = math.radians(-25)
        lx = cx + 188 * math.cos(lock_ang)
        ly = cy + 188 * math.sin(lock_ang)

        b_size = 14
        rot = self.angle_radar * 0.8
        # 4 rotating corner brackets
        for c_i in range(4):
            corner_ang = rot + c_i * (math.pi / 2)
            px = lx + b_size * math.cos(corner_ang)
            py = ly + b_size * math.sin(corner_ang)
            self.create_line(px - 3, py, px + 3, py, fill="#00ffaa", width=1)
            self.create_line(px, py - 3, px, py + 3, fill="#00ffaa", width=1)

        # Digital Telemetry Readout
        self.create_text(lx + 24, ly - 6, text="LOCK: SEC-04", font=("Consolas", 6, "bold"), fill="#00ffaa", anchor="w")
        self.create_text(lx + 24, ly + 4, text="RNG: 14.8 KM // TRK: ACTIVE", font=("Consolas", 6), fill="#38bdf8", anchor="w")

