from ml_auto_learning_app.api_server import NexoraAPIHandler


def test_handler_has_assistant() -> None:
    assert NexoraAPIHandler.assistant is not None


def test_handler_has_rate_limit_config() -> None:
    assert NexoraAPIHandler._max_requests > 0
    assert NexoraAPIHandler._window_seconds > 0


def test_parse_float_validation() -> None:
    value, err = NexoraAPIHandler._parse_float({"notional": ["abc"]}, "notional", 100.0)
    assert value is None
    assert err == "invalid_notional"


def test_parse_int_validation() -> None:
    value, err = NexoraAPIHandler._parse_int({"words": ["nope"]}, "words", 12)
    assert value is None
    assert err == "invalid_words"


def test_parse_int_allows_zero_value() -> None:
    value, err = NexoraAPIHandler._parse_int({"words": ["0"]}, "words", 12)
    assert err is None
    assert value == 0
