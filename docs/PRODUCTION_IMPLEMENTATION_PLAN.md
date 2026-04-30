# Production Implementation Plan (NEXORA 100%)

## 1) Backend/API de producción (no demo)
### Ubicación
- `src/ml_auto_learning_app/api_server.py` -> reemplazar por `src/ml_auto_learning_app/api/v1_app.py`
- `src/ml_auto_learning_app/api/contracts.py`
- `src/ml_auto_learning_app/api/middleware.py`

### Entregables
- FastAPI/ASGI + workers (gunicorn/uvicorn)
- Endpoints REST `POST/PUT` con contratos estrictos
- Middleware de observabilidad/seguridad
- Manejo estandarizado de errores + versionado `/v1`

## 2) Base de datos y transacciones robustas
### Ubicación
- `src/ml_auto_learning_app/persistence_service.py` -> partir en `repositories/*`
- `migrations/` (Alembic)
- `src/ml_auto_learning_app/reconciliation_service.py`

### Entregables
- Migraciones formales + índices + constraints
- Flujo ACID order -> ledger -> audit
- Idempotencia global + reconciliación automática

## 3) Custodia real de llaves
### Ubicación
- `src/ml_auto_learning_app/custody_service.py` -> `src/ml_auto_learning_app/custody/`
- `src/ml_auto_learning_app/custody/kms_provider.py`
- `src/ml_auto_learning_app/custody/recovery_runbook.md`

### Entregables
- Integración KMS/HSM
- Cifrado por entorno y segregación de llaves
- Rotación/revocación de secretos
- Procedimientos de recuperación probados

## 4) Matching/Ledger nivel exchange
### Ubicación
- `src/ml_auto_learning_app/matching_engine.py`
- `src/ml_auto_learning_app/ledger_service.py`
- `src/ml_auto_learning_app/order_lifecycle_service.py`

### Entregables
- Estados de orden completos y auditables
- Concurrencia segura (locks/queues/event stream)
- Reconciliación intradía + cierre diario

## 5) Compliance productivo
### Ubicación
- `src/ml_auto_learning_app/compliance_service.py`
- `src/ml_auto_learning_app/compliance/providers/*.py`
- `src/ml_auto_learning_app/compliance/reporting.py`

### Entregables
- KYC/KYB real
- AML/KYT + sanciones en tiempo real
- Reglas jurisdiccionales + reporting legal

## 6) Seguridad operacional 24/7
### Ubicación
- `src/ml_auto_learning_app/security_service.py`
- `src/ml_auto_learning_app/security/session_service.py`
- `src/ml_auto_learning_app/security/mfa_service.py`

### Entregables
- MFA obligatoria
- Device/session management
- Alertas de fraude/anomalía
- WAF/anti-DDoS/pentesting continuo

## 7) UX completa exchange/wallet
### Ubicación
- `web/dashboard/`
- `web/orders/`
- `web/wallet/`

### Entregables
- Dashboard real-time de mercado
- Módulo completo de órdenes
- Depósitos/retiros on-chain
- Historial/estados transaccionales

## 8) Token NXR Gate formal en pipeline
### Ubicación
- `src/ml_auto_learning_app/token_gate_service.py`
- `ci/gates/token_launch_gate.yml`

### Entregables
- Auditoría externa de contratos/procesos
- Legal opinion multi-jurisdicción
- Treasury governance + Go/No-Go automatizado
