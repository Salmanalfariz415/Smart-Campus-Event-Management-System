"""
Authentication DAO — pure Supabase client (no psycopg2 / cursor)
"""
import jwt
import bcrypt
import datetime
import os
from dotenv import load_dotenv
from ..supabase_client import supabase

load_dotenv()


def _make_token(user_id, user_type):
    """Return a signed JWT valid for 24 hours."""
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")


# ── Register ──────────────────────────────────────────────────────────────────

def register_user(username, password, user_type="user"):
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    result = (
        supabase.table("users")
        .insert({"email": username, "password_hash": hashed_password, "user_type": user_type})
        .execute()
    )

    if not result.data:
        raise Exception("Failed to create user")

    user_id = result.data[0]["id"]
    token = _make_token(user_id, user_type)
    return {"user_id": user_id, "token": token}


# ── Login ─────────────────────────────────────────────────────────────────────

def login_user(username, password):
    result = (
        supabase.table("users")
        .select("id, password_hash, user_type")
        .eq("email", username)
        .execute()
    )

    if not result.data:
        return "Incorrect username or password"

    row = result.data[0]
    stored = row["password_hash"]
    if isinstance(stored, str):
        stored = stored.encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), stored):
        return _make_token(row["id"], row["user_type"])
    return "Incorrect username or password"


# ── User details ──────────────────────────────────────────────────────────────

def get_user_details(user_id):
    result = (
        supabase.table("users")
        .select("id, email, user_type")
        .eq("id", user_id)
        .execute()
    )

    if not result.data:
        return None

    user_data = result.data[0]

    if user_data["user_type"] == "organizer":
        org = (
            supabase.table("organizers")
            .select("id, org_name, org_type, org_description, contact_name, contact_position, phone")
            .eq("user_id", user_id)
            .execute()
        )
        if org.data:
            user_data["organizer_info"] = org.data[0]

    return user_data


# ── Register organizer ────────────────────────────────────────────────────────

def register_organizer(org_data):
    user_result = register_user(org_data["email"], org_data["password"], "organizer")
    user_id = user_result["user_id"]

    org_result = (
        supabase.table("organizers")
        .insert(
            {
                "user_id": user_id,
                "org_name": org_data["org_name"],
                "org_type": org_data["org_type"],
                "org_description": org_data.get("org_description", ""),
                "contact_name": org_data["contact_name"],
                "contact_position": org_data["contact_position"],
                "phone": org_data["phone"],
            }
        )
        .execute()
    )

    if not org_result.data:
        raise Exception("Failed to create organizer profile")

    return {
        "user_id": user_id,
        "organizer_id": org_result.data[0]["id"],
        "token": user_result["token"],
    }


# ── Update organizer profile ─────────────────────────────────────────────────

def update_organizer(user_id, data):
    supabase.table("organizers").update(
        {
            "org_name": data.get("org_name"),
            "org_type": data.get("org_type"),
            "org_description": data.get("org_description", ""),
            "contact_name": data.get("contact_name"),
            "contact_position": data.get("contact_position"),
            "phone": data.get("phone"),
        }
    ).eq("user_id", user_id).execute()


# ── Change password ───────────────────────────────────────────────────────────

def change_password(user_id, current_password, new_password):
    """Verify current password and set the new one. Returns True on success."""
    result = (
        supabase.table("users")
        .select("password_hash")
        .eq("id", user_id)
        .execute()
    )

    if not result.data:
        raise Exception("User not found")

    stored = result.data[0]["password_hash"]
    if isinstance(stored, str):
        stored = stored.encode("utf-8")

    if not bcrypt.checkpw(current_password.encode("utf-8"), stored):
        return False  # wrong current password

    new_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    supabase.table("users").update({"password_hash": new_hash}).eq("id", user_id).execute()
    return True