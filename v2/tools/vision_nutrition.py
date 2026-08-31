import base64
import mimetypes

from pathlib import Path

from v2.models.provider import (
    get_model,
)

from v2.models.nutrition import (
    MealAnalysis,
)


# =========================================================
# IMAGE → DATA URL
# =========================================================

def image_to_data_url(
    image_path: str,
) -> str:
    """
    Convert a local image into a base64 data URL
    that can be sent to the multimodal model.
    """

    path = Path(
        image_path
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )


    mime_type, _ = (
        mimetypes.guess_type(
            str(path)
        )
    )


    if mime_type is None:

        mime_type = (
            "image/jpeg"
        )


    with open(
        path,
        "rb",
    ) as image_file:

        encoded = (
            base64.b64encode(
                image_file.read()
            )
            .decode("utf-8")
        )


    return (
        f"data:{mime_type};"
        f"base64,{encoded}"
    )


# =========================================================
# VISION NUTRITION ANALYSIS
# =========================================================

def analyze_meal_image(
    image_path: str,
) -> MealAnalysis:
    """
    Analyze a meal photograph using a multimodal
    OpenAI model.

    The model estimates:

    - foods
    - approximate portions
    - calories
    - protein
    - carbohydrates
    - fat
    - fiber
    - digestion characteristics
    - uncertainty

    Results are estimates rather than measured
    nutritional facts.
    """

    model = get_model()


    structured_model = (
        model.with_structured_output(
            MealAnalysis
        )
    )


    image_url = image_to_data_url(
        image_path
    )


    message = [
        {
            "role": "system",

            "content": (
                "You are the visual nutrition-analysis "
                "component of Swim Planner. "
                "Analyze meal photographs conservatively. "
                "Never pretend that visual portion or "
                "nutrition estimates are exact."
            ),
        },

        {
            "role": "user",

            "content": [

                {
                    "type": "text",

                    "text": """
Analyze this meal photograph.

First identify visible foods and drinks.

For each item:
- estimate a reasonable portion range or description
- report confidence

Then estimate the nutrition of the entire visible meal:

- calories
- protein
- carbohydrates
- fat
- fiber

Use ranges rather than false precision.

Consider visible cooking methods and obvious sauces or
fried foods when possible.

If portion size, hidden oil, ingredients, or preparation
cannot be determined from the image, explicitly reflect
that uncertainty in:

- confidence
- uncertainty_reason

The analysis is for exercise planning, not medical or
clinical nutrition assessment.
""",
                },

                {
                    "type": "image_url",

                    "image_url": {
                        "url": image_url
                    },
                },
            ],
        },
    ]


    result = structured_model.invoke(
        message
    )


    return result