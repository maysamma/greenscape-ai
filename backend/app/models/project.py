from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        index=True,
    )

    project_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    building_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    orientation: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    area: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    floors: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="uploaded",
        nullable=False,
    )

    # Old fields kept temporarily for backward compatibility.
    # These will not be used by the new analysis workflow.
    legacy_analysis_result: Mapped[str | None] = mapped_column(
        "analysis_result",
        Text,
        nullable=True,
    )

    legacy_report_result: Mapped[str | None] = mapped_column(
        "report_result",
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    analysis = relationship(
        "AnalysisResult",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )