from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CaseCreate(BaseModel):
    text: str = Field(min_length=5, max_length=5000)
    language: str = Field(default="en", min_length=2, max_length=20)
    photo_urls: list[str] = Field(default_factory=list)
    block: str = Field(min_length=1, max_length=100)
    floor: str | None = Field(default=None, max_length=20)
    stairwell: str | None = Field(default=None, max_length=100)
    zone_id: str | None = None


class CaseRead(CaseCreate):
    id: str
    translation: str | None = None
    created_at: datetime
    category: Literal["nuisance", "welfare", "unclassified"] = "unclassified"
    priority: int = Field(default=0, ge=0, le=100)
    root_cause: str | None = None
    status: Literal["new", "in_review", "closed", "archived"] = "new"
