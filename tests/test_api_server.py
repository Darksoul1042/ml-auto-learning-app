from ml_auto_learning_app.api_server import NexoraAPIHandler


def test_handler_has_assistant() -> None:
    assert NexoraAPIHandler.assistant is not None


def test_handler_has_rate_limit_config() -> None:
    assert NexoraAPIHandler._max_requests > 0
    assert NexoraAPIHandler._window_seconds > 0
