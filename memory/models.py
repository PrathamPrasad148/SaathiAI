from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

@dataclass
class UserProfile:
    name: str = 'Boss'
    language_style: str = 'Hinglish'
    preferred_model: str = 'Auto (Smart Agent)'
    preferred_editor: str = 'VS Code'
    coding_preferences: Dict[str, Any] = field(default_factory=lambda: {
        'style': 'modern clean',
        'frameworks': ['html5', 'react', 'python', 'tailwind'],
        'auto_open_browser': True
    })

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class ProjectMemory:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ''
    path: str = ''
    tech_stack: str = ''
    notes: str = ''
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_accessed: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectMemory':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class FactMemory:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    category: str = 'general'  # general, tech, preference, workflow
    key: str = ''
    value: str = ''
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FactMemory':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
