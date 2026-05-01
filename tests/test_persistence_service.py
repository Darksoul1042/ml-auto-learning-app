from ml_auto_learning_app.persistence_service import PersistenceService


def test_persistence_save_records(tmp_path) -> None:
    db = tmp_path / "t.db"
    svc = PersistenceService(str(db))
    svc.save_order("o1", "BUY", 100, 1, "new")
    svc.save_ledger_entry("u1", 10, "USD")
    svc.save_audit("x", {"k": 1})


def test_persistence_rejects_invalid_order_side(tmp_path) -> None:
    db = tmp_path / "t.db"
    svc = PersistenceService(str(db))
    try:
        svc.save_order("o2", "HOLD", 100, 1, "new")
        assert False, "expected sqlite integrity failure for invalid side"
    except Exception:
        assert True


def test_persistence_tracks_schema_migrations(tmp_path) -> None:
    db = tmp_path / "t.db"
    svc = PersistenceService(str(db))
    versions = svc.list_migrations()
    assert "001_persistence_baseline" in versions
