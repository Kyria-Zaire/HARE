"""Endpoints quiz : submit, export PDF. Rate limit sur submit."""
import io
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from loguru import logger
from sqlmodel import Session

from app.core.limiter import limiter
from app.crud.product import get_all_products
from app.db.session import get_db
from app.models.product import Product
from app.schemas.quiz import ExportReportRequest, QuizAnswers, QuizSubmitResponse
from app.schemas.product import ProductRead
from app.services.scoring import calculate_score
from app.services.pdf_generator import generate_personalized_report_pdf

router = APIRouter(prefix="/quiz", tags=["quiz"])
TOP_N = 5


def _to_reco_item(product: Product, score: float, explanation: str) -> Dict[str, Any]:
    base = ProductRead.model_validate(product).model_dump()
    base["score"] = score
    base["explanation"] = explanation
    return base


@router.post("/submit", response_model=QuizSubmitResponse)
@limiter.limit("10/minute")
async def submit_quiz(
    request: Request,
    payload: QuizAnswers,
    session: Session = Depends(get_db),
):
    if not (payload.porosity or "").strip():
        raise HTTPException(status_code=422, detail="Le champ porosity est requis.")
    products = get_all_products(session)
    if not products:
        return QuizSubmitResponse(recommended_products=[], total_matched=0, message="Aucun produit. Lancez l'import CSV.")
    from app.services.explanation import generate_explanation
    scored: List[tuple[Product, float]] = []
    for product in products:
        score = calculate_score(product, payload)
        if score > 0:
            scored.append((product, score))
    scored.sort(key=lambda x: -x[1])
    top = scored[:TOP_N]
    recommended: List[Dict[str, Any]] = []
    for product, score in top:
        explanation = generate_explanation(product, payload)
        recommended.append(_to_reco_item(product, score, explanation))
    logger.info("quiz_submitted", recommendations_count=len(recommended))
    return QuizSubmitResponse(
        recommended_products=recommended,
        total_matched=len(recommended),
        message="Voici les produits adaptés à vos cheveux !",
    )


@router.post("/export-report")
@limiter.limit("5/minute")
async def export_report_pdf(
    request: Request,
    payload: ExportReportRequest,
) -> StreamingResponse:
    try:
        pdf_bytes = await generate_personalized_report_pdf(
            recommended_products=payload.recommended_products,
            user_answers=payload.answers,
            salon_name=payload.salon_name or "[Salon]",
        )
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="Rapport_HARE_Pro.pdf"'},
        )
    except Exception as e:
        logger.exception("export_report_pdf_error", error=str(e))
        raise HTTPException(status_code=500, detail="Erreur génération PDF.") from e
