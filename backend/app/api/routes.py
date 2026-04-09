from fastapi import APIRouter

from app.core.config import settings
from app.graphs.roadmap_graph import run_roadmap_agent
from app.models.schemas import HealthResponse, RoadmapRequest, RoadmapResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name)


@router.post("/roadmap/generate", response_model=RoadmapResponse)
def generate_roadmap(request: RoadmapRequest) -> RoadmapResponse:
    return run_roadmap_agent(request)
