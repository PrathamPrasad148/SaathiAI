"""
Saathi AI — Standalone Background Wake-Daemon
Runs as a silent low-memory background listener on Windows.
Listens continuously for the wake word 'Saathi' or 'Hey Saathi'.
If Saathi AI is not running, launches main.py in full-screen HUD mode.
If Saathi AI is already running, brings the active HUD window to foreground.
"""

import os
import sys
import time
import subprocess
import ctypes
from typing import Optional

LOG_FILE = r"C:\SAATHIAI\wake_daemon.log"

def log_event(msg: str):
    """Write timestamped log message to wake_daemon.log and stdout."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {msg}\n"
    print(log_line, end="")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass

WAKE_KEYWORDS = (
    "saathi", "sathi", "sati", "saat", "sot", "sawthi", "soothie", "sothey",
    "sauthi", "study", "sorry", "sathya", "shawty", "southy", "safi", "shathi",
    "saati", "swati", "saath", "sath", "साथी", "saty", "suty", "shaathi", "satya",
    "scotty", "sari", "saari", "stacy", "shot", "suite", "seth", "sethi"
)

def matches_wake_word(spoken_text: str) -> bool:
    """Check if spoken text matches any phonetic variant of 'Saathi'."""
    clean = spoken_text.lower().strip()
    no_spaces = clean.replace(" ", "")
    words = clean.split()
    
    for kw in WAKE_KEYWORDS:
        if kw in clean or kw in no_spaces:
            return True

    for word in words:
        if word.startswith("sath") or word.startswith("saat") or word.startswith("sati") or word.startswith("saath"):
            return True
            
    return False

def is_saathi_running() -> bool:
    """Check if main Saathi AI process is currently active."""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            cmdline = proc.info.get('cmdline') or []
            cmd_str = " ".join(cmdline).lower()
            if "main.py" in cmd_str and "wake_daemon" not in cmd_str:
                return True
    except Exception:
        pass
    return False

def launch_saathi_full_screen():
    """Launch Saathi AI silently in full-screen HUD mode."""
    python_exe = r"C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe"
    main_script = r"C:\SAATHIAI\main.py"
    try:
        log_event("[WAKE DAEMON] Executing Saathi AI full-screen launch...")
        subprocess.Popen([python_exe, main_script], cwd=r"C:\SAATHIAI")
    except Exception as e:
        log_event(f"[WAKE DAEMON ERROR] Launch failed: {e}")

def focus_saathi_window():
    """Bring existing Saathi AI HUD window to foreground and maximize."""
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
                    user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
                    user32.SetForegroundWindow(hwnd)
                    user32.BringWindowToTop(hwnd)
                    log_event(f"[WAKE DAEMON] Brought window '{title}' to foreground.")
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
        user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
    except Exception as e:
        log_event(f"[WAKE DAEMON ERROR] Focus window failed: {e}")

def on_wake_word_detected(spoken_text: str):
    """Triggered when 'Saathi' or 'Hey Saathi' is heard."""
    log_event(f"[WAKE WORD MATCHED] Spoken phrase: '{spoken_text}'")
    if not is_saathi_running():
        log_event("[ACTION] Saathi AI not open. Launching full-screen HUD...")
        launch_saathi_full_screen()
    else:
        log_event("[ACTION] Saathi AI already open. Focusing HUD window...")
        focus_saathi_window()

def run_speech_recognition_loop():
    """Engine 1: Auto-reconnecting Google STT Microphone Listener."""
    import speech_recognition as sr
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300

    log_event("[WAKE DAEMON] Starting speech recognition listener loop...")

    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.6)
                log_event("[WAKE DAEMON] Microphone calibrated & listening...")
                while True:
                    try:
                        audio = r.listen(source, timeout=3.0, phrase_time_limit=4.0)
                        try:
                            text = r.recognize_google(audio).lower().strip()
                            log_event(f"[AUDIO RECOGNIZED]: '{text}'")
                            if matches_wake_word(text):
                                on_wake_word_detected(text)
                                time.sleep(3.0)  # Cooldown
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as req_err:
                            log_event(f"[STT REQUEST ERROR]: {req_err}")
                            time.sleep(1.0)
                    except sr.WaitTimeoutError:
                        pass
                    except Exception as inner_err:
                        log_event(f"[INNER MIC LOOP ERROR]: {inner_err}")
                        break
        except Exception as mic_err:
            log_event(f"[MIC RE-INIT ERROR]: {mic_err}. Retrying in 2s...")
            time.sleep(2.0)

def run_sapi_loop():
    """Engine 2: Native Windows SAPI COM Recognizer Fallback."""
    try:
        import win32com.client
        recognizer = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
        context = recognizer.CreateRecoContext()
        grammar = context.CreateGrammar()
        grammar.DictationSetState(1)

        log_event("[WAKE DAEMON] Native Windows SAPI Listener active. Listening for 'Saathi'...")

        class ContextEvents:
            def OnRecognition(self, StreamNumber, StreamPosition, RecognitionType, Result):
                try:
                    reco_result = win32com.client.Dispatch(Result)
                    text = reco_result.PhraseInfo.GetText().lower().strip()
                    log_event(f"[SAPI RECOGNIZED]: '{text}'")
                    if matches_wake_word(text):
                        on_wake_word_detected(text)
                except Exception:
                    pass

        win32com.client.WithEvents(context, ContextEvents)

        import pythoncom
        while True:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)
    except Exception as e:
        log_event(f"[WAKE DAEMON] SAPI fallback loop error: {e}")
        while True:
            time.sleep(2.0)

if __name__ == "__main__":
    log_event("==================================================")
    log_event("SAATHI AI WAKE DAEMON INITIALIZING")
    log_event("==================================================")

    # Launch Continuous Self-Advancement Loop whenever System is ON
    try:
        def launch_continuous_advancement():
            python_exe = r"C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe"
            adv_script = r"C:\SAATHIAI\devloop\continuous_advancement.py"
            subprocess.Popen([python_exe, adv_script], cwd=r"C:\SAATHIAI")
            log_event("[WAKE DAEMON] Continuous Self-Advancement Service launched in background (100+ Agents).")

        threading.Thread(target=launch_continuous_advancement, daemon=True).start()
    except Exception as adv_e:
        log_event(f"[WAKE DAEMON] Continuous advancement launch warning: {adv_e}")

    try:
        run_speech_recognition_loop()
    except Exception as top_e:
        log_event(f"[TOP LEVEL CRASH]: {top_e}. Falling back to SAPI...")
        run_sapi_loop()

