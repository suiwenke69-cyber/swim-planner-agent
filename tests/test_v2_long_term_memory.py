from datetime import datetime

from v2.agent.graph import (
    build_graph,
)

from v2.memory.store import (
    add_swimming_session,
    get_swimming_history,
)

from v2.models.training import (
    SwimmingHistoryRecord,
)


# =========================================================
# USER
# =========================================================

user_id = "memory-test-swimmer"


# =========================================================
# ADD TWO COMPLETED SESSIONS
# =========================================================

today = (
    datetime.now()
    .date()
    .isoformat()
)


add_swimming_session(

    user_id,

    SwimmingHistoryRecord(
        date=today,
        duration_minutes=45,
        intensity="hard",
    ),
)


add_swimming_session(

    user_id,

    SwimmingHistoryRecord(
        date=today,
        duration_minutes=40,
        intensity="hard",
    ),
)


# =========================================================
# VERIFY DATABASE
# =========================================================

history = get_swimming_history(
    user_id
)


print()
print("LONG-TERM MEMORY")
print("==============================")
print()

for session in history:

    print(
        session.model_dump()
    )


# =========================================================
# NEW GRAPH REQUEST
# =========================================================

graph = build_graph()


result = graph.invoke(
    {
        "user_id":
            user_id,

        "user_message": (
            "I'm a beginner and I want a "
            "40-minute hard aerobic freestyle "
            "swim in a 25-meter pool."
        ),
    }
)


print()
print("TRAINING LOAD")
print("==============================")
print()

print(
    result[
        "training_load"
    ].model_dump_json(
        indent=2
    )
)


print()
print("INTENSITY DECISION")
print("==============================")
print()

print(
    result[
        "intensity_decision"
    ].model_dump_json(
        indent=2
    )
)


print()
print("FINAL WORKOUT")
print("==============================")
print()

print(
    "Workout intensity:",
    result[
        "workout"
    ].intensity
)

print()