import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from typing import Dict, Any, Optional

from .theme import COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_ERROR
from .telemetry import TopTelemetryBar
from .navigation import NavigationRail
from .task_observer import TaskObserverPanel
from .command_center import CommandCenterView
from .chat_tab import ChatTabView
from .memory_view import MemoryView
from .automation_view import AutomationWorkflowsView
from .projects_view import ProjectsGalleryView
from .system_view import SystemControlView
from .settings_view import SettingsView
from agent.planner import COMMON_REFLEX_PHRASES

class SaathiApp:
    """
    Master Pratham Prasad Desktop Operating System Shell for Saathi AI.
    Integrates Telemetry, Navigation, AI Visualizer, Dedicated Chat Matrix,
    Continuous Voice Loop, Real-Time Task Observer, and Modular Views.
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

        self.root.title("PRATHAM PRASAD // SAATHI AI — COGNITIVE OPERATING INTERFACE")
        self.root.geometry("1480x920")
        self.root.minsize(1120, 720)
        self.root.configure(bg=COLOR_BG)

        # 1. Top Telemetry Bar
        self.telemetry_bar = TopTelemetryBar(
            self.root,
            on_model_change=self._on_model_select,
            on_toggle_master_control=self._prompt_master_control_toggle
        )
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
            "chat": ChatTabView(
                self.center_viewport,
                on_send_command=self.handle_user_input,
                on_toggle_voice=self.toggle_voice
            ),
            "tasks": self.task_observer,
            "memory": MemoryView(self.center_viewport, self.memory),
            "automations": AutomationWorkflowsView(self.center_viewport, self.automations, on_run_workflow=self._run_workflow_direct),
            "projects": ProjectsGalleryView(self.center_viewport, self.projects_dir, on_create_site=self.handle_user_input),
            "system": SystemControlView(self.center_viewport, permission_manager=self.permissions),
            "settings": SettingsView(self.center_viewport, self.permissions)
        }
        self.current_view_key = "core"

        # Pack Layout (Left Nav Rail, Center Viewport, Right Task Observer Panel)
        self.nav_rail = NavigationRail(self.body_frame, on_navigate=self._switch_view)
        self.nav_rail.pack(side="left", fill="y")
        self.task_observer.pack(side="right", fill="y")
        self.center_viewport.pack(side="left", fill="both", expand=True)

        self.views["core"].pack(fill="both", expand=True)

        # Wire Agent and Voice Callbacks
        self._wire_subsystems()

        # Global Keyboard Shortcuts
        self.root.bind("<Escape>", lambda e: self.stop_active_task())

        # Auto-activate continuous voice listening shortly after boot
        self.root.after(1200, self._auto_start_voice)

        # Prewarm instant audio cache for common reflex responses
        self.voice.tts.prewarm_phrases(COMMON_REFLEX_PHRASES)

    def _auto_start_voice(self):
        """Automatically engage continuous voice perception so Saathi listens without manual clicks."""
        try:
            if not self.voice.is_listening:
                self.voice.start_listening()
                if "chat" in self.views:
                    self.views["chat"].set_voice_active(True)
                cmd_center: CommandCenterView = self.views.get("core")
                if cmd_center and hasattr(cmd_center, "btn_mic"):
                    cmd_center.btn_mic.configure(text="🎙️ LISTENING", bg="#062e20", fg=COLOR_EMERALD)
        except Exception:
            pass

    def _append_to_chat_views(self, role: str, text: str):
        """Synchronize message across both Command Center HUD drawer and dedicated Chat Tab."""
        cmd_center: CommandCenterView = self.views.get("core")
        if cmd_center and hasattr(cmd_center, "chat_view"):
            cmd_center.chat_view.append_message(role, text)

        chat_tab: ChatTabView = self.views.get("chat")
        if chat_tab and hasattr(chat_tab, "append_message"):
            chat_tab.append_message(role, text)

    def _wire_subsystems(self):
        cmd_center: CommandCenterView = self.views["core"]

        # 1. Voice audio level -> AI Visualizer
        def on_level(rms):
            self.root.after(0, lambda: cmd_center.visualizer.set_audio_level(rms))
        self.voice.on_audio_level = on_level

        # 2. Voice status change -> AI Visualizer & Telemetry
        def on_voice_status(status):
            self.root.after(0, lambda: cmd_center.visualizer.set_state(status))
            is_active = status in ("LISTENING", "TRANSCRIBING")
            self.root.after(0, lambda: self.telemetry_bar.set_mic_status(status, is_active))
            if "chat" in self.views:
                self.root.after(0, lambda: self.views["chat"].set_voice_active(self.voice.is_listening))
        self.voice.on_status_change = on_voice_status

        # 3. Voice transcription completed -> Handle text
        def on_stt_done(text):
            self.root.after(0, lambda: self.handle_user_input(text))
        self.voice.on_transcription_complete = on_stt_done

        # 4. Agent state change -> AI Visualizer & Telemetry
        def on_agent_state(state, detail):
            self.root.after(0, lambda: cmd_center.visualizer.set_state(state, detail))
            if state == "SPEAKING":
                self.voice.tts.on_amplitude_callback = lambda amp: self.root.after(0, lambda: cmd_center.visualizer.set_audio_level(amp))
        self.agent.on_state_change = on_agent_state

        # 5. Verbal Progress Commentary for Bigger Tasks
        def on_commentary(commentary: str):
            self.root.after(0, lambda: self._append_to_chat_views("action", f"[SAATHI PROGRESS] {commentary}"))
            self.voice.tts.speak(
                commentary,
                on_start=lambda: self.root.after(0, lambda: cmd_center.visualizer.set_state("SPEAKING", "Explaining progress...")),
                on_finish=lambda: self.root.after(0, lambda: cmd_center.visualizer.set_state("EXECUTING", "Working..."))
            )
        self.agent.on_commentary = on_commentary

        # 6. Agent task events -> Real-Time Task Observer
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

        # 7. Agent final reply -> Chat Streams + Edge TTS
        def on_reply(reply):
            def _show():
                self._append_to_chat_views("assistant", reply)
            self.root.after(0, _show)
            self.voice.tts.speak(
                reply,
                on_start=lambda: self.root.after(0, lambda: cmd_center.visualizer.set_state("SPEAKING")),
                on_finish=lambda: self.root.after(0, lambda: cmd_center.visualizer.set_state("IDLE"))
            )
        self.agent.on_reply_ready = on_reply

    def _switch_view(self, key: str):
        if key in self.views and key != self.current_view_key:
            self.views[self.current_view_key].pack_forget()
            self.views[key].pack(fill="both", expand=True)
            self.current_view_key = key
            if hasattr(self.views[key], "refresh"):
                self.views[key].refresh()

    def _on_model_select(self, model: str):
        self.agent.selected_model = model

    def handle_user_input(self, text: str):
        self._append_to_chat_views("user", text)
        # Stay on chat if user is already on chat; only switch to core if on unrelated settings/automations
        if self.current_view_key not in ("core", "chat"):
            self._switch_view("core")
            self.nav_rail.select("core")
        self.agent.run_user_request(text)

    def toggle_voice(self):
        is_listening = self.voice.toggle_listening()
        if "chat" in self.views:
            self.views["chat"].set_voice_active(is_listening)
        cmd_center: CommandCenterView = self.views.get("core")
        if cmd_center and hasattr(cmd_center, "btn_mic"):
            cmd_center.btn_mic.configure(
                text="🎙️ LISTENING" if is_listening else "🎙️ LISTEN",
                bg="#062e20" if is_listening else "#081e3a",
                fg=COLOR_EMERALD if is_listening else COLOR_CYAN
            )

    def stop_active_task(self):
        self.agent.cancel()
        self.voice.stop_listening()
        self.voice.tts.stop()
        cmd_center: CommandCenterView = self.views["core"]
        cmd_center.visualizer.set_state("STOPPED")
        self.task_observer.fail_mission("Operation stopped by user (ESC)")

    def _prompt_master_control_toggle(self):
        if getattr(self.permissions, "master_system_control", False):
            ans = messagebox.askyesno(
                "Revoke Full System Control",
                "Saathi AI currently possesses Full System Control.\n\n"
                "Do you want to revoke autonomous system access and return to safe restricted mode?",
                parent=self.root
            )
            if ans:
                self.permissions.revoke_master_control(persist=True)
                self.voice.tts.speak("Full system control revoked, Pratham. Standing by in restricted mode.")
        else:
            ans = messagebox.askyesno(
                "Grant Full System Control",
                "Saathi AI Sovereign Authorization:\n\n"
                "Do you grant Saathi AI FULL SYSTEM CONTROL?\n\n"
                "• Full autonomous control of mouse, keyboard, and open applications\n"
                "• Sovereign volume adjustments, media playback, and power control\n"
                "• Unrestricted process management and command execution\n"
                "• Requires only this SINGLE permission — no repetitive interruptions.\n\n"
                "Authorize Full System Control for Pratham Prasad?",
                parent=self.root
            )
            if ans:
                self.permissions.authorize_master_control(persist=True)
                self.voice.tts.speak("Full system control authorized, Pratham. All operational controls are armed.")


    def _run_workflow_direct(self, wf):
        self.handle_user_input(f"Run workflow {wf.name}")
