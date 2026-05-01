from __future__ import annotations


class ComplianceService:
    def __init__(self) -> None:
        self.blocked_countries = {"NK", "IR"}

    def kyc_passed(self, full_name: str, id_number: str) -> bool:
        return bool(full_name.strip()) and len(id_number.strip()) >= 6

    def aml_allowed(self, country_code: str) -> bool:
        return country_code.upper() not in self.blocked_countries
