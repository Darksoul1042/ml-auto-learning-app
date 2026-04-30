from __future__ import annotations

import json
from typing import Any

from .contracts import QuoteRequest, QuoteResponse


def handle_quote(req: QuoteRequest) -> QuoteResponse:
    if not req.symbol.strip():
        return QuoteResponse(ok=False, message="symbol_required")
    if req.notional <= 0:
        return QuoteResponse(ok=False, message="invalid_notional")
    return QuoteResponse(ok=True, message="accepted")


async def app(scope: dict[str, Any], receive, send) -> None:
    if scope["type"] != "http":
        await send({"type": "http.response.start", "status": 500, "headers": []})
        await send({"type": "http.response.body", "body": b"unsupported_scope"})
        return

    path = scope.get("path", "")
    method = scope.get("method", "GET")

    if method == "GET" and path == "/health":
        body = json.dumps({"ok": True, "service": "nexora-asgi-v1"}).encode("utf-8")
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": body})
        return

    if method == "POST" and path == "/market/quote":
        event = await receive()
        payload = json.loads(event.get("body", b"{}").decode("utf-8"))
        req = QuoteRequest(symbol=str(payload.get("symbol", "")), notional=float(payload.get("notional", 0)))
        res = handle_quote(req)
        status = 200 if res.ok else 400
        body = json.dumps({"ok": res.ok, "message": res.message}).encode("utf-8")
        await send({"type": "http.response.start", "status": status, "headers": [(b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": body})
        return

    await send({"type": "http.response.start", "status": 404, "headers": [(b"content-type", b"application/json")]})
    await send({"type": "http.response.body", "body": b'{\"ok\":false,\"error\":\"not_found\"}'})
