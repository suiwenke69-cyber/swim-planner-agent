from v2.agent.graph import build_graph

from v2.memory.store import (
    get_swimming_history,
)


# =========================================================
# TEST USER
# =========================================================

user_id = "natural-memory-test"


# =========================================================
# BUILD GRAPH
# =========================================================

graph = build_graph()


# =========================================================
# NATURAL-LANGUAGE MEMORY WRITE
# =========================================================

result = graph.invoke(
    {
        "user_id": user_id,

        "user_message": (
            "I just finished a "
            "40-minute hard swim."
        ),
    }
)


# =========================================================
# DEBUG — RESULT KEYS
# =========================================================

print()
print("RESULT KEYS")
print("==============================")
print()

print(
    result.keys()
)


# =========================================================
# PARSED INTENT
# =========================================================

print()
print("PARSED INTENT")
print("==============================")
print()

print(
    result.get(
        "intent"
    )
)

print(
    "Completed duration:",
    result.get(
        "completed_swim_duration"
    )
)

print(
    "Completed intensity:",
    result.get(
        "completed_swim_intensity"
    )
)


# =========================================================
# PARSED INPUT OBJECT
# =========================================================

print()
print("PARSED INPUT OBJECT")
print("==============================")
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
        "No parsed_input found."
    )


# =========================================================
# MEMORY WRITE RESULT
# =========================================================

print()
print("MEMORY WRITE")
print("==============================")
print()

print(
    "History saved:",
    result.get(
        "history_saved"
    )
)


# =========================================================
# AGENT RESPONSE
# =========================================================

print()
print("AGENT RESPONSE")
print("==============================")
print()

print(
    result.get(
        "final_answer"
    )
)


# =========================================================
# VERIFY SQLITE DATABASE
# =========================================================

history = get_swimming_history(
    user_id
)


print()
print("DATABASE HISTORY")
print("==============================")
print()

for session in history:

    print(
        session.model_dump()
    )


print()