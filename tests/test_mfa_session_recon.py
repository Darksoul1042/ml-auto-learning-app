from ml_auto_learning_app.ledger_service import LedgerService
from ml_auto_learning_app.reconciliation_service import ReconciliationService
from ml_auto_learning_app.security.mfa_service import MFAService
from ml_auto_learning_app.security.session_service import SessionService


def test_mfa_code_cycle() -> None:
    mfa = MFAService("secret")
    code = mfa.generate_code()
    assert mfa.verify_code(code) is True


def test_session_create_revoke() -> None:
    svc = SessionService()
    sess = svc.create("u1", "d1")
    svc.revoke(sess.session_id)


def test_reconciliation_balanced() -> None:
    ledger = LedgerService()
    ledger.transfer("a", "b", 10, "USD")
    assert ReconciliationService(ledger).is_balanced("USD") is True
