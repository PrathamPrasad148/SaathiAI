from pathlib import Path
from typing import Dict, Any
from ..schemas import Tool, RiskLevel
from automation.screen import capture_screen
from automation.ocr import read_text_from_image

def get_vision_tools(projects_dir: Path) -> list[Tool]:
    def screenshot_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        target = capture_screen(projects_dir)
        return f"Screenshot saved to '{target}'."

    def ocr_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        target = capture_screen(projects_dir)
        text = read_text_from_image(target)
        return f"Screen reading:\n{text}"

    return [
        Tool(
            name="take_screenshot",
            category="vision",
            description="Capture a desktop screenshot and save to Projects folder.",
            parameters={"type": "object", "properties": {}},
            risk_level=RiskLevel.LOW,
            run=screenshot_run
        ),
        Tool(
            name="read_screen_text",
            category="vision",
            description="Inspect the current desktop screen and read visible text.",
            parameters={"type": "object", "properties": {}},
            risk_level=RiskLevel.LOW,
            run=ocr_run
        )
    ]
