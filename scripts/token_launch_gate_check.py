from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.token_gate_service import TokenGateService


def _read_bool_env(name: str) -> bool:
    value = os.getenv(name, "").strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


def _read_int_env(name: str, default: int = 0) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    return int(raw)


def main() -> None:
    gate = TokenGateService().evaluate(
        kyc=_read_bool_env("NEXORA_GATE_KYC"),
        aml=_read_bool_env("NEXORA_GATE_AML"),
        legal=_read_bool_env("NEXORA_GATE_LEGAL"),
        treasury_months=_read_int_env("NEXORA_GATE_TREASURY_MONTHS"),
        audit_passed=_read_bool_env("NEXORA_GATE_AUDIT_PASSED"),
    )
    print("GO" if gate.go else f"NO_GO:{','.join(gate.missing)}")


if __name__ == "__main__":
    main()
