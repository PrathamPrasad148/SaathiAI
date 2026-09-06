from pathlib import Path
from typing import Dict, Any, List, Optional
from .system import get_system_telemetry
from .processes import list_running_processes, kill_process
from .windows import list_open_windows, focus_window_by_title, minimize_all_windows
from .keyboard import type_text, send_hotkey
from .mouse import get_cursor_pos, move_mouse, click_mouse, double_click, scroll_mouse
from .clipboard import get_clipboard_text, set_clipboard_text
from .screen import capture_screen
from .ocr import read_text_from_image

class ComputerController:
    """Unified interface for authorized local computer automation."""
    def __init__(self, projects_dir: Path):
        self.projects_dir = projects_dir

    def get_system_info(self) -> Dict[str, Any]:
        return get_system_telemetry()

    def list_processes(self, limit: int = 20) -> List[Dict[str, Any]]:
        return list_running_processes(limit)

    def kill_proc(self, pid: int) -> bool:
        return kill_process(pid)

    def list_windows(self) -> List[Dict[str, Any]]:
        return list_open_windows()

    def focus_window(self, title: str) -> bool:
        return focus_window_by_title(title)

    def minimize_all(self):
        minimize_all_windows()

    def type_string(self, text: str):
        type_text(text)

    def hotkey(self, *keys: str):
        send_hotkey(*keys)

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left"):
        click_mouse(x, y, button)

    def take_screenshot(self) -> str:
        p = capture_screen(self.projects_dir)
        return str(p)

    def inspect_screen_text(self) -> str:
        path = capture_screen(self.projects_dir)
        return read_text_from_image(path)

    def clipboard_read(self) -> str:
        return get_clipboard_text()

    def clipboard_write(self, text: str) -> bool:
        return set_clipboard_text(text)
