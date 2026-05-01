from ml_auto_learning_app.prod_auth_service import ProdAuthService
import base64
import hmac
import json
from hashlib import sha256


def test_issue_and_verify_token() -> None:
    svc = ProdAuthService(secret="x", ttl_seconds=60)
    token = svc.issue_token("alice").token
    payload = svc.verify_token(token)
    assert payload is not None
    assert payload["sub"] == "alice"


def test_requires_secret_when_not_configured(monkeypatch) -> None:
    monkeypatch.delenv("NEXORA_JWT_SECRET", raising=False)
    try:
        ProdAuthService()
        assert False, "expected ValueError when secret is missing"
    except ValueError as exc:
        assert "NEXORA_JWT_SECRET is required" in str(exc)


def test_revoked_token_fails_verification() -> None:
    svc = ProdAuthService(secret="x", ttl_seconds=60)
    token = svc.issue_token("alice").token
    assert svc.verify_token(token) is not None
    assert svc.revoke_token(token) is True
    assert svc.verify_token(token) is None


def test_rejects_token_with_future_iat() -> None:
    svc = ProdAuthService(secret="x", ttl_seconds=60, max_clock_skew_seconds=1)
    issued = svc.issue_token("alice").token
    encoded, _sig = issued.split(".", 1)
    payload = json.loads(base64.urlsafe_b64decode(encoded.encode("utf-8")).decode("utf-8"))
    payload["iat"] = payload["iat"] + 9999
    encoded2 = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    sig2 = hmac.new(b"x", encoded2.encode("utf-8"), sha256).hexdigest()
    forged = f"{encoded2}.{sig2}"
    assert svc.verify_token(forged) is None


def test_supports_key_rotation_keyset() -> None:
    keyset = {"k1": "old", "k2": "new"}
    svc_old = ProdAuthService(secret="old", keyset=keyset, active_kid="k1")
    token_old = svc_old.issue_token("alice").token
    svc_new = ProdAuthService(secret="new", keyset=keyset, active_kid="k2")
    assert svc_new.verify_token(token_old) is not None


def test_revocation_persists_across_instances(tmp_path) -> None:
    store = tmp_path / "revoked.json"
    svc1 = ProdAuthService(secret="x", revoked_store_path=str(store))
    token = svc1.issue_token("alice").token
    assert svc1.revoke_token(token) is True
    svc2 = ProdAuthService(secret="x", revoked_store_path=str(store))
    assert svc2.verify_token(token) is None
