from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuoteRequest:
    symbol: str
    notional: float


@dataclass(frozen=True)
class QuoteResponse:
    ok: bool
    message: str
