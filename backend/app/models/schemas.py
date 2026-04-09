from typing import Any, Literal
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    name: str | None = None
    experience_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    technical_background: bool = False
    budget_range: str = "low"
    timeline_months: int = 6
    country: str | None = None
    market: str | None = None
    team_size: str = "solo"
    current_skills: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class RoadmapRequest(BaseModel):
    goal: str = Field(..., min_length=10, description="What the user wants to achieve")
    goal_type: str = Field(default="general")
    profile: UserProfile


class Phase(BaseModel):
    phase_title: str
    objective: str
    duration: str
    key_tasks: list[str]
    deliverables: list[str]
    success_metrics: list[str]
    risks: list[str] = Field(default_factory=list)


class RoadmapResponse(BaseModel):
    title: str
    summary: str
    readiness_score: int
    execution_mode: str
    tools_needed: list[str]
    next_7_days: list[str]
    next_30_days: list[str]
    next_90_days: list[str]
    phases: list[Phase]
    notes: list[str] = Field(default_factory=list)
    raw_state: dict[str, Any] | None = None


class HealthResponse(BaseModel):
    status: str
    app: str


class ErrorResponse(BaseModel):
    detail: str
