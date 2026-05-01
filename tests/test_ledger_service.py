from ml_auto_learning_app.ledger_service import LedgerService


def test_transfer_double_entry() -> None:
    ledger = LedgerService()
    ledger.transfer("u1", "u2", 10, "USD")
    assert ledger.balance("u1", "USD") == -10
    assert ledger.balance("u2", "USD") == 10
