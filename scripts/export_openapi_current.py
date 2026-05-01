from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ml_auto_learning_app.api.prod_app import OPENAPI_DOC


def main() -> int:
    out = Path("artifacts")
    out.mkdir(parents=True, exist_ok=True)
    dst = out / "openapi_current.json"
    dst.write_text(json.dumps(OPENAPI_DOC, indent=2), encoding="utf-8")
    print(f"OPENAPI_EXPORT_OK:{dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
