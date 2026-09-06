import ctypes
import os
import subprocess
import time
from typing import Optional

user32 = ctypes.windll.user32
shell32 = ctypes.windll.shell32

# Virtual key codes for volume and media
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xB3

def _send_vk(vk_code: int):
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.02)
    user32.keybd_event(vk_code, 0, 2, 0)

def toggle_volume_mute():
    """Toggle system audio mute."""
    _send_vk(VK_VOLUME_MUTE)

def volume_up(steps: int = 5):
    """Increase system volume by a number of steps."""
    for _ in range(max(1, min(50, steps))):
        _send_vk(VK_VOLUME_UP)
        time.sleep(0.01)

def volume_down(steps: int = 5):
    """Decrease system volume by a number of steps."""
    for _ in range(max(1, min(50, steps))):
        _send_vk(VK_VOLUME_DOWN)
        time.sleep(0.01)

def media_play_pause():
    """Play or pause current media playback."""
    _send_vk(VK_MEDIA_PLAY_PAUSE)

def media_next():
    """Skip to next media track."""
    _send_vk(VK_MEDIA_NEXT_TRACK)

def media_prev():
    """Return to previous media track."""
    _send_vk(VK_MEDIA_PREV_TRACK)

def media_stop():
    """Stop media playback."""
    _send_vk(VK_MEDIA_STOP)

def lock_workstation() -> bool:
    """Instantly lock the Windows workstation."""
    return bool(user32.LockWorkStation())

def empty_recycle_bin() -> bool:
    """Empty the Windows Recycle Bin silently."""
    # SHERB_NOCONFIRMATION = 0x00000001
    # SHERB_NOPROGRESSUI = 0x00000002
    # SHERB_NOSOUND = 0x00000004
    flags = 0x00000001 | 0x00000002 | 0x00000004
    res = shell32.SHEmptyRecycleBinW(None, None, flags)
    return res == 0

def sleep_workstation():
    """Put Windows to sleep."""
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=False)

def restart_workstation(delay_seconds: int = 10):
    """Schedule computer restart."""
    subprocess.run(["shutdown", "/r", "/t", str(delay_seconds), "/c", "Saathi AI Autonomous Directive: Restarting system"], check=False)

def shutdown_workstation(delay_seconds: int = 15):
    """Schedule computer shutdown."""
    subprocess.run(["shutdown", "/s", "/t", str(delay_seconds), "/c", "Saathi AI Autonomous Directive: Shutting down system"], check=False)

def abort_shutdown():
    """Abort a scheduled shutdown or restart."""
    subprocess.run(["shutdown", "/a"], check=False)
