from __future__ import annotations

import base64
import hashlib
import hmac
import os
from secrets import token_bytes


class KMSProvider:
    """Local cryptographic envelope helper.

    Note: This is an interim software-only mechanism and should be replaced with
    managed KMS/HSM for production custody workloads.
    """

    def __init__(self, key: str | None = None) -> None:
        raw_key = key if key is not None else os.getenv("NEXORA_KMS_KEY", "")
        if not raw_key:
            raise ValueError("NEXORA_KMS_KEY is required")
        self._key = raw_key.encode("utf-8")

    def encrypt(self, plaintext: str) -> str:
        nonce = token_bytes(16)
        keystream = hashlib.sha256(self._key + nonce).digest()
        plain_bytes = plaintext.encode("utf-8")
        cipher = bytes([plain_bytes[i] ^ keystream[i % len(keystream)] for i in range(len(plain_bytes))])
        mac = hmac.new(self._key, nonce + cipher, hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(nonce + mac + cipher).decode("utf-8")
        return f"kms://v1:{token}"

    def decrypt(self, ciphertext: str) -> str:
        if not ciphertext.startswith("kms://v1:"):
            raise ValueError("unsupported_ciphertext")
        token = ciphertext.split("kms://v1:", 1)[1]
        payload = base64.urlsafe_b64decode(token.encode("utf-8"))
        nonce, mac, cipher = payload[:16], payload[16:48], payload[48:]
        expected = hmac.new(self._key, nonce + cipher, hashlib.sha256).digest()
        if not hmac.compare_digest(mac, expected):
            raise ValueError("invalid_mac")
        keystream = hashlib.sha256(self._key + nonce).digest()
        plain = bytes([cipher[i] ^ keystream[i % len(keystream)] for i in range(len(cipher))])
        return plain.decode("utf-8")
