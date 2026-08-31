from v2.agent.graph import (
    build_graph,
)


graph = build_graph()


# =========================================================
# TEST A — WITH MEAL
# =========================================================

print()
print("TEST A — Meal + Workout")
print("==============================")
print()


result_a = graph.invoke(
    {
        "user_message": (
            "I ate chicken rice and a fried egg "
            "45 minutes ago. I'm a beginner and "
            "want a 40-minute moderate aerobic "
            "freestyle swim in a 25-meter pool."
        )
    }
)


print(
    "Meal Analysis:",
    "meal_analysis" in result_a,
)

print(
    "Meal Timing:",
    "meal_timing" in result_a,
)

print(
    "Workout:",
    "workout" in result_a,
)


# =========================================================
# TEST B — NO MEAL
# =========================================================

print()
print("TEST B — Workout Only")
print("==============================")
print()


result_b = graph.invoke(
    {
        "user_message": (
            "I'm an intermediate swimmer. "
            "Give me a 45-minute moderate "
            "endurance freestyle session "
            "in a 50-meter pool."
        )
    }
)


print(
    "Meal Analysis:",
    "meal_analysis" in result_b,
)

print(
    "Meal Timing:",
    "meal_timing" in result_b,
)

print(
    "Workout:",
    "workout" in result_b,
)


print()

print(
    result_b[
        "workout"
    ].model_dump_json(
        indent=2
    )
)

print()