# =========================================================
# TOOL 1 — MEAL TIMING
# =========================================================

def meal_timing_tool(
    meal_size: str,
    minutes_since_meal: int,
    desired_intensity: str
):

    rules = {
        "light": {
            "easy": 30,
            "moderate": 45,
            "hard": 60
        },

        "medium": {
            "easy": 60,
            "moderate": 90,
            "hard": 120
        },

        "heavy": {
            "easy": 90,
            "moderate": 120,
            "hard": 180
        }
    }

    meal_size = meal_size.lower()
    desired_intensity = desired_intensity.lower()

    if meal_size not in rules:
        meal_size = "medium"

    if desired_intensity not in [
        "easy",
        "moderate",
        "hard"
    ]:
        desired_intensity = "moderate"

    recommended_wait = (
        rules[meal_size][desired_intensity]
    )

    remaining_wait = max(
        0,
        recommended_wait - minutes_since_meal
    )

    status = (
        "READY"
        if remaining_wait == 0
        else "WAIT"
    )

    return {
        "recommended_wait_minutes":
            recommended_wait,

        "minutes_since_meal":
            minutes_since_meal,

        "remaining_wait_minutes":
            remaining_wait,

        "status":
            status
    }


# =========================================================
# TOOL 2 — SWIMMING WORKOUT
# =========================================================

def swim_workout_tool(
    duration_minutes: int,
    intensity: str,
    level: str = "beginner",
    goal: str = "aerobic",
    stroke: str = "freestyle",
    pool_length: int = 25,
):
    """
    Create a structured swimming workout.

    The workout adapts to:
    - swimming level
    - training goal
    - intensity
    - preferred stroke
    - pool length
    """

    # =====================================================
    # VALIDATE INPUTS
    # =====================================================

    duration_minutes = max(
        15,
        min(int(duration_minutes), 120),
    )

    intensity = intensity.lower()
    level = level.lower()
    goal = goal.lower()
    stroke = stroke.lower()

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
    # ESTIMATE DISTANCE
    # =====================================================

    # Approximate sustainable meters per minute.
    # These are planning values, not performance standards.

    pace_map = {
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
    }

    meters_per_minute = (
        pace_map[level][intensity]
    )

    estimated_distance = (
        duration_minutes
        * meters_per_minute
    )

    # Round down to full pool lengths.

    estimated_distance = (
        estimated_distance
        // pool_length
        * pool_length
    )


    # =====================================================
    # WORKOUT ALLOCATION
    # =====================================================

    if duration_minutes <= 30:

        warmup_ratio = 0.20
        cooldown_ratio = 0.15

    else:

        warmup_ratio = 0.15
        cooldown_ratio = 0.10


    warmup_distance = int(
        estimated_distance
        * warmup_ratio
    )

    cooldown_distance = int(
        estimated_distance
        * cooldown_ratio
    )

    # Round to pool lengths.

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
    # MAIN SET DESIGN
    # =====================================================

    if level == "beginner":

        repeat_distance = (
            50 if pool_length == 25 else 100
        )

    elif level == "intermediate":

        repeat_distance = 100

    else:

        repeat_distance = 200


    # Speed training uses shorter intervals.

    if goal == "speed":

        repeat_distance = (
            50 if pool_length == 25 else 100
        )


    repeats = max(
        1,
        main_distance // repeat_distance,
    )


    # Adjust actual main distance.

    main_distance = (
        repeats
        * repeat_distance
    )


    # =====================================================
    # REST INTERVAL
    # =====================================================

    if goal == "recovery":

        rest_seconds = 30

    elif goal == "speed":

        rest_seconds = 40

    elif intensity == "easy":

        rest_seconds = 30

    elif intensity == "moderate":

        rest_seconds = 20

    else:

        rest_seconds = 30


    # =====================================================
    # GOAL DESCRIPTION
    # =====================================================

    goal_descriptions = {

        "aerobic":
            "Maintain a steady sustainable pace and focus "
            "on relaxed breathing.",

        "endurance":
            "Maintain consistent technique across longer "
            "repeats and avoid starting too fast.",

        "recovery":
            "Keep effort comfortable and prioritize smooth "
            "technique over speed.",

        "speed":
            "Swim the work intervals strongly while using "
            "the recovery periods to maintain quality.",
    }


    # =====================================================
    # FINAL WORKOUT
    # =====================================================

    actual_total_distance = (
        warmup_distance
        + main_distance
        + cooldown_distance
    )

    return {
        "level": level,
        "goal": goal,
        "stroke": stroke,
        "pool_length_m": pool_length,

        "duration_minutes": duration_minutes,
        "intensity": intensity,

        "estimated_total_distance_m":
            actual_total_distance,

        "warmup": {
            "distance_m":
                warmup_distance,

            "instruction":
                f"Easy {stroke} focusing on relaxed technique.",
        },

        "main_set": {
            "repeats":
                repeats,

            "distance_per_repeat_m":
                repeat_distance,

            "total_distance_m":
                main_distance,

            "rest_seconds":
                rest_seconds,

            "instruction":
                goal_descriptions[goal],
        },

        "cooldown": {
            "distance_m":
                cooldown_distance,

            "instruction":
                "Very easy swimming with relaxed breathing.",
        },
    }


