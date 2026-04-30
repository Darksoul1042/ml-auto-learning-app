from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.request import urlopen


@dataclass(frozen=True)
class MarketQuote:
    symbol: str
    price: float
    venue: str
    timestamp_utc: str


class MarketDataAdapter:
    """Hybrid adapter: tries real providers and falls back to deterministic demo."""

    def get_market_quote(self, symbol: str, venue: str = "AUTO") -> MarketQuote:
        normalized_symbol = symbol.upper().strip()
        if not normalized_symbol:
            raise ValueError("symbol is required")

        if venue in {"AUTO", "BINANCE"}:
            quote = self._fetch_binance(normalized_symbol)
            if quote:
                return quote

        if venue in {"AUTO", "COINGECKO"}:
            quote = self._fetch_coingecko(normalized_symbol)
            if quote:
                return quote

        if os.getenv("NEXORA_ENV", "dev").lower() == "prod":
            raise ValueError("live market data unavailable")
        return self._deterministic_fallback(normalized_symbol)

    def _fetch_binance(self, symbol: str) -> MarketQuote | None:
        try:
            with urlopen(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=2) as res:
                data = json.loads(res.read().decode("utf-8"))
            return MarketQuote(symbol=symbol, price=float(data["price"]), venue="BINANCE", timestamp_utc=self._now())
        except (URLError, TimeoutError, KeyError, ValueError):
            return None

    def _fetch_coingecko(self, symbol: str) -> MarketQuote | None:
        mapping = {"BTCUSDT": "bitcoin", "ETHUSDT": "ethereum"}
        coin_id = mapping.get(symbol)
        if not coin_id:
            return None
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
            with urlopen(url, timeout=2) as res:
                data = json.loads(res.read().decode("utf-8"))
            return MarketQuote(symbol=symbol, price=float(data[coin_id]["usd"]), venue="COINGECKO", timestamp_utc=self._now())
        except (URLError, TimeoutError, KeyError, ValueError):
            return None

    def _deterministic_fallback(self, symbol: str) -> MarketQuote:
        base = 60000.0 if "BTC" in symbol else 100.0
        offset = (sum(ord(c) for c in symbol) % 500) / 100
        return MarketQuote(symbol=symbol, price=round(base + offset, 2), venue="SIM", timestamp_utc=self._now())

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
