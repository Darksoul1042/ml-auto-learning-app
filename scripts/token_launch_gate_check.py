from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.token_gate_service import TokenGateService


def main() -> None:
    gate = TokenGateService().evaluate(kyc=True, aml=True, legal=True, treasury_months=24, audit_passed=True)
    print("GO" if gate.go else f"NO_GO:{','.join(gate.missing)}")


if __name__ == "__main__":
    main()
