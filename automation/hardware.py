"""
Saathi AI — Hardware Telemetry & GPU Diagnostics Subsystem
Direct GPU VRAM, Temperature, Fan Speed, and Power Telemetry via NVML.
"""

from typing import Dict, Any

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
