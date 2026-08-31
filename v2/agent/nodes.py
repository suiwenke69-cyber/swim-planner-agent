import time

from datetime import datetime

from v2.agent.state import (
    AgentState,
)

from v2.agent.prompts import (
    FINAL_RESPONSE_PROMPT,
)

from v2.models.provider import (
    get_model,
)

from v2.models.training import (
    SwimmingHistoryRecord,
)

from v2.tools.user_input import (
    parse_user_input,
)

from v2.tools.nutrition import (
    analyze_meal,
)

from v2.tools.meal_timing import (
    calculate_meal_timing,
)

from v2.tools.training_load import (
    analyze_training_load,
    decide_workout_intensity,
)

from v2.tools.workout import (
    create_swimming_workout,
)

from v2.memory.store import (
    get_swimming_history,
    add_swimming_session,
)

from v2.tools.vision_nutrition import (
    analyze_meal_image,
)


# =========================================================
# LATENCY HELPER
# =========================================================

def update_latency(
    state: AgentState,
    node_name: str,
    elapsed: float,
) -> dict[str, float]:
    """
    Add or update one node's latency measurement.
    """

    current = dict(
        state.get(
            "latency",
            {},
        )
    )

    current[node_name] = round(
        elapsed,
        3,
    )

    return current


# =========================================================
# NODE 1 — PARSE USER INPUT
# =========================================================

def parse_user_input_node(
    state: AgentState,
) -> dict:
    """
    Convert natural-language input into structured state.

    Possible intents:

    - plan_workout
    - record_completed_swim
    - other
    """

    start = time.perf_counter()

    user_message = state.get(
        "user_message",
        "",
    )

    if not user_message:

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "latency": update_latency(
                state,
                "parse_input",
                elapsed,
            )
        }


    result = parse_user_input(
        user_message
    )


    updates = {
        "parsed_input":
            result,

        "intent":
            result.intent,
    }


    field_mapping = {

        "meal_description":
            result.meal_description,

        "minutes_since_meal":
            result.minutes_since_meal,

        "swim_duration":
            result.swim_duration,

        "planned_intensity":
            result.planned_intensity,

        "swimming_level":
            result.swimming_level,

        "swimming_goal":
            result.swimming_goal,

        "preferred_stroke":
            result.preferred_stroke,

        "pool_length":
            result.pool_length,

        "completed_swim_duration":
            result.completed_swim_duration,

        "completed_swim_intensity":
            result.completed_swim_intensity,
    }


    for key, value in field_mapping.items():

        if value is not None:

            updates[key] = value


    elapsed = (
        time.perf_counter()
        - start
    )


    updates["latency"] = (
        update_latency(
            state,
            "parse_input",
            elapsed,
        )
    )


    return updates


# =========================================================
# NODE 2 — ANALYZE MEAL
# =========================================================

def analyze_meal_node(
    state: AgentState,
) -> dict:
    """
    Analyze meal contents using structured OpenAI output.
    """

    start = time.perf_counter()

    meal_description = state.get(
        "meal_description"
    )


    if not meal_description:

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "latency":
                update_latency(
                    state,
                    "nutrition_analysis",
                    elapsed,
                )
        }


    result = analyze_meal(
        meal_description
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "meal_analysis":
            result,

        "latency":
            update_latency(
                state,
                "nutrition_analysis",
                elapsed,
            ),
    }

# =========================================================
# NODE — ANALYZE MEAL IMAGE
# =========================================================

def analyze_meal_image_node(
    state: AgentState,
) -> dict:
    """
    Analyze a meal photograph using OpenAI vision.

    Reads:
        meal_image_path

    Writes:
        meal_analysis

    The output schema is identical to the text-based
    nutrition-analysis node.
    """

    start = time.perf_counter()

    image_path = state.get(
        "meal_image_path"
    )

    if not image_path:

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "latency": update_latency(
                state,
                "vision_nutrition",
                elapsed,
            )
        }

    result = analyze_meal_image(
        image_path
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    return {
        "meal_analysis":
            result,

        "latency":
            update_latency(
                state,
                "vision_nutrition",
                elapsed,
            ),
    }
    
# =========================================================
# NODE 3 — MEAL TIMING
# =========================================================

def calculate_meal_timing_node(
    state: AgentState,
) -> dict:
    """
    Calculate nutrition-aware pre-swim timing.
    """

    start = time.perf_counter()

    meal_analysis = state.get(
        "meal_analysis"
    )


    if meal_analysis is None:

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "latency":
                update_latency(
                    state,
                    "meal_timing",
                    elapsed,
                )
        }


    result = calculate_meal_timing(

        meal_analysis=(
            meal_analysis
        ),

        minutes_since_meal=(
            state.get(
                "minutes_since_meal",
                0,
            )
        ),

        planned_intensity=(
            state.get(
                "planned_intensity",
                "moderate",
            )
        ),
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "meal_timing":
            result,

        "latency":
            update_latency(
                state,
                "meal_timing",
                elapsed,
            ),
    }


