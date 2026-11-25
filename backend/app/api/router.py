from fastapi import APIRouter

from app.api.routes import actions, cases, detections, events, health, zones

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(cases.router)
api_router.include_router(detections.router)
api_router.include_router(zones.router)
api_router.include_router(actions.router)
api_router.include_router(events.router)
