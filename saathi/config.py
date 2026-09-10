"""
Saathi AI 2.0 — Central Configuration Manager
"""

import os
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
LOGS_DIR = DATA_DIR / "logs"
BACKUPS_DIR = APP_DIR / "backups"
PROJECTS_DIR = APP_DIR / "Projects"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class SecurityConfig:
    autonomy_level: int = 2  # Level 0 (chat) to 5 (highly autonomous)
    network_mode: str = "hybrid"  # offline, local, hybrid, online
    require_confirmation_high_risk: bool = True
    allowed_domains: List[str] = field(default_factory=lambda: [
        "wikipedia.org", "github.com", "python.org", "wttr.in", "arxiv.org"
    ])

@dataclass
class ModelConfig:
    primary_local_model: str = "saathi-distill-brain:latest"
    fallback_local_model: str = "qwen2.5-coder:7b"
    ollama_host: str = "http://localhost:11434"
    timeout_seconds: int = 120

@dataclass
class SystemConfig:
    app_dir: Path = APP_DIR
    data_dir: Path = DATA_DIR
    logs_dir: Path = LOGS_DIR
    backups_dir: Path = BACKUPS_DIR
    projects_dir: Path = PROJECTS_DIR
    security: SecurityConfig = field(default_factory=SecurityConfig)
    models: ModelConfig = field(default_factory=ModelConfig)

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "SystemConfig":
        cfg_file = config_path or (DATA_DIR / "config.json")
        if cfg_file.exists():
            try:
                data = json.loads(cfg_file.read_text(encoding="utf-8"))
                sec = SecurityConfig(**data.get("security", {}))
                mod = ModelConfig(**data.get("models", {}))
                return cls(security=sec, models=mod)
            except Exception:
                pass
        return cls()

    def save(self, config_path: Optional[Path] = None) -> None:
        cfg_file = config_path or (DATA_DIR / "config.json")
        data = {
            "security": {
                "autonomy_level": self.security.autonomy_level,
                "network_mode": self.security.network_mode,
                "require_confirmation_high_risk": self.security.require_confirmation_high_risk,
                "allowed_domains": self.security.allowed_domains
            },
            "models": {
                "primary_local_model": self.models.primary_local_model,
                "fallback_local_model": self.models.fallback_local_model,
                "ollama_host": self.models.ollama_host,
                "timeout_seconds": self.models.timeout_seconds
            }
        }
        cfg_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

config = SystemConfig.load()

