"""
Unit Tests for SaathiOrchestrator and Sub-Agent Architecture
"""

import unittest
import sys
import tempfile
import json
from pathlib import Path


# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agent.orchestrator import SaathiOrchestrator
from agent.base_agent import AgentTask, AgentResponse
from agent.sandbox import ExecutionSandbox
from agent.bus import AgentMessageBus
from agent.shared_memory import SharedContextStore
from tools.builtin.files import get_file_tools
from tools.permissions import PermissionManager
from tools.schemas import RiskLevel
from devloop.self_coder import SelfCodingEngine
from devloop.continuous_advancement import ContinuousAdvancementEngine


class TestSaathiOrchestrator(unittest.TestCase):

    def setUp(self):
        self.projects_dir = ROOT_DIR / "Projects"
        self.orchestrator = SaathiOrchestrator(projects_dir=self.projects_dir)

    def test_orchestrator_initialization(self):
        """Test that core agents and dynamic agents are registered."""
        self.assertGreaterEqual(len(self.orchestrator.registered_agents), 6)
        agent_names = [a.name for a in self.orchestrator.registered_agents]
        self.assertIn("CodingAgent", agent_names)
        self.assertIn("WebAgent", agent_names)
        self.assertIn("ConversationAgent", agent_names)
        self.assertIn("VisionAgent", agent_names)
        self.assertIn("AutomationAgent", agent_names)
        self.assertIn("MemoryAgent", agent_names)

    def test_task_graph_generation(self):
        """Test intent classification & task graph generation."""
        tasks = self.orchestrator.classify_and_build_task_graph("research python then build a web app")
        self.assertGreaterEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_type, "web")

    def test_execution_sandbox(self):
        """Test isolated python code execution in sandbox."""
        sandbox = ExecutionSandbox(allowed_workspace_dir=self.projects_dir)
        success, stdout, stderr = sandbox.run_python_code("print('TEST_PASSED_OK')")
        self.assertTrue(success)
        self.assertIn("TEST_PASSED_OK", stdout)

    def test_message_bus(self):
        """Test event publishing and subscribing on message bus."""
        bus = AgentMessageBus()
        received = []

        def listener(evt):
            received.append(evt)

        bus.subscribe("test_evt", listener)
        bus.publish("test_evt", {"msg": "hello"})
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["payload"]["msg"], "hello")

    def test_shared_memory(self):
        """Test shared context store turns and scratchpad."""
        store = SharedContextStore()
        store.add_episodic_turn("user", "Hello Saathi")
        turns = store.get_recent_conversation()
        self.assertEqual(len(turns), 1)
        self.assertEqual(turns[0]["content"], "Hello Saathi")

        store.set_scratchpad_value("test_key", "test_val")
        self.assertEqual(store.get_scratchpad_value("test_key"), "test_val")

    def test_permissions_default_to_restricted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = PermissionManager(Path(temp_dir) / "permissions.json")
            self.assertFalse(manager.master_system_control)
            self.assertFalse(manager.check_permission("unknown_tool", RiskLevel.HIGH))

    def test_file_tools_reject_paths_outside_workspace(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tools = {tool.name: tool for tool in get_file_tools(Path(temp_dir))}
            result = tools["read_file"].run({"path": "../outside.txt"}, {})
            self.assertIn("must stay inside workspace", result)

    def test_self_coder_rejects_unsafe_candidate_paths(self):
        engine = SelfCodingEngine(ROOT_DIR)
        with self.assertRaises(ValueError):
            engine._validate_candidate({"files": [{"path": "data/permissions.json", "content": "{}"}]})

    def test_self_coder_normalizes_model_change_aliases(self):
        engine = SelfCodingEngine(ROOT_DIR)
        candidate = engine._normalize_candidate({"changes": [{"file": "agent/example.py", "new_content": "print(1)"}]})
        self.assertEqual(candidate["files"][0]["path"], "agent/example.py")
        self.assertEqual(candidate["files"][0]["content"], "print(1)")

    def test_self_coder_selects_task_owner(self):
        engine = SelfCodingEngine(ROOT_DIR)
        self.assertEqual(engine._target_file_for_task("Extend WebAgent with caching"), "agent/agents/web_agent.py")

    def test_self_coder_rejects_unavailable_dependency(self):
        engine = SelfCodingEngine(ROOT_DIR)
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate_root = Path(temp_dir)
            target = candidate_root / "agent" / "agents" / "example.py"
            target.parent.mkdir(parents=True)
            target.write_text("import definitely_missing_saathi_package\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                engine._validate_dependencies(candidate_root, ["agent/agents/example.py"])

    def test_advancement_skips_repeated_failures(self):
        engine = ContinuousAdvancementEngine()
        original = engine.self_coder.trace_file
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".jsonl") as tmp:
            tmp_path = Path(tmp.name)
            failed_task = "Extend CodingAgent with AST validation, code linting, and automated unit test execution harness."
            for _ in range(3):
                tmp.write(json.dumps({"task": failed_task, "status": "failed"}) + "\n")
        try:
            engine.self_coder.trace_file = tmp_path
            tasks = engine.discover_web_advancements()
            self.assertNotIn(failed_task, tasks)
        finally:
            engine.self_coder.trace_file = original
            if tmp_path.exists():
                tmp_path.unlink()



if __name__ == "__main__":
    unittest.main()

