from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def test_generate_sbom_script_creates_artifact(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo-app"\nversion = "1.2.3"\n',
        encoding="utf-8",
    )
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = subprocess.run(
        ["python", str(repo_root / "scripts/generate_sbom.py")],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "SBOM_OK:" in proc.stdout
    sbom_path = tmp_path / "artifacts" / "sbom.json"
    data = json.loads(sbom_path.read_text(encoding="utf-8"))
    assert data["package"]["name"] == "demo-app"
    assert data["package"]["version"] == "1.2.3"
