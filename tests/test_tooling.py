from ml_auto_learning_app.tooling import MarketDataAdapter


def test_tooling_fallback_for_unknown_symbol() -> None:
    adapter = MarketDataAdapter()
    quote = adapter.get_market_quote("AAPL", venue="AUTO")
    assert quote.symbol == "AAPL"
    assert quote.price > 0
    assert quote.venue in {"SIM", "BINANCE", "COINGECKO"}


def test_empty_symbol_raises() -> None:
    try:
        MarketDataAdapter().get_market_quote("")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "symbol is required" in str(exc)


def test_prod_disables_deterministic_fallback(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_ENV", "prod")
    try:
        MarketDataAdapter().get_market_quote("BTCUSDT", venue="UNSUPPORTED")
        assert False, "expected ValueError in prod when live provider is unavailable"
    except ValueError as exc:
        assert "live market data unavailable" in str(exc)
