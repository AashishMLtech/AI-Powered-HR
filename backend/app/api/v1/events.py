from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/events", tags=["events"])


async def empty_event_stream():
    yield "event: ready\ndata: connected\n\n"


@router.get("/job/{job_id}")
async def job_events(job_id: str):
    _ = job_id
    return StreamingResponse(empty_event_stream(), media_type="text/event-stream")
