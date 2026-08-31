import os

from dotenv import load_dotenv
from supabase import create_client


# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()


supabase_url = os.getenv(
    "SUPABASE_URL"
)

supabase_key = os.getenv(
    "SUPABASE_KEY"
)


if not supabase_url:

    raise RuntimeError(
        "SUPABASE_URL not found."
    )


if not supabase_key:

    raise RuntimeError(
        "SUPABASE_KEY not found."
    )


# =========================================================
# CREATE CLIENT
# =========================================================

client = create_client(
    supabase_url,
    supabase_key,
)


# =========================================================
# READ TEST
# =========================================================

response = (
    client
    .table("swimming_history")
    .select("*")
    .limit(5)
    .execute()
)


print()
print("SUPABASE CONNECTION TEST")
print("==============================")
print()

print(
    "Connection successful."
)

print(
    "Rows returned:",
    len(response.data),
)

print()

print(
    response.data
)

print()