from __future__ import annotations


class KMSProvider:
    """Placeholder integration point for external KMS/HSM."""

    def encrypt(self, plaintext: str) -> str:
        return f"kms://{plaintext}"

    def decrypt(self, ciphertext: str) -> str:
        return ciphertext.replace("kms://", "", 1)
