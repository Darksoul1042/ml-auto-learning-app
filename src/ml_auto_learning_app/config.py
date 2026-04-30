from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    env: str
    api_token: str
    jwt_secret: str
    allow_demo_fallbacks: bool


def load_config() -> AppConfig:
    env = os.getenv("NEXORA_ENV", "dev").strip().lower()
    if env not in {"dev", "staging", "prod"}:
        raise ValueError("NEXORA_ENV must be one of: dev, staging, prod")

    api_token = os.getenv("NEXORA_API_TOKEN", "").strip()
    jwt_secret = os.getenv("NEXORA_JWT_SECRET", "").strip()

    if env in {"staging", "prod"}:
        if not api_token:
            raise ValueError("NEXORA_API_TOKEN is required in staging/prod")
        if not jwt_secret:
            raise ValueError("NEXORA_JWT_SECRET is required in staging/prod")

    allow_demo_fallbacks = env == "dev"
    return AppConfig(env=env, api_token=api_token, jwt_secret=jwt_secret, allow_demo_fallbacks=allow_demo_fallbacks)
