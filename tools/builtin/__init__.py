from pathlib import Path
from ..registry import ToolRegistry
from ..schemas import Tool, RiskLevel
from .files import get_file_tools
from .system import get_system_tools
from .system_control import get_system_control_tools
from .web import get_web_tools
from .voice import get_voice_and_note_tools
from .vision import get_vision_tools
from .memory import get_memory_tools

def get_nextgen_tools() -> list[Tool]:
    from saathi.tools import (
        WebCmdTool, SelfEdifyTool, AcontextTool, ClawCodeTool,
        PonytailTool, DeepSeekHarnessTool, PrevJarvisTool
    )
    return [
        Tool(
            name="web_cmd", category="web",
            description="Interface with WebCmd browser session engine for deterministic web tasks and live extraction.",
            parameters={"type": "object", "properties": {"command": {"type": "string", "description": "WebCmd action or URL"}}, "required": ["command"]},
            risk_level=RiskLevel.MEDIUM, run=lambda command="help", **kwargs: WebCmdTool().execute(command=command, **kwargs)
        ),
        Tool(
            name="self_edify", category="ai",
            description="Recursive self-improvement, continuous self-reflection, and prompt optimization engine.",
            parameters={"type": "object", "properties": {"action": {"type": "string", "description": "Action ('status', 'reflect', 'optimize')"}}, "required": ["action"]},
            risk_level=RiskLevel.LOW, run=lambda action="status", **kwargs: SelfEdifyTool().execute(action=action, **kwargs)
        ),
        Tool(
            name="acontext", category="ai",
            description="Dynamic token context compression, memory indexing, and multi-turn state preservation.",
            parameters={"type": "object", "properties": {"action": {"type": "string", "description": "Action ('status', 'compress', 'index')"}}, "required": ["action"]},
            risk_level=RiskLevel.LOW, run=lambda action="status", **kwargs: AcontextTool().execute(action=action, **kwargs)
        ),
        Tool(
            name="claw_code", category="coding",
            description="Fast Rust-accelerated code parser, AST security sandbox verification, and multi-file code editing.",
            parameters={"type": "object", "properties": {"action": {"type": "string", "description": "Action ('status', 'parse', 'verify')"}}, "required": ["action"]},
            risk_level=RiskLevel.MEDIUM, run=lambda action="status", **kwargs: ClawCodeTool().execute(action=action, **kwargs)
        ),
        Tool(
            name="ponytail", category="orchestration",
            description="Autonomous multi-agent task orchestrator, goal breakdown graphs, and tool routing pipeline.",
            parameters={"type": "object", "properties": {"action": {"type": "string", "description": "Action ('status', 'decompose', 'route')"}}, "required": ["action"]},
            risk_level=RiskLevel.MEDIUM, run=lambda action="status", **kwargs: PonytailTool().execute(action=action, **kwargs)
        ),
        Tool(
            name="deepseek_harness", category="ai",
            description="Interface with DeepSeek Harness (dsh) plugin architecture and agent specifications.",
            parameters={"type": "object", "properties": {"action": {"type": "string", "description": "Action ('status', 'inspect', 'list_plugins')"}}, "required": ["action"]},
            risk_level=RiskLevel.MEDIUM, run=lambda action="status", **kwargs: DeepSeekHarnessTool().execute(action=action, **kwargs)
        ),
        Tool(
            name="prev_jarvis", category="system",
            description="Interface with PrevJarvis legacy core, desktop UI capabilities, and Rust acceleration modules.",
            parameters={"type": "object", "properties": {"action": {"type": "string", "description": "Action ('status', 'inspect', 'list_modules')"}}, "required": ["action"]},
            risk_level=RiskLevel.MEDIUM, run=lambda action="status", **kwargs: PrevJarvisTool().execute(action=action, **kwargs)
        )
    ]

def register_all_builtin_tools(registry: ToolRegistry, app_dir: Path, reminder_mgr, notes_file: Path, memory_engine, automation_engine):
    for t in get_file_tools(app_dir):
        registry.register(t)
    for t in get_system_tools(app_dir):
        registry.register(t)
    for t in get_system_control_tools():
        registry.register(t)
    for t in get_web_tools():
        registry.register(t)
    for t in get_voice_and_note_tools(reminder_mgr, notes_file):
        registry.register(t)
    for t in get_vision_tools(app_dir / "Projects"):
        registry.register(t)
    for t in get_memory_tools(memory_engine, automation_engine):
        registry.register(t)
    for t in get_nextgen_tools():
        registry.register(t)


