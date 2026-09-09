"""
Unit Tests for SaathiOrchestrator and Sub-Agent Architecture
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agent.orchestrator import SaathiOrchestrator
from agent.base_agent import AgentTask, AgentResponse
from agent.sandbox import ExecutionSandbox
from agent.bus import AgentMessageBus
from agent.shared_memory import SharedContextStore


class TestSaathiOrchestrator(unittest.TestCase):

    def setUp(self):
        self.projects_dir = ROOT_DIR / "Projects"
        self.orchestrator = SaathiOrchestrator(projects_dir=self.projects_dir)

    def test_orchestrator_initialization(self):
        """Test that orchestrator initializes with 6 sub-agents."""
        self.assertEqual(len(self.orchestrator.registered_agents), 6)
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


if __name__ == "__main__":
    unittest.main()

