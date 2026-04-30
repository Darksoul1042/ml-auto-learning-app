from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateDecision:
    go: bool
    missing: list[str]


class TokenGateService:
    def evaluate(self, *, kyc: bool, aml: bool, legal: bool, treasury_months: int, audit_passed: bool) -> GateDecision:
        missing: list[str] = []
        if not kyc:
            missing.append("kyc")
        if not aml:
            missing.append("aml")
        if not legal:
            missing.append("legal")
        if treasury_months < 18:
            missing.append("treasury")
        if not audit_passed:
            missing.append("security_audit")
        return GateDecision(go=len(missing) == 0, missing=missing)
