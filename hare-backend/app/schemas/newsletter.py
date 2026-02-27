"""Schémas Pydantic pour la newsletter."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field


class NewsletterSubscribe(BaseModel):
    email: EmailStr
    quiz_profile: Dict[str, Any] = Field(default_factory=dict)
    source: Optional[str] = "results_page"
    want_pdf_by_email: bool = False
