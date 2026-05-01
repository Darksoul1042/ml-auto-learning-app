from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ml_auto_learning_app.api.prod_app import OPENAPI_DOC


def main() -> int:
    snapshot = json.loads(Path("docs/openapi_snapshot.json").read_text(encoding="utf-8"))
    current = OPENAPI_DOC

    old_paths = set(snapshot.get("paths", {}).keys())
    new_paths = set(current.get("paths", {}).keys())
    added = sorted(new_paths - old_paths)
    removed = sorted(old_paths - new_paths)

    lines = ["# OpenAPI Contract Report", ""]
    lines.append(f"- Added routes: {', '.join(added) if added else 'none'}")
    lines.append(f"- Removed routes: {', '.join(removed) if removed else 'none'}")

    out_dir = Path("artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "openapi_contract_report.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OPENAPI_REPORT_OK:{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
