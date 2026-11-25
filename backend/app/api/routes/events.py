import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["events"])


async def event_stream() -> AsyncIterator[str]:
    yield f"event: connected\ndata: {json.dumps({'status': 'ready'})}\n\n"
    while True:
        await asyncio.sleep(15)
        yield ": keep-alive\n\n"


@router.get("/events", response_class=StreamingResponse)
async def events() -> StreamingResponse:
    return StreamingResponse(event_stream(), media_type="text/event-stream")
