"""
Saathi AI — Hardware Telemetry & System Power/Audio Control Subsystem
Combines NVML GPU Diagnostics with Windows System Volume, Media Keys, Power & Recycle Bin Controls.
"""

import os
import ctypes
from typing import Dict, Any

# Windows Virtual Key Codes for Hardware Audio/Media
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xB3

KEYEVENTF_KEYUP = 0x0002

def _send_vk(vk_code: int, times: int = 1):
    """Send virtual key code press to Windows user32 input stream."""
    try:
        user32 = ctypes.windll.user32
        for _ in range(times):
            user32.keybd_event(vk_code, 0, 0, 0)
            user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)
    except Exception:
        pass

def toggle_volume_mute():
    """Toggle system audio mute status."""
    _send_vk(VK_VOLUME_MUTE)

def volume_up(steps: int = 5):
    """Increase system volume by specified steps."""
    _send_vk(VK_VOLUME_UP, steps)

def volume_down(steps: int = 5):
    """Decrease system volume by specified steps."""
    _send_vk(VK_VOLUME_DOWN, steps)

def media_play_pause():
    """Toggle global media playback (play/pause)."""
    _send_vk(VK_MEDIA_PLAY_PAUSE)

def media_next():
    """Skip to next media track."""
    _send_vk(VK_MEDIA_NEXT_TRACK)

def media_prev():
    """Skip to previous media track."""
    _send_vk(VK_MEDIA_PREV_TRACK)

def media_stop():
    """Stop active media playback."""
    _send_vk(VK_MEDIA_STOP)

def lock_workstation():
    """Lock the Windows workstation immediately."""
    try:
        ctypes.windll.user32.LockWorkStation()
    except Exception:
        os.system("rundll32.exe user32.dll,LockWorkStation")

def empty_recycle_bin():
    """Empty the Windows Recycle Bin without prompt."""
    try:
        # SHERB_NOCONFIRMATION = 0x00000001, SHERB_NOPROGRESSUI = 0x00000002, SHERB_NOSOUND = 0x00000004
        flags = 0x00000001 | 0x00000002 | 0x00000004
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
    except Exception:
        pass

def sleep_workstation():
    """Put the Windows PC to sleep."""
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def restart_workstation():
    """Restart the Windows PC in 5 seconds."""
    os.system("shutdown /r /t 5")

def shutdown_workstation():
    """Power down the Windows PC in 5 seconds."""
    os.system("shutdown /s /t 5")

def abort_shutdown():
    """Cancel any pending system shutdown or restart."""
    os.system("shutdown /a")

# -------------------------------------------------------------
# NVML GPU Telemetry Section
# -------------------------------------------------------------
_nvml_initialized = False

def _init_nvml():
    global _nvml_initialized
    if _nvml_initialized:
        return True
    try:
        import pynvml
        pynvml.nvmlInit()
        _nvml_initialized = True
        return True
    except Exception:
        _nvml_initialized = False
        return False

def get_gpu_telemetry() -> Dict[str, Any]:
    """
    Query NVIDIA GPU hardware telemetry using NVML.
    Returns dictionary with GPU utilization, VRAM usage, temperature, and fan speed.
    """
    telemetry = {
        "available": False,
        "name": "N/A",
        "gpu_util_percent": 0.0,
        "vram_used_gb": 0.0,
        "vram_total_gb": 0.0,
        "vram_percent": 0.0,
        "temp_c": 0,
        "fan_percent": 0,
        "power_w": 0.0
    }

    if not _init_nvml():
        return telemetry

    try:
        import pynvml
        count = pynvml.nvmlDeviceGetCount()
        if count > 0:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            telemetry["available"] = True

            # GPU Name
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            telemetry["name"] = name

            # Memory Info
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            telemetry["vram_used_gb"] = round(mem.used / (1024**3), 2)
            telemetry["vram_total_gb"] = round(mem.total / (1024**3), 2)
            telemetry["vram_percent"] = round((mem.used / mem.total) * 100, 1)

            # Utilization & Temperature
            try:
                rates = pynvml.nvmlDeviceGetUtilizationRates(handle)
                telemetry["gpu_util_percent"] = float(rates.gpu)
            except Exception:
                pass

            try:
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                telemetry["temp_c"] = int(temp)
            except Exception:
                pass

            try:
                fan = pynvml.nvmlDeviceGetFanSpeed(handle)
                telemetry["fan_percent"] = int(fan)
            except Exception:
                pass

            try:
                pwr = pynvml.nvmlDeviceGetPowerUsage(handle)
                telemetry["power_w"] = round(pwr / 1000.0, 1)
            except Exception:
                pass
    except Exception:
        telemetry["available"] = False

    return telemetry
