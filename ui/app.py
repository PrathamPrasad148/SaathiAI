import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from typing import Dict, Any, Optional

from .theme import COLOR_BG, COLOR_PANEL, COLOR_BORDER
from .telemetry import TopTelemetryBar
from .navigation import NavigationRail
from .task_observer import TaskObserverPanel
from .command_center import CommandCenterView
from .memory_view import MemoryView
from .automation_view import AutomationWorkflowsView
from .projects_view import ProjectsGalleryView
from .system_view import SystemControlView
from .settings_view import SettingsView

class SaathiApp:
    """
    Master Jarvis Desktop Operating System Shell for Saathi AI.
    Integrates Telemetry, Navigation, AI Visualizer, Real-Time Task Observer, and Modular Views.
    """
    def __init__(self,
                 root: tk.Tk,
                 app_dir: Path,
                 projects_dir: Path,
                 agent_planner,
                 voice_engine,
                 memory_engine,
                 automation_engine,
                 permission_manager):
        self.root = root
        self.app_dir = app_dir
        self.projects_dir = projects_dir
        self.agent = agent_planner
        self.voice = voice_engine
        self.memory = memory_engine
        self.automations = automation_engine
        self.permissions = permission_manager

        self.root.title("STARK INDUSTRIES // SAATHI AI — MARK VII OPERATING INTERFACE")
        self.root.geometry("1280x840")
        self.root.minsize(1020, 700)
        self.root.configure(bg=COLOR_BG)

        # 1. Top Telemetry Bar
        self.telemetry_bar = TopTelemetryBar(self.root, on_model_change=self._on_model_select)
        self.telemetry_bar.pack(fill="x", side="top")

        # Body Container
        self.body_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.body_frame.pack(fill="both", expand=True)

        # Center Content View Container
        self.center_viewport = tk.Frame(self.body_frame, bg=COLOR_BG)

        # Right Task Observer Panel
        self.task_observer = TaskObserverPanel(self.body_frame)

        # Build Subviews
        self.views = {
            "core": CommandCenterView(
                self.center_viewport,
                on_send_command=self.handle_user_input,
                on_toggle_voice=self.toggle_voice,
                on_stop_task=self.stop_active_task
            ),
            "memory": MemoryView(self.center_viewport, self.memory),
            "automations": AutomationWorkflowsView(self.center_viewport, self.automations, on_run_workflow=self._run_workflow_direct),
            "projects": ProjectsGalleryView(self.center_viewport, self.projects_dir, on_create_site=self.handle_user_input),
            "system": SystemControlView(self.center_viewport),
            "settings": SettingsView(self.center_viewport, self.permissions)
        }
        self.current_view_key = "core"

        # Pack Layout (Left Nav, Center Viewport, Right Task Observer)
        self.nav_rail = NavigationRail(self.body_frame, on_navigate=self._switch_view)
        self.nav_rail.pack(side="left", fill="y")
        self.task_observer.pack(side="right", fill="y")
        self.center_viewport.pack(side="left", fill="both", expand=True)

        self.views["core"].pack(fill="both", expand=True)

        # Wire Agent and Voice Callbacks
        self._wire_subsystems()

        # Global Keyboard Shortcuts
        self.root.bind("<Escape>", lambda e: self.stop_active_task())

    def _wire_subsystems(self):
        cmd_center: CommandCenterView = self.views["core"]

        # Voice audio level -> AI Visualizer
        def on_level(rms):
            self.root.after(0, lambda: cmd_center.visualizer.set_audio_level(rms))
        self.voice.on_audio_level = on_level

        # Voice status change -> AI Visualizer
        def on_voice_status(status):
            self.root.after(0, lambda: cmd_center.visualizer.set_state(status))
            self.root.after(0, lambda: self.telemetry_bar.set_mic_status(status, status == "LISTENING"))
        self.voice.on_status_change = on_voice_status

        # Voice transcription completed -> Handle text
        def on_stt_done(text):
            self.root.after(0, lambda: self.handle_user_input(text))
        self.voice.on_transcription_complete = on_stt_done

        # Agent state change -> AI Visualizer & Telemetry
        def on_agent_state(state, detail):
            self.root.after(0, lambda: cmd_center.visualizer.set_state(state, detail))
            if state == "SPEAKING":
                self.voice.tts.on_amplitude_callback = lambda amp: self.root.after(0, lambda: cmd_center.visualizer.set_audio_level(amp))
        self.agent.on_state_change = on_agent_state

        # Agent task events -> Real-Time Task Observer
        def on_task_evt(evt_type, data):
            if evt_type == "start":
                self.root.after(0, lambda: self.task_observer.set_mission(data.get("title", ""), data.get("steps", [])))
            elif evt_type == "step_update":
                self.root.after(0, lambda: self.task_observer.update_step(data.get("index", 0), data.get("status", ""), data.get("detail", "")))
            elif evt_type == "complete":
                self.root.after(0, lambda: self.task_observer.complete_mission(data.get("message", "")))
            elif evt_type == "error":
                self.root.after(0, lambda: self.task_observer.fail_mission(data.get("error", "")))
        self.agent.on_task_event = on_task_evt

        # Agent final reply -> Chat Stream + Edge TTS
        def on_reply(reply):
            self.root.after(0, lambda: cmd_center.chat_view.append_message("assistant", reply))
            self.voice.tts.speak(
                reply,
                on_start=lambda: self.root.after(0, lambda: cmd_center.visualizer.set_state("SPEAKING")),
                on_finish=lambda: self.root.after(0, lambda: cmd_center.visualizer.set_state("IDLE"))
            )
        self.agent.on_reply_ready = on_reply

    def _switch_view(self, key: str):
        if key == "tasks":
            # Focus on task observer
            return
        if key in self.views and key != self.current_view_key:
            self.views[self.current_view_key].pack_forget()
            self.views[key].pack(fill="both", expand=True)
            self.current_view_key = key
            if hasattr(self.views[key], "refresh"):
                self.views[key].refresh()

    def _on_model_select(self, model: str):
        self.agent.selected_model = model

    def handle_user_input(self, text: str):
        cmd_center: CommandCenterView = self.views["core"]
        cmd_center.chat_view.append_message("user", text)
        if self.current_view_key != "core":
            self._switch_view("core")
            self.nav_rail.select("core")
        self.agent.run_user_request(text)

    def toggle_voice(self):
        if self.voice.is_listening:
            self.voice.stop_listening()
        else:
            self.voice.start_listening()

    def stop_active_task(self):
        self.agent.cancel()
        self.voice.stop_listening()
        self.voice.tts.stop()
        cmd_center: CommandCenterView = self.views["core"]
        cmd_center.visualizer.set_state("STOPPED")
        self.task_observer.fail_mission("Operation stopped by user (ESC)")

    def _run_workflow_direct(self, wf):
        self.handle_user_input(f"Run workflow {wf.name}")
