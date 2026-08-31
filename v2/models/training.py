from typing import Literal

from pydantic import BaseModel, Field


# =========================================================
# SWIMMING HISTORY RECORD
# =========================================================

class SwimmingHistoryRecord(BaseModel):
    """
    One completed swimming session.

    session_id uniquely identifies the record in
    long-term memory.
    """

    session_id: int | None = Field(
        default=None,
        description=(
            "Unique database ID for this swimming session."
        ),
    )

    date: str

    duration_minutes: int = Field(
        ge=1
    )

    intensity: Literal[
        "easy",
        "moderate",
        "hard",
    ]


# =========================================================
# TRAINING LOAD RESULT
# =========================================================

class TrainingLoadResult(BaseModel):
    """
    Simplified analysis of recent swimming history.

    recommended_intensity may be None when there is not
    enough recent training history to justify changing
    the user's requested intensity.
    """

    sessions_last_7_days: int = Field(
        ge=0
    )

    total_minutes_last_7_days: int = Field(
        ge=0
    )

    easy_sessions: int = Field(
        ge=0
    )

    moderate_sessions: int = Field(
        ge=0
    )

    hard_sessions: int = Field(
        ge=0
    )

    training_load_score: int = Field(
        ge=0
    )

    training_load_level: Literal[
        "unknown",
        "low",
        "moderate",
        "high",
        "very_high",
    ]

    recommended_intensity: (
        Literal[
            "easy",
            "moderate",
            "hard",
        ]
        | None
    )

    has_sufficient_history: bool

    explanation: str


# =========================================================
# INTENSITY DECISION
# =========================================================

class IntensityDecision(BaseModel):
    """
    Final intensity decision before workout generation.
    """

    requested_intensity: Literal[
        "easy",
        "moderate",
        "hard",
    ]

    recommended_intensity: (
        Literal[
            "easy",
            "moderate",
            "hard",
        ]
        | None
    )

    final_intensity: Literal[
        "easy",
        "moderate",
        "hard",
    ]

    adjusted: bool

    explanation: str