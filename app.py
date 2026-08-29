import streamlit as st

from agent_core import (
    run_agent,
    get_current_state,
    get_profile,
    get_history,
    clear_session,
    forget_long_term_memory,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Swim Planner",
    page_icon="🏊",
    layout="wide",
)


# =========================================================
# SESSION STATE FOR WEB CHAT
# =========================================================

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# =========================================================
# HEADER
# =========================================================

st.title("🏊 Swim Planner Agent")

st.caption(
    "AI-powered swimming planning with meal timing, "
    "workout tools, structured state, and persistent memory."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🧠 Agent Memory")

    # -----------------------------------------------------
    # USER PROFILE
    # -----------------------------------------------------

    st.subheader("Your Preferences")

    profile = get_profile()

    preferred_duration = profile.get(
        "preferred_swim_duration"
    )

    preferred_intensity = profile.get(
        "preferred_swim_intensity"
    )

    if preferred_duration is not None:
        st.write(
            f"**Usual duration:** "
            f"{preferred_duration} min"
        )
    else:
        st.write(
            "**Usual duration:** Not saved"
        )

    if preferred_intensity is not None:
        st.write(
            f"**Usual intensity:** "
            f"{preferred_intensity.title()}"
        )
    else:
        st.write(
            "**Usual intensity:** Not saved"
        )

    st.divider()

    # -----------------------------------------------------
    # CURRENT STATE
    # -----------------------------------------------------

    st.subheader("Current State")

    current_state = get_current_state()

    st.json(current_state)

    st.divider()

    # -----------------------------------------------------
    # SWIMMING HISTORY
    # -----------------------------------------------------

    st.subheader("Recent Swims")

    history = get_history()

    if history:

        for record in reversed(
            history[-5:]
        ):

            st.write(
                f"🏊 **{record['date']}**"
            )

            st.caption(
                f"{record['duration_minutes']} min · "
                f"{record['intensity'].title()}"
            )

    else:

        st.caption(
            "No completed swims recorded yet."
        )

    st.divider()

    # -----------------------------------------------------
    # MEMORY CONTROLS
    # -----------------------------------------------------

    st.subheader("Memory Controls")

    if st.button(
        "Clear Current Session",
        use_container_width=True,
    ):

        clear_session()

        st.session_state.chat_messages = []

        st.success(
            "Current session cleared."
        )

        st.rerun()

    if st.button(
        "Forget Long-Term Memory",
        use_container_width=True,
    ):

        forget_long_term_memory()

        st.success(
            "Long-term memory deleted."
        )

        st.rerun()


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.chat_messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "Tell me what you ate or ask me to plan your swim..."
)


# =========================================================
# RUN AGENT
# =========================================================

if user_message:

    # -----------------------------------------------------
    # SHOW USER MESSAGE
    # -----------------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_message
        )

    # -----------------------------------------------------
    # CALL AGENT CORE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Planning your swim..."
        ):

            try:

                result = run_agent(
                    user_message
                )

                answer = result["answer"]

                st.markdown(
                    answer
                )

                # -----------------------------------------
                # OPTIONAL DEBUG INFORMATION
                # -----------------------------------------

                with st.expander(
                    "🔧 See Agent Reasoning Data"
                ):

                    st.subheader(
                        "State Change"
                    )

                    st.json(
                        result[
                            "state_change"
                        ]
                    )

                    st.subheader(
                        "Current State"
                    )

                    st.json(
                        result[
                            "state"
                        ]
                    )

                    st.subheader(
                        "Tool Results"
                    )

                    st.json(
                        result[
                            "tool_results"
                        ]
                    )

                    st.subheader(
                        "Memory Decision"
                    )

                    st.json(
                        result[
                            "memory_decision"
                        ]
                    )

                # -----------------------------------------
                # SAVE ANSWER TO WEB CHAT HISTORY
                # -----------------------------------------

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as error:

                st.error(
                    f"Something went wrong: {error}"
                )


# =========================================================
# EMPTY-CHAT WELCOME SCREEN
# =========================================================

if not st.session_state.chat_messages:

    st.divider()

    st.subheader(
        "Try asking:"
    )

    st.markdown(
        """
- **I ate chicken rice 30 minutes ago and want a moderate 40-minute swim.**
- **What if I wait another hour?**
- **Make today's swim easier.**
- **I usually prefer 40-minute moderate swims.**
- **I finished a 45-minute moderate swim today.**
        """
    )