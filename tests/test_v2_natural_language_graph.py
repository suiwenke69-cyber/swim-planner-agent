import time

from v2.agent.graph import (
    build_graph,
)


graph = build_graph()


# =========================================================
# ONLY RAW USER LANGUAGE
# =========================================================

initial_state = {
    "user_message": (
        "I ate chicken rice, a fried egg, and a large "
        "milk tea 45 minutes ago. I want to swim for "
        "40 minutes at moderate intensity."
    )
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

print(
    "🏊 Swim Planner V2 — Natural Language Graph"
)

print(
    "==========================================="
)


print()
print("🧠 Parsed Input")
print()

print(
    result[
        "parsed_input"
    ].model_dump_json(
        indent=2
    )
)


print()
print("🍽 Nutrition Analysis")
print()

print(
    result[
        "meal_analysis"
    ].model_dump_json(
        indent=2
    )
)


print()
print("⏱ Meal Timing")
print()

print(
    result[
        "meal_timing"
    ].model_dump_json(
        indent=2
    )
)


print()

print(
    "==========================================="
)

print(
    f"Graph execution time: "
    f"{elapsed:.3f} seconds"
)

print()