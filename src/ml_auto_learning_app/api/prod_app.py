from __future__ import annotations

import json
import logging
import time
from hmac import compare_digest
from typing import Any
from uuid import uuid4

from ml_auto_learning_app.config import load_config

from .v1_app import handle_quote
from .contracts import QuoteRequest

logger = logging.getLogger("nexora.api.prod")

OPENAPI_DOC: dict[str, Any] = {
    "openapi": "3.1.0",
    "info": {"title": "NEXORA API", "version": "1.0.0"},
    "paths": {
        "/v1/health": {"get": {"responses": {"200": {"description": "ok"}}}},
        "/v1/market/quote": {"post": {"responses": {"200": {"description": "quote"}}}},
    },
}


async def app(scope: dict[str, Any], receive, send) -> None:
    started = time.time()
    request_id = str(uuid4())
    path = scope.get("path", "")
    method = scope.get("method", "GET")

    async def respond(status: int, payload: dict[str, Any], content_type: bytes = b"application/json") -> None:
        body = json.dumps({**payload, "request_id": request_id, "api_version": "v1"}).encode("utf-8")
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [
                    (b"content-type", content_type),
                    (b"x-api-version", b"v1"),
                    (b"x-request-id", request_id.encode("utf-8")),
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})
        logger.info(
            "request_completed",
            extra={"path": path, "method": method, "status": status, "request_id": request_id, "duration_ms": round((time.time() - started) * 1000, 2)},
        )

    async def problem(status: int, title: str, detail: str, ptype: str = "about:blank") -> None:
        await respond(
            status,
            {
                "type": ptype,
                "title": title,
                "status": status,
                "detail": detail,
            },
            content_type=b"application/problem+json",
        )

    if scope.get("type") != "http":
        await problem(500, "Unsupported Scope", "Only HTTP scope is supported")
        return

    if method == "GET" and path == "/openapi.json":
        await respond(200, OPENAPI_DOC)
        return

    if method == "GET" and path == "/docs":
        html = b"<html><body><h1>NEXORA API Docs</h1><a href='/openapi.json'>openapi.json</a></body></html>"
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/html; charset=utf-8"), (b"x-api-version", b"v1")]})
        await send({"type": "http.response.body", "body": html})
        return

    if method == "GET" and path == "/v1/health":
        await respond(200, {"ok": True, "service": "nexora-prod-api"})
        return

    cfg = load_config()
    token = dict(scope.get("headers", [])).get(b"x-api-token", b"").decode("utf-8")
    if not cfg.api_token or not compare_digest(token, cfg.api_token):
        await problem(401, "Unauthorized", "Missing or invalid API token")
        return

    if method == "POST" and path == "/v1/market/quote":
        try:
            event = await receive()
            payload = json.loads(event.get("body", b"{}").decode("utf-8"))
            req = QuoteRequest(symbol=str(payload.get("symbol", "")), notional=float(payload.get("notional", 0)))
        except Exception:
            await problem(400, "Invalid JSON", "Request payload could not be parsed")
            return
        out = handle_quote(req)
        await respond(200 if out.ok else 400, {"ok": out.ok, "message": out.message})
        return

    await problem(404, "Not Found", "Route does not exist")
