from __future__ import annotations


class RealtimeComplianceProvider:
    def sanctions_ok(self, wallet: str) -> bool:
        # Placeholder for real API integration
        return not wallet.lower().startswith("sanctioned")
