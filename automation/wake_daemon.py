"""
Saathi AI — Standalone Background Wake-Daemon
Runs as a silent low-memory background listener on Windows.
Listens for the wake word 'Saathi' or 'Hey Saathi'.
If Saathi AI is not running, launches main.py in full-screen HUD mode.
If Saathi AI is already running, brings the active HUD window to the foreground.
"""

import os
import sys
import time
import subprocess
import ctypes
from typing import Optional

def is_saathi_running() -> bool:
    """Check if main Saathi AI process is currently active."""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            cmdline = proc.info.get('cmdline') or []
            cmd_str = " ".join(cmdline).lower()
            if "main.py" in cmd_str:
                if "wake_daemon" not in cmd_str:
                    return True
    except Exception:
        pass
    return False

def launch_saathi_full_screen():
    """Launch Saathi AI silently in full-screen HUD mode."""
    vbs_path = r"C:\SAATHIAI\Start-Saathi-Silent.vbs"
    bat_path = r"C:\SAATHIAI\Start-Saathi.bat"

    if os.path.exists(vbs_path):
        os.system(f'wscript.exe "{vbs_path}"')
    elif os.path.exists(bat_path):
        subprocess.Popen([bat_path], shell=True)
    else:
        subprocess.Popen(["py", "-3.12", "main.py"], cwd=r"C:\SAATHIAI")

def focus_saathi_window():
    """Bring existing Saathi AI HUD window to foreground."""
    try:
        user32 = ctypes.windll.user32

        def enum_windows_callback(hwnd, extra):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value
                if "SAATHI AI" in title.upper() or "PRATHAM PRASAD" in title.upper():
                    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                    user32.SetForegroundWindow(hwnd)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
        user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
    except Exception:
        pass

def on_wake_word_detected(spoken_text: str):
    """Triggered when 'Saathi' or 'Hey Saathi' is heard."""
    print(f"[WAKE DAEMON] Wake word detected: '{spoken_text}'")
    if not is_saathi_running():
        print("[WAKE DAEMON] Saathi AI not open. Launching full-screen HUD...")
        launch_saathi_full_screen()
    else:
        print("[WAKE DAEMON] Saathi AI already open. Focusing HUD window...")
        focus_saathi_window()

def run_speech_recognition_loop():
    """Engine 1: PyAudio / SpeechRecognition loop."""
    import speech_recognition as sr
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.8)
        while True:
            try:
                audio = r.listen(source, timeout=3.0, phrase_time_limit=4.0)
                try:
                    text = r.recognize_google(audio).lower().strip()
                    if any(w in text for w in ("saathi", "sathi", "sati", "hey saathi", "hi saathi")):
                        on_wake_word_detected(text)
                        time.sleep(3.0)  # Cooldown
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    time.sleep(1.0)
            except Exception:
                time.sleep(0.5)

def run_sapi_loop():
    """Engine 2: Native Windows SAPI COM Recognizer (Built-in to Windows)."""
    try:
        import win32com.client
        recognizer = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
        context = recognizer.CreateRecoContext()
        grammar = context.CreateGrammar()
        grammar.DictationSetState(1)

        print("[WAKE DAEMON] Native Windows SAPI Listener active. Listening for 'Saathi'...")

        class ContextEvents:
            def OnRecognition(self, StreamNumber, StreamPosition, RecognitionType, Result):
                try:
                    reco_result = win32com.client.Dispatch(Result)
                    text = reco_result.PhraseInfo.GetText().lower().strip()
                    if any(w in text for w in ("saathi", "sathi", "sati", "hey saathi")):
                        on_wake_word_detected(text)
                except Exception:
                    pass

        win32com.client.WithEvents(context, ContextEvents)

        import pythoncom
        while True:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)
    except Exception as e:
        print(f"[WAKE DAEMON] SAPI fallback loop: {e}")
        while True:
            time.sleep(2.0)

if __name__ == "__main__":
    try:
        run_speech_recognition_loop()
    except Exception:
        run_sapi_loop()
