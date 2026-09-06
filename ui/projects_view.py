import os
import webbrowser
import tkinter as tk
from pathlib import Path
from typing import Optional, Callable
from .theme import COLOR_BG, COLOR_PANEL, COLOR_CARD, COLOR_BORDER, COLOR_CYAN, COLOR_EMERALD, COLOR_TEXT, COLOR_TEXT_MUTED, FONT_HEADING

class ProjectsGalleryView(tk.Frame):
    def __init__(self, parent, projects_dir: Path, on_create_site: Optional[Callable[[str], None]] = None, **kwargs):
        super().__init__(parent, bg=COLOR_BG, padx=20, pady=16, **kwargs)
        self.projects_dir = projects_dir
        self.on_create_site = on_create_site

        # Header
        hdr = tk.Frame(self, bg=COLOR_BG)
        hdr.pack(fill="x", pady=(0, 12))

        tk.Label(hdr, text="?? PROJECTS & GENERATED WEBSITES", font=FONT_HEADING, bg=COLOR_BG, fg=COLOR_CYAN).pack(side="left")
        btn_open_folder = tk.Button(hdr, text="Open Projects Folder", bg=COLOR_PANEL, fg=COLOR_TEXT, font=("Segoe UI", 9), relief="flat", padx=10, pady=4, command=self._open_folder, cursor="hand2")
        btn_open_folder.pack(side="right")

        # Quick Builder Row
        quick_frame = tk.Frame(self, bg=COLOR_CARD, padx=14, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        quick_frame.pack(fill="x", pady=(0, 14))

        tk.Label(quick_frame, text="Generate Bespoke Website:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT).pack(side="left", padx=(0, 8))
        self.ent_topic = tk.Entry(quick_frame, bg=COLOR_PANEL, fg=COLOR_TEXT, insertbackground=COLOR_CYAN, width=32, relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.ent_topic.pack(side="left", padx=(0, 8))
        self.ent_topic.insert(0, "Cyberpunk Gaming Lounge")

        btn_build = tk.Button(quick_frame, text="?? Build & Launch", bg=COLOR_EMERALD, fg="#04060c", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=4, command=self._build_topic, cursor="hand2")
        btn_build.pack(side="left")

        # Projects List
        self.list_container = tk.Frame(self, bg=COLOR_BG)
        self.list_container.pack(fill="both", expand=True)

        self.refresh()

    def _open_folder(self):
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(str(self.projects_dir))

    def _build_topic(self):
        topic = self.ent_topic.get().strip()
        if topic and self.on_create_site:
            self.on_create_site(topic)

    def refresh(self):
        for w in self.list_container.winfo_children():
            w.destroy()

        if not self.projects_dir.exists():
            return

        dirs = [d for d in self.projects_dir.iterdir() if d.is_dir()]
        if not dirs:
            tk.Label(self.list_container, text="No generated projects yet. Type a topic above to create one!", bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=10)
            return

        for p_dir in dirs:
            row = tk.Frame(self.list_container, bg=COLOR_CARD, padx=14, pady=8, highlightthickness=1, highlightbackground=COLOR_BORDER)
            row.pack(fill="x", pady=4)

            tk.Label(row, text=f"?? {p_dir.name}", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_CYAN).pack(side="left")

            html_idx = p_dir / "index.html"
            if html_idx.exists():
                btn_view = tk.Button(row, text="Launch in Browser", bg=COLOR_EMERALD, fg="#04060c", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=2, command=lambda p=html_idx: webbrowser.open(p.as_uri()), cursor="hand2")
                btn_view.pack(side="right")
