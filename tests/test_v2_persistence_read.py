from v2.agent.graph import (
    build_graph,
)

from v2.memory.store import (
    get_checkpointer,
)


# =========================================================
# SAME THREAD
# =========================================================

config = {
    "configurable": {
        "thread_id":
            "persistent-swimmer-001"
    }
}


# =========================================================
# LOAD OLD STATE + UPDATE IT
# =========================================================

with get_checkpointer() as checkpointer:

    graph = build_graph(
        checkpointer=checkpointer
    )

    result = graph.invoke(

        {
            "user_message":
                "Actually, make it hard."
        },

        config=config,
    )


    print()
    print("PERSISTENCE READ TEST")
    print("==============================")
    print()

    print(
        "Remembered duration:",
        result.get(
            "swim_duration"
        )
    )

    print(
        "Updated requested intensity:",
        result.get(
            "planned_intensity"
        )
    )

    print(
        "Workout duration:",
        (
            result["workout"]
            .duration_minutes
            if result.get("workout")
            else None
        )
    )

    print(
        "Workout intensity:",
        (
            result["workout"]
            .intensity
            if result.get("workout")
            else None
        )
    )

    print()