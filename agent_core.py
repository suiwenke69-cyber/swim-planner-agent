import json
import ollama

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
# INTERPRET USER MESSAGE
# =========================================================

def interpret_user_message(user_message):

    current_state = get_state()

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

    action = memory_change.get("memory_action")

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

    action = change.get("action")

    if action == "set":

        updates = change.get(
            "updates",
            {},
        )

        update_state(updates)

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

    state = get_state()
    profile = get_user_profile()

    results = {}

    # -----------------------------------------------------
    # NUTRITION
    # -----------------------------------------------------

    if state["foods"]:

        results["nutrition"] = (
            nutrition_analysis_tool(
                state["foods"]
            )
        )

    # -----------------------------------------------------
    # MEAL TIMING
    # -----------------------------------------------------

    if (
        state["meal_size"] is not None
        and state["minutes_since_meal"] is not None
    ):

        intensity = (
            state["swim_intensity"]
            or profile.get(
                "preferred_swim_intensity"
            )
            or "moderate"
        )

        results["meal_timing"] = (
            meal_timing_tool(
                state["meal_size"],
                state["minutes_since_meal"],
                intensity,
            )
        )

    # -----------------------------------------------------
    # WORKOUT
    # -----------------------------------------------------

    duration = (
        state["swim_duration"]
        or profile.get(
            "preferred_swim_duration"
        )
    )

    intensity = (
        state["swim_intensity"]
        or profile.get(
            "preferred_swim_intensity"
        )
        or "moderate"
    )

    if duration is not None:

        results["workout"] = (
            swim_workout_tool(
                duration,
                intensity,
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

    state = get_state()
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

    return response["message"]["content"]


# =========================================================
# PUBLIC AGENT FUNCTION
# =========================================================

def run_agent(user_message):

    # 1. Long-term memory decision

    memory_change = (
        analyze_long_term_memory(
            user_message
        )
    )

    apply_long_term_memory(
        memory_change
    )

    # 2. Interpret temporary state

    state_change = (
        interpret_user_message(
            user_message
        )
    )

    apply_state_change(
        state_change
    )

    # 3. Run deterministic tools

    tool_results = run_tools()

    # 4. Generate final response

    final_answer = (
        create_final_response(
            user_message,
            tool_results,
        )
    )

    # 5. Save session history

    conversation_memory.append(
        {
            "user": user_message,
            "state": get_state().copy(),
            "answer": final_answer,
        }
    )

    # Return everything useful to any UI

    return {
        "answer": final_answer,
        "state": get_state().copy(),
        "tool_results": tool_results,
        "memory_decision": memory_change,
        "state_change": state_change,
    }


# =========================================================
# HELPER FUNCTIONS FOR UI
# =========================================================

def get_current_state():

    return get_state()


def get_profile():

    return get_user_profile()


def get_history():

    return get_swimming_history()


def get_session_memory():

    return conversation_memory


def clear_session():

    reset_state()
    conversation_memory.clear()


def forget_long_term_memory():

    clear_long_term_memory()