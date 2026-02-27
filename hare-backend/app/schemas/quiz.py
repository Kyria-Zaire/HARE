"""Schémas Pydantic pour le quiz et les réponses."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QuizAnswers(BaseModel):
    hair_types: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    porosity: str = Field(...)
    goals: list[str] = Field(default_factory=list)
    scalp: Optional[str] = None


class QuizSubmitResponse(BaseModel):
    recommended_products: List[Dict[str, Any]] = Field(default_factory=list)
    total_matched: int = 0
    message: str = "Voici les produits adaptés à vos cheveux !"


class ExportReportRequest(BaseModel):
    recommended_products: List[Dict[str, Any]] = Field(default_factory=list, max_length=20)
    answers: Dict[str, Any] = Field(default_factory=dict)
    salon_name: Optional[str] = None
