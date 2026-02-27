"""Endpoints admin : login (avec must_change_password), change-password, stats, produits, leads, import CSV, seed-demo-data, chatbot questions."""
from datetime import date
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session

from app.core.admin_deps import get_current_admin
from app.core.security import create_access_token, get_password_hash, verify_password
from app.crud.admin_user import get_admin_by_username, update_password
from app.crud.chatbot_question import get_all_questions
from app.crud.newsletter_lead import get_all_leads
from app.crud.product import create_product, get_all_products
from app.db.session import get_db
from app.models.admin_user import AdminUser
from app.schemas.admin import AdminLogin, AdminStats, ChangePassword, ImportResponse, ProductsPaginated
from app.schemas.product import ProductRead
from app.services.csv_import import import_products_from_csv
from app.utils.seed_demo_data import DEMO_ADMIN_PASSWORD, DEMO_ADMIN_USERNAME, DEMO_PRODUCTS

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=dict)
def admin_login(
    payload: AdminLogin,
    session: Session = Depends(get_db),
):
    """Login admin : retourne JWT + must_change_password si premier login."""
    admin = get_admin_by_username(session, payload.username)
    if not admin or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    token = create_access_token(subject=admin.username)
    must_change = getattr(admin, "must_change_password", False)
    return {
        "access_token": token,
        "token_type": "bearer",
        "must_change_password": must_change,
    }


@router.post("/change-password")
def admin_change_password(
    payload: ChangePassword,
    current_username: Annotated[str, Depends(get_current_admin)],
    session: Session = Depends(get_db),
):
    """Change le mot de passe de l'admin connecté et désactive must_change_password."""
    if len(payload.new_password) < 8:
        raise HTTPException(status_code=400, detail="Le mot de passe doit faire au moins 8 caractères.")
    admin = get_admin_by_username(session, current_username)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin introuvable.")
    update_password(session, admin, get_password_hash(payload.new_password))
    session.commit()
    return {"ok": True, "message": "Mot de passe mis à jour."}


@router.get("/stats", response_model=AdminStats)
def admin_stats(
    _: Annotated[str, Depends(get_current_admin)],
    session: Session = Depends(get_db),
):
    """Stats dashboard : nb produits, leads, quizzes aujourd'hui."""
    products = get_all_products(session, active_only=False)
    leads = get_all_leads(session)
    return AdminStats(
        total_products=len(products),
        total_leads=len(leads),
        quizzes_today=0,
    )


@router.get("/products", response_model=ProductsPaginated)
def admin_list_products(
    _: Annotated[str, Depends(get_current_admin)],
    session: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    q: str | None = Query(None),
):
    """Liste tous les produits (paginated, recherche par nom/marque)."""
    products = get_all_products(session, active_only=False)
    if q and q.strip():
        ql = q.strip().lower()
        products = [p for p in products if ql in (p.name or "").lower() or ql in (p.brand or "").lower()]
    total = len(products)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = products[start:end]
    return ProductsPaginated(
        items=[ProductRead.model_validate(p).model_dump() for p in page_items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/leads")
def admin_list_leads(
    _: Annotated[str, Depends(get_current_admin)],
    session: Session = Depends(get_db),
    q: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
):
    """Liste des inscriptions newsletter (recherche email, filtre par date)."""
    return get_all_leads(session, q=q, date_from=date_from, date_to=date_to)


@router.post("/products/import", response_model=ImportResponse)
def admin_import_csv(
    _: Annotated[str, Depends(get_current_admin)],
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
):
    """Import produits via CSV (admin only)."""
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Fichier CSV requis.")
    content = file.file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 5 Mo).")
    try:
        count = import_products_from_csv(session, content.decode("utf-8"))
        return ImportResponse(ok=True, imported=count)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/seed-default-admin")
def seed_default_admin(
    session: Session = Depends(get_db),
):
    """Crée un admin par défaut (username: admin) si aucun n'existe."""
    if get_admin_by_username(session, "admin"):
        return {"ok": True, "message": "Un admin existe déjà."}
    session.add(AdminUser(username="admin", hashed_password=get_password_hash("admin-change-me"), must_change_password=True))
    session.commit()
    return {"ok": True, "message": "Admin par défaut créé (username: admin). Changez le mot de passe.", "username": "admin"}


@router.post("/seed-demo-data")
def seed_demo_data(
    _: Annotated[str, Depends(get_current_admin)],
    session: Session = Depends(get_db),
):
    """Charge les données de démo : 1 admin (admin@salon.com / change-me-123, must_change_password=True) + 25 produits. Protégé JWT."""
    created_admin = False
    admin = get_admin_by_username(session, DEMO_ADMIN_USERNAME)
    if not admin:
        admin = AdminUser(
            username=DEMO_ADMIN_USERNAME,
            hashed_password=get_password_hash(DEMO_ADMIN_PASSWORD),
            must_change_password=True,
        )
        session.add(admin)
        session.flush()
        created_admin = True
    else:
        admin.hashed_password = get_password_hash(DEMO_ADMIN_PASSWORD)
        admin.must_change_password = True
    count = 0
    for data in DEMO_PRODUCTS:
        data = dict(data)
        data.setdefault("description", "")
        data.setdefault("tags", {})
        data.setdefault("is_active", True)
        create_product(session, data)
        count += 1
    session.commit()
    return {
        "ok": True,
        "message": "Données de démo chargées.",
        "admin_created": created_admin,
        "products_created": count,
        "admin_username": DEMO_ADMIN_USERNAME,
        "admin_password_hint": "change-me-123 (à changer au premier login)",
    }


@router.get("/chatbot-questions")
def admin_chatbot_questions(
    _: Annotated[str, Depends(get_current_admin)],
    session: Session = Depends(get_db),
):
    """Liste des questions libres posées via le chatbot."""
    return get_all_questions(session)
