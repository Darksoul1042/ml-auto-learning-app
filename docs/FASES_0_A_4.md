# Implementación Fases 0 a 4 (NEXORA)

## Fase 0 — MVP seguro
- API local con token + rate limit
- Riesgo y auditoría
- Wallet demo 12/25 palabras

## Fase 1 — Core exchange
- Matching engine básico (`matching_engine.py`)
- Ledger doble entrada (`ledger_service.py`)

## Fase 2 — Compliance
- KYC/AML base (`compliance_service.py`)
- Bloqueo de países restringidos (demo)

## Fase 3 — Operación endurecida
- GSL + whitelist de retiro
- Política de exposición y kill-switch

## Fase 4 — Preparación de token
- Evaluador de readiness (`token_evaluator.py`)
- Requiere KYC, AML, legal opinion y tesorería
