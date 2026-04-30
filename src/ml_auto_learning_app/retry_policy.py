from __future__ import annotations

import time


def with_retry(fn, retries: int = 3, backoff_seconds: float = 0.2):
    last_exc = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(backoff_seconds * (attempt + 1))
    raise last_exc
