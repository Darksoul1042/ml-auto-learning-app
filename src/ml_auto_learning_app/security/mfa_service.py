from __future__ import annotations

import hmac
import time
from hashlib import sha1


class MFAService:
    def __init__(self, secret: str) -> None:
        self.secret = secret.encode("utf-8")

    def generate_code(self, timestep: int | None = None) -> str:
        step = int((timestep or time.time()) // 30)
        digest = hmac.new(self.secret, str(step).encode("utf-8"), sha1).hexdigest()
        return str(int(digest[-6:], 16) % 1_000_000).zfill(6)

    def verify_code(self, code: str) -> bool:
        return code == self.generate_code() or code == self.generate_code(time.time() - 30)
