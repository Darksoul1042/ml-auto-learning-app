from __future__ import annotations

from dataclasses import dataclass
from secrets import token_urlsafe


@dataclass(frozen=True)
class Session:
    session_id: str
    user_id: str
    device_id: str


class SessionService:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(self, user_id: str, device_id: str) -> Session:
        s = Session(session_id=token_urlsafe(20), user_id=user_id, device_id=device_id)
        self._sessions[s.session_id] = s
        return s

    def revoke(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
