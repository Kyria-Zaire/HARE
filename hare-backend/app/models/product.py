"""Modèle Product enrichi (catalogue ~100 produits)."""
from typing import Any, Dict, Optional

from pydantic import ConfigDict
from sqlalchemy import Column, JSON, Text
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "products"

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    brand: str = Field(max_length=128, index=True)
    price: float = Field(ge=0)
    category: str = Field(max_length=64)
    description: str = Field(sa_column=Column("description", Text(), nullable=False))
    image_url: Optional[str] = Field(default=None, max_length=512)
    tags: Dict[str, Any] = Field(default_factory=dict, sa_column=Column("tags", JSON, nullable=True))
    stock: Optional[int] = Field(default=None, ge=0)
    sku: Optional[str] = Field(default=None, max_length=64)
    is_active: bool = Field(default=True)
