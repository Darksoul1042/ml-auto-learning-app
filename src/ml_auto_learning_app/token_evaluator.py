from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenEvaluation:
    recommended: bool
    score: int
    summary: str


class TokenEvaluator:
    """Evaluate readiness for launching an exchange token."""

    def evaluate(self, has_kyc: bool, has_aml: bool, has_legal_opinion: bool, treasury_months: int) -> TokenEvaluation:
        score = 0
        score += 30 if has_kyc else 0
        score += 30 if has_aml else 0
        score += 25 if has_legal_opinion else 0
        score += 15 if treasury_months >= 18 else 0
        recommended = score >= 80
        summary = "Lanzamiento recomendado" if recommended else "Aún no recomendado"
        return TokenEvaluation(recommended=recommended, score=score, summary=summary)
