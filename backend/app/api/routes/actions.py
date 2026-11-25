from fastapi import APIRouter, status

from app.schemas.action import ActionCreate, ActionRead
from app.services.store import store

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("", response_model=list[ActionRead])
async def list_actions() -> list[ActionRead]:
    return store.list_actions()


@router.post("", response_model=ActionRead, status_code=status.HTTP_201_CREATED)
async def create_action(payload: ActionCreate) -> ActionRead:
    return store.create_action(payload)
