import json
import ollama
import time
from datetime import datetime

from state import (
    get_state,
    update_state,
    add_time_since_meal,
    reset_state,
)

from tools import (
    meal_timing_tool,
    swim_workout_tool,
    nutrition_analysis_tool,
    training_load_tool,
)

from prompts import (
    STATE_EXTRACTION_PROMPT,
    FINAL_RESPONSE_PROMPT,
    MEMORY_EXTRACTION_PROMPT,
)

from memory import (
    get_user_profile,
    update_preferences,
    add_swim_history,
    get_swimming_history,
    clear_long_term_memory,
)


# =========================================================
# SESSION MEMORY
# =========================================================

conversation_memory = []


# =========================================================
# STATE SERIALIZATION
# =========================================================

def serialize_state(state=None):
    """
    Convert the internal state into a JSON-safe dictionary.

    datetime objects are converted to ISO-format strings.
    """

    if state is None:
        state = get_state()

    serialized = {}

    for key, value in state.items():

        if isinstance(value, datetime):
            serialized[key] = value.isoformat()

        elif isinstance(value, list):
            serialized[key] = value.copy()

        else:
            serialized[key] = value

    return serialized


# =========================================================
# INTERPRET USER MESSAGE
# =========================================================

def interpret_user_message(user_message):
    """
    Ask Qwen to convert natural language into
    a structured state change.
    """

    current_state = serialize_state()

    prompt = f"""
{STATE_EXTRACTION_PROMPT}

CURRENT STATE:

{json.dumps(current_state, indent=2)}

USER MESSAGE:

{user_message}
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format="json",
    )

    return json.loads(
        response["message"]["content"]
    )


# =========================================================
# LONG-TERM MEMORY ANALYSIS
# =========================================================

def analyze_long_term_memory(user_message):
    """
    Decide whether the user's message contains
    information worth storing permanently.
    """

    prompt = f"""
{MEMORY_EXTRACTION_PROMPT}

USER MESSAGE:

{user_message}
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format="json",
    )

    return json.loads(
        response["message"]["content"]
    )


# =========================================================
# APPLY LONG-TERM MEMORY
# =========================================================

def apply_long_term_memory(memory_change):
    """
    Save stable preferences or completed swimming sessions.
    """

    action = memory_change.get(
        "memory_action"
    )

    # -----------------------------------------------------
    # SAVE PREFERENCE
    # -----------------------------------------------------

    if action == "preference":

        duration = memory_change.get(
            "preferred_swim_duration"
        )

        intensity = memory_change.get(
            "preferred_swim_intensity"
        )

        update_preferences(
            duration=duration,
            intensity=intensity,
        )

    # -----------------------------------------------------
    # SAVE COMPLETED SWIM
    # -----------------------------------------------------

    elif action == "history":

        duration = memory_change.get(
            "duration_minutes"
        )

        intensity = memory_change.get(
            "intensity"
        )

        if (
            duration is not None
            and intensity is not None
        ):

            add_swim_history(
                duration,
                intensity,
            )


# =========================================================
# APPLY TEMPORARY STATE CHANGE
# =========================================================

def apply_state_change(change):
    """
    Apply state changes identified by Qwen.
    """

    action = change.get(
        "action"
    )

    # -----------------------------------------------------
    # SET STATE VALUES
    # -----------------------------------------------------

    if action == "set":

        updates = change.get(
            "updates",
            {},
        )

        update_state(
            updates
        )

    # -----------------------------------------------------
    # HYPOTHETICAL TIME CHANGE
    # -----------------------------------------------------

    elif action == "add_time":

        additional_minutes = change.get(
            "additional_minutes",
            0,
        )

        add_time_since_meal(
            additional_minutes
        )


# =========================================================
# RUN TOOLS
# =========================================================

