"""Modèle AdminUser : accès dashboard admin (username + password hash + force change au premier login)."""
from typing import Optional

from sqlmodel import Field, SQLModel


class AdminUser(SQLModel, table=True):
    __tablename__ = "admin_users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=128, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    must_change_password: bool = Field(default=True)
