from __future__ import annotations

import os
import subprocess


def test_prod_policy_check_passes_in_prod() -> None:
    env = {**os.environ, "PYTHONPATH": "src", "NEXORA_ENV": "prod"}
    proc = subprocess.run(["python", "scripts/prod_policy_check.py"], env=env, capture_output=True, text=True, check=False)
    assert proc.returncode == 0
    assert "POLICY_OK" in proc.stdout
