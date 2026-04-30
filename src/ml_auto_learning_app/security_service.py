from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class SecurityProfile:
    user_id: str
    gsl_enabled: bool = False
    gsl_unlock_requested_at: str | None = None
    gsl_unlock_after_hours: int = 24
    withdrawal_whitelist: set[str] = field(default_factory=set)


class SecurityService:
    """Exchange-inspired controls: Global Settings Lock + withdrawal whitelist."""

    def __init__(self) -> None:
        self._profiles: dict[str, SecurityProfile] = {}

    def get_profile(self, user_id: str) -> SecurityProfile:
        key = user_id.strip().lower()
        if key not in self._profiles:
            self._profiles[key] = SecurityProfile(user_id=key)
        return self._profiles[key]

    def enable_gsl(self, user_id: str, unlock_after_hours: int = 24) -> SecurityProfile:
        profile = self.get_profile(user_id)
        profile.gsl_enabled = True
        profile.gsl_unlock_after_hours = max(24, unlock_after_hours)
        profile.gsl_unlock_requested_at = None
        return profile

    def request_gsl_unlock(self, user_id: str) -> SecurityProfile:
        profile = self.get_profile(user_id)
        if not profile.gsl_enabled:
            return profile
        profile.gsl_unlock_requested_at = datetime.now(timezone.utc).isoformat()
        return profile

    def can_modify_settings(self, user_id: str) -> bool:
        profile = self.get_profile(user_id)
        if not profile.gsl_enabled:
            return True
        if not profile.gsl_unlock_requested_at:
            return False

        requested = datetime.fromisoformat(profile.gsl_unlock_requested_at)
        unlock_time = requested + timedelta(hours=profile.gsl_unlock_after_hours)
        return datetime.now(timezone.utc) >= unlock_time

    def whitelist_address(self, user_id: str, address: str) -> SecurityProfile:
        profile = self.get_profile(user_id)
        profile.withdrawal_whitelist.add(address.strip())
        return profile

    def is_address_whitelisted(self, user_id: str, address: str) -> bool:
        profile = self.get_profile(user_id)
        return address.strip() in profile.withdrawal_whitelist
