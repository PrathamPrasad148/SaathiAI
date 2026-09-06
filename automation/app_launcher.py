import os
import subprocess
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Optional, Tuple

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe")
]

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe")
]

def get_chrome_executable() -> Optional[str]:
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    return None

def get_edge_executable() -> Optional[str]:
    for p in EDGE_PATHS:
        if os.path.exists(p):
            return p
    return None

def open_url_in_browser(url: str, force_chrome: bool = True) -> bool:
    """Open URL in Chrome if available, otherwise default browser."""
    if force_chrome:
        chrome_exe = get_chrome_executable()
        if chrome_exe:
            try:
                subprocess.Popen([chrome_exe, url])
                return True
            except Exception:
                pass
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False

def launch_application(app_name: str) -> Tuple[bool, str]:
    """
    Deterministically launch or focus any Windows application.
    Returns (success: bool, message: str).
    """
    key = app_name.lower().strip()

    # 1. Chrome
    if any(k in key for k in ("chrome", "google chrome")):
        chrome_exe = get_chrome_executable()
        if chrome_exe:
            subprocess.Popen([chrome_exe])
            return True, "Google Chrome launched successfully."
        else:
            webbrowser.open("https://www.google.com")
            return True, "Opened browser to Google."

    # 2. Edge
    if any(k in key for k in ("edge", "microsoft edge")):
        edge_exe = get_edge_executable()
        if edge_exe:
            subprocess.Popen([edge_exe])
            return True, "Microsoft Edge launched."
        else:
            subprocess.Popen(["cmd", "/c", "start", "msedge"])
            return True, "Microsoft Edge launched."

    # 3. Notepad
    if "notepad" in key:
        subprocess.Popen(["notepad.exe"])
        return True, "Notepad opened."

    # 4. Calculator
    if any(k in key for k in ("calc", "calculator")):
        subprocess.Popen(["calc.exe"])
        return True, "Calculator opened."

    # 5. File Explorer / This PC / Downloads
    if any(k in key for k in ("explorer", "file explorer", "files", "folder", "my computer", "this pc")):
        if "download" in key:
            p = str(Path.home() / "Downloads")
            subprocess.Popen(["explorer.exe", p])
            return True, f"Opened Downloads folder: {p}"
        elif "document" in key:
            p = str(Path.home() / "Documents")
            subprocess.Popen(["explorer.exe", p])
            return True, f"Opened Documents folder: {p}"
        subprocess.Popen(["explorer.exe"])
        return True, "File Explorer opened."

    # 6. VS Code
    if any(k in key for k in ("vs code", "vscode", "code")):
        try:
            subprocess.Popen(["code"])
            return True, "Visual Studio Code launched."
        except Exception:
            try:
                subprocess.Popen(["cmd", "/c", "code"])
                return True, "Visual Studio Code launched."
            except Exception:
                pass

    # 7. Terminal / PowerShell / Command Prompt
    if any(k in key for k in ("powershell", "terminal", "cmd", "command prompt")):
        if "cmd" in key or "command prompt" in key:
            subprocess.Popen(["cmd.exe"])
            return True, "Command Prompt opened."
        subprocess.Popen(["powershell.exe"])
        return True, "PowerShell opened."

    # 8. Spotify
    if "spotify" in key:
        try:
            os.startfile("spotify:")
            return True, "Spotify launched."
        except Exception:
            open_url_in_browser("https://open.spotify.com")
            return True, "Opened Spotify web player."

    # 9. YouTube
    if "youtube" in key:
        open_url_in_browser("https://www.youtube.com")
        return True, "YouTube opened in browser."

    # 10. Task Manager
    if any(k in key for k in ("taskmgr", "task manager", "task manager")):
        subprocess.Popen(["taskmgr.exe"])
        return True, "Task Manager opened."

    # 11. Settings
    if any(k in key for k in ("setting", "settings", "control panel")):
        try:
            os.startfile("ms-settings:")
            return True, "Windows Settings opened."
        except Exception:
            subprocess.Popen(["control.exe"])
            return True, "Control Panel opened."

    # General fallback: try startfile or shell start
    try:
        os.startfile(app_name)
        return True, f"Launched '{app_name}'."
    except Exception:
        try:
            subprocess.Popen(["cmd", "/c", "start", app_name])
            return True, f"Launched '{app_name}' via system shell."
        except Exception as err:
            return False, f"Could not launch '{app_name}': {err}"

def search_web_live(query: str, engine: str = "google") -> Tuple[bool, str]:
    """
    Search the web or YouTube immediately and open the results live in Chrome/browser.
    """
    clean_q = query.strip()
    if not clean_q or clean_q.lower() in ("something", "anything", "stuff", "web"):
        # Default interesting landing search or homepage
        url = "https://www.google.com"
        open_url_in_browser(url)
        return True, "Opened Google Search for you, Pratham."

    encoded = urllib.parse.quote_plus(clean_q)

    if engine == "youtube" or "youtube" in query.lower():
        # Strip youtube keywords from search terms
        clean_q = clean_q.replace("on youtube", "").replace("in youtube", "").replace("youtube", "").strip()
        encoded = urllib.parse.quote_plus(clean_q)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        open_url_in_browser(url)
        return True, f"Searching YouTube for '{clean_q}' in browser."

    url = f"https://www.google.com/search?q={encoded}"
    open_url_in_browser(url)
    return True, f"Searching Google for '{clean_q}' in browser."

