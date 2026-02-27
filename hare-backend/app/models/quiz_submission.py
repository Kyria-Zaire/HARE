"""Modèle QuizSubmission : enregistrement des soumissions quiz (optionnel, stats)."""
from typing import Any, Dict, List, Optional

from pydantic import ConfigDict
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class QuizSubmission(SQLModel, table=True):
    __tablename__ = "quiz_submissions"

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    answers: Dict[str, Any] = Field(default_factory=dict, sa_column=Column("answers", JSON, nullable=True))
    recommended_product_ids: List[int] = Field(default_factory=list, sa_column=Column("recommended_product_ids", JSON, nullable=True))
