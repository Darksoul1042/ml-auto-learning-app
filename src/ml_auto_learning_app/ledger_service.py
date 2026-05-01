from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LedgerEntry:
    account: str
    amount: float
    currency: str


class LedgerService:
    def __init__(self) -> None:
        self.entries: list[LedgerEntry] = []

    def transfer(self, from_account: str, to_account: str, amount: float, currency: str) -> None:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self.entries.append(LedgerEntry(account=from_account, amount=-amount, currency=currency))
        self.entries.append(LedgerEntry(account=to_account, amount=amount, currency=currency))

    def balance(self, account: str, currency: str) -> float:
        return sum(e.amount for e in self.entries if e.account == account and e.currency == currency)
