import time

from v2.agent.graph import build_graph


# =========================================================
# BUILD GRAPH
# =========================================================

graph = build_graph()


# =========================================================
# INITIAL STATE
# =========================================================

initial_state = {
    "user_message":
        "I ate chicken rice, a fried egg, "
        "and a large milk tea.",

    "meal_description":
        "Chicken rice, one fried egg, "
        "and a large milk tea. "
        "The chicken rice was a normal restaurant portion.",
}


# =========================================================
# RUN GRAPH
# =========================================================

start = time.perf_counter()


result = graph.invoke(
    initial_state
)


elapsed = (
    time.perf_counter()
    - start
)


# =========================================================
# OUTPUT
# =========================================================

print()
print("🧠 Swim Planner V2 — LangGraph")
print("================================")
print()

print(
    "User Message:"
)

print(
    result["user_message"]
)

print()

print(
    "Meal Analysis:"
)

print(
    result[
        "meal_analysis"
    ].model_dump_json(
        indent=2
    )
)

print()

print(
    "================================"
)

print(
    f"Graph execution time: "
    f"{elapsed:.3f} seconds"
)

print()