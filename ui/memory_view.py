import tkinter as tk
from tkinter import messagebox
from .theme import COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_ERROR, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_HEADING

class MemoryView(tk.Frame):
    def __init__(self, parent, memory_engine, **kwargs):
        super().__init__(parent, bg=COLOR_BG, padx=20, pady=16, **kwargs)
        self.memory = memory_engine

        # Header
        tk.Label(self, text="?? PERSISTENT MEMORY & KNOWLEDGE", font=FONT_HEADING, bg=COLOR_BG, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 12))

        # Add Fact Row
        add_frame = tk.Frame(self, bg=COLOR_CARD, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        add_frame.pack(fill="x", pady=(0, 14))

        tk.Label(add_frame, text="Key / Preference:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", padx=4)
        self.ent_key = tk.Entry(add_frame, bg=COLOR_PANEL, fg=COLOR_TEXT, insertbackground=COLOR_CYAN, width=20, relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.ent_key.grid(row=0, column=1, padx=6)

        tk.Label(add_frame, text="Value / Fact:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).grid(row=0, column=2, sticky="w", padx=4)
        self.ent_val = tk.Entry(add_frame, bg=COLOR_PANEL, fg=COLOR_TEXT, insertbackground=COLOR_CYAN, width=32, relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.ent_val.grid(row=0, column=3, padx=6)

        btn_add = tk.Button(add_frame, text="+ Store Memory", bg=COLOR_EMERALD, fg="#04060c", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=3, command=self._add_fact, cursor="hand2")
        btn_add.grid(row=0, column=4, padx=8)

        # Facts List Container
        tk.Label(self, text="STORED FACTS & KNOWLEDGE", font=("Segoe UI", 9, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(4, 6))

        self.list_frame = tk.Frame(self, bg=COLOR_BG)
        self.list_frame.pack(fill="both", expand=True)

        self.refresh()

    def _add_fact(self):
        k = self.ent_key.get().strip()
        v = self.ent_val.get().strip()
        if k and v:
            self.memory.store_fact(k, v)
            self.ent_key.delete(0, "end")
            self.ent_val.delete(0, "end")
            self.refresh()

    def _delete_fact(self, fact_id: str):
        self.memory.delete_fact(fact_id)
        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        facts = self.memory.facts
        if not facts:
            tk.Label(self.list_frame, text="No facts stored in memory yet.", bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=8)
            return

        for f in facts:
            row = tk.Frame(self.list_frame, bg=COLOR_CARD, padx=12, pady=6, highlightthickness=1, highlightbackground=COLOR_BORDER)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"? {f.key}:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_EMERALD).pack(side="left")
            tk.Label(row, text=f.value, font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT, padx=6).pack(side="left")
            btn_del = tk.Button(row, text="Delete", font=("Segoe UI", 8), bg="#2d1515", fg=COLOR_ERROR, relief="flat", padx=6, command=lambda fid=f.id: self._delete_fact(fid), cursor="hand2")
            btn_del.pack(side="right")
