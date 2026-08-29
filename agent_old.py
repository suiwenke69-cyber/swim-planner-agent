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
# CONVERSATION MEMORY
# =========================================================

conversation_memory = []


# =========================================================
# STEP 1 — INTERPRET USER MESSAGE
# =========================================================

def interpret_user_message(user_message):
    """
    Use the LLM to convert natural language into
    a structured state change.
    """

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
# STEP 2 — LONG-TERM MEMORY ANALYSIS
# =========================================================

def analyze_long_term_memory(user_message):
    """
    Decide whether the user's message contains information
    worth storing permanently.
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
# STEP 3 — APPLY LONG-TERM MEMORY CHANGE
# =========================================================

def apply_long_term_memory(memory_change):
    """
    Save stable preferences or completed swimming sessions.
    """

    action = memory_change.get("memory_action")

    # -----------------------------------------------------
    # SAVE USER PREFERENCE
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

        print("\n🧠 LONG-TERM MEMORY UPDATED")

        print(
            json.dumps(
                get_user_profile(),
                indent=2,
            )
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

            record = add_swim_history(
                duration,
                intensity,
            )

            print("\n🏊 SWIM HISTORY SAVED")

            print(
                json.dumps(
                    record,
                    indent=2,
                )
            )


# =========================================================
# STEP 4 — UPDATE TEMPORARY STRUCTURED STATE
# =========================================================

def apply_state_change(change):
    """
    Apply the state change identified by the LLM.
    """

    action = change.get("action")

    # -----------------------------------------------------
    # SET ABSOLUTE VALUES
    # -----------------------------------------------------

    if action == "set":

        updates = change.get(
            "updates",
            {},
        )

        update_state(updates)

    # -----------------------------------------------------
    # ADD ELAPSED TIME
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
# STEP 5 — RUN TOOLS
# =========================================================

def run_tools():
    """
    Run relevant deterministic tools using the current state
    and long-term user profile.
    """

    state = get_state()
    profile = get_user_profile()

    results = {}

    # -----------------------------------------------------
    # NUTRITION TOOL
    # -----------------------------------------------------

    if state["foods"]:

        results["nutrition"] = (
            nutrition_analysis_tool(
                state["foods"]
            )
        )

    # -----------------------------------------------------
    # MEAL TIMING TOOL
    # -----------------------------------------------------

    if (
        state["meal_size"] is not None
        and state["minutes_since_meal"] is not None
    ):

        intensity = (
            state["swim_intensity"]
            or profile[
                "preferred_swim_intensity"
            ]
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
    # WORKOUT TOOL
    # -----------------------------------------------------

    duration = (
        state["swim_duration"]
        or profile[
            "preferred_swim_duration"
        ]
    )

    intensity = (
        state["swim_intensity"]
        or profile[
            "preferred_swim_intensity"
        ]
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
# STEP 6 — CREATE FINAL RESPONSE
# =========================================================

def create_final_response(
    user_message,
    tool_results,
):
    """
    Give the LLM the current state, persistent profile,
    recent history, and deterministic tool results.
    """

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
# MAIN AGENT
# =========================================================

def run_agent(user_message):
    """
    Complete Swim Planner v6 workflow.
    """

    # -----------------------------------------------------
    # A. LONG-TERM MEMORY DECISION
    # -----------------------------------------------------

    memory_change = (
        analyze_long_term_memory(
            user_message
        )
    )

    print("\n🧠 MEMORY DECISION")

    print(
        json.dumps(
            memory_change,
            indent=2,
        )
    )

    apply_long_term_memory(
        memory_change
    )

    # -----------------------------------------------------
    # B. INTERPRET TEMPORARY STATE CHANGE
    # -----------------------------------------------------

    state_change = (
        interpret_user_message(
            user_message
        )
    )

    print("\n🧠 INTERPRETED STATE CHANGE")

    print(
        json.dumps(
            state_change,
            indent=2,
        )
    )

    # -----------------------------------------------------
    # C. UPDATE STRUCTURED STATE
    # -----------------------------------------------------

    apply_state_change(
        state_change
    )

    print("\n💾 CURRENT STATE")

    print(
        json.dumps(
            get_state(),
            indent=2,
        )
    )

    # -----------------------------------------------------
    # D. RUN TOOLS
    # -----------------------------------------------------

    tool_results = run_tools()

    print("\n🔧 TOOL RESULTS")

    print(
        json.dumps(
            tool_results,
            indent=2,
        )
    )

    # -----------------------------------------------------
    # E. GENERATE FINAL RESPONSE
    # -----------------------------------------------------

    final_answer = (
        create_final_response(
            user_message,
            tool_results,
        )
    )

    # -----------------------------------------------------
    # F. SAVE LIGHTWEIGHT SESSION MEMORY
    # -----------------------------------------------------

    conversation_memory.append(
        {
            "user": user_message,
            "state": get_state().copy(),
            "answer": final_answer,
        }
    )

    return final_answer


# =========================================================
# DISPLAY COMMANDS
# =========================================================

def show_state():

    print("\n💾 CURRENT TEMPORARY STATE")

    print(
        json.dumps(
            get_state(),
            indent=2,
        )
    )

    print()


def show_conversation_memory():

    print("\n🧠 CONVERSATION MEMORY")

    print(
        json.dumps(
            conversation_memory,
            indent=2,
        )
    )

    print()


def show_profile():

    print("\n👤 LONG-TERM USER PROFILE")

    print(
        json.dumps(
            get_user_profile(),
            indent=2,
        )
    )

    print()


def show_history():

    print("\n🏊 SWIMMING HISTORY")

    print(
        json.dumps(
            get_swimming_history(),
            indent=2,
        )
    )

    print()


# =========================================================
# START PROGRAM
# =========================================================

print()
print("🏊 Swim Planner Agent v6")
print("--------------------------------")
print("Structured State + Persistent Memory")
print()
print("Commands:")
print("  state    → show temporary state")
print("  profile  → show long-term preferences")
print("  history  → show swimming history")
print("  memory   → show current session history")
print("  clear    → clear temporary state + session memory")
print("  forget   → delete long-term memory")
print("  quit     → exit")
print()


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    user_input = input("You: ")

    command = user_input.lower().strip()

    # -----------------------------------------------------
    # EXIT
    # -----------------------------------------------------

    if command in [
        "quit",
        "exit",
        "bye",
    ]:

        print(
            "\nSwim Planner: "
            "See you next time! 🏊\n"
        )

        break

    # -----------------------------------------------------
    # SHOW TEMPORARY STATE
    # -----------------------------------------------------

    if command == "state":

        show_state()

        continue

    # -----------------------------------------------------
    # SHOW LONG-TERM PROFILE
    # -----------------------------------------------------

    if command == "profile":

        show_profile()

        continue

    # -----------------------------------------------------
    # SHOW SWIMMING HISTORY
    # -----------------------------------------------------

    if command == "history":

        show_history()

        continue

    # -----------------------------------------------------
    # SHOW SESSION MEMORY
    # -----------------------------------------------------

    if command == "memory":

        show_conversation_memory()

        continue

    # -----------------------------------------------------
    # CLEAR TEMPORARY STATE
    # -----------------------------------------------------

    if command == "clear":

        reset_state()
        conversation_memory.clear()

        print(
            "\n🧹 Temporary state "
            "and session memory cleared.\n"
        )

        continue

    # -----------------------------------------------------
    # DELETE LONG-TERM MEMORY
    # -----------------------------------------------------

    if command == "forget":

        clear_long_term_memory()

        print(
            "\n🧠 Long-term memory deleted.\n"
        )

        continue

    # -----------------------------------------------------
    # NORMAL AGENT REQUEST
    # -----------------------------------------------------

    try:

        answer = run_agent(
            user_input
        )

        print(
            "\n🏊 Swim Planner:\n"
        )

        print(answer)

        print(
            "\n--------------------------------\n"
        )

    except Exception as error:

        print(
            "\n❌ Something went wrong:"
        )

        print(error)

        print()