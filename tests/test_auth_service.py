from ml_auto_learning_app.auth_service import AuthService


def test_register_and_login_ok() -> None:
    auth = AuthService()
    auth.register_user("user@example.com", "Password123")
    result = auth.login("user@example.com", "Password123")
    assert result.ok is True
    assert result.session_token is not None
    assert auth.validate_session(result.session_token)


def test_login_invalid_password() -> None:
    auth = AuthService()
    auth.register_user("user@example.com", "Password123")
    result = auth.login("user@example.com", "wrong-password")
    assert result.ok is False
    assert result.message == "credenciales_invalidas"
