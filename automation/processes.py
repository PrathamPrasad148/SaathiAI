from typing import List, Dict, Any

def list_running_processes(limit: int = 25) -> List[Dict[str, Any]]:
    procs = []
    try:
        import psutil
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                info = p.info
                if info.get("name"):
                    procs.append({
                        "pid": info["pid"],
                        "name": info["name"],
                        "cpu": round(info.get("cpu_percent") or 0.0, 1),
                        "ram": round(info.get("memory_percent") or 0.0, 1)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        procs.sort(key=lambda x: x["ram"], reverse=True)
        return procs[:limit]
    except Exception:
        return [{"pid": 0, "name": "System", "cpu": 0, "ram": 0}]

def kill_process(pid: int) -> bool:
    try:
        import psutil
        p = psutil.Process(pid)
        p.terminate()
        return True
    except Exception:
        return False

def kill_process_by_name(name: str) -> int:
    """Terminate all processes matching name (case-insensitive). Returns count terminated."""
    killed = 0
    try:
        import psutil
        target = name.lower().strip()
        if not target.endswith(".exe") and not "." in target:
            target += ".exe"
        for p in psutil.process_iter(["pid", "name"]):
            try:
                p_name = (p.info.get("name") or "").lower()
                if p_name == target or target in p_name:
                    p.terminate()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except Exception:
        pass
    return killed

