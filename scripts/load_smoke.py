from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.matching_engine import MatchingEngine, Order
from ml_auto_learning_app.risk_engine import RiskEngine


def _risk_job(i: int) -> bool:
    d = RiskEngine(max_notional_usd=1000).evaluate((i % 1500) + 1)
    return d.approved


def _match_job(i: int) -> int:
    engine = MatchingEngine()
    engine.add_order(Order(f"b{i}", "BUY", 100, 2))
    trades = engine.add_order(Order(f"s{i}", "SELL", 99, 1))
    return len(trades)


def main() -> int:
    with ThreadPoolExecutor(max_workers=8) as ex:
        risk_results = list(ex.map(_risk_job, range(300)))
        match_results = list(ex.map(_match_job, range(200)))

    assert len(risk_results) == 300
    assert sum(match_results) == 200
    print("LOAD_SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
