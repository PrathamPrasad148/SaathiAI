from pathlib import Path
from typing import List, Dict, Any, Optional
from .models import UserProfile, ProjectMemory, FactMemory
from .storage import MemoryStorage

class MemoryEngine:
    def __init__(self, data_file: Optional[Path] = None):
        if data_file is None:
            data_file = Path(__file__).resolve().parent.parent / 'data' / 'memory.json'
        self.storage = MemoryStorage(data_file)
        self.profile = UserProfile()
        self.projects: List[ProjectMemory] = []
        self.facts: List[FactMemory] = []
        self.conversation_context: str = ''
        self.load()

    def load(self):
        data = self.storage.load()
        if data.get('profile'):
            self.profile = UserProfile.from_dict(data['profile'])
        self.projects = [ProjectMemory.from_dict(p) for p in data.get('projects', [])]
        self.facts = [FactMemory.from_dict(f) for f in data.get('facts', [])]
        self.conversation_context = data.get('context', '')

    def save(self):
        data = {
            'profile': self.profile.to_dict(),
            'projects': [p.to_dict() for p in self.projects],
            'facts': [f.to_dict() for f in self.facts],
            'context': self.conversation_context
        }
        self.storage.save(data)

    def store_fact(self, key: str, value: str, category: str = 'general') -> FactMemory:
        for f in self.facts:
            if f.key.lower() == key.lower():
                f.value = value
                f.category = category
                self.save()
                return f
        new_fact = FactMemory(key=key, value=value, category=category)
        self.facts.append(new_fact)
        self.save()
        return new_fact

    def get_fact(self, key: str) -> Optional[str]:
        for f in self.facts:
            if f.key.lower() == key.lower():
                return f.value
        return None

    def search_facts(self, query: str) -> List[FactMemory]:
        q = query.lower()
        return [f for f in self.facts if q in f.key.lower() or q in f.value.lower() or q in f.category.lower()]

    def delete_fact(self, fact_id: str) -> bool:
        before = len(self.facts)
        self.facts = [f for f in self.facts if f.id != fact_id]
        if len(self.facts) < before:
            self.save()
            return True
        return False

    def add_project(self, name: str, path: str, tech_stack: str = '', notes: str = '') -> ProjectMemory:
        for p in self.projects:
            if p.name.lower() == name.lower() or p.path == path:
                p.path = path
                p.tech_stack = tech_stack
                p.notes = notes
                self.save()
                return p
        proj = ProjectMemory(name=name, path=path, tech_stack=tech_stack, notes=notes)
        self.projects.append(proj)
        self.save()
        return proj

    def get_projects(self) -> List[ProjectMemory]:
        return list(self.projects)

    def delete_project(self, project_id: str) -> bool:
        before = len(self.projects)
        self.projects = [p for p in self.projects if p.id != project_id]
        if len(self.projects) < before:
            self.save()
            return True
        return False

    def get_context_for_prompt(self) -> str:
        lines = []
        if self.profile.name:
            lines.append(f'User: {self.profile.name}')
        if self.facts:
            lines.append('Known Facts & Memory:')
            for f in self.facts[:12]:
                lines.append(f'  - {f.key}: {f.value}')
        if self.projects:
            lines.append('Active Projects:')
            for p in self.projects[:5]:
                lines.append(f'  - {p.name} ({p.path}) [{p.tech_stack}]')
        return '\n'.join(lines)

    def clear_all(self):
        self.facts.clear()
        self.projects.clear()
        self.conversation_context = ''
        self.save()
