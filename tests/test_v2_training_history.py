from datetime import (
    datetime,
)

from v2.agent.graph import (
    build_graph,
)

from v2.models.training import (
    SwimmingHistoryRecord,
)


graph = build_graph()


today = (
    datetime.now()
    .date()
    .isoformat()
)


history = [

    SwimmingHistoryRecord(
        date=today,
        duration_minutes=45,
        intensity="hard",
    ),

    SwimmingHistoryRecord(
        date=today,
        duration_minutes=40,
        intensity="hard",
    ),
]


result = graph.invoke(
    {
        "user_message": (
            "I'm a beginner and I want a "
            "40-minute hard aerobic freestyle "
            "swim in a 25-meter pool."
        ),

        "swimming_history":
            history,
    }
)


print()
print("TRAINING LOAD")
print("==============================")
print()

print(
    result[
        "training_load"
    ].model_dump_json(
        indent=2
    )
)


print()
print("INTENSITY DECISION")
print("==============================")
print()

print(
    result[
        "intensity_decision"
    ].model_dump_json(
        indent=2
    )
)


print()
print("WORKOUT INTENSITY")
print("==============================")
print()

print(
    result[
        "workout"
    ].intensity
)

print()