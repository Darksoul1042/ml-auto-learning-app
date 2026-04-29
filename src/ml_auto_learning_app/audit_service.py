from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class AuditEvent:
    trace_id: str
    timestamp_utc: str
    action: str
    payload: dict[str, Any]


class AuditService:
    def record(self, action: str, payload: dict[str, Any]) -> AuditEvent:
        return AuditEvent(
            trace_id=str(uuid4()),
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            action=action,
            payload=payload,
        )
