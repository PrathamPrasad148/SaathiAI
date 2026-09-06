import ctypes
from typing import List, Dict, Any

user32 = ctypes.windll.user32

def list_open_windows() -> List[Dict[str, Any]]:
    windows = []
    def enum_cb(hwnd, extra):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value.strip()
                if title and title not in ("Program Manager", "Settings"):
                    windows.append({"hwnd": hwnd, "title": title})
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(EnumWindowsProc(enum_cb), 0)
    return windows

def focus_window_by_title(partial_title: str) -> bool:
    target = partial_title.lower()
    for win in list_open_windows():
        if target in win["title"].lower():
            hwnd = win["hwnd"]
            user32.ShowWindow(hwnd, 9)
            user32.SetForegroundWindow(hwnd)
            return True
    return False

def minimize_all_windows():
    user32.keybd_event(0x5B, 0, 0, 0)
    user32.keybd_event(0x4D, 0, 0, 0)
    user32.keybd_event(0x4D, 0, 2, 0)
    user32.keybd_event(0x5B, 0, 2, 0)
