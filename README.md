# ml-auto-learning-app

Aplicación en Python para análisis de datos, reentrenamiento incremental y orquestación de un asistente IA financiero con controles de riesgo.

## Objetivo

Construir un asistente IA **implementable en producción** para:

1. Consultar datos de mercado (acciones/cripto) en tiempo real.
2. Analizar contexto y generar recomendaciones trazables.
3. Ejecutar (opcionalmente) acciones automatizadas bajo controles estrictos.
4. Mantener una capa de seguridad operativa y criptográfica de nivel empresarial.

---

## Arquitectura de referencia (implementable)

```text
[Client/UI]
   │
   ▼
[API Gateway + AuthN/AuthZ]
   │
   ▼
[Orchestrator Agent]
   ├── [Prompt/Policy Engine]
   ├── [Memory Service: short-term + long-term]
   ├── [Tool Router]
   │      ├── Market Data Adapter (Yahoo/AlphaVantage/Binance/etc.)
   │      ├── News/Search Adapter
   │      └── Portfolio Adapter
   ├── [Risk Engine]
   └── [Audit Logger]
           │
           ▼
      [Event Store + SQL + Vector DB]

(Ops) Observability: Metrics + Logs + Traces + Alerts
(Security) Secrets Manager + KMS/HSM + Multi-sig controls
```

### Módulos mínimos

- **`orchestrator`**: ciclo de decisión del agente (plan → tools → validación → respuesta).
- **`tooling`**: clientes API con retries, timeouts, rate-limiting y fallback.
- **`risk_engine`**: reglas de exposición, límites y kill-switch.
- **`wallet_service`**: firma/gestión de llaves con multi-sig y hardware seguro.
- **`memory_service`**: contexto conversacional + memoria persistente.
- **`audit_service`**: bitácora inmutable de decisiones y acciones.

---

## Contrato de herramientas (Tool Contract)

Cada herramienta debe definir:

- `name`: identificador único.
- `input_schema`: validación estricta (JSON Schema o Pydantic).
- `permissions`: lectura o lectura/escritura.
- `timeout_ms`, `retries`, `backoff`.
- `idempotency_key` para evitar duplicados.
- `error_map` con códigos normalizados.

### Ejemplo de contrato

```json
{
  "name": "get_market_quote",
  "input_schema": {
    "type": "object",
    "properties": {
      "symbol": {"type": "string"},
      "venue": {"type": "string"}
    },
    "required": ["symbol"]
  },
  "permissions": "read",
  "timeout_ms": 3000,
  "retries": 2
}
```

---

## Motor de riesgo (obligatorio antes de operar)

Reglas base recomendadas:

- **Exposición máxima por activo** (ej. 5–10%).
- **Límite de pérdida diaria** (daily stop).
- **Máximo de órdenes por ventana temporal**.
- **Bloqueo por volatilidad extrema**.
- **Human-in-the-loop** para montos altos o activos ilíquidos.
- **Kill switch** global de ejecución.

Si una regla falla: **no se ejecuta orden** y se genera evento de auditoría.

---

## Wallet y custodia

> Una wallet custodia claves privadas; los activos viven en la blockchain.

### Requisitos

- Derivación determinística (BIP-32/39).
- Soporte multi-chain mediante librería auditada (ej. Trust Wallet Core o equivalente).
- Esquema multi-sig para operaciones de valor.
- Integración con KMS/HSM para firmas sin exponer claves.
- Rotación y segregación de llaves por entorno (`dev/staging/prod`).

---

## Seguridad y cumplimiento

### Seguridad técnica

- Cifrado en tránsito (TLS) y en reposo (AES-256 o equivalente).
- Gestión de secretos en Vault/KMS (nunca en código).
- Validación de inputs/outputs contra prompt injection y exfiltración.
- Allowlist de herramientas y destinos de red.

### Seguridad operativa

- Doble aprobación para operaciones sensibles.
- Registro de cambios de políticas y configuración.
- Playbooks de respuesta a incidentes.

### Cumplimiento

- Este sistema **no sustituye asesoría financiera regulada**.
- Verificar requisitos de jurisdicción (KYC/AML, custodio, reporting) antes de operar en real.

---

## Datos, memoria y trazabilidad

### Almacenamiento recomendado

- **SQL**: usuarios, señales, órdenes, estado de ejecución.
- **Event Store**: decisiones del agente y resultados de herramientas.
- **Vector DB**: contexto semántico y conocimiento recuperable.

