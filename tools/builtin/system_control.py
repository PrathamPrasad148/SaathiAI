from typing import Dict, Any, List
from ..schemas import Tool, RiskLevel
from automation.mouse import get_cursor_pos, move_mouse, click_mouse, double_click, scroll_mouse
from automation.keyboard import type_text, send_hotkey
from automation.windows import list_open_windows, focus_window_by_title, minimize_all_windows, close_window_by_title
from automation.processes import list_running_processes, kill_process, kill_process_by_name
from automation.clipboard import get_clipboard_text, set_clipboard_text
from automation.hardware import (
    toggle_volume_mute, volume_up, volume_down,
    media_play_pause, media_next, media_prev, media_stop,
    lock_workstation, empty_recycle_bin, sleep_workstation,
    restart_workstation, shutdown_workstation, abort_shutdown,
    get_display_brightness, set_display_brightness,
    increase_display_brightness, decrease_display_brightness,
    take_screen_snapshot
)

def get_system_control_tools() -> List[Tool]:
    """Exposes native Windows desktop GUI, audio, process, and system controls to Saathi."""

    # 1. Mouse Control
    def mouse_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "get_position").lower().strip()
        x = args.get("x")
        y = args.get("y")
        button = args.get("button", "left").lower().strip()
        clicks = int(args.get("clicks", 1))

        if action == "get_position":
            cur_x, cur_y = get_cursor_pos()
            return f"Current cursor position: X={cur_x}, Y={cur_y}"
        elif action == "move":
            if x is None or y is None:
                return "Error: x and y coordinates are required to move cursor."
            move_mouse(int(x), int(y))
            return f"Cursor moved to ({x}, {y})."
        elif action == "click":
            click_mouse(int(x) if x is not None else None, int(y) if y is not None else None, button=button)
            return f"Mouse {button}-clicked at ({x or 'current'}, {y or 'current'})."
        elif action == "double_click":
            double_click(int(x) if x is not None else None, int(y) if y is not None else None)
            return f"Mouse double-clicked at ({x or 'current'}, {y or 'current'})."
        elif action == "scroll":
            clicks_val = int(args.get("clicks", -3))
            scroll_mouse(clicks_val)
            return f"Scrolled mouse by {clicks_val} clicks."
        return f"Unknown mouse action: {action}"

    # 2. Keyboard Control
    def keyboard_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "type").lower().strip()
        text = args.get("text", "")
        keys = args.get("keys", [])

        if action == "type":
            if not text:
                return "Error: text parameter is required for typing."
            type_text(text)
            return f"Typed text: '{text[:60]}...'"
        elif action == "hotkey":
            if isinstance(keys, str):
                keys = [k.strip() for k in keys.split("+")]
            if not keys:
                return "Error: keys parameter is required for hotkey (e.g. ['ctrl', 'c'] or 'ctrl+c')."
            send_hotkey(*keys)
            return f"Sent hotkey combination: {' + '.join(keys)}"
        return f"Unknown keyboard action: {action}"

    # 3. Window Control
    def window_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "list").lower().strip()
        title = args.get("title", "").strip()

        if action == "list":
            wins = list_open_windows()
            if not wins:
                return "No open user windows detected."
            lines = [f"• {w['title']}" for w in wins[:15]]
            return f"Active Windows ({len(wins)} total):\n" + "\n".join(lines)
        elif action == "focus":
            if not title:
                return "Error: title parameter is required to focus a window."
            ok = focus_window_by_title(title)
            return f"Window '{title}' focused successfully." if ok else f"Window matching '{title}' was not found."
        elif action == "minimize_all":
            minimize_all_windows()
            return "All windows minimized (Desktop visible)."
        elif action == "close":
            if not title:
                return "Error: title parameter is required to close a window."
            ok = close_window_by_title(title)
            return f"Sent close signal to window '{title}'." if ok else f"Window matching '{title}' was not found."
        return f"Unknown window action: {action}"

    # 4. Audio Control
    def audio_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "toggle_mute").lower().strip()
        steps = int(args.get("steps", 5))

        if action in ("mute", "unmute", "toggle_mute"):
            toggle_volume_mute()
            return "System audio mute toggled."
        elif action == "volume_up":
            volume_up(steps)
            return f"System volume increased by {steps} steps."
        elif action == "volume_down":
            volume_down(steps)
            return f"System volume decreased by {steps} steps."
        return f"Unknown audio action: {action}"

    # 5. Media Control
    def media_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "play_pause").lower().strip()
        if action in ("play", "pause", "play_pause"):
            media_play_pause()
            return "Toggled media play/pause."
        elif action == "next":
            media_next()
            return "Skipped to next media track."
        elif action in ("prev", "previous"):
            media_prev()
            return "Returned to previous media track."
        elif action == "stop":
            media_stop()
            return "Media playback stopped."
        return f"Unknown media action: {action}"

    # 6. Power Control
    def power_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "lock").lower().strip()
        if action == "lock":
            lock_workstation()
            return "Workstation locked."
        elif action == "empty_recycle_bin":
            empty_recycle_bin()
            return "Recycle bin emptied."
        elif action == "sleep":
            sleep_workstation()
            return "System sleep initiated."
        elif action == "restart":
            restart_workstation(10)
            return "Computer restart scheduled in 10 seconds. Use power_control action='abort' to cancel."
        elif action == "shutdown":
            shutdown_workstation(15)
            return "Computer shutdown scheduled in 15 seconds. Use power_control action='abort' to cancel."
        elif action == "abort":
            abort_shutdown()
            return "Scheduled shutdown/restart cancelled."
        return f"Unknown power action: {action}"

    # 7. Process Control
    def process_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "list").lower().strip()
        target = args.get("target", "")

        if action == "list":
            procs = list_running_processes(15)
            lines = [f"• PID {p['pid']:5d} | {p['name'][:22]:24} | RAM: {p['ram']}% | CPU: {p['cpu']}%" for p in procs]
            return "Top Processes by RAM:\n" + "\n".join(lines)
        elif action == "kill":
            if not target:
                return "Error: target parameter (PID number or process name like 'notepad.exe') is required."
            if str(target).isdigit():
                ok = kill_process(int(target))
                return f"Terminated process PID {target}." if ok else f"Could not terminate PID {target}."
            else:
                count = kill_process_by_name(str(target))
                return f"Terminated {count} process instance(s) matching '{target}'." if count > 0 else f"No running processes found matching '{target}'."
        return f"Unknown process action: {action}"

    # 8. Clipboard Control
    def clipboard_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "read").lower().strip()
        text = args.get("text", "")

        if action == "read":
            content = get_clipboard_text()
            return f"Clipboard Content:\n{content}" if content else "Clipboard is empty or non-text."
        elif action == "write":
            ok = set_clipboard_text(text)
            return f"Copied text to clipboard ({len(text)} characters)." if ok else "Could not set clipboard."
        return f"Unknown clipboard action: {action}"

    # 9. Display Control
    def display_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "get").lower().strip()
        level = args.get("level")

        if action == "get":
            val = get_display_brightness()
            return f"Current display brightness: {val}%"
        elif action == "set":
            if level is None:
                return "Error: level (0..100) is required for setting brightness."
            set_display_brightness(int(level))
            return f"Display brightness set to {level}%."
        elif action == "increase":
            step = int(level or 15)
            val = increase_display_brightness(step)
            return f"Display brightness increased to {val}%."
        elif action == "decrease":
            step = int(level or 15)
            val = decrease_display_brightness(step)
            return f"Display brightness decreased to {val}%."
        return f"Unknown display action: {action}"

    # 10. Screenshot Tool
    def screenshot_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        path = args.get("target_path")
        saved_path = take_screen_snapshot(path)
        return f"Screenshot saved to {saved_path}."

    return [
        Tool(
            name="mouse_control",
            category="system",
            description="Move mouse cursor, click (left/right/double), scroll, or query current position.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["move", "click", "double_click", "scroll", "get_position"], "description": "Mouse action to perform"},
                    "x": {"type": "integer", "description": "Target X screen coordinate"},
                    "y": {"type": "integer", "description": "Target Y screen coordinate"},
                    "button": {"type": "string", "enum": ["left", "right"], "description": "Mouse button for clicks"},
                    "clicks": {"type": "integer", "description": "Number of scroll clicks (positive=up, negative=down)"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.MEDIUM,
            run=mouse_run
        ),
        Tool(
            name="keyboard_control",
            category="system",
            description="Type arbitrary text or inject keyboard shortcut combinations (e.g. ctrl+c, alt+tab, win+d).",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["type", "hotkey"], "description": "Type text or press hotkey"},
                    "text": {"type": "string", "description": "Text to type into active window"},
                    "keys": {"type": "array", "items": {"type": "string"}, "description": "Keys for hotkey combo (e.g. ['win', 'd'], ['alt', 'tab'])"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.MEDIUM,
            run=keyboard_run
        ),
        Tool(
            name="window_control",
            category="system",
            description="Inspect open application windows, bring a window to the foreground, minimize all, or close a window.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["list", "focus", "minimize_all", "close"], "description": "Window action to take"},
                    "title": {"type": "string", "description": "Target window title substring to focus or close"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.LOW,
            run=window_run
        ),
        Tool(
            name="audio_control",
            category="system",
            description="Control host system audio volume: mute, unmute, volume up, volume down.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["mute", "unmute", "toggle_mute", "volume_up", "volume_down"], "description": "Audio action"},
                    "steps": {"type": "integer", "description": "Number of volume steps to change (default: 5)"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.LOW,
            run=audio_run
        ),
        Tool(
            name="media_control",
            category="system",
            description="Control media playback on Windows: play/pause, next track, previous track, stop.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["play_pause", "next", "prev", "stop"], "description": "Media action"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.LOW,
            run=media_run
        ),
        Tool(
            name="power_control",
            category="system",
            description="Execute system power operations: lock PC, empty recycle bin, sleep, restart, shutdown, or abort shutdown.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["lock", "empty_recycle_bin", "sleep", "restart", "shutdown", "abort"], "description": "Power action"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.HIGH,
            run=power_run
        ),
        Tool(
            name="process_control",
            category="system",
            description="List running computer processes or terminate a process by PID or name.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["list", "kill"], "description": "Process action to execute"},
                    "target": {"type": "string", "description": "PID integer or process name string (e.g. 'notepad.exe') to terminate"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.HIGH,
            run=process_run
        ),
        Tool(
            name="clipboard_control",
            category="system",
            description="Read text from or write text to the Windows system clipboard.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["read", "write"], "description": "Clipboard action"},
                    "text": {"type": "string", "description": "Text to write to clipboard"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.LOW,
            run=clipboard_run
        ),
        Tool(
            name="display_control",
            category="system",
            description="Query or adjust host screen brightness level.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["get", "set", "increase", "decrease"], "description": "Display action"},
                    "level": {"type": "integer", "description": "Brightness percentage (0..100) or step amount"}
                },
                "required": ["action"]
            },
            risk_level=RiskLevel.LOW,
            run=display_run
        ),
        Tool(
            name="screenshot_tool",
            category="system",
            description="Capture a full desktop screenshot and save to disk.",
            parameters={
                "type": "object",
                "properties": {
                    "target_path": {"type": "string", "description": "Optional destination file path"}
                }
            },
            risk_level=RiskLevel.LOW,
            run=screenshot_run
        )
    ]

