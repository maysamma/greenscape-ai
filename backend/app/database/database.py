from app.database.base import Base
from app.database.session import engine, SessionLocal, get_db

# استيراد الـ Models حتى يتعرف SQLAlchemy على الجداول.
from app.models.project import Project
from app.models.analysis_result import AnalysisResult


def create_database_tables() -> None:
    Base.metadata.create_all(bind=engine)


__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "create_database_tables",
]