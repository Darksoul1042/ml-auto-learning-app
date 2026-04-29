# Documento Unificado de Entrega — NEXORA AI Markets

## 1. Resumen ejecutivo
NEXORA AI Markets es un MVP ejecutable de asistente financiero con:
- núcleo de análisis (`FinancialAssistant`),
- motor de riesgo,
- auditoría,
- memoria,
- CLI de operación,
- pantalla de login con branding,
- y autenticación básica en memoria para flujo de inicio de sesión demo.

## 2. Componentes implementados
- `src/ml_auto_learning_app/agent.py`: orquesta quote + riesgo + auditoría + memoria.
- `src/ml_auto_learning_app/risk_engine.py`: validación de notional y kill switch.
- `src/ml_auto_learning_app/tooling.py`: proveedor determinístico de precios para pruebas.
- `src/ml_auto_learning_app/auth_service.py`: registro/login/sesión para MVP.
- `web/index.html` + `web/styles.css`: UI de login estilo exchange.
- `web/assets/nexora-logo.svg`: logotipo oficial de la marca.

## 3. Nombre y branding
- Nombre comercial: **NEXORA AI Markets**.
- Identidad visual: paleta oscura + acento verde (`#43E7AD`, `#2DD598`).

## 4. Ejecución local
```bash
python -m pytest -q
PYTHONPATH=src python -m ml_auto_learning_app.cli --symbol BTCUSDT --notional 250 --max-notional 1000
python -m http.server 8000
# Abrir: http://127.0.0.1:8000/web/index.html
```

## 5. Estado de seguridad (MVP)
Incluye controles base (validación de notional, kill-switch, hash de password PBKDF2 y token de sesión),
pero para producción se requiere: DB persistente, MFA, rotación/revocación de sesiones,
encriptación de secretos gestionada externamente y monitoreo avanzado.

## 6. Lista de pendientes para producción
1. Backend API (FastAPI) con endpoints reales para auth/análisis/auditoría.
2. Persistencia SQL + migraciones.
3. Integraciones reales con proveedores de mercado.
4. Observabilidad (logs estructurados, métricas, trazas).
5. Hardening de seguridad (MFA, rate-limit, bloqueo por intentos, RBAC).
