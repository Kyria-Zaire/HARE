"""
Configuration centralisée (pydantic-settings).
Charge depuis .env / variables d'environnement.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings HARE Pro (pas de secrets en dur)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str = "postgresql://hare:hare_pro_secret@localhost:5432/hare_pro_db"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me-in-production-use-openssl-rand-hex-32"
    debug: bool = False
    allowed_origins: str = "http://localhost:5173,https://*.vercel.app"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
