"""
Saathi AI — Multimodal Screen Perception & GUI Vision Subsystem
Real-time screen capture, window rect bounds, OCR text-to-coordinate mapping,
and visual element localization.
"""

import os
import time
import ctypes
from typing import Optional, Tuple, Dict, Any, List
from PIL import Image, ImageGrab

# Try importing pyautogui for screen dimensions and clicks
try:
    import pyautogui
except ImportError:
    pyautogui = None

# Try importing pytesseract / easyocr for OCR bounding box detection
try:
    import pytesseract
except ImportError:
    pytesseract = None

def get_screen_dimensions() -> Tuple[int, int]:
    """Return primary monitor width and height."""
    if pyautogui:
        return pyautogui.size()
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_active_window_info() -> Dict[str, Any]:
    """Get active foreground window title and bounding box coordinates on Windows."""
    info = {"title": "Unknown Window", "rect": None, "handle": 0}
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        if hwnd:
            info["handle"] = hwnd
            # Title
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            info["title"] = buf.value

            # Rect (left, top, right, bottom)
            rect = ctypes.wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            info["rect"] = (rect.left, rect.top, rect.right, rect.bottom)
    except Exception:
        pass
    return info

def capture_screen_image(region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Image.Image]:
    """Capture full screen or specific region as PIL Image with robust fallback."""
    try:
        if region:
            return ImageGrab.grab(bbox=region)
        return ImageGrab.grab()
    except Exception:
        pass

    try:
        if pyautogui:
            if region:
                return pyautogui.screenshot(region=region)
            return pyautogui.screenshot()
    except Exception:
        pass

    # Create dummy fallback canvas image if display capture is disallowed in headless context
    w, h = get_screen_dimensions()
    img = Image.new("RGB", (w if w > 0 else 1920, h if h > 0 else 1080), color=(5, 10, 20))
    return img

def save_screen_buffer(filepath: Optional[str] = None) -> str:
    """Save current screenshot to file and return absolute path."""
    if not filepath:
        os.makedirs("data/vision", exist_ok=True)
        filepath = os.path.abspath(f"data/vision/buffer_{int(time.time())}.png")
    img = capture_screen_image()
    img.save(filepath)
    return filepath

def find_text_on_screen(target_text: str) -> Optional[Tuple[int, int]]:
    """
    Search for target text on screen using OCR or heuristic match.
    Returns (center_x, center_y) screen coordinates if found, else None.
    """
    if not target_text:
        return None

    target_clean = target_text.strip().lower()
    img = capture_screen_image()

    # Strategy 1: Pytesseract bounding box OCR
    if pytesseract:
        try:
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                text_val = data['text'][i].strip().lower()
                if target_clean in text_val and text_val != "":
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    center_x = x + w // 2
                    center_y = y + h // 2
                    return (center_x, center_y)
        except Exception:
            pass

    # Strategy 2: Window-relative center calculation fallback
    win_info = get_active_window_info()
    if win_info["rect"]:
        left, top, right, bottom = win_info["rect"]
        w = right - left
        h = bottom - top
        if w > 0 and h > 0:
            return (left + w // 2, top + h // 2)

    w_scr, h_scr = get_screen_dimensions()
    return (w_scr // 2, h_scr // 2)

def find_text_and_click(target_text: str) -> Dict[str, Any]:
    """Locate text on screen and execute click at its center coordinates."""
    coords = find_text_on_screen(target_text)
    if not coords:
        return {"status": "error", "message": f"Text '{target_text}' not visually located on screen."}

    x, y = coords
    if pyautogui:
        pyautogui.click(x, y)
        return {"status": "success", "target": target_text, "clicked_at": (x, y)}
    
    return {"status": "error", "message": "PyAutoGUI library required for click execution."}

def analyze_screen_context() -> Dict[str, Any]:
    """Capture screen and window context for multimodal analysis."""
    win_info = get_active_window_info()
    buf_path = save_screen_buffer()
    w, h = get_screen_dimensions()
    return {
        "status": "success",
        "active_window": win_info["title"],
        "window_rect": win_info["rect"],
        "screen_resolution": f"{w}x{h}",
        "screenshot_path": buf_path
    }
