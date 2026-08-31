from typing import Literal

from pydantic import BaseModel, Field


# =========================================================
# PARSED USER INPUT
# =========================================================

class ParsedUserInput(BaseModel):
    """
    Structured interpretation of the user's natural-language
    request.
    """

    # =====================================================
    # USER INTENT
    # =====================================================

    intent: Literal[
        "plan_workout",
        "record_completed_swim",
        "other",
    ] = Field(
        description=(
            "Primary intent of the current message."
        )
    )


    # =====================================================
    # MEAL
    # =====================================================

    meal_description: str | None = Field(
        default=None,
        description=(
            "Foods and drinks consumed. "
            "None if no meal was mentioned."
        ),
    )

    minutes_since_meal: int | None = Field(
        default=None,
        ge=0,
        description=(
            "Minutes since the meal was finished."
        ),
    )


    # =====================================================
    # PLANNED SWIMMING
    # =====================================================

    swim_duration: int | None = Field(
        default=None,
        ge=1,
        description=(
            "Requested or completed swimming duration "
            "in minutes."
        ),
    )

    planned_intensity: Literal[
        "easy",
        "moderate",
        "hard",
    ] | None = None

    swimming_level: Literal[
        "beginner",
        "intermediate",
        "advanced",
    ] | None = None

    swimming_goal: Literal[
        "aerobic",
        "endurance",
        "recovery",
        "speed",
    ] | None = None

    preferred_stroke: Literal[
        "freestyle",
        "breaststroke",
        "backstroke",
        "mixed",
    ] | None = None

    pool_length: Literal[
        25,
        50,
    ] | None = None


    # =====================================================
    # COMPLETED SWIM
    # =====================================================

    completed_swim_duration: int | None = Field(
        default=None,
        ge=1,
        description=(
            "Duration of an explicitly completed swim."
        ),
    )

    completed_swim_intensity: Literal[
        "easy",
        "moderate",
        "hard",
    ] | None = Field(
        default=None,
        description=(
            "Intensity of an explicitly completed swim."
        ),
    )