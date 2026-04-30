from __future__ import annotations

import base64
import hmac
import json
import os
import time
from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class AccessToken:
    token: str
    expires_at: int


class ProdAuthService:
    def __init__(self, secret: str | None = None, ttl_seconds: int = 3600) -> None:
        self.secret = (secret or os.getenv("NEXORA_JWT_SECRET", "dev-secret")).encode("utf-8")
        self.ttl_seconds = ttl_seconds

    def issue_token(self, user_id: str, role: str = "user") -> AccessToken:
        exp = int(time.time()) + self.ttl_seconds
        payload = {"sub": user_id, "role": role, "exp": exp}
        encoded = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        sig = hmac.new(self.secret, encoded.encode("utf-8"), sha256).hexdigest()
        return AccessToken(token=f"{encoded}.{sig}", expires_at=exp)

    def verify_token(self, token: str) -> dict | None:
        try:
            encoded, sig = token.split(".", 1)
            expected = hmac.new(self.secret, encoded.encode("utf-8"), sha256).hexdigest()
            if not hmac.compare_digest(sig, expected):
                return None
            payload = json.loads(base64.urlsafe_b64decode(encoded.encode("utf-8")).decode("utf-8"))
            if int(payload["exp"]) < int(time.time()):
                return None
            return payload
        except Exception:
            return None
