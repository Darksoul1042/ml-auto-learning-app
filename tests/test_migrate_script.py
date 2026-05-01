from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_migrate_script_runs(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/migrate.py")],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "MIGRATIONS_OK:" in proc.stdout
