# Sprint Board NXR (4–6 semanas)

## Sprint 1 — API prod-ready + Auth real

### NXR-101 — Migrar API demo a FastAPI
- **Descripción:** reemplazar `HTTPServer` por FastAPI con rutas versionadas `/v1/*`, validación Pydantic y docs OpenAPI.
- **Criterios de aceptación:**
  1. API levantada con `uvicorn`.
  2. `/docs` y `/openapi.json` accesibles.
  3. Endpoints actuales migrados y testeados.
- **Story points:** 8
- **Dependencias:** ninguna.

### NXR-102 — Auth JWT access/refresh
- **Descripción:** implementar login con access token (corto) + refresh token (rotación).
- **Criterios de aceptación:**
  1. Endpoint `/v1/auth/login` emite access+refresh.
  2. Endpoint `/v1/auth/refresh` rota refresh.
  3. Revocación de sesión funcional.
- **Story points:** 8
- **Dependencias:** NXR-101.

### NXR-103 — Rate limiting distribuido
- **Descripción:** mover rate limit en memoria a backend Redis por IP/user.
- **Criterios de aceptación:**
  1. Límite configurable por endpoint.
  2. Respuesta 429 consistente.
  3. Métricas de throttling expuestas.
- **Story points:** 5
- **Dependencias:** NXR-101.

### NXR-104 — Observabilidad base
- **Descripción:** logs estructurados + trace_id + métricas HTTP.
- **Criterios de aceptación:**
  1. Todos los requests incluyen trace_id.
  2. Métricas de latencia por ruta.
  3. Errores 5xx alertables.
- **Story points:** 5
- **Dependencias:** NXR-101.

---

## Sprint 2 — Persistencia robusta + Matching/Ledger

### NXR-201 — Modelo SQL formal (orders/ledger/audit)
- **Descripción:** normalizar esquema y constraints (PK/FK/unique/check).
- **Criterios de aceptación:**
  1. Migraciones versionadas.
  2. Constraints activas en tablas críticas.
  3. Tests de integridad DB.
- **Story points:** 8
- **Dependencias:** NXR-101.

### NXR-202 — Idempotencia de órdenes
- **Descripción:** agregar `idempotency_key` en creación de órdenes y ejecución.
- **Criterios de aceptación:**
  1. Requests duplicados no generan doble orden.
  2. Respuesta consistente en reintentos.
  3. Cobertura de tests de concurrencia.
- **Story points:** 8
- **Dependencias:** NXR-201.

### NXR-203 — Ledger doble entrada transaccional
- **Descripción:** aplicar transacciones atómicas para asientos contables.
- **Criterios de aceptación:**
  1. No existen asientos huérfanos.
  2. Balance neto por operación = 0.
  3. Rollback correcto ante error.
- **Story points:** 8
- **Dependencias:** NXR-201.

### NXR-204 — Reconciliación automática
- **Descripción:** job periódico que verifica consistencia orders/ledger/audit.
- **Criterios de aceptación:**
  1. Reporte diario de reconciliación.
  2. Alertas en discrepancias.
  3. Evidencia almacenada de ejecución.
- **Story points:** 5
- **Dependencias:** NXR-202, NXR-203.

---

## Sprint 3 — Custodia, Compliance y Go/No-Go token

### NXR-301 — Custodia segura con KMS/HSM
- **Descripción:** reemplazar custodia MVP por cifrado gestionado con KMS/HSM.
- **Criterios de aceptación:**
  1. Semillas no se almacenan en claro.
  2. Rotación de llaves documentada.
  3. Accesos auditados.
- **Story points:** 13
- **Dependencias:** NXR-201.

### NXR-302 — Integración KYC/KYB
- **Descripción:** conectar proveedor externo de identidad y estados de verificación.
- **Criterios de aceptación:**
  1. Flujo KYC completo en API.
  2. Estado persistido por usuario.
  3. Bloqueo de operaciones sin KYC aprobado.
- **Story points:** 8
- **Dependencias:** NXR-101, NXR-201.

### NXR-303 — Integración AML/KYT + sanciones
- **Descripción:** screening de wallets/transacciones y reglas por jurisdicción.
- **Criterios de aceptación:**
  1. Wallet screening antes de retiro.
  2. Bloqueo automático en match sancionado.
  3. Registro de decisiones AML.
- **Story points:** 8
- **Dependencias:** NXR-302.

### NXR-304 — Gate formal de lanzamiento NXR
- **Descripción:** automatizar `Go/No-Go` usando criterios legales/técnicos/tesorería.
- **Criterios de aceptación:**
  1. Endpoint de evaluación de gate.
  2. Checklist firmado de cumplimiento.
  3. Estado final `GO` solo si todos los controles están en verde.
- **Story points:** 5
- **Dependencias:** NXR-301, NXR-302, NXR-303.

---

## Total estimado
- **Sprint 1:** 26 pts
- **Sprint 2:** 29 pts
- **Sprint 3:** 34 pts
- **Total:** 89 story points
