import json
from pathlib import Path
from typing import Dict
from .schemas import RiskLevel

class PermissionAction:
    ALWAYS_ALLOW = "always_allow"
    ASK_ONCE = "ask_once"
    ASK_EVERY_TIME = "ask_every_time"
    BLOCK = "block"

class PermissionManager:
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.rules: Dict[str, str] = {}
        self.session_authorized = set()
        self.load()

    def load(self):
        try:
            if self.config_file.exists():
                self.rules = json.loads(self.config_file.read_text(encoding="utf-8"))
            else:
                self._init_defaults()
        except Exception:
            self._init_defaults()

    def _init_defaults(self):
        # Default authorized configuration: routine safe actions are permitted
        self.rules = {
            "create_file": PermissionAction.ALWAYS_ALLOW,
            "read_file": PermissionAction.ALWAYS_ALLOW,
            "list_directory": PermissionAction.ALWAYS_ALLOW,
            "open_target": PermissionAction.ALWAYS_ALLOW,
            "get_weather": PermissionAction.ALWAYS_ALLOW,
            "get_currency": PermissionAction.ALWAYS_ALLOW,
            "get_wikipedia": PermissionAction.ALWAYS_ALLOW,
            "add_reminder": PermissionAction.ALWAYS_ALLOW,
            "add_note": PermissionAction.ALWAYS_ALLOW,
            "take_screenshot": PermissionAction.ALWAYS_ALLOW,
            "system_info": PermissionAction.ALWAYS_ALLOW,
            "read_screen_text": PermissionAction.ALWAYS_ALLOW,
            "search_files": PermissionAction.ALWAYS_ALLOW,
            "manage_memory": PermissionAction.ALWAYS_ALLOW,
            "run_automation": PermissionAction.ALWAYS_ALLOW,
            "delete_file_safely": PermissionAction.ASK_ONCE,
            "run_command": PermissionAction.ASK_ONCE,
            "kill_process": PermissionAction.ASK_EVERY_TIME
        }
        self.save()

    def save(self):
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config_file.write_text(json.dumps(self.rules, indent=2), encoding="utf-8")
        except OSError:
            pass

    def check_permission(self, tool_name: str, risk_level: RiskLevel, ask_callback=None) -> bool:
        rule = self.rules.get(tool_name)
        if not rule:
            rule = PermissionAction.ALWAYS_ALLOW if risk_level == RiskLevel.LOW else PermissionAction.ASK_ONCE

        if rule == PermissionAction.ALWAYS_ALLOW:
            return True
        if rule == PermissionAction.BLOCK:
            return False
        if rule == PermissionAction.ASK_ONCE:
            if tool_name in self.session_authorized:
                return True
            if ask_callback:
                approved = ask_callback(tool_name)
                if approved:
                    self.session_authorized.add(tool_name)
                return approved
            return False
        if rule == PermissionAction.ASK_EVERY_TIME:
            if ask_callback:
                return ask_callback(tool_name)
            return False
        return True
