from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    project_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    current_stage: Mapped[str] = mapped_column(
        String(100),
        default="waiting",
        nullable=False,
    )

    progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    vision_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    design_analysis_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    architecture_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    sustainability_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    energy_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    lighting_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    ventilation_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    accessibility_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    building_code_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    cost_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    report_result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    overall_score: Mapped[Optional[int]] = mapped_column(
        Integer,
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

    project = relationship(
        "Project",
        back_populates="analysis",
    )