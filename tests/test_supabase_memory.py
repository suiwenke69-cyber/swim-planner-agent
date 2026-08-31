from datetime import (
    datetime,
)

from v2.memory.store import (
    add_swimming_session,
    get_swimming_history,
    delete_swimming_session,
    clear_swimming_history,
)

from v2.models.training import (
    SwimmingHistoryRecord,
)


# =========================================================
# TEST USER
# =========================================================

user_id = (
    "supabase-memory-test"
)


# =========================================================
# CLEAN START
# =========================================================

clear_swimming_history(
    user_id
)


# =========================================================
# CREATE SESSION
# =========================================================

today = (
    datetime.now()
    .date()
    .isoformat()
)


session = SwimmingHistoryRecord(
    date=today,
    duration_minutes=40,
    intensity="hard",
)


# =========================================================
# FIRST WRITE
# =========================================================

first_saved = add_swimming_session(
    user_id,
    session,
)


# =========================================================
# DUPLICATE WRITE
# =========================================================

second_saved = add_swimming_session(
    user_id,
    session,
)


# =========================================================
# READ
# =========================================================

history = get_swimming_history(
    user_id
)


print()
print("SUPABASE MEMORY TEST")
print("==============================")
print()

print(
    "First saved:",
    first_saved,
)

print(
    "Duplicate saved:",
    second_saved,
)

print(
    "History count:",
    len(history),
)

print()


for item in history:

    print(
        item.model_dump()
    )


# =========================================================
# DELETE
# =========================================================

if history:

    deleted = delete_swimming_session(
        user_id,
        history[0].session_id,
    )

else:

    deleted = False


history_after_delete = (
    get_swimming_history(
        user_id
    )
)


print()
print(
    "Delete successful:",
    deleted,
)

print(
    "History after delete:",
    len(history_after_delete),
)

print()