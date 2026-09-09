"""
Saathi AI — Interactive Live Web AI Training Console
Launches Chrome visibly on your main display, opens ChatGPT/Claude/Gemini,
types directives live, extracts responses, and builds agents right before your eyes!
"""

import sys
import time
from pathlib import Path

REPO_ROOT = Path(r"C:\SAATHIAI").resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent.browser_ai_trainer import BrowserAITrainer, get_chrome_user_data_dir

print("=" * 70)
print("       SAATHI AI — LIVE VISUAL WEB AI BROWSER TRAINER")
print("=" * 70)
print()
print("[1/3] Chrome Profile Path:", get_chrome_user_data_dir())
print("[2/3] Opening Chrome to ChatGPT / Claude / Gemini...")
print("[3/3] Watch your screen! Launching now...")
print()

trainer = BrowserAITrainer()
built = trainer.run_super_intelligence_expansion_cycle()

print()
print("=" * 70)
print(f"SUCCESS! Scaffolded {len(built)} new sub-agents live on your system:")
for b in built:
    print(f"  • {b}")
print("=" * 70)
input("\nPress ENTER to close this window...")
