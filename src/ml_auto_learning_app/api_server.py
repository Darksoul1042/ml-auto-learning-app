from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .agent import FinancialAssistant


class NexoraAPIHandler(BaseHTTPRequestHandler):
    assistant = FinancialAssistant()

    def _send_json(self, code: int, payload: dict) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(200, {"ok": True, "service": "nexora-api"})
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
