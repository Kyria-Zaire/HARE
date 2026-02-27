"""Schémas Pydantic pour l'admin : login, stats, import, pagination."""
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    must_change_password: bool = False


class ChangePassword(BaseModel):
    new_password: str


class AdminStats(BaseModel):
    total_products: int = 0
    total_leads: int = 0
    quizzes_today: int = 0


class ImportResponse(BaseModel):
    ok: bool = True
    imported: int = 0
    error: str | None = None


class ProductReadAdmin(BaseModel):
    id: int | None = None
    name: str
    brand: str
    price: float
    category: str
    description: str = ""
    image_url: str | None = None
    is_active: bool = True


class ProductsPaginated(BaseModel):
    items: List[Dict[str, Any]] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 10
