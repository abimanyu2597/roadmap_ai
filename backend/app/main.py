from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="RoadPilot AI — Workflow & roadmap generation engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["roadpilot-ai"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "RoadPilot AI backend is running.",
        "creator": "Raja Abimanyu N — Data Scientist | AI & Applied Machine Learning",
    }
