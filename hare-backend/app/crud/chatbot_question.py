"""CRUD ChatbotQuestion."""
from typing import List

from sqlmodel import Session, select

from app.models.chatbot_question import ChatbotQuestion


def create_question(session: Session, question: str) -> ChatbotQuestion:
    q = ChatbotQuestion(question=question.strip())
    session.add(q)
    session.flush()
    session.refresh(q)
    return q


def get_all_questions(session: Session) -> List[ChatbotQuestion]:
    return list(session.exec(select(ChatbotQuestion).order_by(ChatbotQuestion.id.desc())).all())
