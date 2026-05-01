from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.api.prod_app import OPENAPI_DOC


def main() -> int:
    required_top = {"openapi", "info", "paths"}
    missing = [k for k in required_top if k not in OPENAPI_DOC]
    if missing:
        print(f"OPENAPI_FAIL: missing {missing}")
        return 1
    required_routes = {"/v1/health", "/v1/readiness", "/v1/market/quote"}
    if not required_routes.issubset(set(OPENAPI_DOC["paths"].keys())):
        print("OPENAPI_FAIL: required v1 routes missing")
        return 1
    print("OPENAPI_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
