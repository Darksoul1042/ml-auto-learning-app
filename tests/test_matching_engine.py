from ml_auto_learning_app.matching_engine import MatchingEngine, Order


def test_simple_match() -> None:
    engine = MatchingEngine()
    engine.add_order(Order("b1", "BUY", 100, 2))
    trades = engine.add_order(Order("s1", "SELL", 99, 1))
    assert len(trades) == 1
    assert trades[0].quantity == 1
