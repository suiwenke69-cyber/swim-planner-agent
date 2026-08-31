from datetime import (
    datetime,
    timedelta,
)

from v2.models.training import (
    SwimmingHistoryRecord,
    TrainingLoadResult,
    IntensityDecision,
)


# =========================================================
# TRAINING LOAD ANALYSIS
# =========================================================

def analyze_training_load(
    history: list[SwimmingHistoryRecord],
) -> TrainingLoadResult:
    """
    Analyze swimming activity from the most recent 7 days.

    This is currently a simplified planning heuristic.

    If there is no recent training history, the tool does
    NOT make an intensity recommendation.
    """

    today = datetime.now().date()

    seven_day_start = (
        today - timedelta(days=6)
    )

    recent_sessions = []


    # =====================================================
    # FILTER LAST 7 DAYS
    # =====================================================

    for session in history:

        try:

            session_date = (
                datetime.strptime(
                    session.date,
                    "%Y-%m-%d",
                ).date()
            )

        except (
            ValueError,
            TypeError,
        ):

            continue


        if (
            seven_day_start
            <= session_date
            <= today
        ):

            recent_sessions.append(
                session
            )


    # =====================================================
    # NO RECENT HISTORY
    # =====================================================

    if not recent_sessions:

        return TrainingLoadResult(

            sessions_last_7_days=0,

            total_minutes_last_7_days=0,

            easy_sessions=0,

            moderate_sessions=0,

            hard_sessions=0,

            training_load_score=0,

            training_load_level="unknown",

            recommended_intensity=None,

            has_sufficient_history=False,

            explanation=(
                "No swimming sessions were recorded "
                "during the last 7 days, so the planner "
                "does not have enough training-history "
                "information to adjust the user's "
                "requested intensity."
            ),
        )


    # =====================================================
    # LOAD CALCULATION
    # =====================================================

    intensity_weight = {
        "easy": 1,
        "moderate": 2,
        "hard": 3,
    }

    total_minutes = 0

    easy_sessions = 0
    moderate_sessions = 0
    hard_sessions = 0

    load_score = 0


    for session in recent_sessions:

        total_minutes += (
            session.duration_minutes
        )

        load_score += (
            session.duration_minutes
            * intensity_weight[
                session.intensity
            ]
        )


        if session.intensity == "easy":

            easy_sessions += 1

        elif session.intensity == "moderate":

            moderate_sessions += 1

        elif session.intensity == "hard":

            hard_sessions += 1


    # =====================================================
    # LOAD LEVEL
    # =====================================================

    if load_score < 120:

        load_level = "low"

        recommended = "moderate"

        explanation = (
            "Recent training load is relatively low."
        )


    elif load_score < 300:

        load_level = "moderate"

        recommended = "moderate"

        explanation = (
            "Recent training load is moderate."
        )


    elif load_score < 500:

        load_level = "high"

        recommended = "easy"

        explanation = (
            "Recent training load is relatively high, "
            "so an easier session is recommended."
        )


    else:

        load_level = "very_high"

        recommended = "easy"

        explanation = (
            "Recent training load is very high in this "
            "simplified model, so an easy session is "
            "recommended."
        )


    # =====================================================
    # HARD SESSION SAFEGUARD
    # =====================================================

    if hard_sessions >= 2:

        recommended = "easy"

        explanation = (
            "At least two hard swimming sessions were "
            "recorded during the last 7 days, so the "
            "planner recommends an easier session."
        )


    # =====================================================
    # RETURN ANALYSIS
    # =====================================================

    return TrainingLoadResult(

        sessions_last_7_days=(
            len(recent_sessions)
        ),

        total_minutes_last_7_days=(
            total_minutes
        ),

        easy_sessions=(
            easy_sessions
        ),

        moderate_sessions=(
            moderate_sessions
        ),

        hard_sessions=(
            hard_sessions
        ),

        training_load_score=(
            load_score
        ),

        training_load_level=(
            load_level
        ),

        recommended_intensity=(
            recommended
        ),

        has_sufficient_history=True,

        explanation=(
            explanation
        ),
    )


# =========================================================
# INTENSITY DECISION
# =========================================================

def decide_workout_intensity(
    requested_intensity: str,
    training_load: TrainingLoadResult,
) -> IntensityDecision:
    """
    Decide the final workout intensity.

    If training history does not provide a recommendation,
    preserve the user's requested intensity.

    If history recommends a lower intensity, use the more
    conservative recommendation.
    """

    if requested_intensity not in [
        "easy",
        "moderate",
        "hard",
    ]:

        requested_intensity = (
            "moderate"
        )


    recommended = (
        training_load.recommended_intensity
    )


    # =====================================================
    # NO HISTORY-BASED RECOMMENDATION
    # =====================================================

    if recommended is None:

        return IntensityDecision(

            requested_intensity=(
                requested_intensity
            ),

            recommended_intensity=None,

            final_intensity=(
                requested_intensity
            ),

            adjusted=False,

            explanation=(
                "There is not enough recent swimming "
                "history to justify changing the user's "
                "requested intensity, so the requested "
                "intensity is preserved."
            ),
        )


    # =====================================================
    # COMPARE INTENSITIES
    # =====================================================

    intensity_rank = {
        "easy": 1,
        "moderate": 2,
        "hard": 3,
    }


    if (
        intensity_rank[recommended]
        <
        intensity_rank[
            requested_intensity
        ]
    ):

        final_intensity = (
            recommended
        )

    else:

        final_intensity = (
            requested_intensity
        )


    adjusted = (
        final_intensity
        != requested_intensity
    )


    # =====================================================
    # EXPLANATION
    # =====================================================

    if adjusted:

        explanation = (
            f"The user requested a "
            f"{requested_intensity} session, "
            f"but recent training history supports "
            f"a more conservative "
            f"{final_intensity} session."
        )

    else:

        explanation = (
            f"The requested {requested_intensity} "
            f"intensity is compatible with the "
            f"current training-load recommendation."
        )


    # =====================================================
    # RETURN DECISION
    # =====================================================

    return IntensityDecision(

        requested_intensity=(
            requested_intensity
        ),

        recommended_intensity=(
            recommended
        ),

        final_intensity=(
            final_intensity
        ),

        adjusted=(
            adjusted
        ),

        explanation=(
            explanation
        ),
    )