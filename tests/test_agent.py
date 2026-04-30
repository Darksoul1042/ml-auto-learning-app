from ml_auto_learning_app.agent import FinancialAssistant
from ml_auto_learning_app.risk_engine import RiskEngine


def test_analyze_ok_flow() -> None:
    assistant = FinancialAssistant(risk=RiskEngine(max_notional_usd=1000))
    result = assistant.analyze("AAPL", 100)
    assert result.ok is True
    assert "AAPL" in result.message


def test_analyze_blocked_flow() -> None:
    assistant = FinancialAssistant(risk=RiskEngine(max_notional_usd=10))
    result = assistant.analyze("AAPL", 100)
    assert result.ok is False
    assert "bloqueada" in result.message.lower()
