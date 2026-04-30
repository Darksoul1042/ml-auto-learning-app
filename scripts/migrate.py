from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main() -> int:
    db_path = Path("nexora_prod.db")
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "version TEXT PRIMARY KEY, "
            "applied_at TEXT NOT NULL DEFAULT (datetime('now'))"
            ")"
        )
        conn.execute("INSERT OR IGNORE INTO schema_migrations(version) VALUES(?)", ("001_init_sql",))
        conn.commit()
    finally:
        conn.close()
    print(f"MIGRATIONS_OK:{db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
