# Pre-Production Checklist (NEXORA MVP)

## Automated
- [ ] `pytest -q` green
- [ ] `python -m compileall -q src tests` green
- [ ] `python scripts/deep_checks.py` green

## API Hardening
- [ ] Unauthorized requests return 401
- [ ] Rate limiting returns 429 under pressure
- [ ] Token-protected endpoints require `X-API-Token`

## Wallet/Custody
- [ ] Seed phrase never logged in plain text
- [ ] Wallet creation/import validated (12/25 words)
- [ ] Custody digest generated for secure storage path

## Risk/Controls
- [ ] `kill-switch` blocks trading actions
- [ ] max-notional guard works
- [ ] GSL and whitelist controls active

## Go/No-Go for token
- [ ] KYC ready
- [ ] AML ready
- [ ] Legal opinion approved
- [ ] Treasury >= 18 months
- [ ] Security audit completed
