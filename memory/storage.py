import json
import threading
from pathlib import Path
from typing import Dict, Any

class MemoryStorage:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.lock = threading.RLock()
        self._ensure_file()

    def _ensure_file(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            default_data = {
                'profile': {},
                'projects': [],
                'facts': [],
                'context': ''
            }
            self.save(default_data)

    def load(self) -> Dict[str, Any]:
        with self.lock:
            try:
                if self.file_path.exists():
                    return json.loads(self.file_path.read_text(encoding='utf-8'))
            except (OSError, json.JSONDecodeError):
                pass
            return {'profile': {}, 'projects': [], 'facts': [], 'context': ''}

    def save(self, data: Dict[str, Any]) -> bool:
        with self.lock:
            try:
                self.file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
                return True
            except OSError:
                return False
