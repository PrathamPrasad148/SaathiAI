import time
import ctypes

try:
    import pyautogui
    _HAS_PYAUTOGUI = True
except ImportError:
    _HAS_PYAUTOGUI = False

user32 = ctypes.windll.user32

def get_cursor_pos() -> tuple[int, int]:
    if _HAS_PYAUTOGUI:
        try:
            pt = pyautogui.position()
            return (pt.x, pt.y)
        except Exception:
            pass

    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return (pt.x, pt.y)

def move_mouse(x: int, y: int, duration: float = 0.2):
    if _HAS_PYAUTOGUI:
        try:
            pyautogui.moveTo(int(x), int(y), duration=duration)
            return
        except Exception:
            pass
    user32.SetCursorPos(int(x), int(y))

def click_mouse(x: int = None, y: int = None, button: str = "left"):
    if _HAS_PYAUTOGUI:
        try:
            if x is not None and y is not None:
                pyautogui.click(int(x), int(y), button=button)
            else:
                pyautogui.click(button=button)
            return
        except Exception:
            pass

    if x is not None and y is not None:
        user32.SetCursorPos(int(x), int(y))
    time.sleep(0.02)
    if button == "right":
        user32.mouse_event(0x0008, 0, 0, 0, 0)
        user32.mouse_event(0x0010, 0, 0, 0, 0)
    else:
        user32.mouse_event(0x0002, 0, 0, 0, 0)
        user32.mouse_event(0x0004, 0, 0, 0, 0)

def double_click(x: int = None, y: int = None):
    if _HAS_PYAUTOGUI:
        try:
            if x is not None and y is not None:
                pyautogui.doubleClick(int(x), int(y))
            else:
                pyautogui.doubleClick()
            return
        except Exception:
            pass

    click_mouse(x, y)
    time.sleep(0.08)
    click_mouse(x, y)

def scroll_mouse(clicks: int):
    if _HAS_PYAUTOGUI:
        try:
            pyautogui.scroll(int(clicks) * 100)
            return
        except Exception:
            pass
    user32.mouse_event(0x0800, 0, 0, clicks * 120, 0)

