from pathlib import Path
from typing import Dict, Any
from ..schemas import Tool, RiskLevel
from automation.screen import capture_screen
from automation.ocr import read_text_from_image
from automation.vision import find_text_and_click

def get_vision_tools(projects_dir: Path) -> list[Tool]:
    def screenshot_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        target = capture_screen(projects_dir)
        return f"Screenshot saved to '{target}'."

    def ocr_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        target = capture_screen(projects_dir)
        text = read_text_from_image(target)
        return f"Screen reading:\n{text}"

    def click_text_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        text = args.get("text", "").strip()
        if not text:
            return "Error: text parameter is required."
        res = find_text_and_click(text)
        if res.get("status") == "success":
            return f"Successfully located '{text}' on screen and clicked at coordinates {res.get('clicked_at')}."
        return f"Could not click text: {res.get('message')}"

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
        ),
        Tool(
            name="click_screen_text",
            category="vision",
            description="Locate visible target text or button on screen via OCR and click it.",
            parameters={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text or button label to visually locate and click"}
                },
                "required": ["text"]
            },
            risk_level=RiskLevel.MEDIUM,
            run=click_text_run
        )
    ]

