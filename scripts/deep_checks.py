from __future__ import annotations

import json
import subprocess
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def request(url: str, token: str | None = None) -> tuple[int, dict]:
    req = Request(url)
    if token:
        req.add_header("X-API-Token", token)
    try:
        with urlopen(req, timeout=3) as res:
            return res.status, json.loads(res.read().decode("utf-8"))
    except HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def main() -> None:
    proc = subprocess.Popen(
        ["python", "-m", "ml_auto_learning_app.api_server"],
        env={**__import__("os").environ, "NEXORA_API_TOKEN": "dev-token", "PYTHONPATH": "src"},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    try:
        code, body = request("http://127.0.0.1:8081/health")
        assert code == 200 and body.get("ok") is True

        code, body = request("http://127.0.0.1:8081/market/quote?symbol=BTCUSDT&notional=100", token="wrong")
        assert code == 401 and body.get("error") == "unauthorized"

        code, body = request("http://127.0.0.1:8081/market/quote?symbol=BTCUSDT&notional=100", token="dev-token")
        assert code == 200 and body.get("ok") is True

        code, body = request("http://127.0.0.1:8081/wallet/create?user_id=alice&words=12", token="dev-token")
        assert code == 200 and "wallet_id" in body

        print("DEEP_CHECKS_OK")
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    main()
