from __future__ import annotations

import argparse

from .agent import FinancialAssistant
from .risk_engine import RiskEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Asistente IA financiero (demo ejecutable)")
    parser.add_argument("--symbol", required=True, help="Símbolo, por ejemplo BTCUSDT o AAPL")
    parser.add_argument("--notional", type=float, default=100.0, help="Monto nocional en USD")
    parser.add_argument("--max-notional", type=float, default=1000.0, help="Límite máximo permitido por risk engine")
    parser.add_argument("--kill-switch", action="store_true", help="Bloquea cualquier operación")
    args = parser.parse_args()

    assistant = FinancialAssistant(
        risk=RiskEngine(max_notional_usd=args.max_notional, kill_switch=args.kill_switch)
    )
    response = assistant.analyze(symbol=args.symbol, notional_usd=args.notional)
    print(response.message)


if __name__ == "__main__":
    main()
