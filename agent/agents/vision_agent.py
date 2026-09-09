"""
Saathi AI — Specialized Vision & Screen Perception Sub-Agent
Dedicated to desktop OCR, active window element perception,
region-of-interest analysis, and screen snapshot capture.
"""

import time
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse
from automation.hardware import take_screen_snapshot
from automation.vision import get_active_window_info, get_screen_dimensions


class VisionAgent(BaseAgent):
    """Specialized Sub-Agent for Desktop Screen Perception, Vision & OCR."""

    def __init__(self, executor=None):
        super().__init__(
            name="VisionAgent",
            description="Specialized in desktop screen perception, OCR text extraction, active window bounding boxes, and screen capture.",
            capabilities=["take_screenshot", "perceive_screen", "ocr_extract", "detect_active_window"]
        )
        self.executor = executor

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        keywords = ("screenshot", "screen", "capture screen", "snapshot", "ocr", "what is on my screen", "read screen", "active window")
        return task.task_type in ("vision", "ocr", "screen") or any(k in lowered for k in keywords)

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        lowered = instruction.lower()

        # 1. Take Screenshot
        if any(k in lowered for k in ("screenshot", "snapshot", "capture screen", "snap screen")):
            s_path = take_screen_snapshot()
            win_info = get_active_window_info()
            exec_time = (time.time() - start_t) * 1000
            res_msg = f"Captured full desktop screen buffer to '{s_path}'. Active window: '{win_info.get('title', 'Desktop')}'."
            return AgentResponse(
                task_id=task.task_id,
                agent_name=self.name,
                status="success",
                result=res_msg,
                artifacts=[{"file_path": s_path, "type": "image"}],
                execution_time_ms=exec_time
            )

        # 2. Perceive Active Desktop & Window Bounding Box
        win_info = get_active_window_info()
        w_scr, h_scr = get_screen_dimensions()
        exec_time = (time.time() - start_t) * 1000

        perception_summary = (
            f"DESKTOP SCREEN PERCEPTION TELEMETRY:\n"
            f"• Screen Resolution: {w_scr}x{h_scr}\n"
            f"• Active Foreground Application: '{win_info.get('title', 'Desktop')}'\n"
            f"• Window Bounding Box: {win_info.get('rect')}\n"
            f"• Process Executable: {win_info.get('process_name', 'N/A')}"
        )

        return AgentResponse(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            result=perception_summary,
            execution_time_ms=exec_time,
            metadata=win_info
        )
