from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    path = Path(os.getenv("NEXORA_METRICS_STORE", "artifacts/runtime_metrics.json"))
    if not path.exists():
        print("ALERTS_OK: no metrics file yet")
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    req = int(data.get("requests_total", 0))
    err = int(data.get("errors_total", 0))
    max_error_rate = float(os.getenv("NEXORA_MAX_ERROR_RATE", "0.2"))
    rate = (err / req) if req else 0.0
    if rate > max_error_rate:
        print(f"ALERTS_FAIL: error_rate={rate:.4f} threshold={max_error_rate:.4f}")
        return 1
    print(f"ALERTS_OK: error_rate={rate:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
