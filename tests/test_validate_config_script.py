from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_validate_config_script_staging_requires_secrets() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": "src", "NEXORA_ENV": "staging", "NEXORA_API_TOKEN": "x", "NEXORA_JWT_SECRET": "y"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/validate_config.py")],
        cwd=str(repo_root),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "CONFIG_OK:" in proc.stdout
