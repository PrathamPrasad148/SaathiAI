"""
Saathi AI 2.0 — Unit Tests for Modular Architecture
"""

import unittest
import os
import tempfile
from pathlib import Path
from saathi.config import SystemConfig, SecurityConfig, ModelConfig
from saathi.models.base import ModelProvider
from saathi.models.providers.ollama import OllamaProvider
from saathi.models.router import ModelRouter, TaskCategory
from saathi.tools.base import BaseTool, ToolMetadata, RiskLevel
from saathi.tools.registry import DynamicToolRegistry
from saathi.security.sandbox import ExecutionSandbox
from saathi.memory.store import MultiTierMemoryStore
from saathi.knowledge.store import LocalKnowledgeStore
from saathi.knowledge.ingestion import KnowledgeIngestionPipeline
from saathi.core.evaluator import ResponseEvaluator
from saathi.core.planner import TaskPlanner

class TestSaathi2Core(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_config_loading(self):
        cfg = SystemConfig.load()
        self.assertIsNotNone(cfg.security.autonomy_level)
        self.assertIn(cfg.security.network_mode, ["offline", "local", "hybrid", "online"])

    def test_model_router_classification(self):
        router = ModelRouter()
        self.assertEqual(router.classify_task("Write a python script for scraping"), TaskCategory.CODING)
        self.assertEqual(router.classify_task("Solve the derivative of x^2"), TaskCategory.MATHEMATICS)
        self.assertEqual(router.classify_task("Search for quantum mechanics papers"), TaskCategory.RESEARCH)

    def test_sandbox_ast_validation(self):
        sandbox = ExecutionSandbox(self.workspace)
        valid, err = sandbox.validate_ast("def add(a, b):\n    return a + b")
        self.assertTrue(valid)
        self.assertIsNone(err)

        invalid, err = sandbox.validate_ast("def add(a, b:\n    return a + b")
        self.assertFalse(invalid)
        self.assertIsNotNone(err)

    def test_memory_store_operations(self):
        mem_dir = self.workspace / "memory"
        mem_store = MultiTierMemoryStore(memory_dir=mem_dir)
        mem_store.add_semantic("Python is a dynamic programming language", category="TECH")
        self.assertEqual(len(mem_store.semantic), 1)

        results = mem_store.get_semantic("Python")
        self.assertTrue(len(results) > 0)

        forgotten = mem_store.forget("Python")
        self.assertEqual(forgotten, 1)

    def test_knowledge_db_and_ingestion(self):
        db_file = self.workspace / "knowledge.db"
        store = LocalKnowledgeStore(db_path=db_file)
        pipeline = KnowledgeIngestionPipeline(store=store)

        test_file = self.workspace / "doc.txt"
        test_file.write_text("Saathi AI 2.0 provides local-first agentic computing.", encoding="utf-8")

        count = pipeline.ingest_file(test_file, topic="AI")
        self.assertTrue(count > 0)
        self.assertEqual(store.count(), count)

        hits = store.query("agentic computing")
        self.assertTrue(len(hits) > 0)

    def test_response_evaluator(self):
        evaluator = ResponseEvaluator()
        result = evaluator.evaluate("Explain gravity", "Gravity is a natural phenomenon by which all things with mass are brought toward one another.")
        self.assertTrue(result["passed"])

    def test_file_utils(self):
        from saathi.tools import FileUtils
        json_path = self.workspace / "sample.json"
        data = {"key": "value", "count": 42}
        written = FileUtils.write_json(json_path, data)
        self.assertTrue(written)

        read_data = FileUtils.read_json(json_path)
        self.assertEqual(read_data, data)

    def test_web_cmd_tool(self):
        from saathi.tools import WebCmdTool
        tool = WebCmdTool()
        self.assertEqual(tool.name, "web_cmd")
        self.assertTrue(tool.metadata.requires_network)
        res = tool.execute(command="help")
        self.assertIn("status", res)

    def test_self_edify_tool(self):
        from saathi.tools import SelfEdifyTool
        tool = SelfEdifyTool()
        self.assertEqual(tool.name, "self_edify")
        res = tool.execute(action="status")
        self.assertEqual(res["status"], "success")

if __name__ == "__main__":
    unittest.main()
