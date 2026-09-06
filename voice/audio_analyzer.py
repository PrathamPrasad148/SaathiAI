import numpy as np
from typing import Dict, Any

class AudioAnalyzer:
    """Analyzes live audio chunks for real-time visualizer waveform and energy telemetry."""
    def __init__(self):
        self.current_rms = 0.0
        self.peak_volume = 0.0
        self.is_speaking = False

    def analyze(self, chunk: np.ndarray) -> Dict[str, Any]:
        if len(chunk) == 0:
            return {"rms": 0.0, "peak": 0.0, "active": False}
        rms = float(np.sqrt(np.mean(chunk**2)))
        peak = float(np.max(np.abs(chunk)))
        self.current_rms = rms
        self.peak_volume = peak
        self.is_speaking = rms > 0.02
        return {
            "rms": round(rms, 4),
            "peak": round(peak, 4),
            "active": self.is_speaking
        }
