from ml_auto_learning_app.api.contracts import QuoteRequest
from ml_auto_learning_app.api.v1_app import app, handle_quote


def test_handle_quote_validation() -> None:
    assert handle_quote(QuoteRequest(symbol="", notional=100)).ok is False
    assert handle_quote(QuoteRequest(symbol="BTCUSDT", notional=0)).ok is False
    assert handle_quote(QuoteRequest(symbol="BTCUSDT", notional=100)).ok is True


def _run_app(scope: dict, body: bytes = b"{}") -> tuple[int, dict]:
    import asyncio
    import json

    messages: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": body}

    async def send(msg: dict) -> None:
        messages.append(msg)

    asyncio.run(app(scope, receive, send))
    start = next(m for m in messages if m["type"] == "http.response.start")
    response_body = next(m for m in messages if m["type"] == "http.response.body")["body"]
    return start["status"], json.loads(response_body.decode("utf-8"))


def test_asgi_health() -> None:
    status, payload = _run_app({"type": "http", "method": "GET", "path": "/health", "headers": []})
    assert status == 200
    assert payload["ok"] is True


def test_asgi_requires_auth_token(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "secret")
    status, payload = _run_app({"type": "http", "method": "POST", "path": "/market/quote", "headers": []})
    assert status == 401
    assert payload["error"] == "unauthorized"


def test_asgi_market_quote_success(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "dev")
    monkeypatch.setenv("NEXORA_API_TOKEN", "secret")
    scope = {"type": "http", "method": "POST", "path": "/market/quote", "headers": [(b"x-api-token", b"secret")]}
    status, payload = _run_app(scope, body=b'{"symbol":"BTCUSDT","notional":100}')
    assert status == 200
    assert payload["ok"] is True
