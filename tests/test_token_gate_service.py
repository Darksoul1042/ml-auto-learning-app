from ml_auto_learning_app.token_gate_service import TokenGateService


def test_gate_fails_when_missing_controls() -> None:
    d = TokenGateService().evaluate(kyc=True, aml=False, legal=False, treasury_months=6, audit_passed=False)
    assert d.go is False
    assert "aml" in d.missing


def test_gate_passes_with_all_controls() -> None:
    d = TokenGateService().evaluate(kyc=True, aml=True, legal=True, treasury_months=24, audit_passed=True)
    assert d.go is True
