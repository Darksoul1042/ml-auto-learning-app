from __future__ import annotations

import sqlite3


class TransactionService:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def process_order_ledger_audit(self, order_id: str, side: str, price: float, qty: float, action: str, payload: str) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("BEGIN")
            conn.execute("INSERT OR REPLACE INTO orders(id,side,price,qty,status) VALUES(?,?,?,?,?)", (order_id, side, price, qty, "new"))
            tx_id = f"tx_{order_id}"
            conn.execute("INSERT INTO ledger_entries(tx_id,account,amount,currency) VALUES(?,?,?,?)", (tx_id, "exchange", price * qty, "USD"))
            conn.execute("INSERT INTO audit_events(tx_id,action,payload) VALUES(?,?,?)", (tx_id, action, payload))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
