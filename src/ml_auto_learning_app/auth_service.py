from __future__ import annotations

from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from secrets import token_urlsafe


@dataclass(frozen=True)
class AuthResult:
    ok: bool
    message: str
    session_token: str | None = None


class AuthService:
    """In-memory auth service for MVP/demo.

    This service is intentionally simple and should be replaced with DB-backed
    auth + MFA + hardened session handling for production.
    """

    def __init__(self) -> None:
        self._users: dict[str, str] = {}
        self._sessions: dict[str, str] = {}

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        digest = pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000)
        return digest.hex()

    def register_user(self, identifier: str, password: str) -> None:
        clean_id = identifier.strip().lower()
        if not clean_id:
            raise ValueError("identifier is required")
        if len(password) < 8:
            raise ValueError("password must be at least 8 characters")
        self._users[clean_id] = self._hash_password(password=password, salt=clean_id)

    def login(self, identifier: str, password: str) -> AuthResult:
        clean_id = identifier.strip().lower()
        if clean_id not in self._users:
            return AuthResult(False, "usuario_no_encontrado")

        expected = self._users[clean_id]
        current = self._hash_password(password=password, salt=clean_id)
        if not compare_digest(expected, current):
            return AuthResult(False, "credenciales_invalidas")

        token = token_urlsafe(24)
        self._sessions[token] = clean_id
        return AuthResult(True, "login_ok", session_token=token)

    def validate_session(self, session_token: str) -> bool:
        return session_token in self._sessions
