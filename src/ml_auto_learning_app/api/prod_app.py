from __future__ import annotations

import json
import logging
import os
import time
from hmac import compare_digest
from typing import Any
from uuid import uuid4

from ml_auto_learning_app.config import load_config
from ml_auto_learning_app.matching_engine import MatchingEngine, Order
from ml_auto_learning_app.risk_engine import RiskEngine

from .v1_app import handle_quote
from .contracts import QuoteRequest

logger = logging.getLogger("nexora.api.prod")

OPENAPI_DOC: dict[str, Any] = {
    "openapi": "3.1.0",
    "info": {"title": "NEXORA API", "version": "1.0.0"},
    "paths": {
        "/v1/health": {"get": {"responses": {"200": {"description": "ok"}}}},
        "/v1/readiness": {"get": {"responses": {"200": {"description": "ready"}}}},
        "/v1/info": {"get": {"responses": {"200": {"description": "build info"}}}},
        "/v1/market/quote": {"post": {"responses": {"200": {"description": "quote"}}}},
        "/v1/orders": {"post": {"responses": {"201": {"description": "order created"}}}},
    },
}

_METRICS = {
    "requests_total": 0,
    "errors_total": 0,
}
_ENGINE = MatchingEngine()
_ORDERS: dict[str, dict[str, Any]] = {}
_IDEMPOTENCY_KEYS: dict[str, str] = {}
_RISK = RiskEngine()


def _metrics_store_path() -> str:
    return os.getenv("NEXORA_METRICS_STORE", "artifacts/runtime_metrics.json")


def _persist_metrics() -> None:
    path = _metrics_store_path()
    folder = os.path.dirname(path) or "."
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_METRICS, f)


async def app(scope: dict[str, Any], receive, send) -> None:
    started = time.time()
    request_id = str(uuid4())
    path = scope.get("path", "")
    method = scope.get("method", "GET")

    async def respond(status: int, payload: dict[str, Any], content_type: bytes = b"application/json") -> None:
        _METRICS["requests_total"] += 1
        if status >= 400:
            _METRICS["errors_total"] += 1
        _persist_metrics()
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
    if method == "GET" and path == "/v1/readiness":
        cfg = load_config()
        ready = bool(cfg.api_token)
        await respond(200 if ready else 503, {"ok": ready, "service": "nexora-prod-api"})
        return
    if method == "GET" and path == "/v1/info":
        await respond(
            200,
            {
                "ok": True,
                "service": "nexora-prod-api",
                "openapi_version": OPENAPI_DOC["openapi"],
                "api_doc_version": OPENAPI_DOC["info"]["version"],
            },
        )
        return
    if method == "GET" and path == "/metrics":
        body = (
            f"nexora_requests_total {_METRICS['requests_total']}\n"
            f"nexora_errors_total {_METRICS['errors_total']}\n"
        ).encode("utf-8")
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/plain; version=0.0.4")]})
        await send({"type": "http.response.body", "body": body})
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
    if method == "POST" and path == "/v1/orders":
        try:
            event = await receive()
            payload = json.loads(event.get("body", b"{}").decode("utf-8"))
            headers = dict(scope.get("headers", []))
            idem_key = headers.get(b"idempotency-key", b"").decode("utf-8").strip()
            side = str(payload.get("side", "")).upper()
            price = float(payload.get("price", 0))
            quantity = float(payload.get("quantity", 0))
            symbol = str(payload.get("symbol", ""))
            if not symbol:
                await problem(400, "Invalid Order", "symbol_required")
                return
            if idem_key and idem_key in _IDEMPOTENCY_KEYS:
                existing = _ORDERS.get(_IDEMPOTENCY_KEYS[idem_key])
                if existing:
                    await respond(200, {"ok": True, "order": existing, "idempotent_replay": True, "trades": []})
                    return
            risk = _RISK.evaluate(price * quantity)
            if not risk.approved:
                await problem(400, "Risk Rejected", risk.reason)
                return
            oid = str(uuid4())
            trades = _ENGINE.add_order(Order(order_id=oid, side=side, price=price, quantity=quantity))
            status = "filled" if not any(o.order_id == oid for o in (_ENGINE.buys + _ENGINE.sells)) else "open"
            _ORDERS[oid] = {"order_id": oid, "symbol": symbol, "side": side, "price": price, "quantity": quantity, "status": status}
            if idem_key:
                _IDEMPOTENCY_KEYS[idem_key] = oid
            await respond(201, {"ok": True, "order": _ORDERS[oid], "trades": [t.__dict__ for t in trades]})
        except ValueError as exc:
            await problem(400, "Invalid Order", str(exc))
        except Exception:
            await problem(400, "Invalid JSON", "Request payload could not be parsed")
        return
    if method == "GET" and path.startswith("/v1/orders/"):
        order_id = path.removeprefix("/v1/orders/")
        order = _ORDERS.get(order_id)
        if not order:
            await problem(404, "Not Found", "order_not_found")
            return
        await respond(200, {"ok": True, "order": order})
        return
    if method == "POST" and path.startswith("/v1/orders/") and path.endswith("/cancel"):
        order_id = path.removeprefix("/v1/orders/").removesuffix("/cancel")
        order = _ORDERS.get(order_id)
        if not order:
            await problem(404, "Not Found", "order_not_found")
            return
        if order["status"] == "filled":
            await problem(409, "Conflict", "order_already_filled")
            return
        order["status"] = "cancelled"
        await respond(200, {"ok": True, "order": order})
        return

    await problem(404, "Not Found", "Route does not exist")
