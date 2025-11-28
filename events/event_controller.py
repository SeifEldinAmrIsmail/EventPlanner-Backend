from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status

from core.security import get_current_user_id
from .event_models import EventCreate, EventDetail, EventSummary, AttendanceUpdate
from .event_service import (
    create_event_for_user,
    list_my_events,
    get_event_detail,
    list_invited_events,
    set_attendance,
    delete_event_for_user,
    search_events as service_search_events,
)

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventDetail)
def create_event_endpoint(
    req: EventCreate,
    user_id: str = Depends(get_current_user_id),
):
    return create_event_for_user(user_id, req)


@router.get("/mine", response_model=List[EventSummary])
def list_my_events_endpoint(
    user_id: str = Depends(get_current_user_id),
):
    return list_my_events(user_id)


# 🔼 MOVE THIS ABOVE `/{event_id}`
@router.get("/invited", response_model=List[EventDetail])
def list_invited_events_endpoint(
    user_id: str = Depends(get_current_user_id),
):
    """
    List events where the current user is invited (attendee) but not organizer.
    """
    return list_invited_events(user_id)


@router.get("/{event_id}", response_model=EventDetail)
def get_event_endpoint(
    event_id: str,
    user_id: str = Depends(get_current_user_id),
):
    return get_event_detail(user_id, event_id)

@router.post("/{event_id}/respond", response_model=EventDetail)
def respond_to_event(
    event_id: str,
    req: AttendanceUpdate,
    user_id: str = Depends(get_current_user_id),
):
    return set_attendance(user_id, event_id, req.status)


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: str,
    user_id: str = Depends(get_current_user_id),
):
    delete_event_for_user(user_id, event_id)


@router.get("/search/{keyword}", response_model=List[EventSummary])
def search_events_endpoint(
    keyword: str,
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    role: Optional[str] = Query(None),
    user_id: str = Depends(get_current_user_id),
):
    return service_search_events(
        user_id=user_id,
        q=keyword,
        date_from=date_from,
        date_to=date_to,
        role=role,
    )
