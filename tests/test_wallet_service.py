from ml_auto_learning_app.wallet_service import WalletService


def test_create_wallet_12_words() -> None:
    service = WalletService()
    identity = service.create_wallet("alice", words=12)
    assert len(identity.mnemonic.split()) == 12
    assert identity.wallet_id


def test_import_wallet_25_words() -> None:
    service = WalletService()
    mnemonic = " ".join(["apple"] * 25)
    identity = service.import_wallet("bob", mnemonic)
    assert identity.user_id == "bob"
    assert identity.wallet_id
