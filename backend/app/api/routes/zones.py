from fastapi import APIRouter, status

from app.schemas.zone import ZoneCreate, ZoneRead
from app.services.store import store

router = APIRouter(prefix="/zones", tags=["zones"])


@router.get("", response_model=list[ZoneRead])
async def list_zones() -> list[ZoneRead]:
    return store.list_zones()


@router.post("", response_model=ZoneRead, status_code=status.HTTP_201_CREATED)
async def create_zone(payload: ZoneCreate) -> ZoneRead:
    return store.create_zone(payload)