def run_tools():
    """
    Run deterministic tools using:

    - current state
    - long-term preferences
    - swimming history

    V8 also analyzes recent training load before
    generating today's workout.
    """

    state = get_state()
    profile = get_user_profile()
    history = get_swimming_history()

    results = {}

    # =====================================================
    # TOOL 1 — TRAINING LOAD
    # =====================================================

    training_load = training_load_tool(
        history
    )

    results["training_load"] = (
        training_load
    )

    # =====================================================
    # TOOL 2 — NUTRITION
    # =====================================================

    if state["foods"]:

        results["nutrition"] = (
            nutrition_analysis_tool(
                state["foods"]
            )
        )

    # =====================================================
    # DETERMINE REQUESTED INTENSITY
    # =====================================================

    requested_intensity = (
        state["swim_intensity"]
        or profile.get(
            "preferred_swim_intensity"
        )
        or "moderate"
    )

    # =====================================================
    # TOOL 3 — MEAL TIMING
    # =====================================================

    if (
        state["meal_size"] is not None
        and
        state["minutes_since_meal"] is not None
    ):

        results["meal_timing"] = (
            meal_timing_tool(
                state["meal_size"],
                state["minutes_since_meal"],
                requested_intensity,
            )
        )

    # =====================================================
    # HISTORY-DRIVEN INTENSITY DECISION
    # =====================================================

    recommended_intensity = (
        training_load[
            "recommended_intensity"
        ]
    )

    intensity_rank = {
        "easy": 1,
        "moderate": 2,
        "hard": 3,
    }

    # If history recommends something easier than
    # the user requested, use the easier intensity.

    if (
        intensity_rank[
            recommended_intensity
        ]
        <
        intensity_rank[
            requested_intensity
        ]
    ):

        final_intensity = (
            recommended_intensity
        )

    else:

        final_intensity = (
            requested_intensity
        )

    results["intensity_decision"] = {
        "requested_intensity":
            requested_intensity,

        "recommended_intensity":
            recommended_intensity,

        "final_intensity":
            final_intensity,

        "adjusted":
            final_intensity
            != requested_intensity,
    }

    # =====================================================
    # WORKOUT SETTINGS
    # =====================================================

    duration = (
        state["swim_duration"]
        or profile.get(
            "preferred_swim_duration"
        )
    )

    level = (
        state["swimming_level"]
        or "beginner"
    )

    goal = (
        state["swimming_goal"]
        or "aerobic"
    )

    stroke = (
        state["preferred_stroke"]
        or "freestyle"
    )

    pool_length = (
        state["pool_length"]
        or 25
    )

    # =====================================================
    # TOOL 4 — PROFESSIONAL WORKOUT
    # =====================================================

    if duration is not None:

        results["workout"] = (
            swim_workout_tool(
                duration_minutes=duration,
                intensity=final_intensity,
                level=level,
                goal=goal,
                stroke=stroke,
                pool_length=pool_length,
            )
        )

    return results


# =========================================================
# FINAL RESPONSE
# =========================================================

