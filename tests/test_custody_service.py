from ml_auto_learning_app.custody_service import CustodyService


def test_encrypt_seed_generates_digest() -> None:
    c = CustodyService(master_key="mk")
    rec = c.encrypt_seed("alice", "one two three")
    assert len(rec.encrypted_seed) > 20
