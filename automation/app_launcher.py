"""
Saathi AI — Universal Windows Application Resolver & Launcher Subsystem
Discovers and launches ANY Windows Desktop application, UWP AppX Store app (WhatsApp, Telegram,
Discord, Spotify, Steam, Office, etc.), protocol handler, or Start Menu shortcut.
"""

import os
import json
import time
import subprocess
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

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

# Known Protocol URI handlers for instant Windows launch
KNOWN_PROTOCOLS = {
    "whatsapp": "whatsapp:",
    "whatsapp desktop": "whatsapp:",
    "telegram": "tg:",
    "discord": "discord:",
    "spotify": "spotify:",
    "netflix": "netflix:",
    "steam": "steam:",
    "zoom": "zoommtg:",
    "teams": "msteams:",
    "microsoft teams": "msteams:",
    "settings": "ms-settings:",
    "windows settings": "ms-settings:",
    "store": "ms-windows-store:",
    "microsoft store": "ms-windows-store:",
    "clock": "ms-clock:",
    "calculator": "calculator:",
    "camera": "microsoft.windows.camera:",
    "maps": "bingmaps:",
    "photos": "ms-photos:",
    "paint": "ms-paint:"
}

_start_apps_cache: Optional[List[Dict[str, str]]] = None
_last_cache_time: float = 0.0

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

def get_installed_windows_apps(force_refresh: bool = False) -> List[Dict[str, str]]:
    """
    Query Windows Get-StartApps to retrieve full list of installed Desktop & UWP apps.
    Returns list of dicts: [{"Name": "WhatsApp", "AppID": "5319275A.WhatsAppDesktop..."}, ...]
    """
    global _start_apps_cache, _last_cache_time
    if not force_refresh and _start_apps_cache and (time.time() - _last_cache_time < 300):
        return _start_apps_cache

    try:
        cmd = ["powershell", "-NoProfile", "-Command", "Get-StartApps | ConvertTo-Json"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout)
            if isinstance(data, dict):
                data = [data]
            _start_apps_cache = data
            _last_cache_time = time.time()
            return _start_apps_cache
    except Exception:
        pass

    return _start_apps_cache or []

def find_app_id_by_query(query: str) -> Optional[Tuple[str, str]]:
    """
    Find matching app in Windows Get-StartApps by query string.
    Returns (App_Name, AppID) if found.
    """
    apps = get_installed_windows_apps()
    if not apps:
        return None

    clean_q = query.lower().strip()

    # 1. Exact Name Match
    for app in apps:
        name = app.get("Name", "").lower().strip()
        if name == clean_q:
            return (app.get("Name"), app.get("AppID"))

    # 2. Substring Match
    for app in apps:
        name = app.get("Name", "").lower().strip()
        if clean_q in name:
            return (app.get("Name"), app.get("AppID"))

    # 3. Token Match
    tokens = [t for t in clean_q.split() if len(t) >= 3]
    if tokens:
        for app in apps:
            name = app.get("Name", "").lower().strip()
            if all(t in name for t in tokens):
                return (app.get("Name"), app.get("AppID"))

    return None

def launch_application(app_name: str) -> Tuple[bool, str]:
    """
    Universal Windows Application Resolver & Launcher.
    Launches standard executables, protocol URIs, and UWP Apps (WhatsApp, Discord, Spotify, etc.).
    """
    key = app_name.lower().strip()

    # 1. Check Known Protocol Handlers (Instant URI trigger)
    if key in KNOWN_PROTOCOLS:
        protocol = KNOWN_PROTOCOLS[key]
        try:
            os.startfile(protocol)
            return True, f"Launched {app_name.capitalize()} via protocol '{protocol}'."
        except Exception:
            pass

    # 2. Chrome Specific
    if any(k in key for k in ("chrome", "google chrome")):
        chrome_exe = get_chrome_executable()
        if chrome_exe:
            subprocess.Popen([chrome_exe])
            return True, "Google Chrome launched successfully."
        else:
            webbrowser.open("https://www.google.com")
            return True, "Opened browser to Google."

    # 3. Edge Specific
    if any(k in key for k in ("edge", "microsoft edge")):
        edge_exe = get_edge_executable()
        if edge_exe:
            subprocess.Popen([edge_exe])
            return True, "Microsoft Edge launched."

    # 4. Search Windows StartApps (UWP & Installed Desktop Apps, e.g. WhatsApp, Discord, Spotify)
    app_match = find_app_id_by_query(key)
    if app_match:
        found_name, app_id = app_match
        try:
            # Launch via explorer.exe shell:AppsFolder\AppID
            subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])
            return True, f"Launched '{found_name}' (AppID: {app_id})."
        except Exception:
            try:
                os.startfile(f"shell:AppsFolder\\{app_id}")
                return True, f"Launched '{found_name}' via shell folder."
            except Exception:
                pass

    # 5. Common Executable Names
    exec_map = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "terminal": "wt.exe",
        "task manager": "taskmgr.exe",
        "taskmgr": "taskmgr.exe",
        "control panel": "control.exe",
        "vlc": "vlc.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "vscode": "code",
        "vs code": "code"
    }

    if key in exec_map:
        try:
            subprocess.Popen([exec_map[key]])
            return True, f"Opened {key.capitalize()} ({exec_map[key]})."
        except Exception:
            pass

    # 6. File Explorer special folders
    if any(k in key for k in ("explorer", "file explorer", "my computer", "this pc")):
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

    # 7. Fallback: try startfile or shell start
    try:
        os.startfile(app_name)
        return True, f"Launched '{app_name}'."
    except Exception:
        try:
            subprocess.Popen(["cmd", "/c", "start", app_name])
            return True, f"Launched '{app_name}' via system shell."
        except Exception as err:
            return False, f"Could not locate or launch '{app_name}': {err}"

def list_installed_applications() -> str:
    """Return JSON string of all installed Windows applications for Saathi awareness."""
    apps = get_installed_windows_apps(force_refresh=True)
    if not apps:
        return "No installed applications found via StartApps query."
    names = [a.get("Name") for a in apps if a.get("Name")]
    return f"Total Installed Applications ({len(names)}):\n" + "\n".join(names[:100])

def search_web_live(query: str, engine: str = "google") -> Tuple[bool, str]:
    """
    Search the web or YouTube immediately and open the results live in browser.
    """
    clean_q = query.strip()
    if not clean_q or clean_q.lower() in ("something", "anything", "stuff", "web"):
        url = "https://www.google.com"
        open_url_in_browser(url)
        return True, "Opened Google Search for you, Pratham."

    encoded = urllib.parse.quote_plus(clean_q)

    if engine == "youtube" or "youtube" in query.lower():
        clean_q = clean_q.replace("on youtube", "").replace("in youtube", "").replace("youtube", "").strip()
        encoded = urllib.parse.quote_plus(clean_q)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        open_url_in_browser(url)
        return True, f"Searching YouTube for '{clean_q}' in browser."

    url = f"https://www.google.com/search?q={encoded}"
    open_url_in_browser(url)
    return True, f"Searching Google for '{clean_q}' in browser."
