from __future__ import annotations

import base64
import hmac
import json
import os
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class AccessToken:
    token: str
    expires_at: int


class ProdAuthService:
    def __init__(
        self,
        secret: str | None = None,
        ttl_seconds: int = 3600,
        max_clock_skew_seconds: int = 30,
        keyset: dict[str, str] | None = None,
        active_kid: str = "k1",
        revoked_store_path: str | None = None,
    ) -> None:
        resolved_secret = secret if secret is not None else os.getenv("NEXORA_JWT_SECRET")
        if not resolved_secret:
            raise ValueError("NEXORA_JWT_SECRET is required")
        self.secret = resolved_secret.encode("utf-8")
        self.ttl_seconds = ttl_seconds
        self.max_clock_skew_seconds = max_clock_skew_seconds
        self.revoked_store_path = Path(revoked_store_path) if revoked_store_path else None
        self._revoked_jti: set[str] = self._load_revoked_jti()
        self.keyset = keyset or {active_kid: resolved_secret}
        self.active_kid = active_kid

    def _load_revoked_jti(self) -> set[str]:
        if not self.revoked_store_path or not self.revoked_store_path.exists():
            return set()
        try:
            data = json.loads(self.revoked_store_path.read_text(encoding="utf-8"))
            items = data if isinstance(data, list) else []
            return {str(x) for x in items if str(x)}
        except Exception:
            return set()

    def _persist_revoked_jti(self) -> None:
        if not self.revoked_store_path:
            return
        self.revoked_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.revoked_store_path.write_text(
            json.dumps(sorted(self._revoked_jti)),
            encoding="utf-8",
        )

    def issue_token(self, user_id: str, role: str = "user") -> AccessToken:
        now = int(time.time())
        exp = int(time.time()) + self.ttl_seconds
        payload = {"sub": user_id, "role": role, "exp": exp, "iat": now, "jti": str(uuid4()), "kid": self.active_kid}
        encoded = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        signing_secret = self.keyset[self.active_kid].encode("utf-8")
        sig = hmac.new(signing_secret, encoded.encode("utf-8"), sha256).hexdigest()
        return AccessToken(token=f"{encoded}.{sig}", expires_at=exp)

    def revoke_token(self, token: str) -> bool:
        payload = self.verify_token(token)
        if payload is None:
            return False
        jti = str(payload.get("jti", ""))
        if not jti:
            return False
        self._revoked_jti.add(jti)
        self._persist_revoked_jti()
        return True

    def verify_token(self, token: str) -> dict | None:
        try:
            encoded, sig = token.split(".", 1)
            payload = json.loads(base64.urlsafe_b64decode(encoded.encode("utf-8")).decode("utf-8"))
            kid = str(payload.get("kid", self.active_kid))
            key = self.keyset.get(kid)
            if not key:
                return None
            expected = hmac.new(key.encode("utf-8"), encoded.encode("utf-8"), sha256).hexdigest()
            if not hmac.compare_digest(sig, expected):
                return None
            now = int(time.time())
            if int(payload["exp"]) < int(time.time()):
                return None
            if int(payload.get("iat", 0)) > now + self.max_clock_skew_seconds:
                return None
            if str(payload.get("jti", "")) in self._revoked_jti:
                return None
            return payload
        except Exception:
            return None
