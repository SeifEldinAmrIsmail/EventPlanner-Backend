from typing import List, Optional
from datetime import datetime

from fastapi import HTTPException, status

from .event_models import EventCreate, EventDetail, EventSummary, AttendanceStatus
from . import event_repository as repo


def create_event_for_user(user_id: str, req: EventCreate) -> EventDetail:
    created = repo.create_event(user_id, req)
    return EventDetail(**created)


def list_my_events(user_id: str) -> List[EventSummary]:
    docs = repo.list_events_by_organizer(user_id)
    result: List[EventSummary] = []

    for doc in docs:
        status_value = None
        for att in doc.get("attendees", []):
            if att.get("user_id") == user_id:
                status_value = att.get("status")
                break

        result.append(
            EventSummary(
                id=doc["id"],
                title=doc["title"],
                date=doc["date"],
                location=doc["location"],
                role="organizer",
                status=status_value,
            )
        )
    return result


def get_event_detail(user_id: str, event_id: str) -> EventDetail:
    doc = repo.get_event_by_id(event_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return EventDetail(**doc)


def list_invited_events(user_id: str) -> List[EventDetail]:
    docs = repo.list_events_user_invited(user_id)
    return [EventDetail(**doc) for doc in docs]


def set_attendance(user_id: str, event_id: str, new_status: AttendanceStatus) -> EventDetail:
    doc = repo.update_attendance(event_id, user_id, new_status)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return EventDetail(**doc)


def delete_event_for_user(user_id: str, event_id: str) -> None:
    deleted = repo.delete_event_for_user(user_id, event_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or not owned by this user",
        )


def search_events(
    user_id: str,
    q: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    role: Optional[str] = None,
) -> List[EventSummary]:

    docs = repo.search_events_for_user(
        user_id=user_id,
        q=q,
        date_from=date_from,
        date_to=date_to,
        role=role,
    )

    results: List[EventSummary] = []
    for doc in docs:
        user_role = "organizer" if doc.get("organizer_id") == user_id else "attendee"
        status_value = None

        for att in doc.get("attendees", []):
            if att.get("user_id") == user_id:
                status_value = att.get("status")
                break

        results.append(
            EventSummary(
                id=doc["id"],
                title=doc["title"],
                date=doc["date"],
                location=doc["location"],
                role=user_role,
                status=status_value,
            )
        )

    return results
