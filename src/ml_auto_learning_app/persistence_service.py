from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class PersistenceService:
    def __init__(self, db_path: str = "nexora_prod.db") -> None:
        self.db_path = Path(db_path)
        self._init()

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.db_path)
        c.row_factory = sqlite3.Row
        return c

    def _init(self) -> None:
        with self._conn() as c:
            c.execute(
                "CREATE TABLE IF NOT EXISTS orders ("
                "id TEXT PRIMARY KEY, "
                "side TEXT NOT NULL CHECK(side IN ('BUY','SELL')), "
                "price REAL NOT NULL CHECK(price > 0), "
                "qty REAL NOT NULL CHECK(qty > 0), "
                "status TEXT NOT NULL CHECK(length(status) > 0)"
                ")"
            )
            c.execute(
                "CREATE TABLE IF NOT EXISTS ledger ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "account TEXT NOT NULL CHECK(length(account) > 0), "
                "amount REAL NOT NULL, "
                "currency TEXT NOT NULL CHECK(length(currency) > 0)"
                ")"
            )
            c.execute(
                "CREATE TABLE IF NOT EXISTS audits ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "action TEXT NOT NULL CHECK(length(action) > 0), "
                "payload TEXT NOT NULL"
                ")"
            )

    def save_order(self, order_id: str, side: str, price: float, qty: float, status: str) -> None:
        with self._conn() as c:
            c.execute("INSERT OR REPLACE INTO orders(id,side,price,qty,status) VALUES(?,?,?,?,?)", (order_id, side, price, qty, status))

    def save_ledger_entry(self, account: str, amount: float, currency: str) -> None:
        with self._conn() as c:
            c.execute("INSERT INTO ledger(account,amount,currency) VALUES(?,?,?)", (account, amount, currency))

    def save_audit(self, action: str, payload: dict) -> None:
        with self._conn() as c:
            c.execute("INSERT INTO audits(action,payload) VALUES(?,?)", (action, json.dumps(payload)))
