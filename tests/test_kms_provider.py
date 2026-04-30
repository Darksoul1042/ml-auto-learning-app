from __future__ import annotations

from ml_auto_learning_app.custody.kms_provider import KMSProvider


def test_kms_encrypt_decrypt_roundtrip() -> None:
    kms = KMSProvider(key="local-dev-key")
    token = kms.encrypt("secret-seed")
    assert token.startswith("kms://v1:")
    plain = kms.decrypt(token)
    assert plain == "secret-seed"


def test_kms_rejects_invalid_mac() -> None:
    kms = KMSProvider(key="local-dev-key")
    token = kms.encrypt("secret-seed")
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")
    try:
        kms.decrypt(tampered)
        assert False, "expected ValueError on invalid mac"
    except ValueError as exc:
        assert "invalid_mac" in str(exc)
