from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestMetrics:
    route: str
    status: int
    duration_ms: float


def measure(route: str, status: int, started_at: float) -> RequestMetrics:
    return RequestMetrics(route=route, status=status, duration_ms=(time.time() - started_at) * 1000)
