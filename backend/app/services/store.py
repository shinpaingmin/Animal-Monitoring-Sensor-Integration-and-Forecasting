from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.action import ActionCreate, ActionRead
from app.schemas.case import CaseCreate, CaseRead
from app.schemas.detection import DetectionCreate, DetectionRead
from app.schemas.zone import ZoneCreate, ZoneRead


class InMemoryStore:
    """Integration scaffold. Replace this class with PostgreSQL repositories."""

    def __init__(self) -> None:
        self.cases: dict[str, CaseRead] = {}
        self.detections: dict[str, DetectionRead] = {}
        self.zones: dict[str, ZoneRead] = {}
        self.actions: dict[str, ActionRead] = {}

    def seed(self) -> None:
        if self.zones:
            return
        zone = ZoneRead(
            id="zone-demo",
            name="Sample HDB Zone",
            blocks=["101", "102"],
            geometry=None,
            risk_score=0,
            hotspot_flag=False,
        )
        self.zones[zone.id] = zone

    def list_cases(self) -> list[CaseRead]:
        return sorted(self.cases.values(), key=lambda item: item.created_at, reverse=True)

    def get_case(self, case_id: str) -> CaseRead | None:
        return self.cases.get(case_id)

    def create_case(self, payload: CaseCreate) -> CaseRead:
        case = CaseRead(
            **payload.model_dump(),
            id=f"CASE-{uuid4().hex[:8].upper()}",
            created_at=datetime.now(timezone.utc),
        )
        self.cases[case.id] = case
        return case

    def list_detections(self) -> list[DetectionRead]:
        return list(self.detections.values())

    def create_mock_detection(self, payload: DetectionCreate) -> DetectionRead:
        detection = DetectionRead(
            id=f"DET-{uuid4().hex[:8].upper()}",
            case_id=payload.case_id,
            source=payload.source,
            species=payload.reported_species or "unknown",
            confidence=0,
            boxes=[],
            model_version="mock-starter-no-model",
            review_status="pending",
        )
        self.detections[detection.id] = detection
        return detection

    def list_zones(self) -> list[ZoneRead]:
        return list(self.zones.values())

    def create_zone(self, payload: ZoneCreate) -> ZoneRead:
        zone = ZoneRead(**payload.model_dump(), id=f"ZONE-{uuid4().hex[:8].upper()}")
        self.zones[zone.id] = zone
        return zone

    def list_actions(self) -> list[ActionRead]:
        return list(self.actions.values())

    def create_action(self, payload: ActionCreate) -> ActionRead:
        action = ActionRead(**payload.model_dump(), id=f"ACT-{uuid4().hex[:8].upper()}")
        self.actions[action.id] = action
        return action


store = InMemoryStore()
