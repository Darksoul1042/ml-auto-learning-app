from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.config import load_config


def main() -> int:
    cfg = load_config()
    print(f"CONFIG_OK: env={cfg.env} allow_demo_fallbacks={cfg.allow_demo_fallbacks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
