from __future__ import annotations

from .ledger_service import LedgerService


class ReconciliationService:
    def __init__(self, ledger: LedgerService) -> None:
        self.ledger = ledger

    def is_balanced(self, currency: str) -> bool:
        total = sum(e.amount for e in self.ledger.entries if e.currency == currency)
        return abs(total) < 1e-9
