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
