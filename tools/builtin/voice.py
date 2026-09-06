from typing import Dict, Any
from ..schemas import Tool, RiskLevel

def get_voice_and_note_tools(reminder_mgr, notes_file) -> list[Tool]:
    def add_rem_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        text = args.get("text", "")
        mins = int(args.get("minutes", 10))
        reminder_mgr.add_reminder(text, mins)
        return f"Reminder set: '{text}' in {mins} minutes."

    def add_note_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        from datetime import datetime
        note = args.get("note", "").strip()
        with notes_file.open("a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}\n")
        return f"Note saved: '{note}'."

    return [
        Tool(
            name="add_reminder",
            category="voice",
            description="Set a desktop reminder with notification text and duration in minutes.",
            parameters={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Reminder message"},
                    "minutes": {"type": "integer", "description": "Minutes from now"}
                },
                "required": ["text", "minutes"]
            },
            risk_level=RiskLevel.LOW,
            run=add_rem_run
        ),
        Tool(
            name="add_note",
            category="voice",
            description="Append a note to the user's persistent notes.",
            parameters={
                "type": "object",
                "properties": {"note": {"type": "string", "description": "Note content to save"}},
                "required": ["note"]
            },
            risk_level=RiskLevel.LOW,
            run=add_note_run
        )
    ]
