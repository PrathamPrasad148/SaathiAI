import threading
import time
from typing import Optional, Callable
import numpy as np
from .vad import EnergyVAD
from .audio_analyzer import AudioAnalyzer
from .stt import STTEngine
from .tts import TTSEngine

class VoiceEngine:
    """Non-blocking voice pipeline with real-time mic streaming, VAD, Whisper STT, and Edge TTS."""
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.vad = EnergyVAD()
        self.analyzer = AudioAnalyzer()
        self.stt = STTEngine()
        self.tts = TTSEngine()

        self.is_listening = False
        self._stop_stream = threading.Event()
        self._audio_buffer = []
        self._stream_thread = None

        self.on_audio_level: Optional[Callable[[float], None]] = None
        self.on_transcription_complete: Optional[Callable[[str], None]] = None
        self.on_status_change: Optional[Callable[[str], None]] = None

    def start_listening(self):
        if self.is_listening:
            return
        self.is_listening = True
        self._stop_stream.clear()
        self._audio_buffer = []
        self.vad.reset()
        if self.on_status_change:
            self.on_status_change("LISTENING")

        self._stream_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._stream_thread.start()

    def stop_listening(self):
        self.is_listening = False
        self._stop_stream.set()
        if self.on_audio_level:
            self.on_audio_level(0.0)

    def _listen_loop(self):
        try:
            import sounddevice as sd
            block_size = 1024
            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32", blocksize=block_size) as stream:
                speech_detected = False
                silence_frames = 0
                max_silence_after_speech = int(self.sample_rate / block_size * 1.2)  # 1.2s of silence after speech

                while not self._stop_stream.is_set() and self.is_listening:
                    data, overflowed = stream.read(block_size)
                    chunk = data.flatten()
                    analysis = self.analyzer.analyze(chunk)
                    
                    if self.on_audio_level:
                        self.on_audio_level(analysis["rms"])

                    if analysis["active"]:
                        speech_detected = True
                        silence_frames = 0
                        self._audio_buffer.append(chunk)
                    elif speech_detected:
                        self._audio_buffer.append(chunk)
                        silence_frames += 1
                        if silence_frames >= max_silence_after_speech:
                            break  # Automatic end of utterance!
                    else:
                        # Keep a sliding window of recent background audio (0.3s)
                        if len(self._audio_buffer) > 5:
                            self._audio_buffer.pop(0)
                        self._audio_buffer.append(chunk)

            self.stop_listening()

            if speech_detected and self._audio_buffer:
                if self.on_status_change:
                    self.on_status_change("TRANSCRIBING")
                audio_full = np.concatenate(self._audio_buffer)
                text = self.stt.transcribe(audio_full)
                if self.on_transcription_complete and text:
                    self.on_transcription_complete(text)
                elif self.on_status_change:
                    self.on_status_change("IDLE")
            else:
                if self.on_status_change:
                    self.on_status_change("IDLE")

        except Exception as err:
            self.stop_listening()
            if self.on_status_change:
                self.on_status_change("IDLE")
