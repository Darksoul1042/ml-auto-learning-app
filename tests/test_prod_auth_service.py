from ml_auto_learning_app.prod_auth_service import ProdAuthService


def test_issue_and_verify_token() -> None:
    svc = ProdAuthService(secret="x", ttl_seconds=60)
    token = svc.issue_token("alice").token
    payload = svc.verify_token(token)
    assert payload is not None
    assert payload["sub"] == "alice"
