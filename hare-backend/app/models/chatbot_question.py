"""Modèle ChatbotQuestion : questions libres posées par les utilisateurs (pour futur vrai chatbot)."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class ChatbotQuestion(SQLModel, table=True):
    __tablename__ = "chatbot_questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    question: str = Field(max_length=1000)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime(timezone=False), nullable=True))
