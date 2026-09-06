from typing import Optional, List
from .models import AutomationWorkflow

class TriggerMatcher:
    @staticmethod
    def match_voice_trigger(text: str, workflows: List[AutomationWorkflow]) -> Optional[AutomationWorkflow]:
        lowered = text.lower().strip()
        for wf in workflows:
            if not wf.enabled:
                continue
            if wf.trigger_type in ('voice_phrase', 'manual'):
                trigger = wf.trigger_value.lower().strip()
                if trigger and (trigger in lowered or lowered in trigger):
                    return wf
                name_lowered = wf.name.lower().strip()
                if name_lowered and (name_lowered in lowered):
                    return wf
        return None
