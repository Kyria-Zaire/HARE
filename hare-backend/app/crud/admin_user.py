"""CRUD AdminUser."""
from typing import Optional

from sqlmodel import Session, select

from app.models.admin_user import AdminUser


def get_admin_by_username(session: Session, username: str) -> Optional[AdminUser]:
    return session.exec(select(AdminUser).where(AdminUser.username == username)).first()


def update_password(session: Session, admin: AdminUser, new_hashed_password: str) -> AdminUser:
    admin.hashed_password = new_hashed_password
    admin.must_change_password = False
    session.add(admin)
    session.flush()
    session.refresh(admin)
    return admin
