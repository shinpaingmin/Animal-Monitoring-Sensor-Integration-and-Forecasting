from typing import Any

from pydantic import BaseModel, Field


class ZoneCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    blocks: list[str] = Field(default_factory=list)
    geometry: dict[str, Any] | None = None


class ZoneRead(ZoneCreate):
    id: str
    risk_score: float = Field(default=0, ge=0, le=100)
    hotspot_flag: bool = False
