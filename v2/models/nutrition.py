from typing import Literal

from pydantic import BaseModel, Field


# =========================================================
# NUMERIC RANGE
# =========================================================

class NutritionRange(BaseModel):
    """
    Estimated numerical range.
    """

    low: float = Field(
        ge=0,
    )

    high: float = Field(
        ge=0,
    )


# =========================================================
# INDIVIDUAL FOOD ITEM
# =========================================================

class FoodItemEstimate(BaseModel):
    """
    One food or drink identified in a meal.
    """

    name: str

    estimated_portion: str = Field(
        description=(
            "Human-readable approximate portion, such as "
            "'1 fried egg', 'about 200-250 g rice', or "
            "'one large cup'."
        )
    )

    confidence: Literal[
        "low",
        "medium",
        "high",
    ]


# =========================================================
# COMPLETE MEAL ANALYSIS
# =========================================================

class MealAnalysis(BaseModel):
    """
    Structured nutrition analysis for exercise planning.

    Numerical values are estimates unless verified
    nutrition information is provided.
    """

    foods: list[str]

    food_items: list[
        FoodItemEstimate
    ]

    portion_size: Literal[
        "small",
        "medium",
        "large",
        "unknown",
    ]

    # =====================================================
    # ENERGY
    # =====================================================

    calories_kcal: NutritionRange


    # =====================================================
    # MACRONUTRIENTS
    # =====================================================

    protein_g: NutritionRange

    carbohydrates_g: NutritionRange

    fat_g: NutritionRange

    fiber_g: NutritionRange


    # =====================================================
    # EXERCISE-PLANNING CHARACTERISTICS
    # =====================================================

    digestion_load: Literal[
        "light",
        "moderate",
        "heavy",
    ]

    carbohydrate_load: Literal[
        "low",
        "moderate",
        "high",
    ]

    fat_load: Literal[
        "low",
        "moderate",
        "high",
    ]


    # =====================================================
    # UNCERTAINTY
    # =====================================================

    confidence: Literal[
        "low",
        "medium",
        "high",
    ]

    uncertainty_reason: str

    reasoning_summary: str