# =========================================================
# TOOL 3 — NUTRITION
# =========================================================

def nutrition_analysis_tool(foods):

    food_text = " ".join(foods).lower()

    protein_words = [
        "chicken",
        "beef",
        "fish",
        "egg",
        "eggs",
        "tofu",
        "pork"
    ]

    carb_words = [
        "rice",
        "bread",
        "noodles",
        "pasta",
        "potato",
        "fries",
        "oats",
        "banana"
    ]

    high_fat_words = [
        "fried",
        "fries",
        "burger",
        "pizza",
        "cream",
        "butter"
    ]

    sugary_words = [
        "milk tea",
        "bubble tea",
        "soda",
        "cake",
        "dessert",
        "ice cream"
    ]

    return {

        "foods":
            foods,

        "contains_protein_source":
            any(
                word in food_text
                for word in protein_words
            ),

        "contains_carbohydrate_source":
            any(
                word in food_text
                for word in carb_words
            ),

        "contains_high_fat_food":
            any(
                word in food_text
                for word in high_fat_words
            ),

        "contains_sugary_food_or_drink":
            any(
                word in food_text
                for word in sugary_words
            )
    }

from datetime import datetime, timedelta


# =========================================================
# TOOL 4 — TRAINING LOAD ANALYSIS
# =========================================================

def training_load_tool(
    swimming_history: list,
):
    """
    Analyze swimming activity from the most recent 7 days.

    This is a simple planning heuristic for the demo Agent.
    It is not a medical or professional training-load model.
    """

    today = datetime.now().date()

    seven_days_ago = (
        today - timedelta(days=6)
    )

    recent_sessions = []

    # =====================================================
    # FILTER LAST 7 DAYS
    # =====================================================

    for session in swimming_history:

        try:

            session_date = datetime.strptime(
                session["date"],
                "%Y-%m-%d",
            ).date()

        except (
            KeyError,
            ValueError,
            TypeError,
        ):

            continue

        if (
            seven_days_ago
            <= session_date
            <= today
        ):

            recent_sessions.append(
                session
            )

    # =====================================================
    # NO RECENT TRAINING
    # =====================================================

    if not recent_sessions:

        return {
            "sessions_last_7_days": 0,
            "total_minutes_last_7_days": 0,
            "easy_sessions": 0,
            "moderate_sessions": 0,
            "hard_sessions": 0,
            "training_load_score": 0,
            "training_load_level": "low",
            "recommended_intensity": "moderate",
            "reason":
                "No swimming sessions were recorded "
                "during the last 7 days.",
        }

    # =====================================================
    # CALCULATE TRAINING LOAD
    # =====================================================

    total_minutes = 0

    easy_sessions = 0
    moderate_sessions = 0
    hard_sessions = 0

    training_load_score = 0

    intensity_weights = {
        "easy": 1,
        "moderate": 2,
        "hard": 3,
    }

    for session in recent_sessions:

        duration = session.get(
            "duration_minutes",
            0,
        )

        intensity = session.get(
            "intensity",
            "moderate",
        ).lower()

        if intensity not in intensity_weights:
            intensity = "moderate"

        total_minutes += duration

        if intensity == "easy":
            easy_sessions += 1

        elif intensity == "moderate":
            moderate_sessions += 1

        elif intensity == "hard":
            hard_sessions += 1

        # Simple load score:
        # duration × intensity weight

        training_load_score += (
            duration
            * intensity_weights[intensity]
        )

    # =====================================================
    # DETERMINE LOAD LEVEL
    # =====================================================

    if training_load_score < 120:

        load_level = "low"

        recommended_intensity = (
            "moderate"
        )

        reason = (
            "Recent swimming load is relatively low, "
            "so a moderate session is reasonable."
        )

    elif training_load_score < 300:

        load_level = "moderate"

        recommended_intensity = (
            "moderate"
        )

        reason = (
            "Recent swimming load is moderate. "
            "A moderate session is reasonable, "
            "but avoid unnecessary intensity."
        )

    elif training_load_score < 500:

        load_level = "high"

        recommended_intensity = (
            "easy"
        )

        reason = (
            "Recent swimming load is relatively high. "
            "An easier session may provide better recovery."
        )

    else:

        load_level = "very_high"

        recommended_intensity = (
            "easy"
        )

        reason = (
            "Recent swimming load is very high in this "
            "simplified model. Consider an easy or "
            "recovery-focused session."
        )

    # =====================================================
    # HARD SESSION SAFEGUARD
    # =====================================================

    if hard_sessions >= 2:

        recommended_intensity = "easy"

        reason = (
            "At least two hard sessions were recorded "
            "during the last 7 days, so an easy session "
            "is recommended in this simplified model."
        )

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {
        "sessions_last_7_days":
            len(recent_sessions),

        "total_minutes_last_7_days":
            total_minutes,

        "easy_sessions":
            easy_sessions,

        "moderate_sessions":
            moderate_sessions,

        "hard_sessions":
            hard_sessions,

        "training_load_score":
            training_load_score,

        "training_load_level":
            load_level,

        "recommended_intensity":
            recommended_intensity,

        "reason":
            reason,
    }