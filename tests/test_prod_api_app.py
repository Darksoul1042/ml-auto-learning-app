from __future__ import annotations

import asyncio
import json

from ml_auto_learning_app.api.prod_app import app


def _run(scope: dict, body: bytes = b"{}") -> tuple[int, dict, dict]:
    messages: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": body}

    async def send(msg: dict) -> None:
        messages.append(msg)

    asyncio.run(app(scope, receive, send))
    start = next(m for m in messages if m["type"] == "http.response.start")
    raw = next(m for m in messages if m["type"] == "http.response.body")["body"]
    headers = {k.decode("utf-8"): v.decode("utf-8") for k, v in start.get("headers", [])}
    ct = headers.get("content-type", "")
    payload = json.loads(raw.decode("utf-8")) if ("application/json" in ct or "application/problem+json" in ct) else {"raw": raw.decode("utf-8")}
    return start["status"], payload, headers


def test_openapi_json_available() -> None:
    status, payload, headers = _run({"type": "http", "method": "GET", "path": "/openapi.json", "headers": []})
    assert status == 200
    assert payload["openapi"].startswith("3.")
    assert headers["x-api-version"] == "v1"


def test_prod_quote_requires_auth(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "s3cr3t")
    status, payload, _ = _run({"type": "http", "method": "POST", "path": "/v1/market/quote", "headers": []})
    assert status == 401
    assert payload["title"] == "Unauthorized"
    assert payload["status"] == 401


def test_readiness_and_metrics(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "s3cr3t")
    status, payload, _ = _run({"type": "http", "method": "GET", "path": "/v1/readiness", "headers": []})
    assert status == 200
    assert payload["ok"] is True
    status, payload, headers = _run({"type": "http", "method": "GET", "path": "/metrics", "headers": []})
    assert status == 200
    assert "text/plain" in headers["content-type"]
    assert "nexora_requests_total" in payload["raw"]


def test_metrics_persisted_to_store(monkeypatch, tmp_path) -> None:
    store = tmp_path / "metrics.json"
    monkeypatch.setenv("NEXORA_METRICS_STORE", str(store))
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "s3cr3t")
    _run({"type": "http", "method": "GET", "path": "/v1/health", "headers": []})
    assert store.exists()


def test_order_lifecycle_create_get_cancel(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "s3cr3t")
    headers = [(b"x-api-token", b"s3cr3t")]
    status, payload, _ = _run(
        {"type": "http", "method": "POST", "path": "/v1/orders", "headers": headers},
        body=b'{"symbol":"BTCUSDT","side":"BUY","price":100.0,"quantity":1.0}',
    )
    assert status == 201
    assert payload["ok"] is True
    order_id = payload["order"]["order_id"]
    status, payload, _ = _run({"type": "http", "method": "GET", "path": f"/v1/orders/{order_id}", "headers": headers})
    assert status == 200
    assert payload["order"]["status"] in {"open", "filled"}
    status, payload, _ = _run({"type": "http", "method": "POST", "path": f"/v1/orders/{order_id}/cancel", "headers": headers})
    if payload.get("status") == 409:
        assert status == 409
    else:
        assert status == 200
        assert payload["order"]["status"] == "cancelled"


def test_order_idempotency_key_replay(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "s3cr3t")
    headers = [(b"x-api-token", b"s3cr3t"), (b"idempotency-key", b"k-1")]
    body = b'{"symbol":"ETHUSDT","side":"BUY","price":100.0,"quantity":1.0}'
    status, payload, _ = _run({"type": "http", "method": "POST", "path": "/v1/orders", "headers": headers}, body=body)
    assert status == 201
    order_id = payload["order"]["order_id"]
    status, payload, _ = _run({"type": "http", "method": "POST", "path": "/v1/orders", "headers": headers}, body=body)
    assert status == 200
    assert payload["idempotent_replay"] is True
    assert payload["order"]["order_id"] == order_id


def test_order_risk_rejects_large_notional(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "s3cr3t")
    headers = [(b"x-api-token", b"s3cr3t")]
    status, payload, _ = _run(
        {"type": "http", "method": "POST", "path": "/v1/orders", "headers": headers},
        body=b'{"symbol":"BTCUSDT","side":"BUY","price":5000.0,"quantity":1.0}',
    )
    assert status == 400
    assert payload["title"] == "Risk Rejected"
