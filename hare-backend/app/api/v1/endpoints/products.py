"""Endpoints produits : liste (public). Import CSV = admin only."""
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.crud.product import get_all_products
from app.db.session import get_db
from app.schemas.product import ProductRead
from sqlmodel import Session

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductRead])
def list_products(session: Session = Depends(get_db)):
    """Liste tous les produits actifs (catalogue)."""
    return get_all_products(session)
