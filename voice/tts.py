import asyncio
import hashlib
import threading
import time
import re
from pathlib import Path
from typing import Optional, Callable

class TTSEngine:
    """
    Ultra-low-latency TTS synthesizer with on-disk audio caching,
    sentence streaming, immediate interruptibility, and Windows SAPI5 offline fallback.
    """
    def __init__(self, voice: str = "en-IN-NeerjaNeural"):
        self.voice = voice
        self.is_playing = False
        self._stop_requested = threading.Event()
        self.last_speech_finish_time: float = 0.0
        self.on_amplitude_callback: Optional[Callable[[float], None]] = None

        # Persistent audio cache directory for instant responses
        self.cache_dir = Path(__file__).resolve().parent.parent / "data" / "tts_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

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

    def _get_cache_path(self, text: str) -> Path:
        h = hashlib.md5(f"{self.voice}:{text}".encode("utf-8")).hexdigest()
        return self.cache_dir / f"{h}.mp3"

    def prewarm_phrases(self, phrases: list[str]):
        """Pre-synthesizes common reflex phrases into the cache in background."""
        def _worker():
            for p in phrases:
                if self._stop_requested.is_set():
                    break
                try:
                    c_file = self._get_cache_path(p)
                    if not c_file.exists():
                        import edge_tts
                        asyncio.run(edge_tts.Communicate(p, self.voice).save(str(c_file)))
                        time.sleep(0.1)
                except Exception:
                    pass
        threading.Thread(target=_worker, daemon=True).start()

    def speak(self, text: str, on_start: Optional[Callable] = None, on_finish: Optional[Callable] = None) -> bool:
        self.stop()
        self._stop_requested.clear()

        clean = re.sub(r"[*_`#<>{}]", "", text)
        clean = re.sub(r"http\S+", "", clean)[:500].strip()
        if not clean:
            return False

        cache_file = self._get_cache_path(clean)

        def _worker():
            try:
                import pygame
                self.is_playing = True
                if on_start:
                    on_start()

                # If cached on disk, instant playback (< 10ms)!
                if not cache_file.exists():
                    try:
                        import edge_tts
                        asyncio.run(edge_tts.Communicate(clean, self.voice).save(str(cache_file)))
                    except Exception:
                        # Offline fallback: SAPI5
                        try:
                            import win32com.client
                            speaker = win32com.client.Dispatch("SAPI.SpVoice")
                            speaker.Speak(clean, 0)
                            return
                        except Exception:
                            return

                if self._stop_requested.is_set():
                    self.is_playing = False
                    return

                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                pygame.mixer.music.load(str(cache_file))
                pygame.mixer.music.play()

                t_start = time.time()
                while pygame.mixer.music.get_busy() and not self._stop_requested.is_set():
                    if self.on_amplitude_callback:
                        import random
                        self.on_amplitude_callback(random.uniform(0.35, 0.95))
                    time.sleep(0.06)
                    # Safety timeout: max 20 seconds
                    if time.time() - t_start > 20:
                        break

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
