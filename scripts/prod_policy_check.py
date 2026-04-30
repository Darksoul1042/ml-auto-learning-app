from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.tooling import MarketDataAdapter


def main() -> int:
    env = os.getenv("NEXORA_ENV", "dev").lower()
    if env != "prod":
        print("POLICY_OK: non-prod environment")
        return 0
    try:
        MarketDataAdapter().get_market_quote("BTCUSDT", venue="UNSUPPORTED")
        print("POLICY_FAIL: prod must not use deterministic fallback")
        return 1
    except ValueError:
        print("POLICY_OK: deterministic fallback disabled in prod")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
