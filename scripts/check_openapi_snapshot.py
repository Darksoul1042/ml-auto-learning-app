from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ml_auto_learning_app.api.prod_app import OPENAPI_DOC


def main() -> int:
    snap_path = Path("docs/openapi_snapshot.json")
    expected = json.loads(snap_path.read_text(encoding="utf-8"))
    expected_paths = expected.get("paths", {})
    current_paths = OPENAPI_DOC.get("paths", {})

    removed_routes = sorted(set(expected_paths.keys()) - set(current_paths.keys()))
    breaking_ops: list[str] = []
    for route, methods in expected_paths.items():
        if route not in current_paths:
            continue
        for method in methods.keys():
            if method not in current_paths[route]:
                breaking_ops.append(f"{method.upper()} {route}")

    if removed_routes or breaking_ops:
        print("OPENAPI_SNAPSHOT_FAIL")
        if removed_routes:
            print("removed_routes:", ",".join(removed_routes))
        if breaking_ops:
            print("removed_operations:", ",".join(breaking_ops))
        return 1
    added_routes = sorted(set(current_paths.keys()) - set(expected_paths.keys()))
    if added_routes:
        print("OPENAPI_SNAPSHOT_OK_WITH_ADDITIONS")
        print("added_routes:", ",".join(added_routes))
    else:
        print("OPENAPI_SNAPSHOT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
