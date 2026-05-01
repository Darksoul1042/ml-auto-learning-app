from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_generate_openapi_report_script_ok(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "openapi_snapshot.json").write_text(
        '{"openapi":"3.1.0","info":{"title":"NEXORA API","version":"1.0.0"},"paths":{"/v1/health":{"get":{"responses":{"200":{"description":"ok"}}}}}}',
        encoding="utf-8",
    )
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/generate_openapi_report.py")],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "OPENAPI_REPORT_OK:" in proc.stdout
    assert (tmp_path / "artifacts" / "openapi_contract_report.md").exists()
