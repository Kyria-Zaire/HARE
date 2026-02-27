"""Schémas Pydantic pour les produits."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    brand: str
    price: float
    category: str
    description: str
    image_url: Optional[str] = None
    tags: Dict[str, Any] = Field(default_factory=dict)
    stock: Optional[int] = None
    sku: Optional[str] = None
    is_active: bool = True


class ProductCreate(BaseModel):
    name: str
    brand: str
    price: float
    category: str
    description: str = ""
    image_url: Optional[str] = None
    tags: Dict[str, Any] = Field(default_factory=dict)
    stock: Optional[int] = None
    sku: Optional[str] = None
    is_active: bool = True
