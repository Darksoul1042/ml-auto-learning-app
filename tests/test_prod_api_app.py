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
