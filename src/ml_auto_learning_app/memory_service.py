from __future__ import annotations


class MemoryService:
    def __init__(self) -> None:
        self._messages: list[str] = []

    def add(self, message: str) -> None:
        self._messages.append(message)

    def recent(self, n: int = 5) -> list[str]:
        return self._messages[-n:]
