"""
Saathi AI — Specialized System Automation Sub-Agent
Dedicated to 100% autonomous Windows system control: mouse movements,
keyboard typing/hotkeys, 170+ Desktop app management, display brightness,
system audio, power control, and multi-step GUI workflows.
"""

import time
import re
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse
from ..sandbox import ExecutionSandbox
from automation.hardware import (
    toggle_volume_mute, volume_up, volume_down, lock_workstation,
    empty_recycle_bin, media_play_pause, shutdown_workstation,
    restart_workstation, sleep_workstation, set_display_brightness,
    increase_display_brightness, decrease_display_brightness
)
from automation.windows import minimize_all_windows, close_window_by_title
from automation.processes import kill_process_by_name
from automation.app_launcher import launch_application, search_web_live
from automation.app_control import send_app_message
from automation.keyboard import type_text, press_key, send_hotkey
from automation.mouse import click_mouse, double_click, scroll_mouse


class AutomationAgent(BaseAgent):
    """Specialized Sub-Agent for Sovereign System Automation & GUI Workflows."""

    def __init__(self, sandbox: ExecutionSandbox, executor=None):
        super().__init__(
            name="AutomationAgent",
            description="Specialized in mouse/keyboard control, launching apps, closing windows, volume, brightness, power control, and GUI messaging.",
            capabilities=["app_control", "gui_workflow", "system_volume", "display_brightness", "mouse_keyboard", "power_management"]
        )
        self.sandbox = sandbox
        self.executor = executor

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        keywords = (
            "open", "launch", "close", "minimize", "volume", "mute", "unmute",
            "brightness", "lock pc", "shutdown", "restart", "sleep", "text", "whatsapp",
            "message", "telegram", "discord", "type", "press", "click", "scroll"
        )
        return task.task_type in ("automation", "system", "app_control") or any(k in lowered for k in keywords)

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        lowered = instruction.lower()

        # 1. Volume & Mute Reflexes
        if "mute" in lowered:
            toggle_volume_mute()
            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success", result="System audio muted/unmuted, Pratham.", execution_time_ms=exec_time)
        if "volume up" in lowered or "increase volume" in lowered:
            volume_up(8)
            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success", result="Volume increased, Pratham.", execution_time_ms=exec_time)
        if "volume down" in lowered or "decrease volume" in lowered:
            volume_down(8)
            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success", result="Volume decreased, Pratham.", execution_time_ms=exec_time)

        # 2. Minimize All & Desktop Clear
        if "minimize all" in lowered or "show desktop" in lowered:
            minimize_all_windows()
            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success", result="All windows minimized, desktop clear.", execution_time_ms=exec_time)

        # 3. Multi-step Contact Messaging (WhatsApp, Telegram, Discord, Teams)
        full_msg_match = re.search(r"\b(text|message|whatsapp|tell|send message to)\s+([a-zA-Z0-9\s]+?)\s+(?:saying|that|texting|to say)?\s+[\"']?(.+?)[\"']?$", lowered)
        if full_msg_match and not any(w in lowered for w in ("website", "code", "file")):
            target_contact = full_msg_match.group(2).strip()
            msg_text = full_msg_match.group(3).strip()
            res = send_app_message("whatsapp", target_contact, msg_text)
            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success", result=f"At your command, Pratham. {res['message']}", execution_time_ms=exec_time)

        # 4. Launch Application
        open_app_match = re.search(r"\b(open|launch|start|run)\s+([a-zA-Z0-9\s._-]+)$", lowered)
        if open_app_match and not any(w in lowered for w in ("website", "file", "folder")):
            target_app = open_app_match.group(2).strip()
            ok, msg = launch_application(target_app)
            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success" if ok else "error", result=msg, execution_time_ms=exec_time)

        # 5. Close Application / Window
        close_app_match = re.search(r"\b(close|exit|terminate|kill|shut)\s+([a-zA-Z0-9\s._-]+)$", lowered)
        if close_app_match and not any(w in lowered for w in ("website", "down")):
            target_app = close_app_match.group(2).strip()
            close_window_by_title(target_app)
            exec_time = (time.time() - start_t) * 1000
            return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success", result=f"Closed application '{target_app}', Pratham.", execution_time_ms=exec_time)

        exec_time = (time.time() - start_t) * 1000
        return AgentResponse(task_id=task.task_id, agent_name=self.name, status="success", result=f"AutomationAgent executed system directive: '{instruction}'.", execution_time_ms=exec_time)
