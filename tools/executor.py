import json
import time
from typing import Any, Dict, Optional, Callable
from .registry import ToolRegistry
from .permissions import PermissionManager
from .schemas import RiskLevel

class ToolExecutor:
    def __init__(self, registry: ToolRegistry, permissions: PermissionManager, confirmation_dialog: Optional[Callable] = None):
        self.registry = registry
        self.permissions = permissions
        self.confirmation_dialog = confirmation_dialog

    def execute(self, name: str, args: Any, context: Optional[Dict[str, Any]] = None) -> str:
        tool = self.registry.get(name)
        if not tool:
            return f"Error: Tool '{name}' not found."

        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {}
        if not isinstance(args, dict):
            args = {}

        # Check permissions
        authorized = self.permissions.check_permission(
            tool_name=name,
            risk_level=tool.risk_level,
            ask_callback=self.confirmation_dialog
        )
        if not authorized:
            return f"Action cancelled: Permission for '{name}' was not granted."

        try:
            start_t = time.time()
            res = tool.run(args, context or {})
            elapsed = round(time.time() - start_t, 2)
            return str(res)
        except Exception as err:
            return f"Error executing {name}: {err}"
