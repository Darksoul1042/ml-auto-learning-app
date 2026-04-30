# Backlog técnico (Jira-style) — NXR en Solana

## Épica 1: Foundation y arquitectura
### US-101: Crear entorno Devnet
**Como** equipo de plataforma  
**Quiero** infraestructura Devnet reproducible  
**Para** validar despliegues del token sin riesgo.

**Criterios de aceptación**
- Script `deploy_devnet` ejecutable.
- Variables de entorno documentadas.
- Checklist de smoke test.

### US-102: Definir authorities y multisig
**Criterios de aceptación**
- Mint authority en multisig 3/5.
- Freeze authority definida (on/off) y justificación.
- Firmantes registrados en runbook.

## Épica 2: Token Program y emisión
### US-201: Desplegar NXR en Devnet
**Criterios de aceptación**
- Nombre: NEXORA Token
- Símbolo: NXR
- Decimales: 9
- Supply inicial en cuenta treasury.

### US-202: Script de distribución inicial
**Criterios de aceptación**
- Entrada CSV validada.
- Reporte de transacciones emitidas.
- Idempotencia por `batch_id`.

## Épica 3: Vesting y tesorería
### US-301: Implementar vesting por tramos
**Criterios de aceptación**
- Equipo: 12m cliff + 36m linear.
- Asesores: 6m cliff + 18m linear.
- Eventos de desbloqueo auditables.

### US-302: Política de treasury
**Criterios de aceptación**
- Límites diarios por salida.
- Requiere doble aprobación.
- Alertas en retiros fuera de patrón.

## Épica 4: Compliance y legal
### US-401: Validación KYC/AML antes de airdrop
**Criterios de aceptación**
- Solo wallets aprobadas reciben tokens.
- Registro de denegaciones por regla AML.

### US-402: Legal package por jurisdicción
**Criterios de aceptación**
- Opinión legal archivada.
- ToS/Disclosures publicados.

## Épica 5: Go-live controlado
### US-501: Lanzamiento escalonado
**Criterios de aceptación**
- Fase privada -> beta pública -> apertura.
- KPIs y límites definidos por fase.

### US-502: Plan de incidentes
**Criterios de aceptación**
- Runbook P1/P2.
- Simulación tabletop aprobada.
