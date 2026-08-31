from typing import Literal

from pydantic import BaseModel, Field


# =========================================================
# MEAL TIMING RESULT
# =========================================================

class MealTimingResult(BaseModel):
    """
    Structured result produced by the meal timing tool.

    This is a planning heuristic for the Swim Planner
    prototype and is not medical advice.
    """

    base_wait_minutes: int = Field(
        ge=0,
        description=(
            "Base waiting time determined primarily "
            "by overall digestion load."
        ),
    )

    nutrition_adjustment_minutes: int = Field(
        description=(
            "Additional adjustment based on estimated "
            "meal composition."
        ),
    )

    intensity_adjustment_minutes: int = Field(
        description=(
            "Adjustment based on planned swimming intensity."
        ),
    )

    recommended_wait_minutes: int = Field(
        ge=0,
        description=(
            "Final suggested total waiting time."
        ),
    )

    minutes_since_meal: int = Field(
        ge=0,
        description=(
            "Current elapsed time since the meal."
        ),
    )

    remaining_wait_minutes: int = Field(
        ge=0,
        description=(
            "Estimated remaining waiting time."
        ),
    )

    status: Literal[
        "ready",
        "wait",
    ]

    explanation: str = Field(
        description=(
            "Short deterministic explanation of the "
            "main factors affecting the recommendation."
        ),
    )