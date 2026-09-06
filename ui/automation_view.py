import tkinter as tk
from typing import Callable, Optional
from .theme import COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_AMBER, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_HEADING

class AutomationWorkflowsView(tk.Frame):
    def __init__(self, parent, automation_engine, on_run_workflow: Optional[Callable] = None, **kwargs):
        super().__init__(parent, bg=COLOR_BG, padx=20, pady=16, **kwargs)
        self.automations = automation_engine
        self.on_run_workflow = on_run_workflow

        # Header
        tk.Label(self, text="?? REUSABLE AUTOMATION WORKFLOWS", font=FONT_HEADING, bg=COLOR_BG, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 12))

        self.list_frame = tk.Frame(self, bg=COLOR_BG)
        self.list_frame.pack(fill="both", expand=True)

        self.refresh()

    def _trigger_workflow(self, wf):
        if self.on_run_workflow:
            self.on_run_workflow(wf)

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        workflows = self.automations.get_all()
        if not workflows:
            tk.Label(self.list_frame, text="No workflows defined.", bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            return

        for wf in workflows:
            card = tk.Frame(self.list_frame, bg=COLOR_CARD, padx=16, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
            card.pack(fill="x", pady=6)

            top_row = tk.Frame(card, bg=COLOR_CARD)
            top_row.pack(fill="x")

            tk.Label(top_row, text=wf.name, font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg=COLOR_CYAN).pack(side="left")
            tk.Label(top_row, text=f"Trigger: '{wf.trigger_value}'", font=("Segoe UI", 8, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="left", padx=10)

            btn_run = tk.Button(top_row, text="? Run Workflow", bg=COLOR_EMERALD, fg="#04060c", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=4, cursor="hand2", command=lambda w=wf: self._trigger_workflow(w))
            btn_run.pack(side="right")

            tk.Label(card, text=wf.description, font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(4, 6))

            steps_str = " ? ".join(s.description or s.tool_name for s in wf.steps)
            tk.Label(card, text=f"Steps: {steps_str}", font=("Consolas", 8), bg=COLOR_CARD, fg="#38bdf8").pack(anchor="w")
