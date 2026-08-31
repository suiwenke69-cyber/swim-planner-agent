from v2.agent.graph import (
    build_graph,
)

from v2.memory.store import (
    get_swimming_history,
    clear_swimming_history,
    delete_swimming_session,
)


# =========================================================
# TEST USER
# =========================================================

user_id = "robustness-test-user"


# =========================================================
# CLEAN TEST ENVIRONMENT
# =========================================================

clear_swimming_history(
    user_id
)


# =========================================================
# BUILD GRAPH
# =========================================================

graph = build_graph()


# =========================================================
# FIRST WRITE
# =========================================================

first = graph.invoke(
    {
        "user_id":
            user_id,

        "user_message": (
            "I just finished a "
            "40-minute hard swim."
        ),
    }
)


# =========================================================
# SECOND IDENTICAL WRITE
# =========================================================

second = graph.invoke(
    {
        "user_id":
            user_id,

        "user_message": (
            "I just finished a "
            "40-minute hard swim."
        ),
    }
)


# =========================================================
# READ HISTORY
# =========================================================

history = get_swimming_history(
    user_id
)


# =========================================================
# RESULTS
# =========================================================

print()
print("FIRST WRITE")
print("==============================")
print()

print(
    first.get(
        "final_answer"
    )
)


print()
print("SECOND WRITE")
print("==============================")
print()

print(
    second.get(
        "final_answer"
    )
)


print()
print("HISTORY COUNT")
print("==============================")
print()

print(
    len(history)
)


print()
print("HISTORY RECORD")
print("==============================")
print()


if history:

    print(
        history[0].model_dump()
    )


# =========================================================
# DELETE TEST
# =========================================================

print()
print("DELETE RESULT")
print("==============================")
print()


if history:

    session_id = (
        history[0]
        .session_id
    )

    deleted = delete_swimming_session(
        user_id,
        session_id,
    )

else:

    deleted = False


print(
    deleted
)


# =========================================================
# VERIFY DELETE
# =========================================================

history_after_delete = (
    get_swimming_history(
        user_id
    )
)


print()
print("HISTORY AFTER DELETE")
print("==============================")
print()

print(
    len(
        history_after_delete
    )
)

print()