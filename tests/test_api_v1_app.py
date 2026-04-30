from ml_auto_learning_app.api.contracts import QuoteRequest
from ml_auto_learning_app.api.v1_app import handle_quote


def test_handle_quote_validation() -> None:
    assert handle_quote(QuoteRequest(symbol="", notional=100)).ok is False
    assert handle_quote(QuoteRequest(symbol="BTCUSDT", notional=0)).ok is False
    assert handle_quote(QuoteRequest(symbol="BTCUSDT", notional=100)).ok is True
