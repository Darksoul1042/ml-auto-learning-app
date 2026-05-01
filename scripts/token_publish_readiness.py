from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.token_gate_service import TokenGateService


def _read_bool_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _read_int_env(name: str, default: int = 0) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def build_report() -> dict[str, object]:
    gate = TokenGateService().evaluate(
        kyc=_read_bool_env("NEXORA_GATE_KYC"),
        aml=_read_bool_env("NEXORA_GATE_AML"),
        legal=_read_bool_env("NEXORA_GATE_LEGAL"),
        treasury_months=_read_int_env("NEXORA_GATE_TREASURY_MONTHS"),
        audit_passed=_read_bool_env("NEXORA_GATE_AUDIT_PASSED"),
    )
    return {
        "go_live": gate.go,
        "missing": gate.missing,
        "checks": {
            "kyc_operational": "kyc" not in gate.missing,
            "aml_kyt_operational": "aml" not in gate.missing,
            "legal_opinion_approved": "legal" not in gate.missing,
            "treasury_months_gte_18": "treasury" not in gate.missing,
            "external_security_audit": "security_audit" not in gate.missing,
        },
        "solana_confidential_transfer_note": (
            "Solana docs indicate ZK ElGamal program is temporarily disabled on mainnet/devnet for audit; "
            "Confidential Transfer examples may not run there right now."
        ),
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["go_live"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
