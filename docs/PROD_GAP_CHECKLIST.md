# Production Gap Checklist

## API
- [ ] FastAPI/ASGI
- [ ] Versionado `/v1`
- [ ] Contratos request/response
- [ ] Middleware tracing/security

## Data
- [ ] Migraciones formales
- [ ] Constraints + índices
- [ ] ACID order->ledger->audit
- [ ] Idempotencia global

## Custody
- [ ] KMS/HSM
- [ ] Rotación llaves
- [ ] Revocación secretos
- [ ] Recovery drill

## Exchange Core
- [ ] Estados orden completos
- [ ] Concurrencia segura
- [ ] Reconciliación intradía
- [ ] Cierre diario

## Compliance
- [ ] KYC/KYB proveedor real
- [ ] AML/KYT
- [ ] Sanciones en tiempo real
- [ ] Reporting por jurisdicción

## Security 24/7
- [ ] MFA obligatoria
- [ ] Device/session mgmt
- [ ] Anti-fraude
- [ ] WAF + DDoS + pentest

## UX
- [ ] Dashboard real-time
- [ ] Órdenes completas
- [ ] Depósitos/retiros on-chain
- [ ] Historial transaccional

## Token
- [ ] Auditoría externa
- [ ] Legal opinion
- [ ] Treasury governance
- [ ] Gate automatizado GO/NO-GO