def create_final_response(
    user_message,
    tool_results,
):
    """
    Ask Qwen to turn structured state and tool results
    into a concise final response.
    """

    state = serialize_state()
    profile = get_user_profile()
    history = get_swimming_history()

    prompt = f"""
{FINAL_RESPONSE_PROMPT}

USER MESSAGE:

{user_message}

CURRENT TEMPORARY STATE:

{json.dumps(state, indent=2)}

LONG-TERM USER PROFILE:

{json.dumps(profile, indent=2)}

RECENT SWIMMING HISTORY:

{json.dumps(history[-5:], indent=2)}

TOOL RESULTS:

{json.dumps(tool_results, indent=2)}

IMPORTANT:

The tool results may contain:

- training_load
- intensity_decision
- nutrition
- meal_timing
- workout

If intensity_decision shows:

"adjusted": true

then clearly explain:

1. what intensity the user requested
2. what intensity the planner selected
3. that the adjustment was based on recent swimming history

Do not present the simplified training-load model as
medical advice or a medical requirement.

When workout information is available, clearly present:

- total distance
- warm-up
- main set
- rest interval
- cool-down
- intensity
- goal
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response[
        "message"
    ][
        "content"
    ]


# =========================================================
# PUBLIC AGENT FUNCTION
# =========================================================

def run_agent(user_message):
    """
    Complete V9 Swim Planner workflow
    with latency tracking.
    """

    total_start = time.perf_counter()

    latency = {}

    # =====================================================
    # 1 — LONG-TERM MEMORY ANALYSIS
    # =====================================================

    start = time.perf_counter()

    memory_change = (
        analyze_long_term_memory(
            user_message
        )
    )

    apply_long_term_memory(
        memory_change
    )

    latency["memory_analysis"] = (
        time.perf_counter() - start
    )

    # =====================================================
    # 2 — STATE INTERPRETATION
    # =====================================================

    start = time.perf_counter()

    state_change = (
        interpret_user_message(
            user_message
        )
    )

    apply_state_change(
        state_change
    )

    latency["state_extraction"] = (
        time.perf_counter() - start
    )

    # =====================================================
    # 3 — PYTHON TOOLS
    # =====================================================

    start = time.perf_counter()

    tool_results = run_tools()

    latency["python_tools"] = (
        time.perf_counter() - start
    )

    # =====================================================
    # 4 — FINAL LLM RESPONSE
    # =====================================================

    start = time.perf_counter()

    final_answer = (
        create_final_response(
            user_message,
            tool_results,
        )
    )

    latency["final_response"] = (
        time.perf_counter() - start
    )

    # =====================================================
    # TOTAL LATENCY
    # =====================================================

    latency["total"] = (
        time.perf_counter()
        - total_start
    )

    # Round values for readability

    latency = {
        key: round(value, 3)
        for key, value
        in latency.items()
    }

    # =====================================================
    # SAVE SESSION MEMORY
    # =====================================================

    current_state = serialize_state()

    conversation_memory.append(
        {
            "user": user_message,
            "state": current_state,
            "tool_results": tool_results,
            "latency": latency,
            "answer": final_answer,
        }
    )

    # =====================================================
    # RETURN TO CLI / STREAMLIT
    # =====================================================

    return {
        "answer": final_answer,
        "state": current_state,
        "tool_results": tool_results,
        "memory_decision": memory_change,
        "state_change": state_change,
        "latency": latency,
    }

    # =====================================================
    # 1 — LONG-TERM MEMORY
    # =====================================================

    memory_change = (
        analyze_long_term_memory(
            user_message
        )
    )

    apply_long_term_memory(
        memory_change
    )

    # =====================================================
    # 2 — STATE INTERPRETATION
    # =====================================================

    state_change = (
        interpret_user_message(
            user_message
        )
    )

    apply_state_change(
        state_change
    )

    # =====================================================
    # 3 — RUN TOOLS
    # =====================================================

    tool_results = (
        run_tools()
    )

    # =====================================================
    # 4 — FINAL RESPONSE
    # =====================================================

    final_answer = (
        create_final_response(
            user_message,
            tool_results,
        )
    )

    # =====================================================
    # 5 — SAVE SESSION MEMORY
    # =====================================================

    current_state = (
        serialize_state()
    )

    conversation_memory.append(
        {
            "user":
                user_message,

            "state":
                current_state,

            "tool_results":
                tool_results,

            "answer":
                final_answer,
        }
    )

    # =====================================================
    # RETURN DATA TO CLI / STREAMLIT
    # =====================================================

    return {
        "answer":
            final_answer,

        "state":
            current_state,

        "tool_results":
            tool_results,

        "memory_decision":
            memory_change,

        "state_change":
            state_change,
    }


# =========================================================
# UI HELPER FUNCTIONS
# =========================================================

def get_current_state():
    """
    Return JSON-safe current state.
    """

    return serialize_state()


def get_profile():
    """
    Return long-term user profile.
    """

    return get_user_profile()


def get_history():
    """
    Return persistent swimming history.
    """

    return get_swimming_history()


def get_session_memory():
    """
    Return current in-session conversation history.
    """

    return conversation_memory


def clear_session():
    """
    Clear temporary state and session memory.

    Long-term memory is preserved.
    """

    reset_state()

    conversation_memory.clear()


def forget_long_term_memory():
    """
    Delete persistent user preferences and swimming history.
    """

    clear_long_term_memory()