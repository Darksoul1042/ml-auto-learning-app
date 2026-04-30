from __future__ import annotations


def build_jurisdiction_report(jurisdiction: str, events_count: int) -> dict:
    return {"jurisdiction": jurisdiction, "events": events_count, "status": "generated"}
