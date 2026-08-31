from datetime import datetime, timedelta


# =========================================================
# TEMPORARY USER STATE
# =========================================================

user_state = {
    "foods": [],
    "meal_size": None,
    "meal_finished_at": None,
    "minutes_since_meal": None,

    # Swimming plan
    "swim_duration": None,
    "swim_intensity": None,

    # V7 swimming profile
    "swimming_level": None,
    "swimming_goal": None,
    "preferred_stroke": None,
    "pool_length": None,
}


# =========================================================
# REFRESH REAL-TIME MEAL TIMER
# =========================================================

def refresh_meal_time():
    """
    Recalculate minutes_since_meal using the real clock.

    Example:
        meal_finished_at = 18:00
        current time = 19:30

        minutes_since_meal = 90
    """

    meal_finished_at = user_state["meal_finished_at"]

    if meal_finished_at is None:
        user_state["minutes_since_meal"] = None
        return

    now = datetime.now()

    elapsed = now - meal_finished_at

    elapsed_minutes = int(
        elapsed.total_seconds() / 60
    )

    user_state["minutes_since_meal"] = max(
        0,
        elapsed_minutes,
    )


# =========================================================
# GET STATE
# =========================================================

def get_state():
    """
    Return the current state.

    Meal timing is refreshed every time the state is read.
    """

    refresh_meal_time()

    return user_state


# =========================================================
# UPDATE STATE
# =========================================================

def update_state(updates):
    """
    Update temporary state.

    Special rule:

    If the LLM gives:
        minutes_since_meal = 30

    Python converts this into:
        meal_finished_at = current time - 30 minutes

    This allows elapsed meal time to increase automatically
    as real-world time passes.
    """

    for key, value in updates.items():

        if value is None:
            continue

        # -------------------------------------------------
        # MEAL TIME
        # -------------------------------------------------

        if key == "minutes_since_meal":

            try:
                minutes = int(value)

            except (TypeError, ValueError):
                continue

            minutes = max(
                0,
                minutes,
            )

            user_state["meal_finished_at"] = (
                datetime.now()
                - timedelta(
                    minutes=minutes
                )
            )

            user_state["minutes_since_meal"] = minutes

        # -------------------------------------------------
        # OTHER STATE VALUES
        # -------------------------------------------------

        elif key in user_state:

            user_state[key] = value

    refresh_meal_time()

    return user_state


# =========================================================
# ADD HYPOTHETICAL WAITING TIME
# =========================================================

def add_time_since_meal(minutes):
    """
    Handle messages such as:

        "What if I wait another hour?"

    Example:

        Current elapsed time = 30 minutes
        Additional hypothetical wait = 60 minutes

    The stored meal timestamp is moved backward by 60 minutes,
    producing approximately 90 minutes of elapsed meal time.

    Note:
    This currently modifies the temporary state. A future
    version can separate real state from hypothetical scenarios.
    """

    try:
        minutes = int(minutes)

    except (TypeError, ValueError):
        return user_state["minutes_since_meal"]

    minutes = max(
        0,
        minutes,
    )

    # No meal time exists yet.
    if user_state["meal_finished_at"] is None:

        user_state["meal_finished_at"] = (
            datetime.now()
            - timedelta(
                minutes=minutes
            )
        )

    # Existing meal time:
    # move it backward to simulate extra waiting.
    else:

        user_state["meal_finished_at"] = (
            user_state["meal_finished_at"]
            - timedelta(
                minutes=minutes
            )
        )

    refresh_meal_time()

    return user_state["minutes_since_meal"]


# =========================================================
# RESET STATE
# =========================================================

def reset_state():
    """
    Clear all temporary state.
    """

    user_state["foods"] = []
    user_state["meal_size"] = None
    user_state["meal_finished_at"] = None
    user_state["minutes_since_meal"] = None
    user_state["swim_duration"] = None
    user_state["swim_intensity"] = None
    user_state["swimming_level"] = None
    user_state["swimming_goal"] = None
    user_state["preferred_stroke"] = None
    user_state["pool_length"] = None

# =========================================================
# JSON-SAFE STATE
# =========================================================

def get_serializable_state():
    """
    Return a copy of the state that can safely be displayed
    as JSON.

    datetime objects are converted into ISO-format strings.
    """

    refresh_meal_time()

    state_copy = user_state.copy()

    meal_finished_at = state_copy[
        "meal_finished_at"
    ]

    if meal_finished_at is not None:

        state_copy["meal_finished_at"] = (
            meal_finished_at.isoformat()
        )

    state_copy["foods"] = (
        state_copy["foods"].copy()
    )

    return state_copy