def get_clipboard_text() -> str:
    try:
        import pyperclip
        return pyperclip.paste()
    except Exception:
        pass
    try:
        import tkinter as tk
        r = tk.Tk()
        r.withdraw()
        txt = r.clipboard_get()
        r.destroy()
        return txt
    except Exception:
        return ""

def set_clipboard_text(text: str) -> bool:
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        pass
    try:
        import tkinter as tk
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.update()
        r.destroy()
        return True
    except Exception:
        return False

# Aliases for universal clipboard API
copy_to_clipboard = set_clipboard_text
paste_from_clipboard = get_clipboard_text

