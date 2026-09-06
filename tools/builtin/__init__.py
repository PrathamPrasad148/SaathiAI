from pathlib import Path
from ..registry import ToolRegistry
from .files import get_file_tools
from .system import get_system_tools
from .system_control import get_system_control_tools
from .web import get_web_tools
from .voice import get_voice_and_note_tools
from .vision import get_vision_tools
from .memory import get_memory_tools

def register_all_builtin_tools(registry: ToolRegistry, app_dir: Path, reminder_mgr, notes_file: Path, memory_engine, automation_engine):
    for t in get_file_tools(app_dir):
        registry.register(t)
    for t in get_system_tools(app_dir):
        registry.register(t)
    for t in get_system_control_tools():
        registry.register(t)
    for t in get_web_tools():
        registry.register(t)
    for t in get_voice_and_note_tools(reminder_mgr, notes_file):
        registry.register(t)
    for t in get_vision_tools(app_dir / "Projects"):
        registry.register(t)
    for t in get_memory_tools(memory_engine, automation_engine):
        registry.register(t)

