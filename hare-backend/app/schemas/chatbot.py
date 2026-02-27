"""Schémas Pydantic pour le chatbot."""
from pydantic import BaseModel, Field


class ChatbotAsk(BaseModel):
    question: str = Field(..., max_length=1000)


class ChatbotFaqItem(BaseModel):
    question: str
    answer: str


class ChatbotAskResponse(BaseModel):
    answer: str | None
    saved: bool = False
