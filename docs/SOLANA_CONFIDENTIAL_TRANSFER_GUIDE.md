# Solana Confidential Transfer (Token-2022) — guía operativa NEXORA

## Estado actual importante

La documentación oficial de Solana indica que el programa ZK ElGamal está temporalmente deshabilitado en mainnet y devnet mientras pasa auditoría de seguridad.  
Conclusión: los ejemplos de Confidential Transfer pueden no ejecutar en esos entornos actualmente.

## Crear token account con Confidential Transfer (resumen)

Según la guía oficial, el flujo requiere 3 instrucciones:

1. Crear la Associated Token Account (`AssociatedTokenAccountInstruction::Create`).
2. Reasignar espacio de la cuenta (`TokenInstruction::Reallocate`) para añadir estado `ConfidentialTransferAccount`.
3. Configurar la cuenta (`ConfidentialTransferInstruction::ConfigureAccount`) con claves/pruebas generadas del lado cliente.

## Implicaciones para NEXORA

- No bloquear el plan de publicación del token a esta extensión mientras siga temporalmente deshabilitada.
- Mantenerlo como capability opcional “post-launch” hasta que Solana confirme disponibilidad estable.
- Condicionar habilitación a:
  - auditoría de seguridad externa cerrada,
  - pruebas de integración en red soportada,
  - validación legal/compliance del feature.

## Gate de publicación del token (NEXORA)

Antes de publicar:

- KYC operativo real.
- AML/KYT operativo real.
- Opinión legal aprobada por jurisdicción.
- Tesorería mínima de 18+ meses.
- Auditoría de seguridad externa cerrada.

Para validar rápidamente el estado de gate en este repo:

```bash
python scripts/token_publish_readiness.py
```
