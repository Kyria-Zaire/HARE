"""Moteur de scoring produit / réponses quiz."""
from typing import List

from app.models.product import Product
from app.schemas.quiz import QuizAnswers

WEIGHTS = {"hair_type": 6.0, "concern": 5.0, "porosity": 4.0, "goal": 7.0, "scalp": 3.0}


def _tag_list(product: Product, key: str) -> List[str]:
    raw = product.tags.get(key)
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x).strip().lower() for x in raw if x]
    return [str(raw).strip().lower()]


def calculate_score(product: Product, answers: QuizAnswers) -> float:
    score = 0.0
    product_hair = _tag_list(product, "hair_types")
    if product_hair and ("all" in product_hair or any(h in product_hair for h in [x.strip().lower() for x in answers.hair_types])):
        score += WEIGHTS["hair_type"]
    product_concerns = _tag_list(product, "concerns")
    for uc in [x.strip().lower() for x in answers.concerns]:
        if uc in product_concerns:
            score += WEIGHTS["concern"]
    user_porosity = (answers.porosity or "").strip().lower()
    product_porosity = _tag_list(product, "porosity")
    if user_porosity and (user_porosity in product_porosity or "all" in product_porosity):
        score += WEIGHTS["porosity"]
    product_goals = _tag_list(product, "goals")
    for ug in [x.strip().lower() for x in answers.goals]:
        if ug in product_goals:
            score += WEIGHTS["goal"]
    if answers.scalp:
        product_scalp = _tag_list(product, "scalp")
        if product_scalp and answers.scalp.strip().lower() in product_scalp:
            score += WEIGHTS["scalp"]
    return round(score, 2)
