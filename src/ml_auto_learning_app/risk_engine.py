from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskDecision:
    approved: bool
    reason: str


class RiskEngine:
    def __init__(self, max_notional_usd: float = 1000.0, kill_switch: bool = False) -> None:
        self.max_notional_usd = max_notional_usd
        self.kill_switch = kill_switch

    def evaluate(self, notional_usd: float) -> RiskDecision:
        if self.kill_switch:
            return RiskDecision(False, "kill_switch_enabled")
        if notional_usd <= 0:
            return RiskDecision(False, "invalid_notional")
        if notional_usd > self.max_notional_usd:
            return RiskDecision(False, "exceeds_max_notional")
        return RiskDecision(True, "approved")
