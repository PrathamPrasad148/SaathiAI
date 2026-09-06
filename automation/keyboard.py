import time
import ctypes

try:
    import pyautogui
    import pyperclip
    _HAS_PYAUTOGUI = True
except ImportError:
    _HAS_PYAUTOGUI = False

user32 = ctypes.windll.user32

VK_CODES = {
    "enter": 0x0D, "return": 0x0D, "esc": 0x1B, "escape": 0x1B,
    "space": 0x20, "tab": 0x09, "backspace": 0x08, "shift": 0x10,
    "ctrl": 0x11, "control": 0x11, "alt": 0x12, "win": 0x5B,
    "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28,
    "delete": 0x2E, "home": 0x24, "end": 0x23, "pageup": 0x21, "pagedown": 0x22
}

def type_text(text: str, delay: float = 0.01, use_clipboard_for_complex: bool = True):
    """
    Type text into currently focused application.
    Uses PyAutoGUI or clipboard paste for flawless Unicode/special character support.
    """
    if not text:
        return

    # If text has newlines, special symbols, or non-ASCII, clipboard paste is 100x more reliable!
    has_complex = any(ord(c) > 127 or c in "\n\r\t\"'`~$^{}[]" for c in text)
    if has_complex and _HAS_PYAUTOGUI and use_clipboard_for_complex:
        try:
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.05)
            return
        except Exception:
            pass

    if _HAS_PYAUTOGUI:
        try:
            pyautogui.write(text, interval=delay)
            return
        except Exception:
            pass

    # Windows user32 fallback
    for char in text:
        vk = user32.VkKeyScanW(ord(char))
        if vk != -1:
            code = vk & 0xFF
            shift = (vk >> 8) & 1
            if shift:
                user32.keybd_event(0x10, 0, 0, 0)
            user32.keybd_event(code, 0, 0, 0)
            user32.keybd_event(code, 0, 2, 0)
            if shift:
                user32.keybd_event(0x10, 0, 2, 0)
            if delay > 0:
                time.sleep(delay)

def press_key(key: str):
    """Press a single key (e.g. 'enter', 'esc', 'tab', 'backspace')."""
    k = key.lower().strip()
    if _HAS_PYAUTOGUI:
        try:
            pyautogui.press(k)
            return
        except Exception:
            pass
    vk = VK_CODES.get(k)
    if vk:
        user32.keybd_event(vk, 0, 0, 0)
        time.sleep(0.02)
        user32.keybd_event(vk, 0, 2, 0)

def send_hotkey(*keys: str):
    """Send hotkey combination like ('ctrl', 'c') or ('win', 'd')."""
    clean_keys = [k.lower().strip() for k in keys if k.strip()]
    if not clean_keys:
        return

    if _HAS_PYAUTOGUI:
        try:
            pyautogui.hotkey(*clean_keys)
            return
        except Exception:
            pass

    # Windows user32 fallback
    vk_list = [VK_CODES.get(k, ord(k.upper())) if len(k) == 1 else VK_CODES.get(k, 0) for k in clean_keys]
    for vk in vk_list:
        if vk:
            user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.05)
    for vk in reversed(vk_list):
        if vk:
            user32.keybd_event(vk, 0, 2, 0)

