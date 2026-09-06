from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

def capture_screen(save_dir: Path, bbox: Optional[Tuple[int, int, int, int]] = None) -> Path:
    save_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = save_dir / f"screenshot_{timestamp}.png"
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab(bbox=bbox)
        img.save(target)
        return target
    except Exception as err:
        raise RuntimeError(f"Failed to grab screenshot: {err}")
