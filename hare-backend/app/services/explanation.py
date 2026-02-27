"""Génération d'explications en français pour chaque recommandation."""
from typing import List

from app.models.product import Product
from app.schemas.quiz import QuizAnswers

CONCERN_MAP = {
    "dry": "secs et déshydratés",
    "frizz": "avec des frisottis",
    "damaged": "abîmés",
    "fine": "fins",
    "flat": "plats",
    "color_treated": "colorés",
    "hair_loss": "en chute",
}


def _tag_list(product: Product, key: str) -> List[str]:
    raw = product.tags.get(key)
    if raw is None:
        return []
    return [str(x) for x in raw] if isinstance(raw, list) else [str(raw)]


def generate_explanation(product: Product, answers: QuizAnswers) -> str:
    subject = "Vos cheveux"
    if answers.hair_types:
        subject = "Vos cheveux " + ", ".join(answers.hair_types[:3])
    concern_labels = [CONCERN_MAP.get(c.strip().lower().replace(" ", "_"), c) for c in (answers.concerns or [])[:3]]
    parts = []
    if concern_labels:
        parts.append("sont " + " et ".join(concern_labels))
    porosity_fr = {"high": "très poreux", "medium": "poreux", "low": "peu poreux"}.get((answers.porosity or "").strip().lower(), "")
    if porosity_fr:
        parts.append(porosity_fr)
    profile = subject + (" " + ", ".join(parts) if parts else "")
    desc = (product.description or "").strip()[:100] or "correspondre à vos critères."
    return f"Parce que {profile}, ce {product.category or 'soin'} {product.brand} va {desc}.".replace("  ", " ").strip()
