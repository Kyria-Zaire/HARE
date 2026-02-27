"""CRUD NewsletterLead."""
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from sqlmodel import Session, select

from app.models.newsletter_lead import NewsletterLead


def create_lead(
    session: Session,
    email: str,
    quiz_profile: Dict[str, Any] | None = None,
    source: str = "results_page",
) -> NewsletterLead:
    lead = NewsletterLead(email=email, quiz_profile=quiz_profile or {}, source=source)
    session.add(lead)
    session.flush()
    session.refresh(lead)
    return lead


def get_all_leads(
    session: Session,
    q: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[NewsletterLead]:
    stmt = select(NewsletterLead).order_by(NewsletterLead.id.desc())
    all_leads = list(session.exec(stmt).all())
    if q and q.strip():
        ql = q.strip().lower()
        all_leads = [l for l in all_leads if ql in (l.email or "").lower()]
    if date_from is not None:
        all_leads = [l for l in all_leads if getattr(l, "created_at", None) and l.created_at.date() >= date_from]
    if date_to is not None:
        all_leads = [l for l in all_leads if getattr(l, "created_at", None) and l.created_at.date() <= date_to]
    return all_leads
