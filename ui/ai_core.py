import math
import time
import tkinter as tk
from typing import Optional
from .theme import COLOR_BG, COLOR_CYAN, COLOR_EMERALD, COLOR_AMBER, COLOR_PURPLE, COLOR_ERROR, COLOR_TEXT_MUTED

class AICoreVisualizer(tk.Canvas):
    """
    Jarvis Dynamic AI Core Visualizer.
    Renders concentric procedural telemetry rings, pulsing energy core,
    and dynamic audio wave fields synchronized with AI states.
    """
    def __init__(self, parent, width=320, height=220, **kwargs):
        super().__init__(parent, width=width, height=height, bg=COLOR_BG, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.cx = width / 2
        self.cy = height / 2

        self.state = "IDLE"
        self.status_detail = "Ready"
        self.angle_outer = 0.0
        self.angle_inner = 0.0
        self.pulse = 0.0
        self.audio_level = 0.0
        self.target_audio_level = 0.0

        self._running = True
        self.after(30, self._render_frame)

    def set_state(self, state: str, detail: str = ""):
        self.state = state.upper()
        if detail:
            self.status_detail = detail
        elif self.state == "IDLE":
            self.status_detail = "Online ? Standing By"
        elif self.state == "LISTENING":
            self.status_detail = "Listening to microphone..."
        elif self.state == "TRANSCRIBING":
            self.status_detail = "Transcribing voice..."
        elif self.state == "THINKING":
            self.status_detail = "Reasoning & Analyzing..."
        elif self.state == "PLANNING":
            self.status_detail = "Planning multi-step execution..."
        elif self.state == "EXECUTING":
            self.status_detail = "Executing authorized tool..."
        elif self.state == "SPEAKING":
            self.status_detail = "Speaking response..."
        elif self.state == "COMPLETED":
            self.status_detail = "Task Complete"
        elif self.state == "ERROR":
            self.status_detail = "Operational Alert"
        elif self.state == "STOPPED":
            self.status_detail = "Stopped"

    def set_audio_level(self, level: float):
        """Feed live microphone RMS or speech playback volume."""
        self.target_audio_level = min(1.0, max(0.0, level * 5.0))

    def _render_frame(self):
        if not self._running:
            return

        self.delete("all")

        # Smooth audio level transition
        self.audio_level += (self.target_audio_level - self.audio_level) * 0.35

        # Speed adjustment per state
        speed = 0.03
        if self.state in ("THINKING", "PLANNING"):
            speed = 0.08
        elif self.state == "EXECUTING":
            speed = 0.12
        elif self.state in ("LISTENING", "SPEAKING"):
            speed = 0.05

        self.angle_outer = (self.angle_outer + speed) % (2 * math.pi)
        self.angle_inner = (self.angle_inner - speed * 1.5) % (2 * math.pi)
        self.pulse = (self.pulse + 0.06) % (2 * math.pi)

        # Base Color Palette based on State
        core_color = COLOR_EMERALD
        ring_color = COLOR_CYAN
        if self.state in ("THINKING", "PLANNING"):
            core_color = COLOR_PURPLE
            ring_color = COLOR_CYAN
        elif self.state == "EXECUTING":
            core_color = COLOR_AMBER
            ring_color = COLOR_EMERALD
        elif self.state == "LISTENING":
            core_color = COLOR_CYAN
            ring_color = COLOR_EMERALD
        elif self.state == "SPEAKING":
            core_color = COLOR_EMERALD
            ring_color = COLOR_CYAN
        elif self.state == "ERROR":
            core_color = COLOR_ERROR
            ring_color = COLOR_AMBER
        elif self.state == "STOPPED":
            core_color = COLOR_TEXT_MUTED
            ring_color = "#334155"

        # 1. Outer Concentric Telemetry Orbit
        r_outer = 75 + math.sin(self.pulse) * 2
        self.create_oval(
            self.cx - r_outer, self.cy - r_outer,
            self.cx + r_outer, self.cy + r_outer,
            outline="#1e293b", width=1
        )

        # 2. Segmented Rotating Outer Arcs
        num_segments = 4
        seg_len = 0.35 * math.pi
        for i in range(num_segments):
            start_ang = self.angle_outer + i * (2 * math.pi / num_segments)
            x1 = self.cx + r_outer * math.cos(start_ang)
            y1 = self.cy + r_outer * math.sin(start_ang)
            x2 = self.cx + r_outer * math.cos(start_ang + seg_len)
            y2 = self.cy + r_outer * math.sin(start_ang + seg_len)
            self.create_line(x1, y1, x2, y2, fill=ring_color, width=2)

        # 3. Middle Counter-Rotating Gyroscope Ring
        r_mid = 52 + (self.audio_level * 18)
        num_mid = 3
        for i in range(num_mid):
            ang = self.angle_inner + i * (2 * math.pi / num_mid)
            p_x = self.cx + r_mid * math.cos(ang)
            p_y = self.cy + r_mid * math.sin(ang)
            self.create_oval(p_x - 3, p_y - 3, p_x + 3, p_y + 3, fill=core_color, outline="")

        self.create_oval(
            self.cx - r_mid, self.cy - r_mid,
            self.cx + r_mid, self.cy + r_mid,
            outline="#2a334a", width=1, dash=(3, 3)
        )

        # 4. Central Energy Core
        r_core = 28 + math.sin(self.pulse) * 4 + (self.audio_level * 14)
        # Core Glow Aura
        self.create_oval(
            self.cx - (r_core + 8), self.cy - (r_core + 8),
            self.cx + (r_core + 8), self.cy + (r_core + 8),
            fill="", outline=core_color, width=1
        )
        # Inner Solid Disc
        self.create_oval(
            self.cx - r_core, self.cy - r_core,
            self.cx + r_core, self.cy + r_core,
            fill="#0c1020", outline=core_color, width=2
        )
        # Core Dot
        r_center = 7 + (self.audio_level * 6)
        self.create_oval(
            self.cx - r_center, self.cy - r_center,
            self.cx + r_center, self.cy + r_center,
            fill=core_color, outline=""
        )

        # 5. Audio Waveform Bars (Active when Listening, Speaking, or Executing)
        if self.state in ("LISTENING", "SPEAKING", "EXECUTING"):
            bars = 16
            bar_w = 4
            gap = 6
            start_x = self.cx - (bars * (bar_w + gap)) / 2
            base_y = self.cy + 92
            for b in range(bars):
                offset = abs(b - bars / 2)
                h = 4 + (self.audio_level * 32 * math.sin((b / bars) * math.pi))
                if self.state == "EXECUTING":
                    h = 6 + math.sin(self.pulse * 2 + b * 0.4) * 8
                bx = start_x + b * (bar_w + gap)
                self.create_rectangle(bx, base_y - h, bx + bar_w, base_y, fill=ring_color, outline="")

        # 6. Status Label Text inside Canvas
        self.create_text(
            self.cx, self.cy + 104,
            text=f"? {self.state}",
            font=("Segoe UI", 9, "bold"),
            fill=core_color
        )

        self.after(33, self._render_frame)  # ~30-35ms = smooth ~30-60fps
