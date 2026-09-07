import platform
import os
from typing import Dict, Any

def get_system_telemetry() -> Dict[str, Any]:
    info = {
        "os": f"{platform.system()} {platform.release()}",
        "hostname": platform.node(),
        "cpu_percent": 0.0,
        "ram_percent": 0.0,
        "ram_used_gb": 0.0,
        "ram_total_gb": 0.0,
        "disk_percent": 0.0,
        "battery_percent": None,
        "is_charging": None
    }
    try:
        import psutil
        info["cpu_percent"] = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        info["ram_percent"] = mem.percent
        info["ram_used_gb"] = round(mem.used / (1024**3), 1)
        info["ram_total_gb"] = round(mem.total / (1024**3), 1)
        disk = psutil.disk_usage(os.getcwd())
        info["disk_percent"] = disk.percent
        battery = psutil.sensors_battery()
        if battery:
            info["battery_percent"] = battery.percent
            info["is_charging"] = battery.power_plugged
    except Exception:
        pass
    return info

def set_autostart_on_boot(enable: bool = True) -> tuple[bool, str]:
    """Register or unregister Saathi AI in Windows startup registry to launch on laptop boot."""
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "SaathiAI"
        vbs_path = r"C:\SAATHIAI\Start-Saathi-Silent.vbs"

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        if enable:
            if not os.path.exists(vbs_path):
                with open(vbs_path, "w", encoding="utf-8") as f:
                    f.write('CreateObject("Wscript.Shell").Run """C:\\SAATHIAI\\Start-Saathi.bat""", 0, False\n')
            cmd_val = f'wscript.exe "{vbs_path}"'
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd_val)
            winreg.CloseKey(key)
            return True, "Saathi AI registered to autolaunch on Windows boot."
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True, "Saathi AI boot autolaunch disabled."
    except Exception as e:
        return False, str(e)

