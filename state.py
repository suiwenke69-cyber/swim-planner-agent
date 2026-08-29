# =========================================================
# SWIM PLANNER STATE
# =========================================================

user_state = {
    "foods": [],
    "meal_size": None,
    "minutes_since_meal": None,
    "swim_duration": None,
    "swim_intensity": None
}


def get_state():
    """
    Return the current user state.
    """
    return user_state


def update_state(updates):
    """
    Update specific values in the user state.
    """

    for key, value in updates.items():

        if key in user_state and value is not None:
            user_state[key] = value

    return user_state


def add_time_since_meal(minutes):
    """
    Add elapsed time to minutes_since_meal.

    Example:
    current = 30
    user says "wait another hour"
    add 60
    result = 90
    """

    if user_state["minutes_since_meal"] is None:
        user_state["minutes_since_meal"] = minutes

    else:
        user_state["minutes_since_meal"] += minutes

    return user_state["minutes_since_meal"]


def reset_state():
    """
    Reset the user state.
    """

    user_state["foods"] = []
    user_state["meal_size"] = None
    user_state["minutes_since_meal"] = None
    user_state["swim_duration"] = None
    user_state["swim_intensity"] = None