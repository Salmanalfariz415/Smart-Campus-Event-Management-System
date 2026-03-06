"""
Database connection module — Supabase client only.
All psycopg2 / raw SQL code has been removed.
"""
from ..supabase_client import supabase


def get_supabase_client():
    """Return the shared Supabase client instance."""
    return supabase