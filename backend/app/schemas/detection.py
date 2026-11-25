from typing import Literal

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(ge=0)
    height: float = Field(ge=0)


class DetectionCreate(BaseModel):
    case_id: str | None = None
    source: str = Field(min_length=1, max_length=500)
    reported_species: Literal["cat", "chicken"] | None = None


class DetectionRead(BaseModel):
    id: str
    case_id: str | None = None
    source: str
    species: Literal["cat", "chicken", "unknown"]
    confidence: float = Field(ge=0, le=1)
    boxes: list[BoundingBox] = Field(default_factory=list)
    model_version: str
    review_status: Literal["pending", "confirmed", "corrected"]
    profile_id: str | None = None
    behaviour: str | None = None
