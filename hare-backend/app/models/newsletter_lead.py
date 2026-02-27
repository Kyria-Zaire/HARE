"""Modèle NewsletterLead : capture email + profil quiz après recommandations."""
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import ConfigDict
from sqlalchemy import Column, JSON, DateTime
from sqlmodel import Field, SQLModel


class NewsletterLead(SQLModel, table=True):
    __tablename__ = "newsletter_leads"

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, index=True, unique=True)
    quiz_profile: Dict[str, Any] = Field(default_factory=dict, sa_column=Column("quiz_profile", JSON, nullable=True))
    source: Optional[str] = Field(default="results_page", max_length=64)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime(timezone=False), nullable=True))
