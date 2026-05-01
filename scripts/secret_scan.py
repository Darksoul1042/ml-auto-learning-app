from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS access key id
    re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
]

ALLOWLIST = {"tests/"}


def is_allowed(path: Path) -> bool:
    s = str(path).replace("\\", "/")
    return any(s.startswith(prefix) for prefix in ALLOWLIST)


def main() -> int:
    root = Path(".")
    offenders: list[str] = []
    for p in root.rglob("*"):
        if not p.is_file() or is_allowed(p):
            continue
        if ".git/" in str(p):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for rx in PATTERNS:
            if rx.search(text):
                offenders.append(str(p))
                break

    if offenders:
        print("SECRET_SCAN_FAIL")
        for o in offenders:
            print(o)
        return 1
    print("SECRET_SCAN_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
