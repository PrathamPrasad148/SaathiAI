import ctypes
import time

user32 = ctypes.windll.user32

def get_cursor_pos() -> tuple[int, int]:
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return (pt.x, pt.y)

def move_mouse(x: int, y: int):
    user32.SetCursorPos(x, y)

def click_mouse(x: int = None, y: int = None, button: str = "left"):
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
    time.sleep(0.02)
    if button == "right":
        user32.mouse_event(0x0008, 0, 0, 0, 0)
        user32.mouse_event(0x0010, 0, 0, 0, 0)
    else:
        user32.mouse_event(0x0002, 0, 0, 0, 0)
        user32.mouse_event(0x0004, 0, 0, 0, 0)

def double_click(x: int = None, y: int = None):
    click_mouse(x, y)
    time.sleep(0.08)
    click_mouse(x, y)

def scroll_mouse(clicks: int):
    user32.mouse_event(0x0800, 0, 0, clicks * 120, 0)
