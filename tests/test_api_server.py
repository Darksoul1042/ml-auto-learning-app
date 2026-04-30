from ml_auto_learning_app.api_server import NexoraAPIHandler


def test_handler_has_assistant() -> None:
    assert NexoraAPIHandler.assistant is not None
