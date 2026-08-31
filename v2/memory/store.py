import os

from contextlib import contextmanager

from dotenv import load_dotenv

from supabase import (
    Client,
    create_client,
)

from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from v2.models.training import (
    SwimmingHistoryRecord,
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# SUPABASE CLIENT
# =========================================================

def get_supabase_client() -> Client:
    """
    Create the Supabase client used for persistent
    long-term swimming memory.
    """

    url = os.getenv(
        "SUPABASE_URL"
    )

    key = os.getenv(
        "SUPABASE_KEY"
    )


    if not url:

        raise RuntimeError(
            "SUPABASE_URL was not found."
        )


    if not key:

        raise RuntimeError(
            "SUPABASE_KEY was not found."
        )


    return create_client(
        url,
        key,
    )


# =========================================================
# LANGGRAPH THREAD CHECKPOINTER
# =========================================================

@contextmanager
def get_checkpointer():
    """
    Provide temporary thread-level LangGraph persistence.

    Long-term swimming history is stored separately
    in Supabase.

    For the current public beta, conversation checkpoints
    live in application memory rather than permanent
    database storage.
    """

    checkpointer = InMemorySaver()

    yield checkpointer


# =========================================================
# DUPLICATE CHECK
# =========================================================

def swimming_session_exists(
    user_id: str,
    session: SwimmingHistoryRecord,
) -> bool:
    """
    Check whether an identical swimming record already
    exists for the same user.

    Current duplicate definition:

    same user
    + same date
    + same duration
    + same intensity
    """

    client = get_supabase_client()


    response = (
        client
        .table(
            "swimming_history"
        )
        .select(
            "id"
        )
        .eq(
            "user_id",
            user_id,
        )
        .eq(
            "date",
            session.date,
        )
        .eq(
            "duration_minutes",
            session.duration_minutes,
        )
        .eq(
            "intensity",
            session.intensity,
        )
        .limit(
            1
        )
        .execute()
    )


    return bool(
        response.data
    )


# =========================================================
# ADD SWIMMING SESSION
# =========================================================

def add_swimming_session(
    user_id: str,
    session: SwimmingHistoryRecord,
) -> bool:
    """
    Save one completed swimming session to Supabase.

    Returns:

    True
        New record saved.

    False
        Duplicate detected.
    """

    if swimming_session_exists(
        user_id,
        session,
    ):

        return False


    client = get_supabase_client()


    response = (
        client
        .table(
            "swimming_history"
        )
        .insert(
            {
                "user_id":
                    user_id,

                "date":
                    session.date,

                "duration_minutes":
                    session.duration_minutes,

                "intensity":
                    session.intensity,
            }
        )
        .execute()
    )


    return bool(
        response.data
    )


# =========================================================
# GET SWIMMING HISTORY
# =========================================================

def get_swimming_history(
    user_id: str,
) -> list[SwimmingHistoryRecord]:
    """
    Load one user's persistent swimming history
    from Supabase.
    """

    client = get_supabase_client()


    response = (
        client
        .table(
            "swimming_history"
        )
        .select(
            "id,date,duration_minutes,intensity"
        )
        .eq(
            "user_id",
            user_id,
        )
        .order(
            "date"
        )
        .order(
            "id"
        )
        .execute()
    )


    history = []


    for row in response.data:

        history.append(
            SwimmingHistoryRecord(

                session_id=(
                    row["id"]
                ),

                date=(
                    row["date"]
                ),

                duration_minutes=(
                    row[
                        "duration_minutes"
                    ]
                ),

                intensity=(
                    row["intensity"]
                ),
            )
        )


    return history


# =========================================================
# DELETE SWIMMING SESSION
# =========================================================

def delete_swimming_session(
    user_id: str,
    session_id: int,
) -> bool:
    """
    Delete one swimming session.

    Both user_id and session_id are checked so one
    anonymous user cannot delete another user's record.
    """

    client = get_supabase_client()


    response = (
        client
        .table(
            "swimming_history"
        )
        .delete()
        .eq(
            "user_id",
            user_id,
        )
        .eq(
            "id",
            session_id,
        )
        .execute()
    )


    return bool(
        response.data
    )


# =========================================================
# CLEAR USER HISTORY
# =========================================================

def clear_swimming_history(
    user_id: str,
) -> None:
    """
    Delete all swimming history belonging to one user.
    """

    client = get_supabase_client()


    (
        client
        .table(
            "swimming_history"
        )
        .delete()
        .eq(
            "user_id",
            user_id,
        )
        .execute()
    )