from __future__ import annotations

import json
import logging
import os
import time
from uuid import uuid4
from collections import defaultdict, deque
from hmac import compare_digest
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .agent import FinancialAssistant
from .config import load_config
from .security_service import SecurityService
from .wallet_service import WalletService


class NexoraAPIHandler(BaseHTTPRequestHandler):
    assistant = FinancialAssistant()
    wallet_service = WalletService()
    security_service = SecurityService()
    logger = logging.getLogger("nexora.api_server")
    _hits: dict[str, deque[float]] = defaultdict(deque)
    _window_seconds = 60
    _max_requests = 60

    def _send_json(self, code: int, payload: dict, request_id: str | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-API-Version", "v1")
        if request_id:
            self.send_header("X-Request-Id", request_id)
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _authorized(self) -> bool:
        expected = os.getenv("NEXORA_API_TOKEN")
        if not expected:
            return False
        provided = self.headers.get("X-API-Token", "")
        return compare_digest(provided, expected)

    def _rate_limited(self) -> bool:
        client = self.client_address[0]
        now = time.time()
        q = self._hits[client]
        while q and now - q[0] > self._window_seconds:
            q.popleft()
        if len(q) >= self._max_requests:
            return True
        q.append(now)
        return False

    @staticmethod
    def _parse_int(params: dict[str, list[str]], key: str, default: int) -> tuple[int | None, str | None]:
        raw = params.get(key, [str(default)])[0]
        try:
            return int(raw), None
        except ValueError:
            return None, f"invalid_{key}"

    @staticmethod
    def _parse_float(params: dict[str, list[str]], key: str, default: float) -> tuple[float | None, str | None]:
        raw = params.get(key, [str(default)])[0]
        try:
            return float(raw), None
        except ValueError:
            return None, f"invalid_{key}"

    def do_GET(self) -> None:  # noqa: N802
        started_at = time.time()
        request_id = str(uuid4())

        def respond(code: int, payload: dict) -> None:
            payload = {**payload, "request_id": request_id, "api_version": "v1"}
            self._send_json(code, payload, request_id=request_id)
            self.logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "path": self.path,
                    "status": code,
                    "duration_ms": round((time.time() - started_at) * 1000, 2),
                },
            )

        if self._rate_limited():
            respond(429, {"ok": False, "error": "rate_limited"})
            return

        parsed = urlparse(self.path)
        if parsed.path == "/health":
            respond(200, {"ok": True, "service": "nexora-api"})
            return

        if not self._authorized():
            respond(401, {"ok": False, "error": "unauthorized"})
            return

        params = parse_qs(parsed.query)

        if parsed.path == "/security/gsl/enable":
            user_id = params.get("user_id", [""])[0]
            hours, err = self._parse_int(params, "hours", 24)
            if err:
                respond(400, {"ok": False, "error": err})
                return
            profile = self.security_service.enable_gsl(user_id=user_id, unlock_after_hours=hours if hours is not None else 24)
            respond(200, {"ok": True, "gsl_enabled": profile.gsl_enabled, "unlock_after_hours": profile.gsl_unlock_after_hours})
            return

        if parsed.path == "/security/gsl/request-unlock":
            user_id = params.get("user_id", [""])[0]
            profile = self.security_service.request_gsl_unlock(user_id=user_id)
            respond(200, {"ok": True, "gsl_unlock_requested_at": profile.gsl_unlock_requested_at})
            return

        if parsed.path == "/security/whitelist/add":
            user_id = params.get("user_id", [""])[0]
            address = params.get("address", [""])[0]
            profile = self.security_service.whitelist_address(user_id=user_id, address=address)
            respond(200, {"ok": True, "count": len(profile.withdrawal_whitelist)})
            return

        if parsed.path == "/wallet/create":
            user_id = params.get("user_id", [""])[0]
            words, err = self._parse_int(params, "words", 12)
            if err:
                respond(400, {"ok": False, "error": err})
                return
            reveal = params.get("reveal", ["false"])[0].lower() == "true"
            try:
                identity = self.wallet_service.create_wallet(user_id=user_id, words=words if words is not None else 12)
            except ValueError as exc:
                respond(400, {"ok": False, "error": str(exc)})
                return
            payload = {"ok": True, "user_id": identity.user_id, "wallet_id": identity.wallet_id}
            if reveal:
                payload["mnemonic"] = identity.mnemonic
            respond(200, payload)
            return

        if parsed.path == "/wallet/import":
            user_id = params.get("user_id", [""])[0]
            mnemonic = params.get("mnemonic", [""])[0]
            try:
                identity = self.wallet_service.import_wallet(user_id=user_id, mnemonic=mnemonic)
            except ValueError as exc:
                respond(400, {"ok": False, "error": str(exc)})
                return
            respond(200, {"ok": True, "user_id": identity.user_id, "wallet_id": identity.wallet_id})
            return

        if parsed.path == "/market/quote":
            symbol = params.get("symbol", [""])[0]
            notional, err = self._parse_float(params, "notional", 100.0)
            if err:
                respond(400, {"ok": False, "error": err})
                return
            if notional is None:
                respond(400, {"ok": False, "error": "invalid_notional"})
                return
            try:
                result = self.assistant.analyze(symbol=symbol, notional_usd=notional)
            except ValueError as exc:
                respond(400, {"ok": False, "error": str(exc)})
                return
            respond(200, {"ok": result.ok, "message": result.message})
            return

        respond(404, {"error": "not_found"})


def run_api_server(host: str = "127.0.0.1", port: int = 8081) -> None:
    load_config()
    server = HTTPServer((host, port), NexoraAPIHandler)
    print(f"NEXORA API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_api_server()
