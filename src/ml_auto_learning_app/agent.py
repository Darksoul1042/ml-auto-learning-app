from __future__ import annotations

from dataclasses import dataclass

from .audit_service import AuditService
from .memory_service import MemoryService
from .risk_engine import RiskEngine
from .tooling import MarketDataAdapter


@dataclass(frozen=True)
class AssistantResponse:
    ok: bool
    message: str


class FinancialAssistant:
    def __init__(
        self,
        tooling: MarketDataAdapter | None = None,
        risk: RiskEngine | None = None,
        memory: MemoryService | None = None,
        audit: AuditService | None = None,
    ) -> None:
        self.tooling = tooling or MarketDataAdapter()
        self.risk = risk or RiskEngine()
        self.memory = memory or MemoryService()
        self.audit = audit or AuditService()

    def analyze(self, symbol: str, notional_usd: float) -> AssistantResponse:
        quote = self.tooling.get_market_quote(symbol)
        decision = self.risk.evaluate(notional_usd)

        event = self.audit.record(
            action="analyze_quote",
            payload={
                "symbol": quote.symbol,
                "price": quote.price,
                "notional_usd": notional_usd,
                "risk": decision.reason,
            },
        )
        self.memory.add(
            f"{quote.symbol}@{quote.price} risk={decision.reason} trace={event.trace_id}"
        )

        if not decision.approved:
            return AssistantResponse(
                ok=False,
                message=(
                    f"Operación bloqueada por riesgo: {decision.reason}. "
                    f"Precio actual {quote.symbol}: {quote.price} ({quote.venue})."
                ),
            )

        return AssistantResponse(
            ok=True,
            message=(
                f"Análisis listo para {quote.symbol}. "
                f"Precio actual: {quote.price} ({quote.venue}). "
                "Notional validado por risk_engine."
            ),
        )
