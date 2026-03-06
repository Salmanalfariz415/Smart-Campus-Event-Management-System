"""
Event DAO — pure Supabase client (no psycopg2 / cursor)
"""
from ..supabase_client import supabase


def submitl(username, event_type, event_sub_type, desc, org,
            st_date, end_date, st_time, end_time,
            venue, building, capacity, fee, reg,
            img, contact, website, tag):
    """Insert a new event and return its id."""
    result = (
        supabase.table("events")
        .insert(
            {
                "title": username,
                "event_type": event_type,
                "event_category": event_sub_type,
                "description": desc,
                "organizer": org,
                "start_date": st_date,
                "end_date": end_date,
                "start_time": st_time,
                "end_time": end_time,
                "venue": venue,
                "building": building,
                "capacity": capacity,
                "fee": fee,
                "registration_required": 1 if reg else 0,
                "image_url": img,
                "contact_email": contact,
                "website": website,
                "tags": tag,
            }
        )
        .execute()
    )

    if not result.data:
        raise Exception("Failed to create event")

    return result.data[0]["id"]


def eventcard():
    """Return all events ordered by id descending."""
    result = (
        supabase.table("events")
        .select("*")
        .order("id", desc=True)
        .execute()
    )

    rows = result.data or []
    # Stringify non-primitive values (dates, times, etc.) so they are JSON-safe
    for row in rows:
        for key, value in row.items():
            if value is not None and not isinstance(value, (int, str, float, bool)):
                row[key] = str(value)

    return rows
