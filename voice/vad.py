import numpy as np

class EnergyVAD:
    """Energy-based Voice Activity Detection with dynamic noise floor tracking."""
    def __init__(self, energy_threshold: float = 0.006, silence_frames_threshold: int = 16):
        self.energy_threshold = energy_threshold
        self.silence_frames_threshold = silence_frames_threshold
        self.speech_active = False
        self.silence_counter = 0
        self.noise_floor = 0.003
        self._history = []

    def process_chunk(self, chunk: np.ndarray) -> tuple[bool, float]:
        """Calculates RMS energy and returns (is_speech, energy)."""
        if len(chunk) == 0:
            return (False, 0.0)
        rms = float(np.sqrt(np.mean(chunk**2)))
        
        self._history.append(rms)
        if len(self._history) > 30:
            self._history.pop(0)

        min_ambient = min(self._history)
        self.noise_floor = 0.9 * self.noise_floor + 0.1 * min_ambient
        dynamic_threshold = max(self.energy_threshold, self.noise_floor * 1.5)

        is_speech = rms > dynamic_threshold

        if is_speech:
            self.speech_active = True
            self.silence_counter = 0
        elif self.speech_active:
            self.silence_counter += 1
            if self.silence_counter >= self.silence_frames_threshold:
                self.speech_active = False

        return (self.speech_active, rms)

    def reset(self):
        self.speech_active = False
        self.silence_counter = 0
