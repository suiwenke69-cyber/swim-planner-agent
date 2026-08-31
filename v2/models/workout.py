from typing import Literal

from pydantic import BaseModel, Field


# =========================================================
# WORKOUT SET
# =========================================================

class WorkoutSet(BaseModel):
    """
    One section of a swimming workout.
    """

    name: str

    distance_m: int = Field(
        ge=0
    )

    instruction: str


# =========================================================
# SWIMMING WORKOUT
# =========================================================

class SwimmingWorkout(BaseModel):
    """
    Structured swimming workout produced by the
    deterministic workout-planning tool.
    """

    duration_minutes: int = Field(
        ge=1
    )

    intensity: Literal[
        "easy",
        "moderate",
        "hard",
    ]

    goal: Literal[
        "aerobic",
        "endurance",
        "recovery",
        "speed",
    ]

    level: Literal[
        "beginner",
        "intermediate",
        "advanced",
    ]

    stroke: Literal[
        "freestyle",
        "breaststroke",
        "backstroke",
        "mixed",
    ]

    pool_length_m: Literal[
        25,
        50,
    ]

    estimated_total_distance_m: int = Field(
        ge=0
    )

    warmup: WorkoutSet

    main_set: WorkoutSet

    cooldown: WorkoutSet

    planning_note: str