# =========================================================
# NODE 4 — SAVE COMPLETED SWIM
# =========================================================

def save_completed_swim_node(
    state: AgentState,
) -> dict:
    """
    Save an explicitly completed swimming session into
    long-term SQLite memory.

    Duplicate protection is handled by the memory store.

    Writes:

    history_saved
    history_duplicate
    """

    start = time.perf_counter()


    user_id = state.get(
        "user_id",
        "default-user",
    )


    duration = state.get(
        "completed_swim_duration"
    )


    intensity = state.get(
        "completed_swim_intensity"
    )


    # =====================================================
    # MISSING REQUIRED INFORMATION
    # =====================================================

    if (
        duration is None
        or intensity is None
    ):

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "history_saved":
                False,

            "history_duplicate":
                False,

            "latency":
                update_latency(
                    state,
                    "save_history",
                    elapsed,
                ),
        }


    # =====================================================
    # CREATE SESSION RECORD
    # =====================================================

    today = (
        datetime.now()
        .date()
        .isoformat()
    )


    session = SwimmingHistoryRecord(

        date=today,

        duration_minutes=(
            duration
        ),

        intensity=(
            intensity
        ),
    )


    # =====================================================
    # WRITE TO LONG-TERM MEMORY
    # =====================================================

    saved = add_swimming_session(
        user_id,
        session,
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "history_saved":
            saved,

        "history_duplicate":
            not saved,

        "latency":
            update_latency(
                state,
                "save_history",
                elapsed,
            ),
    }


# =========================================================
# NODE 5 — LOAD LONG-TERM HISTORY
# =========================================================

def load_history_node(
    state: AgentState,
) -> dict:
    """
    Load persistent swimming history belonging to
    the current user.
    """

    start = time.perf_counter()


    user_id = state.get(
        "user_id",
        "default-user",
    )


    history = get_swimming_history(
        user_id
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "swimming_history":
            history,

        "latency":
            update_latency(
                state,
                "load_history",
                elapsed,
            ),
    }


# =========================================================
# NODE 6 — TRAINING LOAD
# =========================================================

def training_load_node(
    state: AgentState,
) -> dict:
    """
    Analyze recent persistent swimming history.
    """

    start = time.perf_counter()


    history = state.get(
        "swimming_history",
        [],
    )


    result = analyze_training_load(
        history
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "training_load":
            result,

        "latency":
            update_latency(
                state,
                "training_load",
                elapsed,
            ),
    }


# =========================================================
# NODE 7 — INTENSITY DECISION
# =========================================================

def intensity_decision_node(
    state: AgentState,
) -> dict:
    """
    Compare requested intensity with the recommendation
    derived from training history.
    """

    start = time.perf_counter()


    requested_intensity = state.get(
        "planned_intensity",
        "moderate",
    )


    training_load = state.get(
        "training_load"
    )


    if training_load is None:

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "latency":
                update_latency(
                    state,
                    "intensity_decision",
                    elapsed,
                )
        }


    result = decide_workout_intensity(

        requested_intensity=(
            requested_intensity
        ),

        training_load=(
            training_load
        ),
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "intensity_decision":
            result,

        "latency":
            update_latency(
                state,
                "intensity_decision",
                elapsed,
            ),
    }


# =========================================================
# NODE 8 — CREATE WORKOUT
# =========================================================

