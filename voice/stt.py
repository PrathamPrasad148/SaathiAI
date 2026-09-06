import threading
from typing import Optional
import numpy as np

class STTEngine:
    """Local high-performance Speech-to-Text powered by faster-whisper."""
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self._model = None
        self._lock = threading.Lock()

    def _get_model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    from faster_whisper import WhisperModel
                    try:
                        self._model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
                    except Exception:
                        self._model = WhisperModel(self.model_size, device="cpu", compute_type="float32")
        return self._model

    def transcribe(self, audio_data: np.ndarray, language: Optional[str] = None) -> str:
        if len(audio_data) == 0:
            return ""
        try:
            model = self._get_model()
            segments, _ = model.transcribe(
                audio_data,
                language=language,
                beam_size=1,
                best_of=1,
                temperature=0.0,
                vad_filter=True
            )
            return " ".join(seg.text.strip() for seg in segments).strip()
        except Exception:
            return ""
