from __future__ import annotations

import os
import subprocess


def test_token_launch_gate_check_exits_non_zero_on_no_go() -> None:
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(["python", "scripts/token_launch_gate_check.py"], env=env, capture_output=True, text=True, check=False)
    assert proc.returncode == 1
    assert "NO_GO:" in proc.stdout


def test_token_launch_gate_check_exits_zero_on_go() -> None:
    env = {
        **os.environ,
        "PYTHONPATH": "src",
        "NEXORA_GATE_KYC": "true",
        "NEXORA_GATE_AML": "true",
        "NEXORA_GATE_LEGAL": "true",
        "NEXORA_GATE_TREASURY_MONTHS": "24",
        "NEXORA_GATE_AUDIT_PASSED": "true",
    }
    proc = subprocess.run(["python", "scripts/token_launch_gate_check.py"], env=env, capture_output=True, text=True, check=False)
    assert proc.returncode == 0
    assert proc.stdout.strip() == "GO"
