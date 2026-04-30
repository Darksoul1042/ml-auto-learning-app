from __future__ import annotations


def is_anomalous_login(new_country: str, last_country: str) -> bool:
    return new_country != last_country
