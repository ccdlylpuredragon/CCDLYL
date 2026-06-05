"""Database engine and session helpers."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from document_db.models import Base

_engine = None
_SessionLocal = None

DEFAULT_DB_URL = "sqlite:///documents.db"


def init_db(db_url=DEFAULT_DB_URL):
    """Create the engine, session factory, and all tables.

    Args:
        db_url: SQLAlchemy database URL. Defaults to a local SQLite file.

    Returns:
        The SQLAlchemy engine.
    """
    global _engine, _SessionLocal
    _engine = create_engine(db_url, echo=False, future=True)
    _SessionLocal = sessionmaker(bind=_engine)
    Base.metadata.create_all(_engine)
    return _engine


def get_session():
    """Return a new database session.

    Raises:
        RuntimeError: If ``init_db`` has not been called yet.
    """
    if _SessionLocal is None:
        raise RuntimeError("Database not initialised. Call init_db() first.")
    return _SessionLocal()
