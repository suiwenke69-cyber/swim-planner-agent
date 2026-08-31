from v2.agent.graph import (
    build_graph,
)

from v2.memory.store import (
    get_swimming_history,
)


# =========================================================
# TEST USERS
# =========================================================

user_a = "cross-thread-user-a"

user_b = "cross-thread-user-b"


# =========================================================
# GRAPH
# =========================================================

graph = build_graph()


# =========================================================
# STEP 1 — USER A RECORDS COMPLETED SWIMS
# =========================================================

print()
print("========================================")
print("STEP 1 — USER A WRITES LONG-TERM MEMORY")
print("========================================")
print()


result_a1 = graph.invoke(
    {
        "user_id": user_a,

        "user_message": (
            "I just finished a "
            "45-minute hard swim."
        ),
    }
)


print(
    result_a1.get(
        "final_answer"
    )
)


result_a2 = graph.invoke(
    {
        "user_id": user_a,

        "user_message": (
            "I just finished another "
            "40-minute hard swim."
        ),
    }
)


print(
    result_a2.get(
        "final_answer"
    )
)


# =========================================================
# STEP 2 — VERIFY USER A DATABASE
# =========================================================

print()
print("========================================")
print("STEP 2 — USER A DATABASE")
print("========================================")
print()


history_a = get_swimming_history(
    user_a
)


for session in history_a:

    print(
        session.model_dump()
    )


# =========================================================
# STEP 3 — NEW GRAPH INSTANCE
# =========================================================

print()
print("========================================")
print("STEP 3 — NEW GRAPH INSTANCE")
print("========================================")
print()


new_graph = build_graph()


# =========================================================
# STEP 4 — USER A REQUESTS HARD WORKOUT
# =========================================================

print()
print("========================================")
print("STEP 4 — USER A PLANS NEW WORKOUT")
print("========================================")
print()


result_a3 = new_graph.invoke(
    {
        "user_id": user_a,

        "user_message": (
            "I'm a beginner and I want a "
            "40-minute hard aerobic freestyle "
            "swim in a 25-meter pool."
        ),
    }
)


training_load_a = result_a3.get(
    "training_load"
)

decision_a = result_a3.get(
    "intensity_decision"
)

workout_a = result_a3.get(
    "workout"
)


print(
    "History sessions:",
    training_load_a.sessions_last_7_days
)

print(
    "Hard sessions:",
    training_load_a.hard_sessions
)

print(
    "Recommended intensity:",
    training_load_a.recommended_intensity
)

print(
    "Requested intensity:",
    decision_a.requested_intensity
)

print(
    "Final intensity:",
    decision_a.final_intensity
)

print(
    "Workout intensity:",
    workout_a.intensity
)


# =========================================================
# STEP 5 — USER B REQUESTS SAME WORKOUT
# =========================================================

print()
print("========================================")
print("STEP 5 — USER B PLANS SAME WORKOUT")
print("========================================")
print()


result_b = new_graph.invoke(
    {
        "user_id": user_b,

        "user_message": (
            "I'm a beginner and I want a "
            "40-minute hard aerobic freestyle "
            "swim in a 25-meter pool."
        ),
    }
)


training_load_b = result_b.get(
    "training_load"
)

decision_b = result_b.get(
    "intensity_decision"
)

workout_b = result_b.get(
    "workout"
)


print(
    "History sessions:",
    training_load_b.sessions_last_7_days
)

print(
    "Hard sessions:",
    training_load_b.hard_sessions
)

print(
    "Recommended intensity:",
    training_load_b.recommended_intensity
)

print(
    "Requested intensity:",
    decision_b.requested_intensity
)

print(
    "Final intensity:",
    decision_b.final_intensity
)

print(
    "Workout intensity:",
    workout_b.intensity
)


# =========================================================
# STEP 6 — USER ISOLATION CHECK
# =========================================================

print()
print("========================================")
print("STEP 6 — USER ISOLATION")
print("========================================")
print()


history_b = get_swimming_history(
    user_b
)


print(
    "User A history count:",
    len(history_a)
)

print(
    "User B history count:",
    len(history_b)
)


print()
print("========================================")
print("TEST COMPLETE")
print("========================================")
print()