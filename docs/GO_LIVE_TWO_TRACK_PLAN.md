# NEXORA Token Go-Live Plan (2 Tracks)

Fecha de elaboración: 2026-05-01

## Objetivo

Pasar de estado **NO_GO** a **GO** de forma controlada, trazable y auditable, separando:

- **Track A**: activación on-chain de Solana Confidential Transfer (CT).
- **Track B**: publicación regulatoria/operativa del token NEXORA.

---

## Track A — Solana Confidential Transfer (on-chain)

### A0. Precondición de red

1. Verificar estado oficial del programa ZK ElGamal y soporte CT en la red objetivo.
2. Definir red objetivo inicial (`devnet` o `mainnet-beta`) y ventana de activación.
3. Mantener feature-flag `NEXORA_ENABLE_CONFIDENTIAL_TRANSFER=false` hasta confirmación formal.

**Evidencia mínima**
- Captura/registro de estado de red y decisión aprobada por arquitectura.
- Ticket de cambio con fecha/hora de activación.

### A1. Provisionamiento y cuentas base

1. Preparar payer/custodia y políticas de firma.
2. Crear mint Token-2022 con extensión CT habilitada.
3. Crear token account destino (ATA).
4. Ejecutar flujo de cuenta CT:
   - `Create` ATA,
   - `Reallocate` para `ConfidentialTransferAccount`,
   - `ConfigureAccount`.

**Evidencia mínima**
- Dirección del mint, owner, account y tx signatures.
- Log de configuración de cuenta confidencial.

### A2. Flujo de fondos confidenciales

1. Depositar tokens al balance pending (`deposit-tokens`).
2. Aplicar balance pendiente (`apply-pending-balance`).
3. Verificar consistencia de balance disponible vs. pending.

**Evidencia mínima**
- Tx signatures de deposit/apply.
- Snapshot antes/después de balances.

### A3. Hardening técnico

1. Reintentos idempotentes por operación crítica.
2. Alertas de fallos de confirmación y latencia de finalización.
3. Runbook de rollback (desactivar CT y fallback a token estándar si procede).

**Evidencia mínima**
- Resultado de pruebas de resiliencia.
- Runbook aprobado por SRE + Seguridad.

### A4. Gate Track A

**GO-A** solo si:
- Red soporta CT oficialmente.
- Flujo create/reallocate/configure validado.
- Flujo deposit/apply validado.
- Monitoreo + rollback listos.

---

## Track B — Publicación token NEXORA (compliance + seguridad)

### B0. Requisitos de gate (obligatorios)

1. KYC operativo real.
2. AML/KYT operativo real.
3. Opinión legal aprobada por jurisdicción.
4. Tesorería >= 18 meses demostrable.
5. Auditoría externa de seguridad cerrada.

**Evidencia mínima**
- Contratos/proveedor KYC-KYT activos.
- Informe legal firmado.
- Informe treasury aprobado por finanzas.
- Informe de auditoría externa + remediaciones cerradas.

### B1. Implementación operativa

1. Activar proveedores de compliance en producción.
2. Integrar revisión de sanciones/listas en onboarding y transacciones.
3. Establecer comité de riesgo y protocolo de freeze/emergencia.
4. Definir playbooks de incidentes regulatorios.

### B2. Controles de seguridad

1. Gestión de llaves y secretos con KMS/HSM.
2. Rotación de secretos y segregación por entorno.
3. Monitoreo 24/7 (SIEM/alertas críticas).
4. Pentest final y validación de remediaciones.

### B3. Gate Track B

**GO-B** solo si los 5 checks de `token_publish_readiness.py` están en true y la salida devuelve:

```json
{
  "go_live": true,
  "missing": []
}
```

---

## Cronograma sugerido (6 semanas)

### Semana 1–2
- Cerrar B0 (compliance/legal/treasury/auditoría) con responsables y evidencias.
- Preparar A0-A1 en entorno de prueba.

### Semana 3–4
- Ejecutar A2-A3 y pruebas de resiliencia.
- Cerrar B1 y validaciones cruzadas Compliance/Security.

### Semana 5
- Cerrar B2 (hardening seguridad + remediaciones finales).
- Dry-run de go-live con comité.

### Semana 6
- Ventana de go-live:
  - aprobar GO-A y GO-B,
  - activar feature flags,
  - monitoreo reforzado 72h.

---

## Criterio final de salida

Solo se publica cuando ambos gates estén en verde:

- `GO-A = true` (track técnico on-chain).
- `GO-B = true` (track regulatorio/seguridad).

Si cualquiera falla: **NO_GO** y se ejecuta rollback/control de cambios.
