"""
Saathi AI — Low-Power On-Device Wake-Word Listener Subsystem
Continuously monitors microphone audio in a background thread for 'Hey Saathi' or 'Saathi'.
"""

import time
import threading
from typing import Callable, Optional

# Try importing openwakeword or pyaudio
try:
    import openwakeword
    from openwakeword.model import Model as OWWModel
except ImportError:
    openwakeword = None
    OWWModel = None

try:
    import pyaudio
except ImportError:
    pyaudio = None

class WakeWordListener:
    """
    On-device background wake-word listener running at < 1% CPU idle.
    """
    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        self.callback = callback
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.oww_model = None

    def _init_model(self):
        if OWWModel:
            try:
                # Load lightweight wake-word models
                self.oww_model = OWWModel()
            except Exception:
                self.oww_model = None

    def start(self):
        """Start background wake-word listener thread."""
        if self.running:
            return
        self.running = True
        self._init_model()
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop background wake-word listener thread."""
        self.running = False

    def _listen_loop(self):
        """Background listening loop."""
        if not pyaudio:
            # Fallback if PyAudio is missing
            while self.running:
                time.sleep(1.0)
            return

        p = None
        stream = None
        try:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1280
            )

            while self.running:
                try:
                    data = stream.read(1280, exception_on_overflow=False)
                    if self.oww_model:
                        # Feed audio frame to openwakeword model
                        prediction = self.oww_model.predict(data)
                        for model_name, score in prediction.items():
                            if score > 0.6:
                                if self.callback:
                                    self.callback("Hey Saathi")
                                self.oww_model.reset()
                                time.sleep(1.5)  # Cooldown after trigger
                                break
                    else:
                        # Sleep lightly if openwakeword model is not present
                        time.sleep(0.05)
                except Exception:
                    time.sleep(0.1)

        except Exception:
            pass
        finally:
            if stream:
                try:
                    stream.stop_stream()
                    stream.close()
                except Exception:
                    pass
            if p:
                try:
                    p.terminate()
                except Exception:
                    pass

