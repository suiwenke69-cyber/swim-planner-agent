import time

from v2.agent.graph import (
    build_graph,
)


# =========================================================
# BUILD GRAPH
# =========================================================

graph = build_graph()


# =========================================================
# TEST INPUT
# =========================================================

user_message = """
I ate chicken rice, a fried egg, and a large milk tea
45 minutes ago.

I'm a beginner and I want a 40-minute moderate aerobic
freestyle swim in a 25-meter pool.
"""


# =========================================================
# RUN COMPLETE V2 GRAPH
# =========================================================

print()
print("🏊 SWIM PLANNER V2 — END-TO-END TEST")
print("============================================")
print()

print("👤 User")
print()
print(user_message.strip())
print()

print("🤖 Running LangGraph...")
print()


start = time.perf_counter()


result = graph.invoke(
    {
        "user_message": user_message
    }
)


elapsed = (
    time.perf_counter()
    - start
)


# =========================================================
# PARSED INPUT
# =========================================================

print()
print("============================================")
print("🧠 PARSED INPUT")
print("============================================")
print()

parsed_input = result.get(
    "parsed_input"
)

if parsed_input is not None:

    print(
        parsed_input.model_dump_json(
            indent=2
        )
    )

else:

    print(
        "No parsed input."
    )


# =========================================================
# NUTRITION ANALYSIS
# =========================================================

print()
print("============================================")
print("🍽 NUTRITION ANALYSIS")
print("============================================")
print()

meal_analysis = result.get(
    "meal_analysis"
)

if meal_analysis is not None:

    print(
        meal_analysis.model_dump_json(
            indent=2
        )
    )

else:

    print(
        "No meal analysis."
    )


# =========================================================
# MEAL TIMING
# =========================================================

print()
print("============================================")
print("⏱ MEAL TIMING")
print("============================================")
print()

meal_timing = result.get(
    "meal_timing"
)

if meal_timing is not None:

    print(
        meal_timing.model_dump_json(
            indent=2
        )
    )

else:

    print(
        "No meal timing result."
    )


# =========================================================
# WORKOUT
# =========================================================

print()
print("============================================")
print("🏊 WORKOUT")
print("============================================")
print()

workout = result.get(
    "workout"
)

if workout is not None:

    print(
        workout.model_dump_json(
            indent=2
        )
    )

else:

    print(
        "No workout generated."
    )


# =========================================================
# FINAL RESPONSE
# =========================================================

print()
print("============================================")
print("💬 FINAL RESPONSE")
print("============================================")
print()

final_answer = result.get(
    "final_answer"
)

if final_answer:

    print(
        final_answer
    )

else:

    print(
        "No final answer generated."
    )


# =========================================================
# PERFORMANCE
# =========================================================

print()
print("============================================")
print("⚡ PERFORMANCE")
print("============================================")
print()

print(
    f"Total LangGraph execution time: "
    f"{elapsed:.3f} seconds"
)

print()

latency = result.get(
    "latency",
    {}
)

print("Per-node latency:")
print()

print(
    f"Parse Input:        "
    f"{latency.get('parse_input', 0):.3f} s"
)

print(
    f"Nutrition Analysis: "
    f"{latency.get('nutrition_analysis', 0):.3f} s"
)

print(
    f"Meal Timing:        "
    f"{latency.get('meal_timing', 0):.3f} s"
)

print(
    f"Workout:            "
    f"{latency.get('workout', 0):.3f} s"
)

print(
    f"Final Response:     "
    f"{latency.get('final_response', 0):.3f} s"
)

print()

print(
    "Pipeline:"
)

print(
    "User Input"
)

print(
    "  ↓"
)

print(
    "Structured Input Parsing (OpenAI)"
)

print(
    "  ↓"
)

print(
    "Conditional Routing (LangGraph)"
)

print(
    "  ↓"
)

print(
    "Nutrition Analysis (OpenAI)"
)

print(
    "  ↓"
)

print(
    "Meal Timing (Python)"
)

print(
    "  ↓"
)

print(
    "Workout Planning (Python)"
)

print(
    "  ↓"
)

print(
    "Final Response (OpenAI)"
)

print(
    "  ↓"
)

print(
    "END"
)

print()