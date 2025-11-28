from typing import Optional,List

from datetime import datetime

from db.mongo import events_collection  # same collection you already use


def search_events_for_user(
    user_id: str,
    q: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    role: Optional[str] = None,
) -> list[dict]:
    filters = []

    # user must be organizer OR attendee
    filters.append({
        "$or": [
            {"organizer_id": user_id},
            {"attendees.user_id": user_id},
        ]
    })

    # keyword filter (title OR description, case-insensitive)
    if q:
        regex = {"$regex": q, "$options": "i"}
        filters.append({
            "$or": [
                {"title": regex},
                {"description": regex},
            ]
        })

    # date range filter
    if date_from or date_to:
        date_cond: dict = {}
        if date_from:
            date_cond["$gte"] = date_from
        if date_to:
            date_cond["$lte"] = date_to
        filters.append({"date": date_cond})

    # role filter
    if role == "organizer":
        filters.append({"organizer_id": user_id})
    elif role == "attendee":
        filters.append({"attendees.user_id": user_id})

    query = {"$and": filters} if filters else {}

    docs = list(events_collection.find(query))

    result: list[dict] = []
    for doc in docs:
        # make sure we have an 'id' field as string
        if "_id" in doc:
            doc["id"] = str(doc["_id"])
        result.append(doc)

    return result


def list_events_by_organizer(user_id: str) -> List[dict]:
    """
    Return all events where this user is the organizer.
    """
    docs = list(events_collection.find({"organizer_id": user_id}))

    result: List[dict] = []
    for doc in docs:
        # convert MongoDB _id to plain string "id"
        if "_id" in doc:
            doc["id"] = str(doc["_id"])
        result.append(doc)

    return result