from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class MarketQuote:
    symbol: str
    price: float
    venue: str
    timestamp_utc: str


class MarketDataAdapter:
    """Stub adapter for market data.

    Replace this class with real providers (Binance, Yahoo, etc.).
    """

    def get_market_quote(self, symbol: str, venue: str = "SIM") -> MarketQuote:
        normalized_symbol = symbol.upper().strip()
        if not normalized_symbol:
            raise ValueError("symbol is required")

        # Deterministic demo price by symbol to make tests/replays stable.
        base = 60000.0 if "BTC" in normalized_symbol else 100.0
        offset = (sum(ord(c) for c in normalized_symbol) % 500) / 100
        price = round(base + offset, 2)

        return MarketQuote(
            symbol=normalized_symbol,
            price=price,
            venue=venue,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
