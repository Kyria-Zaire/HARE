"""Import produits depuis CSV (admin only). Colonnes : name, brand, price, category, image_url, description, tags (JSON). Upsert sur name+brand."""
import csv
import io
import json
from typing import Any, Dict

from sqlmodel import Session

from app.crud.product import create_product, get_all_products, update_product
from app.models.product import Product

MAX_ROWS = 500
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 Mo
REQUIRED_HEADERS = {"name", "brand", "price", "category"}


def _normalize_key(h: str) -> str:
    return h.strip().lower().replace(" ", "_")


def import_products_from_csv(session: Session, content: str) -> int:
    """Parse CSV, valide, upsert (name+brand). Retourne le nombre de lignes importées/mises à jour."""
    if len(content.encode("utf-8")) > MAX_SIZE_BYTES:
        raise ValueError("Fichier trop volumineux (max 5 Mo).")
    reader = csv.DictReader(io.StringIO(content), delimiter=",")
    if not reader.fieldnames:
        raise ValueError("CSV vide ou sans en-têtes.")
    headers = {_normalize_key(h) for h in reader.fieldnames if h}
    missing = REQUIRED_HEADERS - headers
    if missing:
        raise ValueError(f"Colonnes requises manquantes : {missing}")
    existing = get_all_products(session, active_only=False)
    by_key: Dict[tuple[str, str], Product] = {(p.name.strip(), p.brand.strip()): p for p in existing}
    count = 0
    for i, row in enumerate(reader):
        if i >= MAX_ROWS:
            break
        data: Dict[str, Any] = {}
        for k, v in row.items():
            if not k:
                continue
            key = _normalize_key(k)
            if key == "name":
                data["name"] = (v or "").strip()
            elif key == "brand":
                data["brand"] = (v or "").strip()
            elif key == "price":
                try:
                    data["price"] = float(str(v).replace(",", "."))
                except ValueError:
                    data["price"] = 0.0
            elif key == "category":
                data["category"] = (v or "soin").strip()
            elif key == "image_url":
                data["image_url"] = (v or "").strip() or None
            elif key == "description":
                data["description"] = (v or "").strip()
            elif key == "tags":
                if (v or "").strip():
                    try:
                        data["tags"] = json.loads(v.strip())
                    except json.JSONDecodeError:
                        data["tags"] = {}
                else:
                    data["tags"] = {}
        if not data.get("name") or not data.get("brand"):
            continue
        data.setdefault("description", "")
        data.setdefault("tags", {})
        data.setdefault("is_active", True)
        key = (data["name"], data["brand"])
        if key in by_key:
            update_product(session, by_key[key], data)
        else:
            product = create_product(session, data)
            by_key[key] = product
        count += 1
    return count
