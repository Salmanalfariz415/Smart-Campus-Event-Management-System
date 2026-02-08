import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)
print("SUPABASE URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE KEY EXISTS:", bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY")))
