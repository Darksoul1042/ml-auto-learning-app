from __future__ import annotations

import time
from random import random


def with_retry(fn, retries: int = 3, backoff_seconds: float = 0.2, retry_on: tuple[type[Exception], ...] = (Exception,)):
    last_exc = None
    for attempt in range(retries):
        try:
            return fn()
        except retry_on as exc:
            last_exc = exc
            if attempt < retries - 1:
                jitter = backoff_seconds * 0.1 * random()
                time.sleep((backoff_seconds * (attempt + 1)) + jitter)
    raise last_exc
