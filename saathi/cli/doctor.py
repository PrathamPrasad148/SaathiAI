"""
Saathi AI 2.0 — Doctor System Diagnostic Command
"""

import sys
import os
import urllib.request
from pathlib import Path
from ..config import config
from ..models.providers.ollama import OllamaProvider
from ..knowledge.store import LocalKnowledgeStore
from ..memory.store import MultiTierMemoryStore

def run_doctor() -> bool:
    print("=" * 65)
    print("           SAATHI AI 2.0 SYSTEM DOCTOR DIAGNOSTIC           ")
    print("=" * 65)

    all_passed = True

    # 1. Python Check
    py_ver = sys.version.split()[0]
    print(f"[OK] Python Version: {py_ver} ({sys.executable})")

    # 2. Key Directories Check
    for name, p in [
        ("Data Dir", config.data_dir),
        ("Logs Dir", config.logs_dir),
        ("Projects Dir", config.projects_dir),
        ("Backups Dir", config.backups_dir)
    ]:
        if p.exists():
            print(f"[OK] {name}: {p}")
        else:
            print(f"[FAIL] {name} Missing: {p}")
            all_passed = False

    # 3. Dependencies Check
    deps = ["sounddevice", "requests", "pillow"]
    for dep in deps:
        try:
            __import__(dep)
            print(f"[OK] Dependency '{dep}': Installed")
        except ImportError:
            print(f"[WARN] Dependency '{dep}': Not Installed (Optional)")

    # 4. Ollama & Models Check
    ollama = OllamaProvider(model_id=config.models.primary_local_model, host=config.models.ollama_host)
    if ollama.health_check():
        print(f"[OK] Ollama Server: Online ({config.models.ollama_host})")
        print(f"[OK] Primary Model '{config.models.primary_local_model}': Configured & Active")
    else:
        print(f"[WARN] Ollama Server: Offline/Unreachable ({config.models.ollama_host})")

    # 5. Database Check
    try:
        store = LocalKnowledgeStore()
        item_count = store.count()
        print(f"[OK] Knowledge DB: SQLite Active ({item_count} items stored)")
    except Exception as e:
        print(f"[FAIL] Knowledge DB Error: {e}")
        all_passed = False

    # 6. Memory Store Check
    try:
        mem = MultiTierMemoryStore()
        sem_count = len(mem.semantic)
        print(f"[OK] Multi-Tier Memory: Active ({sem_count} semantic facts)")
    except Exception as e:
        print(f"[FAIL] Memory Store Error: {e}")
        all_passed = False

    # 7. Internet Connectivity Check
    try:
        req = urllib.request.Request("https://www.google.com", headers={"User-Agent": "SaathiDoctor/2.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                print(f"[OK] Internet Connectivity: Online (Hybrid Mode)")
    except Exception:
        print(f"[WARN] Internet Connectivity: Offline (Falling back to Local Mode)")

    print("=" * 65)
    if all_passed:
        print("          ALL SAATHI AI 2.0 CORE DIAGNOSTICS PASSED!         ")
    else:
        print("          DIAGNOSTIC COMPLETED WITH SOME WARNINGS.          ")
    print("=" * 65)
    return all_passed

if __name__ == "__main__":
    run_doctor()
