from ml_auto_learning_app.tooling import MarketDataAdapter


def test_tooling_fallback_for_unknown_symbol() -> None:
    adapter = MarketDataAdapter()
    quote = adapter.get_market_quote("AAPL", venue="AUTO")
    assert quote.symbol == "AAPL"
    assert quote.price > 0
    assert quote.venue in {"SIM", "BINANCE", "COINGECKO"}