### Campos de auditoría por decisión

- `trace_id`, `user_id`, `timestamp_utc`
- `model`, `tool_calls`, `risk_checks`
- `decision_summary`, `final_action`, `confidence`

---

## Plan de pruebas

1. **Unit tests**: validadores, reglas de riesgo, serialización de tools.
2. **Integration tests**: adapters con APIs mockeadas.
3. **Backtesting**: estrategias con datos históricos.
4. **Chaos tests**: caídas de API, latencia, respuestas corruptas.
5. **Security tests**: prompt injection, fuga de secretos, replay.

Criterio de salida mínimo: ninguna ruta de ejecución de órdenes sin pasar por `risk_engine`.

---

## Roadmap por fases

### Fase 1 — Asistente analítico (sin ejecución)
- Consulta mercado + noticias.
- Genera análisis y recomendaciones citables.

### Fase 2 — Paper trading
- Simulación end-to-end con riesgo y auditoría completos.

### Fase 3 — Ejecución real controlada
- Activación gradual por activos, límites bajos y supervisión humana.

---

## Prompt base (producción)

```text
Eres un asistente IA financiero en español.
Debes priorizar seguridad, trazabilidad y cumplimiento.

Reglas:
1) No ejecutar acciones de trading sin autorización explícita y válida.
2) Siempre pasar por validación del motor de riesgo.
3) Citar fuentes/datos de mercado utilizados.
4) Si faltan datos confiables, declararlo y abstenerse de actuar.
5) Nunca revelar secretos, claves ni información sensible.
```

## Siguientes pasos de implementación

1. Crear estructura de paquetes Python (`orchestrator`, `tooling`, `risk_engine`, `audit_service`).
2. Definir contratos Pydantic de tools y eventos.
3. Implementar `risk_engine` con reglas configurables por YAML/DB.
4. Integrar observabilidad (OpenTelemetry + métricas de negocio).
5. Desplegar en `staging` con paper trading y pruebas de resiliencia.

---

## Ejecución local (demo)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
ml-assistant --symbol BTCUSDT --notional 250
```

## Pruebas

```bash
pytest -q
```

---

## Branding y pantalla de inicio de sesión

Nombre propuesto de la app: **NEXORA AI Markets**.

Se agregó una pantalla de login inspirada en el estilo visual de exchanges modernos, con:
- tarjeta central oscura,
- CTA principal con alto contraste,
- alternativas de autenticación,
- diseño responsive.

### Paleta de colores
- `#0B1020` (fondo base)
- `#11182D` (panel)
- `#43E7AD` (acento primario)
- `#2DD598` (gradiente acento)
- `#F3F6FF` (texto principal)
- `#A7B3D1` (texto secundario)

### Archivos UI
- `web/index.html`
- `web/styles.css`
- `web/assets/nexora-logo.svg`

### Vista local
```bash
python -m http.server 8000
# abrir http://127.0.0.1:8000/web/index.html
```


---

## Documento unificado para entrega

Se incluye `docs/DOCUMENTO_UNIFICADO.md` como versión consolidada para subir a cliente/plataforma.


## Wallet: creación/importación de frase semilla

API demo disponible en `api_server.py`:

- `GET /wallet/create?user_id=alice&words=12`
- `GET /wallet/create?user_id=alice&words=25`
- `GET /wallet/import?user_id=alice&mnemonic=palabra1+palabra2+...`

> Nota: este MVP usa un banco compacto de palabras para demo. En producción debe usarse BIP-39 oficial.


### Seguridad API (MVP endurecido)

- Header requerido para endpoints protegidos: `X-API-Token`
- Token por defecto local: `dev-token` (configurable con `NEXORA_API_TOKEN`)
- Rate limit básico por IP: 60 requests/minuto
- `/health` queda público para monitoreo.


## Mejoras inspiradas en exchanges

Se agregaron controles inspirados en prácticas comunes de exchanges:

- **Global Settings Lock (GSL)** con ventana de desbloqueo mínima.
- **Withdrawal Address Whitelist** para direcciones permitidas de retiro.
- **Token + rate limiting** para endpoints protegidos.

Endpoints demo:
- `GET /security/gsl/enable?user_id=alice&hours=24`
- `GET /security/gsl/request-unlock?user_id=alice`
- `GET /security/whitelist/add?user_id=alice&address=0xABC...`
