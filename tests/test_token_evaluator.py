from ml_auto_learning_app.token_evaluator import TokenEvaluator


def test_token_evaluation_not_ready() -> None:
    ev = TokenEvaluator().evaluate(False, True, False, 6)
    assert ev.recommended is False


def test_token_evaluation_ready() -> None:
    ev = TokenEvaluator().evaluate(True, True, True, 24)
    assert ev.recommended is True
