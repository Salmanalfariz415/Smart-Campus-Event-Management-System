"""
Booking DAO — pure Supabase client (no psycopg2 / cursor)
"""
import random
import string
from ..supabase_client import supabase


def generate_booking_reference():
    """Generate a unique booking reference like BK001234"""
    random_num = "".join(random.choices(string.digits, k=6))
    return f"BK{random_num}"


def create_booking(booking_data):
    """Create a new booking for an event"""

    # Generate unique booking reference
    booking_ref = generate_booking_reference()
    while True:
        check = (
            supabase.table("bookings")
            .select("id")
            .eq("booking_reference", booking_ref)
            .execute()
        )
        if not check.data:
            break
        booking_ref = generate_booking_reference()

    # Check available capacity
    cap = (
        supabase.table("event_capacity")
        .select("max_capacity, current_bookings, available_spots")
        .eq("event_id", booking_data["event_id"])
        .execute()
    )
    attendees = booking_data.get("attendees_count", 1)

    if cap.data:
        available = cap.data[0]["available_spots"]
        if available < attendees:
            return {
                "success": False,
                "message": f"Not enough spots available. Only {available} spots remaining.",
                "available_spots": available,
            }

    # Insert booking
    row = {
        "event_id": booking_data["event_id"],
        "user_id": booking_data.get("user_id"),
        "booking_reference": booking_ref,
        "attendees_count": attendees,
        "contact_name": booking_data["contact_name"],
        "contact_email": booking_data["contact_email"],
        "contact_phone": booking_data.get("contact_phone", ""),
        "special_requirements": booking_data.get("special_requirements", ""),
        "payment_amount": booking_data.get("payment_amount", 0.00),
        "status": "confirmed",
    }
    ins = supabase.table("bookings").insert(row).execute()
    if not ins.data:
        raise Exception("Failed to create booking")

    booking_id = ins.data[0]["id"]

    # Update event capacity
    if cap.data:
        new_current = cap.data[0]["current_bookings"] + attendees
        supabase.table("event_capacity").update(
            {"current_bookings": new_current}
        ).eq("event_id", booking_data["event_id"]).execute()

    # Log the booking creation
    try:
        supabase.table("booking_logs").insert(
            {
                "booking_id": booking_id,
                "action": "created",
                "new_status": "confirmed",
                "notes": "Booking created successfully",
            }
        ).execute()
    except Exception:
        pass  # logging is best-effort

    return {
        "success": True,
        "booking_id": booking_id,
        "booking_reference": booking_ref,
        "message": "Booking confirmed successfully!",
    }


def get_booking_by_reference(booking_reference):
    """Get booking details by reference number"""
    result = (
        supabase.table("bookings")
        .select(
            "id, event_id, booking_reference, attendees_count, status, "
            "contact_name, contact_email, contact_phone, special_requirements, "
            "payment_amount, payment_status, booking_date, created_at, "
            "events(title, start_date, start_time, venue)"
        )
        .eq("booking_reference", booking_reference)
        .execute()
    )

    if not result.data:
        return None

    row = result.data[0]
    evt = row.get("events") or {}

    return {
        "id": row["id"],
        "event_id": row["event_id"],
        "booking_reference": row["booking_reference"],
        "attendees_count": row["attendees_count"],
        "status": row["status"],
        "contact_name": row["contact_name"],
        "contact_email": row["contact_email"],
        "contact_phone": row.get("contact_phone", ""),
        "special_requirements": row.get("special_requirements", ""),
        "payment_amount": float(row["payment_amount"]) if row.get("payment_amount") else 0.00,
        "payment_status": row.get("payment_status"),
        "booking_date": str(row.get("booking_date", "")),
        "created_at": str(row.get("created_at", "")),
        "event_details": {
            "title": evt.get("title", ""),
            "start_date": str(evt.get("start_date", "")),
            "start_time": str(evt.get("start_time", "")),
            "venue": evt.get("venue", ""),
        },
    }


def cancel_booking(booking_reference):
    """Cancel a booking by reference number"""
    result = (
        supabase.table("bookings")
        .select("id, event_id, attendees_count, status")
        .eq("booking_reference", booking_reference)
        .execute()
    )

    if not result.data:
        return {"success": False, "message": "Booking not found"}

    row = result.data[0]
    if row["status"] == "cancelled":
        return {"success": False, "message": "Booking is already cancelled"}

    # Update status
    supabase.table("bookings").update({"status": "cancelled"}).eq(
        "booking_reference", booking_reference
    ).execute()

    # Update event capacity
    cap = (
        supabase.table("event_capacity")
        .select("current_bookings")
        .eq("event_id", row["event_id"])
        .execute()
    )
    if cap.data:
        new_current = max(0, cap.data[0]["current_bookings"] - row["attendees_count"])
        supabase.table("event_capacity").update(
            {"current_bookings": new_current}
        ).eq("event_id", row["event_id"]).execute()

    # Log the cancellation
    try:
        supabase.table("booking_logs").insert(
            {
                "booking_id": row["id"],
                "action": "cancelled",
                "old_status": row["status"],
                "new_status": "cancelled",
                "notes": "Booking cancelled by user",
            }
        ).execute()
    except Exception:
        pass

    return {"success": True, "message": "Booking cancelled successfully"}


def get_user_bookings(user_id):
    """Get all bookings for a specific user"""
    result = (
        supabase.table("bookings")
        .select(
            "id, booking_reference, attendees_count, status, contact_name, "
            "contact_email, payment_amount, payment_status, booking_date, created_at, "
            "events(id, title, start_date, start_time, venue)"
        )
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    bookings = []
    for row in result.data:
        evt = row.get("events") or {}
        bookings.append(
            {
                "id": row["id"],
                "booking_reference": row["booking_reference"],
                "attendees_count": row["attendees_count"],
                "status": row["status"],
                "contact_name": row["contact_name"],
                "contact_email": row["contact_email"],
                "payment_amount": float(row["payment_amount"]) if row.get("payment_amount") else 0.00,
                "payment_status": row.get("payment_status"),
                "booking_date": str(row.get("booking_date", "")),
                "created_at": str(row.get("created_at", "")),
                "event_title": evt.get("title", ""),
                "event_start_date": str(evt.get("start_date", "")),
                "event_start_time": str(evt.get("start_time", "")),
                "event_venue": evt.get("venue", ""),
                "event_id": evt.get("id"),
            }
        )
    return bookings


def get_event_bookings(event_id):
    """Get all bookings for a specific event"""
    result = (
        supabase.table("bookings")
        .select(
            "booking_reference, contact_name, contact_email, attendees_count, "
            "status, booking_date, payment_status"
        )
        .eq("event_id", event_id)
        .order("booking_date", desc=True)
        .execute()
    )

    bookings = []
    for row in result.data:
        bookings.append(
            {
                "booking_reference": row["booking_reference"],
                "contact_name": row["contact_name"],
                "contact_email": row["contact_email"],
                "attendees_count": row["attendees_count"],
                "status": row["status"],
                "booking_date": str(row.get("booking_date", "")),
                "payment_status": row.get("payment_status"),
            }
        )
    return bookings