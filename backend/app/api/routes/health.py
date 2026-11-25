from fastapi import APIRouter

from app.schemas.system import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="habitat-api", storage="in-memory")
