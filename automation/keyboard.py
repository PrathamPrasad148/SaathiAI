import ctypes
import time

user32 = ctypes.windll.user32

VK_CODES = {
    "enter": 0x0D, "esc": 0x1B, "space": 0x20, "tab": 0x09,
    "backspace": 0x08, "shift": 0x10, "ctrl": 0x11, "alt": 0x12,
    "win": 0x5B, "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28
}

def type_text(text: str, delay: float = 0.01):
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

def send_hotkey(*keys: str):
    vk_list = [VK_CODES.get(k.lower(), ord(k.upper())) if len(k) == 1 else VK_CODES.get(k.lower(), 0) for k in keys]
    for vk in vk_list:
        if vk:
            user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.05)
    for vk in reversed(vk_list):
        if vk:
            user32.keybd_event(vk, 0, 2, 0)
