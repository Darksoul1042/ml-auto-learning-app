from ml_auto_learning_app.risk_engine import RiskEngine


def test_risk_engine_approves_under_limit() -> None:
    risk = RiskEngine(max_notional_usd=1000)
    decision = risk.evaluate(500)
    assert decision.approved is True


def test_risk_engine_blocks_over_limit() -> None:
    risk = RiskEngine(max_notional_usd=1000)
    decision = risk.evaluate(1500)
    assert decision.approved is False
    assert decision.reason == "exceeds_max_notional"


def test_risk_engine_blocks_invalid_notional() -> None:
    risk = RiskEngine(max_notional_usd=1000)
    decision = risk.evaluate(0)
    assert decision.approved is False
    assert decision.reason == "invalid_notional"


def test_risk_engine_respects_kill_switch() -> None:
    risk = RiskEngine(max_notional_usd=1000, kill_switch=True)
    decision = risk.evaluate(100)
    assert decision.approved is False
    assert decision.reason == "kill_switch_enabled"
