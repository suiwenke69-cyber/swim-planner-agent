from v2.models.nutrition import MealAnalysis

from v2.models.meal_timing import (
    MealTimingResult,
)


# =========================================================
# NUTRITION-AWARE MEAL TIMING TOOL
# =========================================================

def calculate_meal_timing(
    meal_analysis: MealAnalysis,
    minutes_since_meal: int,
    planned_intensity: str = "moderate",
) -> MealTimingResult:
    """
    Estimate a conservative pre-swim waiting period using
    structured meal information.

    This is a simplified planning heuristic for the
    Swim Planner prototype.

    It is NOT a medical model.
    """

    # =====================================================
    # VALIDATE INPUT
    # =====================================================

    minutes_since_meal = max(
        0,
        int(minutes_since_meal),
    )

    planned_intensity = (
        planned_intensity.lower()
    )

    if planned_intensity not in [
        "easy",
        "moderate",
        "hard",
    ]:
        planned_intensity = "moderate"


    # =====================================================
    # 1 — BASE WAIT FROM DIGESTION LOAD
    # =====================================================

    digestion_wait = {
        "light": 30,
        "moderate": 60,
        "heavy": 90,
    }

    base_wait = digestion_wait[
        meal_analysis.digestion_load
    ]


    # =====================================================
    # 2 — NUTRITION COMPOSITION ADJUSTMENTS
    # =====================================================

    nutrition_adjustment = 0

    reasons = []


    # -----------------------------------------------------
    # FAT
    # -----------------------------------------------------

    average_fat = (
        meal_analysis.fat_g.low
        + meal_analysis.fat_g.high
    ) / 2

    if average_fat >= 35:

        nutrition_adjustment += 30

        reasons.append(
            "higher estimated fat content"
        )

    elif average_fat >= 20:

        nutrition_adjustment += 15

        reasons.append(
            "moderate estimated fat content"
        )


    # -----------------------------------------------------
    # TOTAL ENERGY
    # -----------------------------------------------------

    average_calories = (
        meal_analysis.calories_kcal.low
        + meal_analysis.calories_kcal.high
    ) / 2

    if average_calories >= 1000:

        nutrition_adjustment += 30

        reasons.append(
            "large estimated energy intake"
        )

    elif average_calories >= 700:

        nutrition_adjustment += 15

        reasons.append(
            "substantial estimated meal size"
        )


    # -----------------------------------------------------
    # FIBER
    # -----------------------------------------------------

    average_fiber = (
        meal_analysis.fiber_g.low
        + meal_analysis.fiber_g.high
    ) / 2

    if average_fiber >= 12:

        nutrition_adjustment += 15

        reasons.append(
            "higher estimated fiber content"
        )


    # =====================================================
    # 3 — SWIMMING INTENSITY ADJUSTMENT
    # =====================================================

    intensity_adjustments = {
        "easy": 0,
        "moderate": 15,
        "hard": 30,
    }

    intensity_adjustment = (
        intensity_adjustments[
            planned_intensity
        ]
    )

    if planned_intensity == "moderate":

        reasons.append(
            "moderate planned swimming intensity"
        )

    elif planned_intensity == "hard":

        reasons.append(
            "hard planned swimming intensity"
        )


    # =====================================================
    # 4 — FINAL WAIT
    # =====================================================

    recommended_wait = (
        base_wait
        + nutrition_adjustment
        + intensity_adjustment
    )


    # Keep the prototype within a sensible planning range.

    recommended_wait = max(
        30,
        min(
            recommended_wait,
            180,
        ),
    )


    # =====================================================
    # 5 — REMAINING TIME
    # =====================================================

    remaining_wait = max(
        0,
        recommended_wait
        - minutes_since_meal,
    )


    if remaining_wait == 0:

        status = "ready"

    else:

        status = "wait"


    # =====================================================
    # 6 — EXPLANATION
    # =====================================================

    if reasons:

        factor_text = ", ".join(
            reasons
        )

        explanation = (
            f"The estimate reflects a "
            f"{meal_analysis.digestion_load} digestion "
            f"load, with additional consideration for "
            f"{factor_text}."
        )

    else:

        explanation = (
            f"The estimate is primarily based on the "
            f"{meal_analysis.digestion_load} digestion "
            f"load of the meal."
        )


    # =====================================================
    # RETURN STRUCTURED RESULT
    # =====================================================

    return MealTimingResult(
        base_wait_minutes=base_wait,

        nutrition_adjustment_minutes=(
            nutrition_adjustment
        ),

        intensity_adjustment_minutes=(
            intensity_adjustment
        ),

        recommended_wait_minutes=(
            recommended_wait
        ),

        minutes_since_meal=(
            minutes_since_meal
        ),

        remaining_wait_minutes=(
            remaining_wait
        ),

        status=status,

        explanation=explanation,
    )