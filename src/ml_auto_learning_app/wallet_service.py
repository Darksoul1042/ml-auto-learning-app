from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from secrets import choice, token_hex

WORD_OPTIONS = (12, 25)

# Compact demo dictionary (replace with full BIP-39 list in production)
WORD_BANK = [
    "apple", "balance", "candle", "dragon", "energy", "forest", "galaxy", "harbor", "island", "jungle",
    "kitten", "legend", "matrix", "nebula", "orange", "planet", "quantum", "rocket", "silver", "thunder",
    "update", "velvet", "window", "xenon", "yellow", "zenith", "anchor", "binary", "crypto", "delta",
    "ember", "future", "golden", "horizon", "insight", "jacket", "kernel", "lunar", "magnet", "native",
]


@dataclass(frozen=True)
class WalletIdentity:
    user_id: str
    mnemonic: str
    wallet_id: str


class WalletService:
    def __init__(self) -> None:
        self._wallets: dict[str, str] = {}

    def create_wallet(self, user_id: str, words: int = 12) -> WalletIdentity:
        clean_user = user_id.strip().lower()
        if not clean_user:
            raise ValueError("user_id is required")
        if words not in WORD_OPTIONS:
            raise ValueError("words must be 12 or 25")

        mnemonic_words = [choice(WORD_BANK) for _ in range(words)]
        mnemonic = " ".join(mnemonic_words)
        wallet_id = sha256(f"{clean_user}:{mnemonic}".encode("utf-8")).hexdigest()[:16]
        self._wallets[clean_user] = wallet_id
        return WalletIdentity(user_id=clean_user, mnemonic=mnemonic, wallet_id=wallet_id)

    def get_wallet_id(self, user_id: str) -> str | None:
        return self._wallets.get(user_id.strip().lower())

    def import_wallet(self, user_id: str, mnemonic: str) -> WalletIdentity:
        clean_user = user_id.strip().lower()
        parts = [p.strip().lower() for p in mnemonic.split() if p.strip()]
        if len(parts) not in WORD_OPTIONS:
            raise ValueError("mnemonic must contain 12 or 25 words")
        wallet_id = sha256(f"{clean_user}:{' '.join(parts)}".encode("utf-8")).hexdigest()[:16]
        self._wallets[clean_user] = wallet_id
        return WalletIdentity(user_id=clean_user, mnemonic=' '.join(parts), wallet_id=wallet_id)
