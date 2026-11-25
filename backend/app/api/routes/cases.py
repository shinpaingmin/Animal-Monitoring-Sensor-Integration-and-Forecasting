from fastapi import APIRouter, HTTPException, status

from app.schemas.case import CaseCreate, CaseRead
from app.services.store import store

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[CaseRead])
async def list_cases() -> list[CaseRead]:
    return store.list_cases()


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
async def create_case(payload: CaseCreate) -> CaseRead:
    return store.create_case(payload)


@router.get("/{case_id}", response_model=CaseRead)
async def get_case(case_id: str) -> CaseRead:
    case = store.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
