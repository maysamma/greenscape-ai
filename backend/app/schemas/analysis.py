from pydantic import BaseModel, Field


class ProjectInfo(BaseModel):
    name: str
    building_type: str
    location: str
    floor_area: str
    floors: int


class Scores(BaseModel):
    architecture: int | float = 0
    sustainability: int | float = 0
    energy: int | float = 0
    ventilation: int | float = 0
    lighting: int | float = 0
    accessibility: int | float = 0
    building_code: int | float = 0
    cost: int | float = 0


class AgentStatus(BaseModel):
    name: str
    status: str


class AnalysisDetails(BaseModel):
    progress: int
    status: str
    analysis_time: str
    agents: list[AgentStatus] = Field(
        default_factory=list
    )


class AnalysisResponse(BaseModel):
    project: ProjectInfo
    overall_score: int | float
    scores: Scores
    recommendations: list[str] = Field(
        default_factory=list
    )
    analysis: AnalysisDetails