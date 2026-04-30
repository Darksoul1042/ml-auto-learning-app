from __future__ import annotations

import json
import os
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .agent import FinancialAssistant
from .wallet_service import WalletService


class NexoraAPIHandler(BaseHTTPRequestHandler):
    assistant = FinancialAssistant()
    wallet_service = WalletService()
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
        return provided == expected

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

        if parsed.path == "/wallet/create":
            params = parse_qs(parsed.query)
            user_id = params.get("user_id", [""])[0]
            words = int(params.get("words", ["12"])[0])
            reveal = params.get("reveal", ["false"])[0].lower() == "true"
            try:
                identity = self.wallet_service.create_wallet(user_id=user_id, words=words)
            except ValueError as exc:
                self._send_json(400, {"ok": False, "error": str(exc)})
                return
            payload = {"ok": True, "user_id": identity.user_id, "wallet_id": identity.wallet_id}
            if reveal:
                payload["mnemonic"] = identity.mnemonic
            self._send_json(200, payload)
            return

        if parsed.path == "/wallet/import":
            params = parse_qs(parsed.query)
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
            params = parse_qs(parsed.query)
            symbol = params.get("symbol", [""])[0]
            notional = float(params.get("notional", ["100"])[0])
            result = self.assistant.analyze(symbol=symbol, notional_usd=notional)
            self._send_json(200, {"ok": result.ok, "message": result.message})
            return

        self._send_json(404, {"error": "not_found"})


def run_api_server(host: str = "127.0.0.1", port: int = 8081) -> None:
    server = HTTPServer((host, port), NexoraAPIHandler)
    print(f"NEXORA API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_api_server()
