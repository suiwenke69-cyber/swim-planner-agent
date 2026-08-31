from v2.models.workout import (
    SwimmingWorkout,
    WorkoutSet,
)


# =========================================================
# WORKOUT PLANNING TOOL
# =========================================================

def create_swimming_workout(
    duration_minutes: int,
    intensity: str = "moderate",
    level: str = "beginner",
    goal: str = "aerobic",
    stroke: str = "freestyle",
    pool_length: int = 25,
) -> SwimmingWorkout:
    """
    Create a deterministic swimming workout.

    This tool does not use an LLM.

    It converts structured user preferences into a
    distance-based workout.
    """

    # =====================================================
    # VALIDATION
    # =====================================================

    duration_minutes = max(
        15,
        min(
            int(duration_minutes),
            120,
        ),
    )

    if intensity not in [
        "easy",
        "moderate",
        "hard",
    ]:
        intensity = "moderate"

    if level not in [
        "beginner",
        "intermediate",
        "advanced",
    ]:
        level = "beginner"

    if goal not in [
        "aerobic",
        "endurance",
        "recovery",
        "speed",
    ]:
        goal = "aerobic"

    if stroke not in [
        "freestyle",
        "breaststroke",
        "backstroke",
        "mixed",
    ]:
        stroke = "freestyle"

    if pool_length not in [
        25,
        50,
    ]:
        pool_length = 25


    # =====================================================
    # APPROXIMATE SWIMMING SPEED
    # =====================================================

    meters_per_minute = {
        "beginner": {
            "easy": 18,
            "moderate": 22,
            "hard": 25,
        },

        "intermediate": {
            "easy": 25,
            "moderate": 30,
            "hard": 35,
        },

        "advanced": {
            "easy": 32,
            "moderate": 38,
            "hard": 45,
        },
    }[level][intensity]


    estimated_distance = (
        duration_minutes
        * meters_per_minute
    )

    estimated_distance = int(
        estimated_distance
        // pool_length
        * pool_length
    )


    # =====================================================
    # DISTANCE DISTRIBUTION
    # =====================================================

    warmup_distance = int(
        estimated_distance
        * 0.15
    )

    cooldown_distance = int(
        estimated_distance
        * 0.10
    )


    warmup_distance = (
        warmup_distance
        // pool_length
        * pool_length
    )

    cooldown_distance = (
        cooldown_distance
        // pool_length
        * pool_length
    )


    main_distance = (
        estimated_distance
        - warmup_distance
        - cooldown_distance
    )


    # =====================================================
    # MAIN SET DESCRIPTION
    # =====================================================

    if goal == "recovery":

        main_instruction = (
            f"Easy continuous {stroke}. "
            f"Keep breathing relaxed and focus on technique."
        )

    elif goal == "speed":

        main_instruction = (
            f"Short, strong {stroke} intervals with "
            f"generous recovery between efforts."
        )

    elif goal == "endurance":

        main_instruction = (
            f"Longer steady {stroke} repeats. "
            f"Maintain consistent technique and pacing."
        )

    else:

        main_instruction = (
            f"Steady aerobic {stroke}. "
            f"Maintain a sustainable rhythm."
        )


    # =====================================================
    # RETURN
    # =====================================================

    return SwimmingWorkout(

        duration_minutes=duration_minutes,

        intensity=intensity,

        goal=goal,

        level=level,

        stroke=stroke,

        pool_length_m=pool_length,

        estimated_total_distance_m=(
            warmup_distance
            + main_distance
            + cooldown_distance
        ),

        warmup=WorkoutSet(
            name="Warm-up",
            distance_m=warmup_distance,
            instruction=(
                f"Easy {stroke} with relaxed technique."
            ),
        ),

        main_set=WorkoutSet(
            name="Main Set",
            distance_m=main_distance,
            instruction=main_instruction,
        ),

        cooldown=WorkoutSet(
            name="Cool-down",
            distance_m=cooldown_distance,
            instruction=(
                "Very easy swimming with relaxed breathing."
            ),
        ),

        planning_note=(
            "Workout distances are approximate planning "
            "estimates and should be adjusted to the "
            "swimmer's actual pace and comfort."
        ),
    )