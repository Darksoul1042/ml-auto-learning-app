from ml_auto_learning_app.api.v1_app import handle_quote
from ml_auto_learning_app.api.contracts import QuoteRequest
from ml_auto_learning_app.compliance.reporting import build_jurisdiction_report
from ml_auto_learning_app.security.anomaly_service import is_anomalous_login


def test_v1_quote_contract() -> None:
    resp = handle_quote(QuoteRequest(symbol="BTCUSDT", notional=100))
    assert resp.ok is True


def test_reporting() -> None:
    report = build_jurisdiction_report("US", 10)
    assert report["status"] == "generated"


def test_anomaly() -> None:
    assert is_anomalous_login("US", "CA") is True
