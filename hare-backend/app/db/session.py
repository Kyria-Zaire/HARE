"""Session SQLModel synchrone pour PostgreSQL."""
from collections.abc import Generator
from contextlib import contextmanager

from sqlmodel import Session, create_engine

from app.core.config import get_settings
from app.db.base import SQLModel

_settings = get_settings()
engine = create_engine(
    _settings.database_url,
    echo=_settings.debug,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


def create_db_and_tables() -> None:
    """Crée les tables au démarrage. En prod : préférer Alembic."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """Dépendance FastAPI."""
    with get_session() as session:
        yield session
