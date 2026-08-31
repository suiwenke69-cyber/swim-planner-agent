import time

from langchain_openai import ChatOpenAI

from models.nutrition import MealAnalysis


# =========================================================
# MODEL
# =========================================================

model = ChatOpenAI(
    model="gpt-5-mini"
)


# =========================================================
# STRUCTURED MODEL
# =========================================================

nutrition_model = model.with_structured_output(
    MealAnalysis
)


# =========================================================
# USER MEAL
# =========================================================

meal_description = """
I ate chicken rice, a fried egg, and a large milk tea.
It was a normal-sized chicken rice portion.
"""


# =========================================================
# PROMPT
# =========================================================

prompt = f"""
You are analyzing a meal for a swimming-planning application.

Analyze the meal conservatively using the provided
structured schema.

The purpose is to help downstream exercise-planning tools
understand the approximate nutritional and digestive
characteristics of the meal.

Important:

- Estimates are approximate.
- Do not claim medical precision.
- Do not invent exact food weights.
- Use wider calorie ranges when information is uncertain.
- Confidence should reflect how much information was given.

Meal:

{meal_description}
"""


# =========================================================
# CALL MODEL
# =========================================================

start = time.perf_counter()

result = nutrition_model.invoke(
    prompt
)

elapsed = (
    time.perf_counter()
    - start
)


# =========================================================
# OUTPUT
# =========================================================

print()
print("🍽 Structured Meal Analysis")
print("================================")
print()

print(
    result.model_dump_json(
        indent=2
    )
)

print()
print("================================")

print(
    f"⏱ Analysis time: "
    f"{elapsed:.3f} seconds"
)

print()