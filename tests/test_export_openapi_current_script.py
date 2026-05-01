from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def test_export_openapi_current_script_ok(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/export_openapi_current.py")],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "OPENAPI_EXPORT_OK:" in proc.stdout
    current = json.loads((tmp_path / "artifacts" / "openapi_current.json").read_text(encoding="utf-8"))
    assert "/v1/health" in current["paths"]
