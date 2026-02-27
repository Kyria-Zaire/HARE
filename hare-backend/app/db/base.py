"""Déclaration SQLModel metadata pour Alembic et create_all."""
from sqlmodel import SQLModel

from app.models.admin_user import AdminUser
from app.models.chatbot_question import ChatbotQuestion
from app.models.newsletter_lead import NewsletterLead
from app.models.product import Product
from app.models.quiz_submission import QuizSubmission

__all__ = ["SQLModel", "Product", "QuizSubmission", "NewsletterLead", "AdminUser", "ChatbotQuestion"]
