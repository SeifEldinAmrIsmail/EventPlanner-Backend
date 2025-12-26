from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

AttendanceStatus = Literal["going", "maybe", "not_going"]
RoleType = Literal["organizer", "attendee"]


class Attendee(BaseModel):
    user_id: str
    role: RoleType
    status: AttendanceStatus


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    date: datetime
    location: str


class EventCreate(EventBase):
    """Request body when creating an event"""
    # so your JSON body can contain "invitees": ["userB_id", ...]
    invitees: Optional[List[str]] = None


class EventSummary(BaseModel):
    id: str
    title: str
    date: datetime
    location: str
    role: RoleType
    status: Optional[AttendanceStatus] = None


class EventDetail(EventBase):
    id: str
    organizer_id: str
    attendees: List[Attendee]
    created_at: datetime
    updated_at: datetime


class AttendanceUpdate(BaseModel):
    status: AttendanceStatus