"""CRUD Produits."""
from typing import Any, Dict, List, Optional

from sqlmodel import Session, select

from app.models.product import Product


def get_all_products(session: Session, active_only: bool = True) -> List[Product]:
    q = select(Product).order_by(Product.brand, Product.name)
    if active_only:
        q = q.where(Product.is_active == True)
    return list(session.exec(q).all())


def get_product_by_id(session: Session, product_id: int) -> Optional[Product]:
    return session.get(Product, product_id)


def create_product(session: Session, data: Dict[str, Any]) -> Product:
    product = Product(**data)
    session.add(product)
    session.flush()
    session.refresh(product)
    return product


def update_product(session: Session, product: Product, data: Dict[str, Any]) -> Product:
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    session.add(product)
    session.flush()
    session.refresh(product)
    return product
