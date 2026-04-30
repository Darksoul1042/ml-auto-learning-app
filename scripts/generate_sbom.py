from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    pyproject = Path("pyproject.toml")
    data = pyproject.read_text(encoding="utf-8")
    name = "unknown"
    version = "0.0.0"
    for line in data.splitlines():
        if line.strip().startswith("name ="):
            name = line.split("=", 1)[1].strip().strip('"')
        if line.strip().startswith("version ="):
            version = line.split("=", 1)[1].strip().strip('"')

    sbom = {
        "sbom_version": "0.1",
        "package": {"name": name, "version": version},
        "components": [
            {"name": name, "version": version, "type": "application"},
        ],
    }
    out = Path("artifacts")
    out.mkdir(parents=True, exist_ok=True)
    out_file = out / "sbom.json"
    out_file.write_text(json.dumps(sbom, indent=2), encoding="utf-8")
    print(f"SBOM_OK:{out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
