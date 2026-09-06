from typing import Dict, Any
from ..schemas import Tool, RiskLevel

def get_memory_tools(memory_engine, automation_engine) -> list[Tool]:
    def manage_mem_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        action = args.get("action", "store").lower()
        key = args.get("key", "").strip()
        val = args.get("value", "").strip()
        if action == "store":
            if not key or not val:
                return "Error: key and value required to store memory."
            memory_engine.store_fact(key, val)
            return f"Remembered: '{key}' = '{val}'."
        elif action == "recall":
            facts = memory_engine.search_facts(key)
            if not facts:
                return f"No memory found for '{key}'."
            return "\n".join(f"- {f.key}: {f.value}" for f in facts)
        return "Unknown memory action."

    def run_auto_run(args: Dict[str, Any], ctx: Dict[str, Any]) -> str:
        wf_name = args.get("workflow", "")
        wf = automation_engine.find_matching_workflow(wf_name)
        if not wf:
            return f"Automation workflow '{wf_name}' not found."
        res = automation_engine.execute_workflow(wf)
        return f"Executed workflow '{wf.name}': {len(res.get('results', []))} steps completed."

    return [
        Tool(
            name="manage_memory",
            category="memory",
            description="Store or recall facts, preferences, and details in Saathi persistent memory.",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["store", "recall"], "description": "Action to perform"},
                    "key": {"type": "string", "description": "Fact or preference name"},
                    "value": {"type": "string", "description": "Value to store (for action='store')"}
                },
                "required": ["action", "key"]
            },
            risk_level=RiskLevel.LOW,
            run=manage_mem_run
        ),
        Tool(
            name="run_automation",
            category="automations",
            description="Execute a saved multi-step automation workflow by name or phrase.",
            parameters={
                "type": "object",
                "properties": {
                    "workflow": {"type": "string", "description": "Name or trigger phrase of the workflow"}
                },
                "required": ["workflow"]
            },
            risk_level=RiskLevel.LOW,
            run=run_auto_run
        )
    ]
