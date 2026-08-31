from v2.models.provider import get_model
from v2.models.nutrition import MealAnalysis


# =========================================================
# NUTRITION ANALYSIS TOOL
# =========================================================

def analyze_meal(
    meal_description: str,
) -> MealAnalysis:
    """
    Analyze a meal using an OpenAI model and return
    structured nutritional information.

    The result is intended for downstream exercise-planning
    tools, not for clinical nutrition assessment.
    """

    model = get_model()

    structured_model = (
        model.with_structured_output(
            MealAnalysis
        )
    )

    prompt = f"""
You are the nutrition-analysis component of a swimming
planning system.

Analyze the user's meal and estimate its nutritional
characteristics.

The output will be used by downstream exercise-planning
tools.

Important rules:

1. Nutrition values are estimates.

2. Do not pretend to know exact food weights unless the
   user provides them.

3. Use reasonable ranges rather than false precision.

4. Consider:
   - portion size
   - cooking method
   - sauces
   - added oil
   - sugary drinks
   - uncertainty in restaurant food

5. The digestion_load field should consider the overall
   meal size and composition, especially:
   - fat
   - protein
   - fiber
   - total food volume

6. confidence should reflect how much information the user
   actually provided.

7. Do not provide medical advice.

USER MEAL:

{meal_description}
"""

    result = structured_model.invoke(
        prompt
    )

    return result