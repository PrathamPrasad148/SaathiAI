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
    """
    Manages security policy and Master Full System Control authorization for Saathi AI.
    When master_system_control is True, Saathi operates with complete sovereign autonomy
    over system tools, mouse, keyboard, and commands with zero repeated prompts.
    """
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.rules: Dict[str, str] = {}
        self.session_authorized = set()
        self.master_system_control: bool = False
        self._listeners: list = []
        self.load()

    def add_listener(self, callback):
        """Register a callback that receives (is_authorized: bool) when master control changes."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def _notify_listeners(self):
        for cb in self._listeners:
            try:
                cb(self.master_system_control)
            except Exception:
                pass

    def authorize_master_control(self, persist: bool = True):
        """Grant Saathi AI full, unrestricted system control."""
        self.master_system_control = True
        self.save(persist=persist)
        self._notify_listeners()

    def revoke_master_control(self, persist: bool = True):
        """Revoke full system control and return to safe restricted mode."""
        self.master_system_control = False
        self.save(persist=persist)
        self._notify_listeners()

    def toggle_master_control(self, persist: bool = True) -> bool:
        if self.master_system_control:
            self.revoke_master_control(persist=persist)
        else:
            self.authorize_master_control(persist=persist)
        return self.master_system_control

    def load(self):
        try:
            if self.config_file.exists():
                data = json.loads(self.config_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    self.master_system_control = bool(data.get("master_system_control", False))
                    self.rules = data.get("rules", data)
                else:
                    self._init_defaults()
            else:
                self._init_defaults()
        except Exception:
            self._init_defaults()

    def _init_defaults(self):
        self.master_system_control = False
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
            "click_screen_text": PermissionAction.ALWAYS_ALLOW,
            "search_files": PermissionAction.ALWAYS_ALLOW,
            "manage_memory": PermissionAction.ALWAYS_ALLOW,
            "run_automation": PermissionAction.ALWAYS_ALLOW,
            "delete_file_safely": PermissionAction.ALWAYS_ALLOW,
            "run_command": PermissionAction.ALWAYS_ALLOW,
            "kill_process": PermissionAction.ALWAYS_ALLOW,
            "mouse_control": PermissionAction.ALWAYS_ALLOW,
            "keyboard_control": PermissionAction.ALWAYS_ALLOW,
            "window_control": PermissionAction.ALWAYS_ALLOW,
            "audio_control": PermissionAction.ALWAYS_ALLOW,
            "media_control": PermissionAction.ALWAYS_ALLOW,
            "power_control": PermissionAction.ALWAYS_ALLOW,
            "process_control": PermissionAction.ALWAYS_ALLOW,
            "clipboard_control": PermissionAction.ALWAYS_ALLOW
        }
        self.save()

    def save(self, persist: bool = True):
        if not persist:
            return
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "master_system_control": self.master_system_control,
                "rules": self.rules
            }
            self.config_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except OSError:
            pass

    def check_permission(self, tool_name: str, risk_level: RiskLevel, ask_callback=None) -> bool:
        # If Master Full System Control is authorized, bypass ALL restrictions instantly!
        if self.master_system_control:
            return True

        rule = self.rules.get(tool_name)
        if not rule:
            rule = PermissionAction.ALWAYS_ALLOW if risk_level == RiskLevel.LOW else PermissionAction.ASK_ONCE

        if rule == PermissionAction.ALWAYS_ALLOW:
            return True
        if rule == PermissionAction.BLOCK:
            return False

        if rule in (PermissionAction.ASK_ONCE, PermissionAction.ASK_EVERY_TIME):
            if rule == PermissionAction.ASK_ONCE and tool_name in self.session_authorized:
                return True
            if ask_callback:
                # ask_callback can grant Master Control or single tool permission
                approved = ask_callback(tool_name)
                if approved:
                    self.session_authorized.add(tool_name)
                return approved
            return False

        return True
