from __future__ import annotations

import json
import os
import time
from collections import defaultdict, deque
from hmac import compare_digest
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .agent import FinancialAssistant
from .security_service import SecurityService
from .wallet_service import WalletService


class NexoraAPIHandler(BaseHTTPRequestHandler):
    assistant = FinancialAssistant()
    wallet_service = WalletService()
    security_service = SecurityService()
    _hits: dict[str, deque[float]] = defaultdict(deque)
    _window_seconds = 60
    _max_requests = 60

    def _send_json(self, code: int, payload: dict) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _authorized(self) -> bool:
        expected = os.getenv("NEXORA_API_TOKEN", "dev-token")
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
        if self._rate_limited():
            self._send_json(429, {"ok": False, "error": "rate_limited"})
            return

        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(200, {"ok": True, "service": "nexora-api"})
            return

        if not self._authorized():
            self._send_json(401, {"ok": False, "error": "unauthorized"})
            return

        params = parse_qs(parsed.query)

        if parsed.path == "/security/gsl/enable":
            user_id = params.get("user_id", [""])[0]
            hours, err = self._parse_int(params, "hours", 24)
            if err:
                self._send_json(400, {"ok": False, "error": err})
                return
            profile = self.security_service.enable_gsl(user_id=user_id, unlock_after_hours=hours if hours is not None else 24)
            self._send_json(200, {"ok": True, "gsl_enabled": profile.gsl_enabled, "unlock_after_hours": profile.gsl_unlock_after_hours})
            return

        if parsed.path == "/security/gsl/request-unlock":
            user_id = params.get("user_id", [""])[0]
            profile = self.security_service.request_gsl_unlock(user_id=user_id)
            self._send_json(200, {"ok": True, "gsl_unlock_requested_at": profile.gsl_unlock_requested_at})
            return

        if parsed.path == "/security/whitelist/add":
            user_id = params.get("user_id", [""])[0]
            address = params.get("address", [""])[0]
            profile = self.security_service.whitelist_address(user_id=user_id, address=address)
            self._send_json(200, {"ok": True, "count": len(profile.withdrawal_whitelist)})
            return

        if parsed.path == "/wallet/create":
            user_id = params.get("user_id", [""])[0]
            words, err = self._parse_int(params, "words", 12)
            if err:
                self._send_json(400, {"ok": False, "error": err})
                return
            reveal = params.get("reveal", ["false"])[0].lower() == "true"
            try:
                identity = self.wallet_service.create_wallet(user_id=user_id, words=words if words is not None else 12)
            except ValueError as exc:
                self._send_json(400, {"ok": False, "error": str(exc)})
                return
            payload = {"ok": True, "user_id": identity.user_id, "wallet_id": identity.wallet_id}
            if reveal:
                payload["mnemonic"] = identity.mnemonic
            self._send_json(200, payload)
            return

        if parsed.path == "/wallet/import":
            user_id = params.get("user_id", [""])[0]
            mnemonic = params.get("mnemonic", [""])[0]
            try:
                identity = self.wallet_service.import_wallet(user_id=user_id, mnemonic=mnemonic)
            except ValueError as exc:
                self._send_json(400, {"ok": False, "error": str(exc)})
                return
            self._send_json(200, {"ok": True, "user_id": identity.user_id, "wallet_id": identity.wallet_id})
            return

        if parsed.path == "/market/quote":
            symbol = params.get("symbol", [""])[0]
            notional, err = self._parse_float(params, "notional", 100.0)
            if err:
                self._send_json(400, {"ok": False, "error": err})
                return
            result = self.assistant.analyze(symbol=symbol, notional_usd=notional if notional is not None else 100.0)
            self._send_json(200, {"ok": result.ok, "message": result.message})
            return

        self._send_json(404, {"error": "not_found"})


def run_api_server(host: str = "127.0.0.1", port: int = 8081) -> None:
    server = HTTPServer((host, port), NexoraAPIHandler)
    print(f"NEXORA API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_api_server()
