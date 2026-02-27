"""Endpoint newsletter : inscription après recommandations (avec option PDF par email)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.newsletter_lead import create_lead
from app.db.session import get_db
from app.schemas.newsletter import NewsletterSubscribe

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("/subscribe")
def subscribe(
    payload: NewsletterSubscribe,
    session: Session = Depends(get_db),
):
    """Capture email + profil quiz. Option want_pdf_by_email stockée dans quiz_profile (bonus futur)."""
    try:
        profile = dict(payload.quiz_profile or {})
        profile["want_pdf_by_email"] = payload.want_pdf_by_email
        create_lead(
            session,
            email=payload.email,
            quiz_profile=profile,
            source=payload.source or "results_page",
        )
        return {"ok": True, "message": "Inscription enregistrée. Merci !"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Email déjà inscrit ou erreur.") from e
