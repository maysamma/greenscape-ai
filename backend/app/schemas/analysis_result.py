from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentStatus(BaseModel):
    name: str
    status: str


class AnalysisStartResponse(BaseModel):
    success: bool
    project_id: str
    analysis_id: int
    status: str
    message: str


class AnalysisResultResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    project_id: str

    status: str
    current_stage: str
    progress: int

    error_message: str | None = None
    overall_score: int | None = None

    vision_result: dict[str, Any] | None = None
    design_analysis: dict[str, Any] | None = None
    architecture_result: dict[str, Any] | None = None
    sustainability_result: dict[str, Any] | None = None
    energy_result: dict[str, Any] | None = None
    lighting_result: dict[str, Any] | None = None
    ventilation_result: dict[str, Any] | None = None
    accessibility_result: dict[str, Any] | None = None
    building_code_result: dict[str, Any] | None = None
    cost_result: dict[str, Any] | None = None
    report_result: dict[str, Any] | None = None

    agents: list[AgentStatus] = Field(
        default_factory=list
    )

    created_at: datetime
    updated_at: datetime