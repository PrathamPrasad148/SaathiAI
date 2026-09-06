import threading
import time
from typing import Optional, Callable
import numpy as np
from .vad import EnergyVAD
from .audio_analyzer import AudioAnalyzer
from .stt import STTEngine
from .tts import TTSEngine

class VoiceEngine:
    """
    Non-blocking continuous voice pipeline with real-time mic streaming,
    VAD, low-latency Whisper STT, acoustic echo suppression, and Edge TTS.
    """
    def __init__(self, sample_rate: int = 16000, continuous_mode: bool = True):
        self.sample_rate = sample_rate
        self.continuous_mode = continuous_mode
        self.vad = EnergyVAD()
        self.analyzer = AudioAnalyzer()
        self.stt = STTEngine()
        self.tts = TTSEngine()

        self.is_listening = False
        self._stop_stream = threading.Event()
        self._audio_buffer = []
        self._stream_thread = None
        self._is_transcribing = False

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
        if self.on_status_change:
            self.on_status_change("IDLE")

    def toggle_listening(self) -> bool:
        if self.is_listening:
            self.stop_listening()
            return False
        else:
            self.start_listening()
            return True

    def _listen_loop(self):
        try:
            import sounddevice as sd
            block_size = 1024
            # 0.40s of silence after speech indicates utterance completion (snappy turnaround)
            max_silence_after_speech = int(self.sample_rate / block_size * 0.40)

            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32", blocksize=block_size) as stream:
                speech_detected = False
                silence_frames = 0

                while not self._stop_stream.is_set() and self.is_listening:
                    data, overflowed = stream.read(block_size)
                    chunk = data.flatten()

                    # Acoustic Echo Suppression: Discard input while Saathi is speaking
                    if self.tts.is_speaking():
                        speech_detected = False
                        silence_frames = 0
                        self._audio_buffer = []
                        time.sleep(0.05)
                        continue

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

                        # Utterance complete
                        if silence_frames >= max_silence_after_speech:
                            audio_full = np.concatenate(self._audio_buffer)
                            self._audio_buffer = []
                            speech_detected = False
                            silence_frames = 0

                            # Process transcription in background worker
                            if len(audio_full) > self.sample_rate * 0.25:  # Minimum 0.25s speech
                                self._dispatch_transcription(audio_full)

                            if not self.continuous_mode:
                                break
                    else:
                        # Keep a small rolling window of ambient audio (0.25s)
                        if len(self._audio_buffer) > 5:
                            self._audio_buffer.pop(0)
                        self._audio_buffer.append(chunk)

        except Exception as err:
            print(f"[VOICE STREAM ERROR] {err}")
        finally:
            if not self.continuous_mode or self._stop_stream.is_set():
                self.is_listening = False
                if self.on_status_change:
                    self.on_status_change("IDLE")

    def _dispatch_transcription(self, audio_data: np.ndarray):
        """Asynchronously transcribe speech without blocking the audio stream."""
        def _worker():
            try:
                self._is_transcribing = True
                if self.on_status_change:
                    self.on_status_change("TRANSCRIBING")

                text = self.stt.transcribe(audio_data)
                cleaned = text.strip()
                if cleaned:
                    print(f"[VOICE HEARD] '{cleaned}'")
                    if self.on_transcription_complete:
                        self.on_transcription_complete(cleaned)
            except Exception as err:
                print(f"[TRANSCRIPTION EXCEPTION] {err}")
            finally:
                self._is_transcribing = False
                if self.is_listening and self.on_status_change:
                    self.on_status_change("LISTENING" if not self.tts.is_speaking() else "SPEAKING")

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
