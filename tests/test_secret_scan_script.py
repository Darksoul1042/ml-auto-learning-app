from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_secret_scan_passes_clean_tree(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/secret_scan.py")],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "SECRET_SCAN_OK" in proc.stdout


def test_secret_scan_detects_key_pattern(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    f = tmp_path / "leak.txt"
    f.write_text('api_key = "abcdefghijklmnopqrstuvwxyz1234"', encoding="utf-8")
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/secret_scan.py")],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "SECRET_SCAN_FAIL" in proc.stdout
