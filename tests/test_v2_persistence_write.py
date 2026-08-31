from v2.agent.graph import (
    build_graph,
)

from v2.memory.store import (
    get_checkpointer,
)


# =========================================================
# THREAD
# =========================================================

config = {
    "configurable": {
        "thread_id":
            "persistent-swimmer-001"
    }
}


# =========================================================
# WRITE STATE
# =========================================================

with get_checkpointer() as checkpointer:

    graph = build_graph(
        checkpointer=checkpointer
    )

    result = graph.invoke(

        {
            "user_message": (
                "I'm a beginner and I want a "
                "40-minute moderate aerobic "
                "freestyle swim in a 25-meter pool."
            )
        },

        config=config,
    )


    print()
    print("PERSISTENCE WRITE TEST")
    print("==============================")
    print()

    print(
        "Saved duration:",
        result.get(
            "swim_duration"
        )
    )

    print(
        "Saved intensity:",
        result.get(
            "planned_intensity"
        )
    )

    print()