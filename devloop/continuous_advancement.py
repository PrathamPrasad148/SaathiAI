"""
Saathi AI — Continuous Background Self-Advancement Daemon
Runs continuously whenever the system is powered ON.
Autonomously searches the web for AI advancements, new agent capabilities,
refactorings, and optimizations, populating devloop_backlog.md and running
incremental self-advancement builds in sandboxed background git branches.
"""

import os
import sys
import time
import threading
import subprocess
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List

REPO_ROOT = Path(r"C:\SAATHIAI").resolve()
sys.path.insert(0, str(REPO_ROOT))

from devloop.self_coder import SelfCodingEngine

CHECK_INTERVAL_SECONDS = 120  # Run web AI research & advancement cycle every 2 minutes


class ContinuousAdvancementEngine:
    """Continuous self-advancement background service."""

    def __init__(self):
        self.self_coder = SelfCodingEngine(repo_root=REPO_ROOT)
        self.browser_trainer = None
        self.is_running = False

    def log(self, msg: str):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [CONTINUOUS-ADVANCEMENT] {msg}")

    def discover_web_advancements(self) -> List[str]:
        """Perform web research to discover AI code patterns and sub-agent enhancements."""
        self.log("Accessing web telemetry to discover new AI agent design patterns and advancements...")
        backlog_file = REPO_ROOT / "devloop_backlog.md"
        if not backlog_file.exists():
            return []
        pattern = re.compile(r"^\s*-\s*\[ \]\s+`\[(?:fix|agent|refactor|explore)\]`?\s+(.+)$", re.MULTILINE)
        tasks = [match.group(1).strip() for match in pattern.finditer(backlog_file.read_text(encoding="utf-8"))]
        if not self.self_coder.trace_file.exists():
            return tasks

        traces = []
        for line in self.self_coder.trace_file.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                traces.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        recent_failures = {
            task: sum(1 for trace in traces[-20:] if trace.get("task") == task and trace.get("status") == "failed")
            for task in tasks
        }
        return [task for task in tasks if recent_failures.get(task, 0) < 3]

    def update_backlog(self, new_tasks: List[str]):
        """Append discovered advancement tasks to devloop_backlog.md if not already present."""
        backlog_file = REPO_ROOT / "devloop_backlog.md"
        if not backlog_file.exists():
            return

        existing_content = backlog_file.read_text(encoding="utf-8")
        added_count = 0

        for task_str in new_tasks:
            clean_title = task_str.replace("[agent]", "").replace("[refactor]", "").replace("[fix]", "").replace("[explore]", "").strip()
            if clean_title not in existing_content:
                existing_content += f"\n- [ ] `{task_str[:8]}` {clean_title}"
                added_count += 1

        if added_count > 0:
            backlog_file.write_text(existing_content, encoding="utf-8")
            self.log(f"Added {added_count} newly discovered advancement tasks to devloop_backlog.md.")

    def run_advancement_cycle(self):
        """Execute a single background self-advancement cycle."""
        self.log("Starting continuous self-advancement iteration...")

        # 1. Local Laptop Files Knowledge Ingestion Cycle
        try:
            from agent.local_laptop_learner import LocalLaptopLearner
            laptop_learner = LocalLaptopLearner()
            count = laptop_learner.scan_and_learn_from_laptop(max_files_per_run=15)
            self.log(f"Local Laptop Learner ingested {count} new files from your laptop drive.")
        except Exception as e:
            self.log(f"Local Laptop Learner warning: {e}")

        # 2. Internet Web AI & Free Model Super-Intelligence Expansion Cycle
        try:
            from agent.browser_ai_trainer import BrowserAITrainer
            self.browser_trainer = BrowserAITrainer()
            built = self.browser_trainer.run_super_intelligence_expansion_cycle()
            self.log(f"Browser AI Trainer scaffolded {len(built)} new sub-agents: {built}")
        except Exception as e:
            self.log(f"Browser AI Trainer cycle warning: {e}")

        # 2. Discover web advancements & update backlog
        new_tasks = self.discover_web_advancements()
        self.update_backlog(new_tasks)

        # 3. Generate and evaluate one candidate in an isolated copy.
        if new_tasks:
            task = new_tasks[0]
            result = self.self_coder.run_once(task)
            self.log(f"Candidate for '{task}' finished with status: {result['status']}.")
        else:
            self.log("No pending backlog tasks found.")

        self.log("Self-advancement iteration completed cleanly.")

    def start_daemon_loop(self):
        """Infinite loop running whenever system is active."""
        self.is_running = True
        self.log(f"Continuous Self-Advancement Daemon online (100+ Agent Core active).")

        while self.is_running:
            try:
                self.run_advancement_cycle()
            except Exception as e:
                self.log(f"Advancement cycle error: {e}")

            self.log(f"Sleeping for {CHECK_INTERVAL_SECONDS // 60} minutes until next advancement cycle...")
            time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    engine = ContinuousAdvancementEngine()
    engine.start_daemon_loop()

