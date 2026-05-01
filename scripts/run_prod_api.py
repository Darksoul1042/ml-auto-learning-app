from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.api.prod_app import app


def main() -> int:
    try:
        import uvicorn  # type: ignore
    except Exception:
        print("RUN_PROD_API_FAIL: uvicorn is required to run the production ASGI app")
        return 1
    uvicorn.run(app, host="127.0.0.1", port=8082, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
