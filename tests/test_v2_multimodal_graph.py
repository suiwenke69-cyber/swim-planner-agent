import time

from v2.agent.graph import (
    build_graph,
)


# =========================================================
# BUILD GRAPH
# =========================================================

graph = build_graph()


# =========================================================
# MULTIMODAL INPUT
# =========================================================

initial_state = {

    "user_id":
        "vision-test-user",

    "user_message": (
        "I ate this meal 45 minutes ago. "
        "I'm a beginner and I want a "
        "40-minute moderate aerobic freestyle "
        "swim in a 25-meter pool."
    ),

    "meal_image_path":
        "tests/sample_meal.jpg",
}


# =========================================================
# RUN GRAPH
# =========================================================

print()
print("📷 SWIM PLANNER V2 — MULTIMODAL TEST")
print("============================================")
print()

start = time.perf_counter()


result = graph.invoke(
    initial_state
)


elapsed = (
    time.perf_counter()
    - start
)


# =========================================================
# PARSED INPUT
# =========================================================

print()
print("PARSED INPUT")
print("============================================")
print()

print(
    result[
        "parsed_input"
    ].model_dump_json(
        indent=2
    )
)


# =========================================================
# VISION NUTRITION
# =========================================================

print()
print("VISION NUTRITION")
print("============================================")
print()

print(
    result[
        "meal_analysis"
    ].model_dump_json(
        indent=2
    )
)


# =========================================================
# MEAL TIMING
# =========================================================

print()
print("MEAL TIMING")
print("============================================")
print()

print(
    result[
        "meal_timing"
    ].model_dump_json(
        indent=2
    )
)


# =========================================================
# WORKOUT
# =========================================================

print()
print("WORKOUT")
print("============================================")
print()

print(
    result[
        "workout"
    ].model_dump_json(
        indent=2
    )
)


# =========================================================
# FINAL ANSWER
# =========================================================

print()
print("FINAL ANSWER")
print("============================================")
print()

print(
    result[
        "final_answer"
    ]
)


# =========================================================
# PERFORMANCE
# =========================================================

print()
print("PERFORMANCE")
print("============================================")
print()

latency = result.get(
    "latency",
    {}
)


for name, value in latency.items():

    print(
        f"{name}: {value:.3f} s"
    )


print()

print(
    f"Total graph time: "
    f"{elapsed:.3f} s"
)

print()