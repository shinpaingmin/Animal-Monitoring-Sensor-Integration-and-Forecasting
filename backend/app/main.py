from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.services.store import store


@asynccontextmanager
async def lifespan(_: FastAPI):
    store.seed()
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Starter API for Habitat. Module data is held in memory until the "
        "PostgreSQL repositories are implemented."
    ),
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "docs": "/docs",
        "health": f"{settings.api_prefix}/health",
    }
