from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def test_check_runtime_alerts_ok(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    metrics = tmp_path / "m.json"
    metrics.write_text(json.dumps({"requests_total": 100, "errors_total": 10}), encoding="utf-8")
    env = {**os.environ, "NEXORA_METRICS_STORE": str(metrics), "NEXORA_MAX_ERROR_RATE": "0.2"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/check_runtime_alerts.py")],
        cwd=str(repo_root),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "ALERTS_OK" in proc.stdout
