from __future__ import annotations

import json
import subprocess
import sys


def test_token_publish_readiness_no_go_by_default() -> None:
    proc = subprocess.run([sys.executable, "scripts/token_publish_readiness.py"], capture_output=True, text=True)
    assert proc.returncode == 1
    payload = json.loads(proc.stdout)
    assert payload["go_live"] is False
    assert "kyc" in payload["missing"]


def test_token_publish_readiness_go_when_all_requirements_set(monkeypatch) -> None:
    monkeypatch.setenv("NEXORA_GATE_KYC", "true")
    monkeypatch.setenv("NEXORA_GATE_AML", "true")
    monkeypatch.setenv("NEXORA_GATE_LEGAL", "true")
    monkeypatch.setenv("NEXORA_GATE_TREASURY_MONTHS", "24")
    monkeypatch.setenv("NEXORA_GATE_AUDIT_PASSED", "true")
    proc = subprocess.run([sys.executable, "scripts/token_publish_readiness.py"], capture_output=True, text=True)
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["go_live"] is True
    assert payload["missing"] == []
