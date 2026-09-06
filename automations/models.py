from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

@dataclass
class AutomationStep:
    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    description: str = ''
    continue_on_error: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AutomationStep':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class AutomationWorkflow:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ''
    description: str = ''
    trigger_type: str = 'manual'  # manual, voice_phrase, startup
    trigger_value: str = ''       # e.g. 'dev mode', 'start studying'
    steps: List[AutomationStep] = field(default_factory=list)
    enabled: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_run: Optional[str] = None
    run_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['steps'] = [s.to_dict() if hasattr(s, 'to_dict') else s for s in self.steps]
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AutomationWorkflow':
        steps_data = data.pop('steps', [])
        steps = [AutomationStep.from_dict(s) if isinstance(s, dict) else s for s in steps_data]
        valid_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(steps=steps, **valid_fields)
