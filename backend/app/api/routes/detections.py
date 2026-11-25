from fastapi import APIRouter, status

from app.schemas.detection import DetectionCreate, DetectionRead
from app.services.store import store

router = APIRouter(tags=["detections"])


@router.get("/detections", response_model=list[DetectionRead])
async def list_detections() -> list[DetectionRead]:
    return store.list_detections()


@router.post("/detect", response_model=DetectionRead, status_code=status.HTTP_202_ACCEPTED)
async def detect(payload: DetectionCreate) -> DetectionRead:
    """Create a clearly labelled mock result until the YOLO worker is connected."""
    return store.create_mock_detection(payload)
