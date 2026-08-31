import json

from agent_core import (
    run_agent,
    get_current_state,
    get_profile,
    get_history,
    get_session_memory,
    clear_session,
    forget_long_term_memory,
)


# =========================================================
# DISPLAY HELP
# =========================================================

def show_help():
    print()
    print("Available commands:")
    print("  state    → show current temporary state")
    print("  profile  → show long-term preferences")
    print("  history  → show swimming history")
    print("  memory   → show current session memory")
    print("  clear    → clear temporary state + session memory")
    print("  forget   → delete long-term memory")
    print("  help     → show commands")
    print("  quit     → exit")
    print()


# =========================================================
# DISPLAY PERFORMANCE
# =========================================================

def show_performance(latency):
    """
    Display latency information returned by agent_core.
    """

    print()
    print("⏱ Agent Performance")
    print("-------------------------------")

    print(
        f"Memory analysis:  "
        f"{latency.get('memory_analysis', 0):.3f} s"
    )

    print(
        f"State extraction: "
        f"{latency.get('state_extraction', 0):.3f} s"
    )

    print(
        f"Python tools:     "
        f"{latency.get('python_tools', 0):.3f} s"
    )

    print(
        f"Final response:   "
        f"{latency.get('final_response', 0):.3f} s"
    )

    print("-------------------------------")

    print(
        f"Total:            "
        f"{latency.get('total', 0):.3f} s"
    )

    print()


# =========================================================
# START PROGRAM
# =========================================================

print()
print("🏊 Swim Planner Agent V9")
print("================================")
print("Local AI + Tools + Memory")
print("Real-Time State + Training History")
print("Performance Tracking Enabled")
print()

show_help()


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    user_input = input("You: ")

    command = user_input.lower().strip()


    # =====================================================
    # EXIT
    # =====================================================

    if command in [
        "quit",
        "exit",
        "bye",
    ]:

        print()
        print(
            "Swim Planner: "
            "See you next time! 🏊"
        )
        print()

        break


    # =====================================================
    # HELP
    # =====================================================

    if command == "help":

        show_help()

        continue


    # =====================================================
    # CURRENT STATE
    # =====================================================

    if command == "state":

        print()
        print("💾 CURRENT STATE")
        print("-------------------------------")

        print(
            json.dumps(
                get_current_state(),
                indent=2,
                ensure_ascii=False,
            )
        )

        print()

        continue


    # =====================================================
    # USER PROFILE
    # =====================================================

    if command == "profile":

        print()
        print("👤 USER PROFILE")
        print("-------------------------------")

        print(
            json.dumps(
                get_profile(),
                indent=2,
                ensure_ascii=False,
            )
        )

        print()

        continue


    # =====================================================
    # SWIMMING HISTORY
    # =====================================================

    if command == "history":

        print()
        print("🏊 SWIMMING HISTORY")
        print("-------------------------------")

        print(
            json.dumps(
                get_history(),
                indent=2,
                ensure_ascii=False,
            )
        )

        print()

        continue


    # =====================================================
    # SESSION MEMORY
    # =====================================================

    if command == "memory":

        print()
        print("🧠 SESSION MEMORY")
        print("-------------------------------")

        print(
            json.dumps(
                get_session_memory(),
                indent=2,
                ensure_ascii=False,
            )
        )

        print()

        continue


    # =====================================================
    # CLEAR TEMPORARY SESSION
    # =====================================================

    if command == "clear":

        clear_session()

        print()
        print(
            "🧹 Temporary state and "
            "session memory cleared."
        )
        print(
            "Long-term preferences and "
            "swimming history were preserved."
        )
        print()

        continue


    # =====================================================
    # DELETE LONG-TERM MEMORY
    # =====================================================

    if command == "forget":

        forget_long_term_memory()

        print()
        print(
            "🧠 Long-term preferences and "
            "swimming history deleted."
        )
        print()

        continue


    # =====================================================
    # NORMAL AGENT REQUEST
    # =====================================================

    try:

        print()
        print("🤖 Swim Planner is thinking...")
        print()

        result = run_agent(
            user_input
        )

        # -------------------------------------------------
        # FINAL ANSWER
        # -------------------------------------------------

        print()
        print("🏊 Swim Planner")
        print("================================")
        print()

        print(
            result["answer"]
        )

        print()

        # -------------------------------------------------
        # PERFORMANCE
        # -------------------------------------------------

        latency = result.get(
            "latency"
        )

        if latency:

            show_performance(
                latency
            )

        else:

            print(
                "⚠️ No latency data returned "
                "by agent_core."
            )

            print()

        print(
            "================================"
        )

        print()


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except KeyboardInterrupt:

        print()
        print()
        print(
            "Request interrupted."
        )
        print()

        continue


    except Exception as error:

        print()
        print("❌ Something went wrong:")
        print()
        print(error)
        print()