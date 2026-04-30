from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    side: str  # BUY | SELL
    price: float
    quantity: float


@dataclass
class Trade:
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: float


class MatchingEngine:
    """Simple FIFO-like price matching for MVP progression."""

    def __init__(self) -> None:
        self.buys: list[Order] = []
        self.sells: list[Order] = []

    def add_order(self, order: Order) -> list[Trade]:
        if order.side == "BUY":
            self.buys.append(order)
            self.buys.sort(key=lambda o: o.price, reverse=True)
        elif order.side == "SELL":
            self.sells.append(order)
            self.sells.sort(key=lambda o: o.price)
        else:
            raise ValueError("side must be BUY or SELL")
        return self._match()

    def _match(self) -> list[Trade]:
        trades: list[Trade] = []
        while self.buys and self.sells and self.buys[0].price >= self.sells[0].price:
            buy = self.buys[0]
            sell = self.sells[0]
            qty = min(buy.quantity, sell.quantity)
            trades.append(Trade(buy.order_id, sell.order_id, sell.price, qty))
            buy.quantity -= qty
            sell.quantity -= qty
            if buy.quantity <= 0:
                self.buys.pop(0)
            if sell.quantity <= 0:
                self.sells.pop(0)
        return trades
