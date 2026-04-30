from __future__ import annotations

from ml_auto_learning_app.retry_policy import with_retry


def test_with_retry_eventually_succeeds() -> None:
    state = {"n": 0}

    def flakey() -> str:
        state["n"] += 1
        if state["n"] < 2:
            raise ValueError("transient")
        return "ok"

    out = with_retry(flakey, retries=3, backoff_seconds=0.0, retry_on=(ValueError,))
    assert out == "ok"


def test_with_retry_does_not_retry_other_exceptions() -> None:
    state = {"n": 0}

    def bad() -> str:
        state["n"] += 1
        raise RuntimeError("fatal")

    try:
        with_retry(bad, retries=3, backoff_seconds=0.0, retry_on=(ValueError,))
        assert False, "expected RuntimeError"
    except RuntimeError:
        assert state["n"] == 1
