from __future__ import annotations

from dataclasses import dataclass
from hashlib import pbkdf2_hmac


@dataclass(frozen=True)
class CustodyRecord:
    user_id: str
    encrypted_seed: str


class CustodyService:
    def __init__(self, master_key: str) -> None:
        self.master_key = master_key.encode("utf-8")

    def encrypt_seed(self, user_id: str, seed_phrase: str) -> CustodyRecord:
        digest = pbkdf2_hmac("sha256", seed_phrase.encode("utf-8"), self.master_key + user_id.encode("utf-8"), 150_000)
        return CustodyRecord(user_id=user_id, encrypted_seed=digest.hex())
