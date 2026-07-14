from pydantic import BaseModel


class Score(BaseModel):
    energy: int
    lighting: int
    sustainability: int


class AgentSummary(BaseModel):
    name: str
    score: int
    summary: str


class ReportResponse(BaseModel):
    executive_summary: str
    overall_score: int
    scores: Score
    issues: list[str]
    recommendations: list[str]
    agents: list[AgentSummary]