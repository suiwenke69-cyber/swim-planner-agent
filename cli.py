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


print()
print("🏊 Swim Planner")
print("-------------------------------")
print("Terminal Interface")
print()
print("Commands:")
print("  state")
print("  profile")
print("  history")
print("  memory")
print("  clear")
print("  forget")
print("  quit")
print()


while True:

    user_input = input("You: ")

    command = user_input.lower().strip()


    if command in [
        "quit",
        "exit",
        "bye",
    ]:

        print(
            "\nSee you next time! 🏊\n"
        )

        break


    if command == "state":

        print(
            json.dumps(
                get_current_state(),
                indent=2,
            )
        )

        continue


    if command == "profile":

        print(
            json.dumps(
                get_profile(),
                indent=2,
            )
        )

        continue


    if command == "history":

        print(
            json.dumps(
                get_history(),
                indent=2,
            )
        )

        continue


    if command == "memory":

        print(
            json.dumps(
                get_session_memory(),
                indent=2,
            )
        )

        continue


    if command == "clear":

        clear_session()

        print(
            "\nTemporary state cleared.\n"
        )

        continue


    if command == "forget":

        forget_long_term_memory()

        print(
            "\nLong-term memory deleted.\n"
        )

        continue


    try:

        result = run_agent(
            user_input
        )

        print(
            "\n🏊 Swim Planner:\n"
        )

        print(
            result["answer"]
        )

        print(
            "\n-------------------------------\n"
        )


    except Exception as error:

        print(
            f"\n❌ Error: {error}\n"
        )