import math
import time
import threading
import tkinter as tk
from typing import Optional, Dict, Any
from .theme import (
    COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_BORDER_GLOW,
    COLOR_CYAN, COLOR_BLUE, COLOR_EMERALD, COLOR_AMBER, COLOR_PURPLE,
    COLOR_ERROR, COLOR_CORE_WHITE, COLOR_COPPER, COLOR_TEXT, COLOR_TEXT_MUTED,
    COLOR_TEXT_DIM, COLOR_HIGHLIGHT, FONT_MONO_BOLD, FONT_HUD_TINY, FONT_HUD_LABEL
)
from automation.system import get_system_telemetry

class AICoreVisualizer(tk.Canvas):
    """
    Stark Industries Mark VII Holographic Arc Reactor & Telemetry HUD.
    Procedurally generates:
    - Outer degree compass ring (000..330) with radial calibration ticks
    - Dual counter-rotating segmented telemetry rings with trailing glow
    - 10 Electromagnetic Induction Coils with animated energy pulses
    - Central pulsing plasma core with audio-reactive iris expansion
    - 360-degree sweeping holographic radar/diagnostic beam
    - Flanking telemetry dials: CPU Load, RAM Utilization, Reactor Energy (100%), and Audio Spectrum
    - Oscilloscope waveform strip reacting to live voice and speech audio
    """
    def __init__(self, parent, width=820, height=270, **kwargs):
        super().__init__(parent, width=width, height=height, bg=COLOR_BG, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height

        # State & Status
        self.state = "IDLE"
        self.status_detail = "All Systems Nominal"

        # Procedural Rotation & Pulse Values
        self.angle_outer = 0.0
        self.angle_inner = 0.0
        self.angle_sweep = 0.0
        self.angle_coils = 0.0
        self.pulse = 0.0

        # Audio Reactivity
        self.audio_level = 0.0
        self.target_audio_level = 0.0

        # Live Telemetry Metrics
        self.cpu_pct = 18.0
        self.ram_pct = 42.0
        self.ram_used_gb = 7.2
        self.ram_total_gb = 16.0
        self.energy_pct = 100.0

        # Start Telemetry Poller Thread
        self._running = True
        self._start_telemetry_thread()

        # Bind Resize Event for Dynamic Centering
        self.bind("<Configure>", self._on_resize)

        # Kick off ~30-60 FPS procedural animation loop
        self.after(30, self._render_frame)

    def _on_resize(self, event):
        if event.width > 50 and event.height > 50:
            self.width = event.width
            self.height = event.height

    def _start_telemetry_thread(self):
        def _poll():
            while self._running:
                try:
                    data = get_system_telemetry()
                    self.cpu_pct = float(data.get("cpu_percent", self.cpu_pct))
                    self.ram_pct = float(data.get("ram_percent", self.ram_pct))
                    self.ram_used_gb = float(data.get("ram_used_gb", self.ram_used_gb))
                    self.ram_total_gb = float(data.get("ram_total_gb", self.ram_total_gb))
                except Exception:
                    pass
                time.sleep(1.8)
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
            self.status_detail = "Online • Cognitive Co-Pilot Nominal"
        elif self.state == "LISTENING":
            self.status_detail = "Acoustic Sensors Active • Receiving..."
        elif self.state == "TRANSCRIBING":
            self.status_detail = "Whisper Neural Decryption Active..."
        elif self.state == "THINKING":
            self.status_detail = "Neural Link Active • Reasoning Intent..."
        elif self.state == "PLANNING":
            self.status_detail = "Synthesizing Multi-Vector Strategy..."
        elif self.state == "EXECUTING":
            self.status_detail = "Deploying Authorized System Directives..."
        elif self.state == "SPEAKING":
            self.status_detail = "Audio Synthesis Output Active..."
        elif self.state == "COMPLETED":
            self.status_detail = "Directive Executed Cleanly"
        elif self.state == "ERROR":
            self.status_detail = "Security / Neural Link Alert"
        elif self.state == "STOPPED":
            self.status_detail = "Execution Halted by User (ESC)"

    def set_audio_level(self, level: float):
        """Feed live microphone RMS or speech audio amplitude."""
        self.target_audio_level = min(1.0, max(0.0, level * 4.5))

    def _render_frame(self):
        if not self._running:
            return

        self.delete("all")

        cx = self.width / 2
        cy = self.height / 2 - 4

        # Audio interpolation
        self.audio_level += (self.target_audio_level - self.audio_level) * 0.35

        # Speed adjustment based on state
        speed = 0.025
        if self.state in ("THINKING", "PLANNING"):
            speed = 0.07
        elif self.state == "EXECUTING":
            speed = 0.11
        elif self.state in ("LISTENING", "SPEAKING"):
            speed = 0.045

        self.angle_outer = (self.angle_outer + speed) % (2 * math.pi)
        self.angle_inner = (self.angle_inner - speed * 1.6) % (2 * math.pi)
        self.angle_sweep = (self.angle_sweep + speed * 1.8) % (2 * math.pi)
        self.angle_coils = (self.angle_coils + speed * 0.3) % (2 * math.pi)
        self.pulse = (self.pulse + 0.055) % (2 * math.pi)

        # Primary palette based on state
        core_color = COLOR_CYAN
        accent_color = COLOR_HIGHLIGHT
        if self.state in ("THINKING", "PLANNING"):
            core_color = COLOR_PURPLE
            accent_color = COLOR_CYAN
        elif self.state == "EXECUTING":
            core_color = COLOR_AMBER
            accent_color = COLOR_EMERALD
        elif self.state == "LISTENING":
            core_color = COLOR_CYAN
            accent_color = COLOR_EMERALD
        elif self.state == "SPEAKING":
            core_color = COLOR_EMERALD
            accent_color = COLOR_CYAN
        elif self.state == "ERROR":
            core_color = COLOR_ERROR
            accent_color = COLOR_AMBER
        elif self.state == "STOPPED":
            core_color = COLOR_TEXT_MUTED
            accent_color = "#334155"

        # --- 0. BACKGROUND HUD TACTICAL RETICLES & CORNER BRACKETS ---
        self._draw_hud_corners(self.width, self.height, accent_color)

        # Draw Stark Industries Watermark & Protocol Info
        self.create_text(
            22, 16,
            text="STARK INDUSTRIES // MARK VII HUD",
            font=FONT_HUD_LABEL,
            fill="#1e3a5f",
            anchor="w"
        )
        self.create_text(
            self.width - 22, 16,
            text="COGNITIVE CO-PILOT // SAATHI OS 2.0",
            font=FONT_HUD_LABEL,
            fill="#1e3a5f",
            anchor="e"
        )

        # --- 1. FLANKING TELEMETRY DIALS (IF WIDTH >= 660) ---
        if self.width >= 660:
            # Left Dial 1: CPU Load
            self._draw_radial_gauge(
                cx - 245, cy,
                radius=42,
                pct=self.cpu_pct,
                title="CPU LOAD",
                subtext=f"{self.cpu_pct:.1f}%",
                gauge_color=core_color
            )
            # Left Dial 2: RAM Utilization
            self._draw_radial_gauge(
                cx - 145, cy,
                radius=42,
                pct=self.ram_pct,
                title="MEMORY",
                subtext=f"{self.ram_used_gb}G/{int(self.ram_total_gb)}G",
                gauge_color=accent_color
            )
            # Right Dial 1: Reactor Energy (100%)
            self._draw_radial_gauge(
                cx + 145, cy,
                radius=42,
                pct=self.energy_pct,
                title="REACTOR",
                subtext="100% NOMINAL",
                gauge_color=COLOR_EMERALD
            )
            # Right Dial 2: Audio & Neural Oscilloscope Ring
            self._draw_radial_oscilloscope(
                cx + 245, cy,
                radius=42,
                color=core_color
            )

        # --- 2. CENTRAL MASTER ARC REACTOR ---
        self._draw_arc_reactor(cx, cy, core_color, accent_color)

        # --- 3. BOTTOM OSCILLOSCOPE WAVEFORM STRIP ---
        self._draw_bottom_waveform(cx, cy + 96, self.width - 80, core_color)

        # --- 4. HUD STATUS LINE ---
        status_text = f"● [{self.state}] {self.status_detail}"
        self.create_text(
            cx, cy + 115,
            text=status_text,
            font=("Segoe UI", 9, "bold"),
            fill=core_color
        )

        self.after(33, self._render_frame)

    def _draw_hud_corners(self, w, h, color):
        """Draw holographic Stark HUD corner brackets and calibration reticles."""
        bracket_len = 16
        pad = 8
        # Top-Left
        self.create_line(pad, pad, pad + bracket_len, pad, fill=color, width=1)
        self.create_line(pad, pad, pad, pad + bracket_len, fill=color, width=1)
        # Top-Right
        self.create_line(w - pad, pad, w - pad - bracket_len, pad, fill=color, width=1)
        self.create_line(w - pad, pad, w - pad, pad + bracket_len, fill=color, width=1)
        # Bottom-Left
        self.create_line(pad, h - pad, pad + bracket_len, h - pad, fill=color, width=1)
        self.create_line(pad, h - pad, pad, h - pad - bracket_len, fill=color, width=1)
        # Bottom-Right
        self.create_line(w - pad, h - pad, w - pad - bracket_len, h - pad, fill=color, width=1)
        self.create_line(w - pad, h - pad, w - pad, h - pad - bracket_len, fill=color, width=1)

    def _draw_radial_gauge(self, gx, gy, radius, pct, title, subtext, gauge_color):
        """Draw authentic Stark circular telemetry meter."""
        # Outer border ring
        self.create_oval(
            gx - radius, gy - radius, gx + radius, gy + radius,
            outline="#0c203b", width=1
        )
        # Background arc (-210 to 30 deg, 240 deg total)
        self.create_arc(
            gx - radius + 3, gy - radius + 3, gx + radius - 3, gy + radius - 3,
            start=-210, extent=-240, style="arc", outline="#08172c", width=3
        )
        # Filled Value Arc
        clamped_pct = min(100.0, max(0.0, pct))
        extent_val = - (240.0 * (clamped_pct / 100.0))
        if abs(extent_val) > 1:
            self.create_arc(
                gx - radius + 3, gy - radius + 3, gx + radius - 3, gy + radius - 3,
                start=-210, extent=extent_val, style="arc", outline=gauge_color, width=3
            )
        # Center readout
        self.create_text(
            gx, gy - 6,
            text=f"{int(pct)}%",
            font=("Segoe UI", 11, "bold"),
            fill=COLOR_TEXT
        )
        # Labels
        self.create_text(
            gx, gy + 10,
            text=title,
            font=FONT_HUD_TINY,
            fill=COLOR_TEXT_MUTED
        )
        self.create_text(
            gx, gy + radius + 10,
            text=subtext,
            font=FONT_HUD_TINY,
            fill=gauge_color
        )

    def _draw_radial_oscilloscope(self, ox, oy, radius, color):
        """Draw circular frequency oscilloscope dial reacting to audio."""
        self.create_oval(
            ox - radius, oy - radius, ox + radius, oy + radius,
            outline="#0c203b", width=1
        )
        # Segmented radial frequency bars
        bars = 16
        for i in range(bars):
            ang = i * (2 * math.pi / bars) + self.pulse * 0.4
            bar_amp = 2 + (self.audio_level * 10 * math.sin(i * 0.8 + self.pulse))
            x1 = ox + (radius - 12) * math.cos(ang)
            y1 = oy + (radius - 12) * math.sin(ang)
            x2 = ox + (radius - 12 + bar_amp) * math.cos(ang)
            y2 = oy + (radius - 12 + bar_amp) * math.sin(ang)
            self.create_line(x1, y1, x2, y2, fill=color, width=2)

        self.create_text(
            ox, oy - 6,
            text="SPECTRUM",
            font=FONT_HUD_TINY,
            fill=COLOR_TEXT_MUTED
        )
        self.create_text(
            ox, oy + 8,
            text=f"{int(self.audio_level * 100)} dB",
            font=("Segoe UI", 8, "bold"),
            fill=color
        )
        self.create_text(
            ox, oy + radius + 10,
            text="ACOUSTIC LIVE",
            font=FONT_HUD_TINY,
            fill=color
        )

    def _draw_arc_reactor(self, cx, cy, core_color, accent_color):
        """Draw the Master Stark Industries Arc Reactor assembly."""
        # 1. Outer Calibrated Compass Ring (Radius = 92)
        r_scale = 92
        self.create_oval(
            cx - r_scale, cy - r_scale, cx + r_scale, cy + r_scale,
            outline="#0f2b4c", width=1
        )

        # 36 Degree Calibration Ticks
        for deg in range(0, 360, 10):
            rad = math.radians(deg)
            is_major = (deg % 30 == 0)
            t_len = 6 if is_major else 3
            x1 = cx + (r_scale - t_len) * math.cos(rad)
            y1 = cy + (r_scale - t_len) * math.sin(rad)
            x2 = cx + r_scale * math.cos(rad)
            y2 = cy + r_scale * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill=accent_color if is_major else "#123052", width=1)

            if is_major and deg % 60 == 0:
                tx = cx + (r_scale + 12) * math.cos(rad)
                ty = cy + (r_scale + 12) * math.sin(rad)
                self.create_text(tx, ty, text=f"{deg:03d}", font=FONT_HUD_TINY, fill="#38bdf8")

        # 2. Segmented Rotating Outer Telemetry Ring (Radius = 82)
        r_outer_telemetry = 82
        num_segments = 4
        seg_span = 0.38 * math.pi
        for i in range(num_segments):
            start_ang = self.angle_outer + i * (2 * math.pi / num_segments)
            x1 = cx + r_outer_telemetry * math.cos(start_ang)
            y1 = cy + r_outer_telemetry * math.sin(start_ang)
            x2 = cx + r_outer_telemetry * math.cos(start_ang + seg_span)
            y2 = cy + r_outer_telemetry * math.sin(start_ang + seg_span)
            self.create_line(x1, y1, x2, y2, fill=core_color, width=2)
            # Leading highlight dot
            self.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill="#ffffff", outline="")

        # 3. Notched Counter-Rotating Stator / Turbine Teeth (Radius = 70)
        r_stator = 70
        num_teeth = 12
        for i in range(num_teeth):
            tooth_ang = self.angle_inner + i * (2 * math.pi / num_teeth)
            tx1 = cx + (r_stator - 4) * math.cos(tooth_ang)
            ty1 = cy + (r_stator - 4) * math.sin(tooth_ang)
            tx2 = cx + (r_stator + 4) * math.cos(tooth_ang)
            ty2 = cy + (r_stator + 4) * math.sin(tooth_ang)
            self.create_line(tx1, ty1, tx2, ty2, fill="#1a3b66", width=2)

        self.create_oval(
            cx - r_stator, cy - r_stator, cx + r_stator, cy + r_stator,
            outline="#0c2545", width=1, dash=(2, 3)
        )

        # 4. 10 Electromagnetic Induction Coils (Radii: 48 to 64)
        num_coils = 10
        r_coil_in = 46
        r_coil_out = 62
        for i in range(num_coils):
            ang = self.angle_coils + i * (2 * math.pi / num_coils)
            c_mid_x = cx + ((r_coil_in + r_coil_out) / 2) * math.cos(ang)
            c_mid_y = cy + ((r_coil_in + r_coil_out) / 2) * math.sin(ang)

            # Coil pulse glow
            coil_pulse = math.sin(self.pulse * 2 + i * 0.6)
            coil_color = COLOR_COPPER if coil_pulse < 0 else core_color

            cx1 = cx + r_coil_in * math.cos(ang)
            cy1 = cy + r_coil_in * math.sin(ang)
            cx2 = cx + r_coil_out * math.cos(ang)
            cy2 = cy + r_coil_out * math.sin(ang)
            self.create_line(cx1, cy1, cx2, cy2, fill=coil_color, width=4)

        # 5. Holographic Sweeping Radar Beam (Radius = 90)
        sw_rad = self.angle_sweep
        sweep_x = cx + 90 * math.cos(sw_rad)
        sweep_y = cy + 90 * math.sin(sw_rad)
        self.create_line(cx, cy, sweep_x, sweep_y, fill=accent_color, width=1)
        # Subtle sweep trail
        trail_rad = sw_rad - 0.08
        self.create_line(cx, cy, cx + 88 * math.cos(trail_rad), cy + 88 * math.sin(trail_rad), fill="#072b4f", width=1)

        # 6. Central Arc Reactor Plasma Iris
        r_core = 26 + math.sin(self.pulse) * 3 + (self.audio_level * 18)

        # Outer Halo Ring
        self.create_oval(
            cx - (r_core + 10), cy - (r_core + 10),
            cx + (r_core + 10), cy + (r_core + 10),
            outline=accent_color, width=1
        )
        # Inner Core Container
        self.create_oval(
            cx - r_core, cy - r_core,
            cx + r_core, cy + r_core,
            fill="#051428", outline=core_color, width=2
        )
        # Concentric Plasma Disc
        r_plasma = max(6, r_core * 0.62)
        self.create_oval(
            cx - r_plasma, cy - r_plasma,
            cx + r_plasma, cy + r_plasma,
            fill=core_color, outline=""
        )
        # White Hot Plasma Nucleus
        r_nuc = max(3, r_plasma * 0.45)
        self.create_oval(
            cx - r_nuc, cy - r_nuc,
            cx + r_nuc, cy + r_nuc,
            fill=COLOR_CORE_WHITE, outline=""
        )

        # Crosshairs inside core
        ch_len = r_core + 6
        self.create_line(cx - ch_len, cy, cx - (r_core - 4), cy, fill=core_color, width=1)
        self.create_line(cx + (r_core - 4), cy, cx + ch_len, cy, fill=core_color, width=1)
        self.create_line(cx, cy - ch_len, cx, cy - (r_core - 4), fill=core_color, width=1)
        self.create_line(cx, cy + (r_core - 4), cx, cy + ch_len, fill=core_color, width=1)

    def _draw_bottom_waveform(self, cx, base_y, width, color):
        """Draw an oscilloscope audio waveform strip beneath the Arc Reactor."""
        bars = 36
        bar_w = 4
        gap = 4
        total_w = bars * (bar_w + gap)
        start_x = cx - (total_w / 2)

        for b in range(bars):
            dist_norm = 1.0 - abs(b - (bars / 2)) / (bars / 2)
            wave_h = 2 + (self.audio_level * 22 * dist_norm * math.sin(b * 0.4 + self.pulse * 2))
            if self.state in ("THINKING", "PLANNING"):
                wave_h = 2 + math.sin(self.pulse * 3 + b * 0.5) * 6
            elif self.state == "EXECUTING":
                wave_h = 3 + math.sin(self.pulse * 4 + b * 0.6) * 10

            bx = start_x + b * (bar_w + gap)
            self.create_rectangle(
                bx, base_y - wave_h, bx + bar_w, base_y + wave_h,
                fill=color, outline=""
            )
