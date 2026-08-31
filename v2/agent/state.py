from typing import TypedDict

from v2.models.user_input import (
    ParsedUserInput,
)

from v2.models.nutrition import (
    MealAnalysis,
)

from v2.models.meal_timing import (
    MealTimingResult,
)

from v2.models.workout import (
    SwimmingWorkout,
)

from v2.models.training import (
    SwimmingHistoryRecord,
    TrainingLoadResult,
    IntensityDecision,
)


# =========================================================
# LANGGRAPH AGENT STATE
# =========================================================

class AgentState(
    TypedDict,
    total=False,
):
    """
    Shared state used by Swim Planner V2.

    The state separates:

    - user identity
    - raw user input
    - parsed intent
    - temporary meal/workout information
    - completed-swim information
    - long-term swimming history
    - deterministic planning results
    - final response
    - latency measurements

    total=False allows the graph to start with only a
    subset of these fields.
    """

    # =====================================================
    # USER IDENTITY
    # =====================================================

    user_id: str


    # =====================================================
    # RAW USER INPUT
    # =====================================================

    user_message: str


    # =====================================================
    # PARSED USER INPUT
    # =====================================================

    parsed_input: ParsedUserInput

    intent: str


    # =====================================================
    # MEAL INPUT
    # =====================================================

    meal_description: str

    minutes_since_meal: int

    meal_image_path: str


    # =====================================================
    # PLANNED SWIMMING
    # =====================================================

    swim_duration: int

    planned_intensity: str

    swimming_level: str

    swimming_goal: str

    preferred_stroke: str

    pool_length: int


    # =====================================================
    # COMPLETED SWIM
    # =====================================================

    completed_swim_duration: int

    completed_swim_intensity: str

    history_saved: bool

    history_duplicate: bool


    # =====================================================
    # NUTRITION ANALYSIS
    # =====================================================

    meal_analysis: MealAnalysis


    # =====================================================
    # MEAL TIMING
    # =====================================================

    meal_timing: MealTimingResult


    # =====================================================
    # LONG-TERM SWIMMING HISTORY
    # =====================================================

    swimming_history: list[
        SwimmingHistoryRecord
    ]


    # =====================================================
    # TRAINING LOAD
    # =====================================================

    training_load: TrainingLoadResult


    # =====================================================
    # INTENSITY DECISION
    # =====================================================

    intensity_decision: IntensityDecision


    # =====================================================
    # GENERATED WORKOUT
    # =====================================================

    workout: SwimmingWorkout


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    final_answer: str


    # =====================================================
    # PERFORMANCE
    # =====================================================

    latency: dict[
        str,
        float,
    ]