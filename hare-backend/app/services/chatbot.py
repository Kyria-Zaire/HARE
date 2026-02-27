"""FAQ chatbot : réponses prédéfinies. Enregistrement des questions libres pour futur vrai chatbot."""
from typing import List, Tuple

FAQ: List[Tuple[str, str]] = [
    ("Comment savoir ma porosité ?", "Testez en plaçant un cheveu dans un verre d'eau : s'il coule vite, vous êtes plutôt poreuse ; s'il flotte, peu poreuse. En salon, votre coiffeuse peut faire un diagnostic précis."),
    ("Quel produit pour cheveux secs ?", "Privilégiez les masques nourrissants et les huiles (argan, coco). Nos recommandations du quiz incluent des soins adaptés à la sécheresse."),
    ("Je suis débutante, par où commencer ?", "Faites le quiz HARE Pro pour obtenir des recommandations personnalisées selon votre type de cheveux, votre porosité et vos objectifs. C'est le meilleur point de départ !"),
    ("Comment utiliser un masque capillaire ?", "Appliquez sur cheveux essorés, des longueurs aux pointes. Laissez poser 5 à 15 min selon le produit, puis rincez à l'eau tiède."),
    ("Quelle différence entre shampooing et après-shampooing ?", "Le shampooing nettoie le cuir chevelu ; l'après-shampooing ou le masque nourrit et gaine les longueurs. Utilisez les deux pour une routine équilibrée."),
]


def get_faq_list() -> List[dict]:
    """Retourne la liste FAQ pour l'API (question, réponse)."""
    return [{"question": q, "answer": a} for q, a in FAQ]


def find_answer(user_question: str) -> str | None:
    """Recherche une réponse dans la FAQ par similarité simple (mots-clés). Retourne None si pas de match."""
    ql = user_question.strip().lower()
    if not ql:
        return None
    for question, answer in FAQ:
        if ql in question.lower() or any(w in question.lower() for w in ql.split() if len(w) > 2):
            return answer
    return None
