"""
Saathi AI — Inter-Agent Communication Bus & Event System
Thread-safe message bus for inter-agent communication, event dispatching,
task queuing, and real-time UI status notifications.
"""

import queue
import threading
import time
from typing import Dict, Any, List, Callable, Optional
from .base_agent import AgentTask, AgentResponse


class AgentMessageBus:
    """Central event broker for inter-agent communication & event broadcasting."""

    def __init__(self):
        self._listeners: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self._task_queue: queue.Queue = queue.Queue()
        self._lock = threading.Lock()
        self._history: List[Dict[str, Any]] = []

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe a listener callback to a specific event type (e.g. 'agent_start', 'agent_complete', 'task_step')."""
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            if callback not in self._listeners[event_type]:
                self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        """Unsubscribe a listener callback."""
        with self._lock:
            if event_type in self._listeners and callback in self._listeners[event_type]:
                self._listeners[event_type].remove(callback)

    def publish(self, event_type: str, payload: Dict[str, Any]):
        """Broadcast an event payload to all subscribed callbacks."""
        event_data = {
            "event_type": event_type,
            "timestamp": time.time(),
            "payload": payload
        }
        with self._lock:
            self._history.append(event_data)
            if len(self._history) > 500:
                self._history = self._history[-500:]

            target_listeners = list(self._listeners.get(event_type, [])) + list(self._listeners.get("*", []))

        for cb in target_listeners:
            try:
                cb(event_data)
            except Exception as e:
                print(f"[MESSAGE BUS ERROR] Event listener exception on '{event_type}': {e}")

    def enqueue_task(self, task: AgentTask):
        """Enqueue an AgentTask for background worker agents."""
        self._task_queue.put(task)
        self.publish("task_enqueued", {"task_id": task.task_id, "type": task.task_type, "instruction": task.instruction})

    def get_next_task(self, timeout: Optional[float] = None) -> Optional[AgentTask]:
        """Fetch next task from queue."""
        try:
            return self._task_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def get_event_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent event history."""
        with self._lock:
            return list(self._history[-limit:])
