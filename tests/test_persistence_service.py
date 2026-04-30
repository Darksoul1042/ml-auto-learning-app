from ml_auto_learning_app.persistence_service import PersistenceService


def test_persistence_save_records(tmp_path) -> None:
    db = tmp_path / "t.db"
    svc = PersistenceService(str(db))
    svc.save_order("o1", "BUY", 100, 1, "new")
    svc.save_ledger_entry("u1", 10, "USD")
    svc.save_audit("x", {"k": 1})
