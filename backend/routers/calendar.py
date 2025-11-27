from fastapi import APIRouter, HTTPException, Depends
from services.calendar_service import calendar_service
from schemas import (
    FreeBusyRequest, FreeBusyResponse, 
    EventCreateRequest, EventResponse, 
    EventUpdateRequest, DeleteEventRequest,
    EventListRequest
)

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.post("/freebusy", response_model=FreeBusyResponse)
def get_free_busy(request: FreeBusyRequest):
    try:
        busy, available = calendar_service.get_free_busy(
            request.time_min, request.time_max, request.timezone, request.email or 'primary'
        )
        return {"busy_slots": busy, "available_slots": available}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", response_model=EventResponse)
def create_event(request: EventCreateRequest):
    try:
        event = calendar_service.create_event(request)
        return {
            "event_id": event['id'],
            "html_link": event['htmlLink'],
            "status": event['status'],
            "summary": event['summary'],
            "start": event['start'].get('dateTime'),
            "end": event['end'].get('dateTime')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update")
def update_event(request: EventUpdateRequest):
    try:
        event = calendar_service.update_event(request)
        return {"message": "Event updated successfully", "event": event}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete")
def delete_event(request: DeleteEventRequest):
    try:
        calendar_service.delete_event(request.event_id)
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/list")
def list_events(request: EventListRequest):
    try:
        events = calendar_service.list_events(request.max_results, request.time_min)
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
