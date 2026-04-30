from __future__ import annotations

import json
import logging
import time
from hmac import compare_digest
from uuid import uuid4
from typing import Any

from ml_auto_learning_app.config import load_config

from .contracts import QuoteRequest, QuoteResponse
from .middleware import measure

logger = logging.getLogger("nexora.api.v1")


def handle_quote(req: QuoteRequest) -> QuoteResponse:
    if not req.symbol.strip():
        return QuoteResponse(ok=False, message="symbol_required")
    if req.notional <= 0:
        return QuoteResponse(ok=False, message="invalid_notional")
    return QuoteResponse(ok=True, message="accepted")


async def app(scope: dict[str, Any], receive, send) -> None:
    started_at = time.time()
    request_id = str(uuid4())

    async def _respond(status: int, payload: dict[str, Any]) -> None:
        payload = {**payload, "api_version": "v1"}
        metrics = measure(scope.get("path", ""), status, started_at)
        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "route": metrics.route,
                "status": metrics.status,
                "duration_ms": round(metrics.duration_ms, 2),
            },
        )
        body = json.dumps(payload).encode("utf-8")
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"x-api-version", b"v1"),
                    (b"x-request-id", request_id.encode("utf-8")),
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})

    if scope["type"] != "http":
        await _respond(500, {"ok": False, "error": "unsupported_scope", "request_id": request_id})
        return

    path = scope.get("path", "")
    method = scope.get("method", "GET")
    headers = dict(scope.get("headers", []))
    token = headers.get(b"x-api-token", b"").decode("utf-8")

    if method == "GET" and path == "/health":
        await _respond(200, {"ok": True, "service": "nexora-asgi-v1", "request_id": request_id})
        return

    try:
        cfg = load_config()
    except ValueError as exc:
        await _respond(500, {"ok": False, "error": str(exc), "request_id": request_id})
        return

    if not cfg.api_token:
        await _respond(500, {"ok": False, "error": "api_token_not_configured", "request_id": request_id})
        return

    if not compare_digest(token, cfg.api_token):
        await _respond(401, {"ok": False, "error": "unauthorized", "request_id": request_id})
        return

    if method == "POST" and path == "/market/quote":
        try:
            event = await receive()
            payload = json.loads(event.get("body", b"{}").decode("utf-8"))
            req = QuoteRequest(symbol=str(payload.get("symbol", "")), notional=float(payload.get("notional", 0)))
        except (ValueError, json.JSONDecodeError):
            await _respond(400, {"ok": False, "error": "invalid_json", "request_id": request_id})
            return
        res = handle_quote(req)
        status = 200 if res.ok else 400
        await _respond(status, {"ok": res.ok, "message": res.message, "request_id": request_id})
        return

    await _respond(404, {"ok": False, "error": "not_found", "request_id": request_id})
