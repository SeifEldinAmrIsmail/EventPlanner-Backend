from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4

from .event_models import EventCreate, AttendanceStatus

# Simple in-memory "DB"
_events_store: List[Dict[str, Any]] = []


def create_event(user_id: str, req: EventCreate) -> dict:
    now = datetime.utcnow()
    payload = req.model_dump()
    event_id = uuid4().hex

    attendees_list: List[Dict[str, Any]] = []

    # organizer
    attendees_list.append({
        "user_id": user_id,
        "role": "organizer",
        "status": "going",
    })

    # optional invitees
    invitees = payload.pop("invitees", None) or []
    for invited_id in invitees:
        if invited_id != user_id:
            attendees_list.append({
                "user_id": invited_id,
                "role": "attendee",
                "status": "maybe",
            })

    doc = {
        "id": event_id,
        "organizer_id": user_id,
        "attendees": attendees_list,
        "created_at": now,
        "updated_at": now,
        **payload,
    }

    _events_store.append(doc)
    return doc


def list_events_by_organizer(user_id: str) -> List[dict]:
    return [e for e in _events_store if e.get("organizer_id") == user_id]


def list_events_user_invited(user_id: str) -> List[dict]:
    """
    Events where user is in attendees but is NOT the organizer
    """
    results: List[dict] = []
    for e in _events_store:
        if e.get("organizer_id") == user_id:
            continue
        attendees = e.get("attendees", [])
        if any(a.get("user_id") == user_id for a in attendees):
            results.append(e)
    return results


def get_event_by_id(event_id: str) -> Optional[dict]:
    for e in _events_store:
        if e.get("id") == event_id:
            return e
    return None


def update_attendance(event_id: str, user_id: str, status: AttendanceStatus) -> Optional[dict]:
    """
    Update user's attendance status ('going'/'maybe'/'not_going').
    If user not in attendees → add as attendee.
    """
    doc = get_event_by_id(event_id)
    if not doc:
        return None

    attendees: List[Dict[str, Any]] = doc.setdefault("attendees", [])

    # existing attendee → just change status
    for att in attendees:
        if att.get("user_id") == user_id:
            att["status"] = status
            doc["updated_at"] = datetime.utcnow()
            return doc

    # new attendee
    attendees.append({
        "user_id": user_id,
        "role": "attendee",
        "status": status,
    })
    doc["updated_at"] = datetime.utcnow()
    return doc


def delete_event_for_user(user_id: str, event_id: str) -> bool:
    for idx, e in enumerate(_events_store):
        if e.get("id") == event_id and e.get("organizer_id") == user_id:
            _events_store.pop(idx)
            return True
    return False


def _get_user_status_in_event(e: dict, user_id: str) -> Optional[str]:
    for att in e.get("attendees", []):
        if att.get("user_id") == user_id:
            return att.get("status")
    return None


def search_events_for_user(
    user_id: str,
    q: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    role: Optional[str] = None,
) -> List[dict]:
    results: List[dict] = []

    for e in _events_store:
        is_organizer = e.get("organizer_id") == user_id
        user_status = _get_user_status_in_event(e, user_id)
        is_related = is_organizer or user_status is not None
        if not is_related:
            continue

        if q:
            text = f"{e.get('title', '')} {e.get('description', '')}".lower()
            if q.lower() not in text:
                continue

        start = e.get("date")
        if isinstance(start, datetime):
            if date_from and start < date_from:
                continue
            if date_to and start > date_to:
                continue

        if role:
            if role == "organizer":
                if not is_organizer:
                    continue
            else:  # attendee
                if not user_status:
                    continue

        results.append(e)

    return results
