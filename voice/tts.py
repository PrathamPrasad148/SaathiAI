import asyncio
import tempfile
import threading
import time
import re
from pathlib import Path
from typing import Optional, Callable

class TTSEngine:
    """Edge TTS synthesizer with immediate interruptibility and amplitude feedback."""
    def __init__(self, voice: str = "en-IN-NeerjaNeural"):
        self.voice = voice
        self.is_playing = False
        self._stop_requested = threading.Event()
        self.last_speech_finish_time: float = 0.0
        self.on_amplitude_callback: Optional[Callable[[float], None]] = None

    def is_speaking(self) -> bool:
        """Returns True if TTS is actively playing or finished within cooldown period."""
        if self.is_playing:
            return True
        if self.last_speech_finish_time > 0:
            return (time.time() - self.last_speech_finish_time < 0.35)
        return False

    def stop(self):
        """Immediately interrupt and stop ongoing speech."""
        self._stop_requested.set()
        try:
            import pygame
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except Exception:
            pass
        self.is_playing = False
        self.last_speech_finish_time = time.time()

    def speak(self, text: str, on_start: Optional[Callable] = None, on_finish: Optional[Callable] = None) -> bool:
        self.stop()
        self._stop_requested.clear()

        clean = re.sub(r"[*_`#<>{}]", "", text)
        clean = re.sub(r"http\S+", "", clean)[:500].strip()
        if not clean:
            return False

        def _worker():
            try:
                import edge_tts
                import pygame
                self.is_playing = True
                if on_start:
                    on_start()

                out_file = Path(tempfile.gettempdir()) / f"saathi_tts_{int(time.time())}.mp3"
                asyncio.run(edge_tts.Communicate(clean, self.voice).save(str(out_file)))

                if self._stop_requested.is_set():
                    self.is_playing = False
                    return

                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                pygame.mixer.music.load(str(out_file))
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy() and not self._stop_requested.is_set():
                    # Emit procedural speaking amplitude for visualizer
                    if self.on_amplitude_callback:
                        import random
                        self.on_amplitude_callback(random.uniform(0.35, 0.95))
                    time.sleep(0.08)

                if self.on_amplitude_callback:
                    self.on_amplitude_callback(0.0)

            except Exception:
                pass
            finally:
                self.is_playing = False
                self.last_speech_finish_time = time.time()
                if on_finish:
                    on_finish()

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        return True