def create_workout_node(
    state: AgentState,
) -> dict:
    """
    Generate the actual swimming workout.

    planned_intensity preserves user intent.

    The actual workout uses:
        intensity_decision.final_intensity
    """

    start = time.perf_counter()


    duration = state.get(
        "swim_duration"
    )


    if duration is None:

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "latency":
                update_latency(
                    state,
                    "workout",
                    elapsed,
                )
        }


    intensity_decision = state.get(
        "intensity_decision"
    )


    if intensity_decision is not None:

        final_intensity = (
            intensity_decision
            .final_intensity
        )

    else:

        final_intensity = state.get(
            "planned_intensity",
            "moderate",
        )


    workout = create_swimming_workout(

        duration_minutes=(
            duration
        ),

        intensity=(
            final_intensity
        ),

        level=(
            state.get(
                "swimming_level",
                "beginner",
            )
        ),

        goal=(
            state.get(
                "swimming_goal",
                "aerobic",
            )
        ),

        stroke=(
            state.get(
                "preferred_stroke",
                "freestyle",
            )
        ),

        pool_length=(
            state.get(
                "pool_length",
                25,
            )
        ),
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "workout":
            workout,

        "latency":
            update_latency(
                state,
                "workout",
                elapsed,
            ),
    }


# =========================================================
# NODE 9 — FINAL RESPONSE
# =========================================================

def final_response_node(
    state: AgentState,
) -> dict:
    """
    Produce the final user-facing response.

    Completed-swim recording is handled deterministically.

    Workout-planning responses use OpenAI to explain
    structured tool results.
    """

    start = time.perf_counter()


    # =====================================================
    # COMPLETED SWIM RESPONSE
    # =====================================================

    if (
        state.get("intent")
        == "record_completed_swim"
    ):

        duration = state.get(
            "completed_swim_duration"
        )

        intensity = state.get(
            "completed_swim_intensity"
        )

        saved = state.get(
            "history_saved",
            False,
        )

        duplicate = state.get(
            "history_duplicate",
            False,
        )


        if saved:

            answer = (
                f"Recorded your completed "
                f"{duration}-minute "
                f"{intensity} swim in your "
                f"training history."
            )


        elif duplicate:

            answer = (
                f"That {duration}-minute "
                f"{intensity} swim already appears "
                f"to be in today's training history, "
                f"so I did not add a duplicate."
            )


        else:

            answer = (
                "I understood that you completed a swim, "
                "but I could not save it because the "
                "required workout information was missing."
            )


        elapsed = (
            time.perf_counter()
            - start
        )


        return {
            "final_answer":
                answer,

            "latency":
                update_latency(
                    state,
                    "final_response",
                    elapsed,
                ),
        }


    # =====================================================
    # NORMAL PLANNING RESPONSE
    # =====================================================

    model = get_model()


    meal_analysis = state.get(
        "meal_analysis"
    )

    meal_timing = state.get(
        "meal_timing"
    )

    training_load = state.get(
        "training_load"
    )

    intensity_decision = state.get(
        "intensity_decision"
    )

    workout = state.get(
        "workout"
    )


    # =====================================================
    # SERIALIZE STRUCTURED RESULTS
    # =====================================================

    meal_analysis_text = (
        meal_analysis.model_dump_json(
            indent=2
        )
        if meal_analysis is not None
        else "Not available"
    )


    meal_timing_text = (
        meal_timing.model_dump_json(
            indent=2
        )
        if meal_timing is not None
        else "Not available"
    )


    training_load_text = (
        training_load.model_dump_json(
            indent=2
        )
        if training_load is not None
        else "Not available"
    )


    intensity_decision_text = (
        intensity_decision.model_dump_json(
            indent=2
        )
        if intensity_decision is not None
        else "Not available"
    )


    workout_text = (
        workout.model_dump_json(
            indent=2
        )
        if workout is not None
        else "Not available"
    )


    # =====================================================
    # FINAL PROMPT
    # =====================================================

    prompt = f"""
{FINAL_RESPONSE_PROMPT}

=========================================================
ORIGINAL USER MESSAGE
=========================================================

{state.get("user_message", "")}


=========================================================
MEAL ANALYSIS
=========================================================

{meal_analysis_text}


=========================================================
MEAL TIMING
=========================================================

{meal_timing_text}


=========================================================
TRAINING LOAD
=========================================================

{training_load_text}


=========================================================
INTENSITY DECISION
=========================================================

{intensity_decision_text}


=========================================================
WORKOUT
=========================================================

{workout_text}
"""


    response = model.invoke(
        prompt
    )


    elapsed = (
        time.perf_counter()
        - start
    )


    return {
        "final_answer":
            response.content,

        "latency":
            update_latency(
                state,
                "final_response",
                elapsed,
            ),
    }