from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from v2.agent.graph import (
    build_graph,
)


# =========================================================
# CREATE IN-MEMORY CHECKPOINTER
# =========================================================

checkpointer = InMemorySaver()


# =========================================================
# BUILD GRAPH WITH PERSISTENCE
# =========================================================

graph = build_graph(
    checkpointer=checkpointer
)


# =========================================================
# THREAD CONFIGURATION
# =========================================================

config = {
    "configurable": {
        "thread_id": "swimmer-001"
    }
}


# =========================================================
# MESSAGE 1
# =========================================================

print()
print("================================")
print("MESSAGE 1")
print("================================")
print()


result_1 = graph.invoke(

    {
        "user_message": (
            "I'm a beginner and I want a "
            "40-minute moderate aerobic "
            "freestyle swim in a 25-meter pool."
        )
    },

    config=config,
)


print(
    "Duration:",
    result_1.get(
        "swim_duration"
    )
)

print(
    "Intensity:",
    result_1.get(
        "planned_intensity"
    )
)


# =========================================================
# MESSAGE 2 — SAME THREAD
# =========================================================

print()
print("================================")
print("MESSAGE 2 — SAME THREAD")
print("================================")
print()


result_2 = graph.invoke(

    {
        "user_message":
            "Actually, make it hard."
    },

    config=config,
)


print(
    "Duration:",
    result_2.get(
        "swim_duration"
    )
)

print(
    "Requested intensity:",
    result_2.get(
        "planned_intensity"
    )
)

print(
    "Final workout duration:",
    (
        result_2["workout"]
        .duration_minutes
        if result_2.get("workout")
        else None
    )
)

print(
    "Final workout intensity:",
    (
        result_2["workout"]
        .intensity
        if result_2.get("workout")
        else None
    )
)


# =========================================================
# INSPECT SAVED GRAPH STATE
# =========================================================

print()
print("================================")
print("SAVED THREAD STATE")
print("================================")
print()


snapshot = graph.get_state(
    config
)


print(
    "Saved duration:",
    snapshot.values.get(
        "swim_duration"
    )
)

print(
    "Saved requested intensity:",
    snapshot.values.get(
        "planned_intensity"
    )
)

print()