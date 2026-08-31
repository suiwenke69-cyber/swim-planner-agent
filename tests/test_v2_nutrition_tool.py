import time

from v2.tools.nutrition import analyze_meal


meal = """
I ate chicken rice, a fried egg, and a large milk tea.
The chicken rice was a normal restaurant portion.
"""


start = time.perf_counter()


result = analyze_meal(
    meal
)


elapsed = (
    time.perf_counter()
    - start
)


print()
print("🍽 V2 Nutrition Tool")
print("==============================")
print()

print(
    result.model_dump_json(
        indent=2
    )
)

print()
print("==============================")

print(
    f"Analysis time: "
    f"{elapsed:.3f} seconds"
)

print()