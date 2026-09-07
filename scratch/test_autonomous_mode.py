import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.permissions import PermissionManager, PermissionAction
from tools.registry import ToolRegistry
from tools.executor import ToolExecutor
from tools.schemas import RiskLevel
from tools.builtin import register_all_builtin_tools

def test():
    pm = PermissionManager(Path("data/permissions.json"))
    print(f"Master System Control: {pm.master_system_control}")
    assert pm.master_system_control == True, "Master system control should be True!"

    reg = ToolRegistry()
    executor = ToolExecutor(registry=reg, permissions=pm)

    # Test permissions for high-risk actions
    for tool_name in ["run_command", "kill_process", "mouse_control", "keyboard_control", "power_control", "delete_file_safely", "click_screen_text"]:
        allowed = pm.check_permission(tool_name, RiskLevel.HIGH)
        print(f"Permission check for '{tool_name}': {allowed}")
        assert allowed == True, f"{tool_name} should be allowed!"

    print("ALL AUTONOMOUS PERMISSION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    test()

