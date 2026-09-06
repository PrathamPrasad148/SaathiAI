import numpy as np
from typing import Dict, Any

class AudioAnalyzer:
    """
    Analyzes live audio chunks for real-time visualizer waveform, energy telemetry,
    and adaptive voice activity thresholding.
    """
    def __init__(self, initial_threshold: float = 0.006):
        self.current_rms = 0.0
        self.peak_volume = 0.0
        self.is_speaking = False
        self.noise_floor = 0.003
        self.threshold = initial_threshold
        self._history = []

    def analyze(self, chunk: np.ndarray) -> Dict[str, Any]:
        if len(chunk) == 0:
            return {"rms": 0.0, "peak": 0.0, "active": False}
        
        rms = float(np.sqrt(np.mean(chunk**2)))
        peak = float(np.max(np.abs(chunk)))
        self.current_rms = rms
        self.peak_volume = peak

        # Keep rolling history for ambient noise floor calibration (last 30 chunks ~ 1.5s)
        self._history.append(rms)
        if len(self._history) > 30:
            self._history.pop(0)

        # Dynamic threshold adapts slightly above minimum background noise
        min_ambient = min(self._history)
        self.noise_floor = 0.9 * self.noise_floor + 0.1 * min_ambient
        dynamic_threshold = max(0.006, self.noise_floor * 1.5)

        self.is_speaking = rms > dynamic_threshold

        return {
            "rms": round(rms, 4),
            "peak": round(peak, 4),
            "active": self.is_speaking,
            "threshold": round(dynamic_threshold, 4)
        }
