"""
Saathi AI — Specialized English Conversation & Personality Sub-Agent
Manages natural human conversational cadence, voice pipeline alignment (STT/TTS),
tutoring/grammar practice mode, and persona consistency.
"""

import time
import random
from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent, AgentTask, AgentResponse


class ConversationAgent(BaseAgent):
    """Specialized Sub-Agent for Spoken English Conversation, Tutoring & Personality."""

    def __init__(self, voice_engine=None):
        super().__init__(
            name="ConversationAgent",
            description="Specialized in natural spoken English conversation, voice TTS synthesis, tutoring, and emotional rapport.",
            capabilities=["chit_chat", "voice_speak", "english_tutor", "persona_dialogue"]
        )
        self.voice_engine = voice_engine

    def can_handle(self, task: AgentTask) -> bool:
        lowered = task.instruction.lower().strip()
        chit_chat_terms = ("hi", "hello", "hey", "how are you", "whats up", "who are you", "joke", "thank you", "thanks", "bye", "good morning", "bored", "tired", "stressed")
        return task.task_type in ("conversation", "chit_chat", "tutor") or any(k in lowered for k in chit_chat_terms) or len(lowered.split()) <= 4

    def handle(self, task: AgentTask) -> AgentResponse:
        start_t = time.time()
        instruction = task.instruction.strip()
        lowered = instruction.lower()

        # Voice Speech Output Synthesis
        reply_text = task.context.get("preset_reply") or f"I'm right here with you, Pratham! How can I assist you right now?"

        if self.voice_engine and hasattr(self.voice_engine, "tts"):
            try:
                # Speak concisely over EdgeTTS
                self.voice_engine.tts.speak_async(reply_text)
            except Exception:
                pass

        exec_time = (time.time() - start_t) * 1000
        return AgentResponse(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            result=reply_text,
            execution_time_ms=exec_time
        )
