import time

from v2.tools.vision_nutrition import (
    analyze_meal_image,
)


# =========================================================
# TEST IMAGE
# =========================================================

IMAGE_PATH = (
    "tests/sample_meal.jpg"
)


# =========================================================
# ANALYZE
# =========================================================

print()
print("📷 V2 VISION NUTRITION TEST")
print("================================")
print()

print(
    f"Image: {IMAGE_PATH}"
)

print()

print(
    "Analyzing meal..."
)

print()


start = time.perf_counter()


result = analyze_meal_image(
    IMAGE_PATH
)


elapsed = (
    time.perf_counter()
    - start
)


# =========================================================
# OUTPUT
# =========================================================

print(
    result.model_dump_json(
        indent=2
    )
)


print()
print("================================")

print(
    f"Vision analysis time: "
    f"{elapsed:.3f} seconds"
)

print()