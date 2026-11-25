from typing import Literal

from pydantic import BaseModel, Field


class RecommendationSource(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    url: str = Field(min_length=1, max_length=1000)


class ActionCreate(BaseModel):
    zone_id: str
    case_ids: list[str] = Field(default_factory=list)
    recommendation: str = Field(min_length=5, max_length=5000)
    sources: list[RecommendationSource] = Field(min_length=1)
    cost: float | None = Field(default=None, ge=0)


class ActionRead(ActionCreate):
    id: str
    status: Literal["draft", "pending_approval", "approved", "declined", "completed"] = "draft"
    decision_reason: str | None = None
