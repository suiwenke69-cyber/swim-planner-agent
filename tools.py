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
    intensity: str
):

    duration_minutes = max(
        15,
        min(duration_minutes, 120)
    )

    if duration_minutes <= 30:

        warmup = 5
        cooldown = 5

    elif duration_minutes <= 60:

        warmup = 10
        cooldown = 5

    else:

        warmup = 10
        cooldown = 10

    main_swim = (
        duration_minutes
        - warmup
        - cooldown
    )

    descriptions = {

        "easy":
            "Relaxed continuous swimming with comfortable breathing.",

        "moderate":
            "Steady swimming at a sustainable pace with short rests.",

        "hard":
            "Higher-intensity intervals with recovery periods."
    }

    if intensity not in descriptions:
        intensity = "moderate"

    return {
        "total_duration_minutes":
            duration_minutes,

        "intensity":
            intensity,

        "warmup_minutes":
            warmup,

        "main_swim_minutes":
            main_swim,

        "cooldown_minutes":
            cooldown,

        "main_swim_description":
            descriptions[intensity]
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