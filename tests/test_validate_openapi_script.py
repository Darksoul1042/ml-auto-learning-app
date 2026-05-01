from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_validate_openapi_script_ok() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/validate_openapi.py")],
        cwd=str(repo_root),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "OPENAPI_OK" in proc.stdout
