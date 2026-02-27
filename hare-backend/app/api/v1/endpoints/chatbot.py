"""Endpoints chatbot : FAQ et enregistrement des questions libres."""
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.chatbot_question import create_question, get_all_questions
from app.db.session import get_db
from app.schemas.chatbot import ChatbotAsk, ChatbotAskResponse
from app.services.chatbot import find_answer, get_faq_list

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.get("/faq")
def get_faq() -> List[dict]:
    """Liste des questions/réponses prédéfinies (FAQ)."""
    return get_faq_list()


@router.post("/ask", response_model=ChatbotAskResponse)
def ask(
    payload: ChatbotAsk,
    session: Session = Depends(get_db),
):
    """Recherche une réponse dans la FAQ ; enregistre la question si pas de match (pour futur chatbot)."""
    answer = find_answer(payload.question)
    saved = False
    if not answer and payload.question.strip():
        create_question(session, payload.question)
        saved = True
        answer = "Votre question a été enregistrée. Notre équipe vous répondra prochainement."
    elif not answer:
        answer = "Posez une question ou choisissez une suggestion ci-dessus."
    return ChatbotAskResponse(answer=answer, saved=saved)
