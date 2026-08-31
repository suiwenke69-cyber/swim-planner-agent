from v2.models.provider import get_model

from v2.models.user_input import (
    ParsedUserInput,
)


# =========================================================
# USER INPUT PARSER
# =========================================================

def parse_user_input(
    user_message: str,
) -> ParsedUserInput:
    """
    Convert natural-language input into structured
    Swim Planner state and classify the user's intent.
    """

    model = get_model()

    structured_model = (
        model.with_structured_output(
            ParsedUserInput
        )
    )

    prompt = f"""
You are the input-understanding component of Swim Planner.

Extract only information that the user actually provides.

Do not invent missing information.


=========================================================
INTENT
=========================================================

Choose exactly one primary intent.

plan_workout:
The user wants to plan, create, modify, or discuss an
upcoming swimming workout.

Examples:

"I want a 40-minute moderate swim."

"Make today's workout hard."

"Can you give me a recovery session?"


record_completed_swim:
The user explicitly says they already completed a swimming
session.

Examples:

"I just finished a 40-minute hard swim."

"I completed a 30-minute easy swim today."

"I swam hard for 45 minutes this morning."


other:
The message is neither a workout-planning request nor an
explicit report of a completed swim.


IMPORTANT:

Do NOT classify:

"I want to swim for 40 minutes."

as record_completed_swim.

That is a future/planned workout.


=========================================================
COMPLETED SWIM
=========================================================

When intent is:

record_completed_swim

extract:

completed_swim_duration
completed_swim_intensity

Only populate these fields when the user clearly says the
swim already happened.


=========================================================
TIME
=========================================================

Convert time expressions into minutes.

Examples:

"half an hour ago"
→ 30

"an hour ago"
→ 60

"an hour and a half ago"
→ 90


=========================================================
ALLOWED VALUES
=========================================================

Intensity:

easy
moderate
hard


Swimming level:

beginner
intermediate
advanced


Goal:

aerobic
endurance
recovery
speed


Stroke:

freestyle
breaststroke
backstroke
mixed


Pool length:

25
50


=========================================================
MISSING INFORMATION
=========================================================

If information was not provided, return null.

Do not assume:
- swimming level
- pool length
- goal
- stroke
- completed workout information


USER MESSAGE:

{user_message}
"""

    return structured_model.invoke(
        prompt
    )