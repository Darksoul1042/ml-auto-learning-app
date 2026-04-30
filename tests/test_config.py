from ml_auto_learning_app.config import load_config


def test_load_config_dev_defaults(monkeypatch) -> None:
    monkeypatch.delenv("NEXORA_ENV", raising=False)
    monkeypatch.delenv("NEXORA_API_TOKEN", raising=False)
    monkeypatch.delenv("NEXORA_JWT_SECRET", raising=False)
    c = load_config()
    assert c.env == "dev"
    assert c.allow_demo_fallbacks is True


def test_load_config_prod_requires_secrets(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "prod")
    monkeypatch.delenv("NEXORA_API_TOKEN", raising=False)
    monkeypatch.delenv("NEXORA_JWT_SECRET", raising=False)
    try:
        load_config()
        assert False, "expected ValueError for missing prod secrets"
    except ValueError as exc:
        assert "NEXORA_API_TOKEN is required" in str(exc)
