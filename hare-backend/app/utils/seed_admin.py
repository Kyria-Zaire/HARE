"""
Script one-shot : crée le premier admin (username admin / mot de passe à définir).
Usage : python -m app.utils.seed_admin
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.security import get_password_hash
from app.crud.admin_user import get_admin_by_username
from app.db.session import get_session
from app.models.admin_user import AdminUser


def main() -> None:
    password = os.environ.get("ADMIN_INITIAL_PASSWORD", "admin-change-me")
    with get_session() as session:
        if get_admin_by_username(session, "admin"):
            print("Admin 'admin' existe déjà.")
            return
        session.add(AdminUser(username="admin", hashed_password=get_password_hash(password)))
        session.commit()
    print("Admin 'admin' créé. Changez le mot de passe en prod.")


if __name__ == "__main__":
    main()
