import json
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from .models import AutomationWorkflow, AutomationStep
from .triggers import TriggerMatcher

class AutomationEngine:
    def __init__(self, data_file: Optional[Path] = None, tool_executor: Optional[Callable] = None):
        if data_file is None:
            data_file = Path(__file__).resolve().parent.parent / 'data' / 'automations.json'
        self.file_path = data_file
        self.tool_executor = tool_executor
        self.workflows: List[AutomationWorkflow] = []
        self.lock = threading.RLock()
        self._load()

    def _ensure_default_workflows(self):
        if not self.workflows:
            # Default Starter Workflows
            self.workflows = [
                AutomationWorkflow(
                    id='wf-study',
                    name='Study Session',
                    description='Opens Projects folder, creates quick notes, and fetches weather',
                    trigger_type='voice_phrase',
                    trigger_value='start study',
                    steps=[
                        AutomationStep('open_target', {'target': 'Projects'}, 'Open Projects workspace'),
                        AutomationStep('get_weather', {'city': 'Delhi'}, 'Check local weather'),
                        AutomationStep('add_note', {'note': 'Study session started'}, 'Log study note')
                    ]
                ),
                AutomationWorkflow(
                    id='wf-devmode',
                    name='Developer Mode',
                    description='Launches VS Code / notepad and opens projects directory',
                    trigger_type='voice_phrase',
                    trigger_value='dev mode',
                    steps=[
                        AutomationStep('open_target', {'target': 'notepad'}, 'Launch text editor'),
                        AutomationStep('open_target', {'target': 'Projects'}, 'Open projects folder')
                    ]
                )
            ]
            self.save()

    def _load(self):
        with self.lock:
            try:
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                if self.file_path.exists():
                    data = json.loads(self.file_path.read_text(encoding='utf-8'))
                    self.workflows = [AutomationWorkflow.from_dict(w) for w in data]
                else:
                    self._ensure_default_workflows()
            except Exception:
                self._ensure_default_workflows()

    def save(self):
        with self.lock:
            try:
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                data = [w.to_dict() for w in self.workflows]
                self.file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
            except OSError:
                pass

    def get_all(self) -> List[AutomationWorkflow]:
        return list(self.workflows)

    def add_workflow(self, workflow: AutomationWorkflow):
        self.workflows.append(workflow)
        self.save()

    def delete_workflow(self, workflow_id: str) -> bool:
        before = len(self.workflows)
        self.workflows = [w for w in self.workflows if w.id != workflow_id]
        if len(self.workflows) < before:
            self.save()
            return True
        return False

    def find_matching_workflow(self, query: str) -> Optional[AutomationWorkflow]:
        return TriggerMatcher.match_voice_trigger(query, self.workflows)

    def execute_workflow(self, workflow: AutomationWorkflow, step_callback: Optional[Callable] = None) -> Dict[str, Any]:
        results = []
        workflow.last_run = datetime.now().isoformat()
        workflow.run_count += 1
        self.save()

        success = True
        for idx, step in enumerate(workflow.steps):
            if step_callback:
                step_callback('running', idx, step.description or step.tool_name)
            res_str = ''
            try:
                if self.tool_executor:
                    res = self.tool_executor(step.tool_name, step.arguments)
                    res_str = str(res)
                else:
                    res_str = f'Tool executor not bound for {step.tool_name}'
                results.append({'step': idx, 'status': 'success', 'output': res_str})
                if step_callback:
                    step_callback('success', idx, res_str)
            except Exception as err:
                success = False
                results.append({'step': idx, 'status': 'error', 'error': str(err)})
                if step_callback:
                    step_callback('error', idx, str(err))
                if not step.continue_on_error:
                    break

        return {'workflow': workflow.name, 'success': success, 'results': results}
