"""ASGI-ready API placeholder.

This module is the target replacement for demo HTTPServer.
"""

from __future__ import annotations

from .contracts import QuoteRequest, QuoteResponse


def handle_quote(req: QuoteRequest) -> QuoteResponse:
    if not req.symbol.strip():
        return QuoteResponse(ok=False, message="symbol_required")
    if req.notional <= 0:
        return QuoteResponse(ok=False, message="invalid_notional")
    return QuoteResponse(ok=True, message="accepted")
