from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_load_smoke_script_runs() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/load_smoke.py")],
        cwd=str(repo_root),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "LOAD_SMOKE_OK" in proc.stdout
