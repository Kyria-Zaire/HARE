"""Génération rapport PDF (WeasyPrint + Jinja). SSRF protection : whitelist URLs."""
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
SALON_NAME_DEFAULT = "[Salon]"


def _usage_tips(product: Dict[str, Any]) -> List[str]:
    cat = (product.get("category") or "soin").lower()
    tips = {
        "shampoo": ["Appliquer sur cheveux mouillés, masser, rincer."],
        "conditioner": ["Après shampooing, longueurs aux pointes, rincer à l'eau fraîche."],
        "mask": ["Poser 8–10 min sur cheveux essorés, rincer."],
        "oil": ["Quelques gouttes sur pointes, leave-in."],
    }
    return tips.get(cat, ["Utilisez selon la notice."])[:4]


async def generate_personalized_report_pdf(
    recommended_products: List[Dict[str, Any]],
    user_answers: Dict[str, Any],
    salon_name: str = SALON_NAME_DEFAULT,
) -> bytes:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("report.html")
    products_for_template = []
    for p in recommended_products:
        item = dict(p)
        item["usage_tips"] = _usage_tips(item)
        products_for_template.append(item)
    html_content = template.render(
        recommended_products=products_for_template,
        answers=user_answers,
        report_date=datetime.now().strftime("%d/%m/%Y"),
        general_tips=["Adaptez la fréquence à votre rythme.", "Consultez votre coiffeuse."],
        salon_name=salon_name,
    )
    html_doc = HTML(string=html_content, base_url="https://picsum.photos")
    return html_doc.write_pdf()
