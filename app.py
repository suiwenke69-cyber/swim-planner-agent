import streamlit as st

from agent_core import (
    run_agent,
    get_current_state,
    get_profile,
    get_history,
    clear_session,
    forget_long_term_memory,
)

from tools import training_load_tool


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Swim Planner V9",
    page_icon="🏊",
    layout="wide",
)


# =========================================================
# STREAMLIT SESSION STATE
# =========================================================

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


if "last_latency" not in st.session_state:
    st.session_state.last_latency = None


if "last_tool_results" not in st.session_state:
    st.session_state.last_tool_results = None


# =========================================================
# LOAD AGENT DATA
# =========================================================

current_state = get_current_state()

profile = get_profile()

history = get_history()

training_load = training_load_tool(
    history
)


# =========================================================
# HEADER
# =========================================================

st.title("🏊 Swim Planner V9")

st.caption(
    "Local AI swimming planner powered by "
    "Qwen + Ollama + Python tools + persistent memory."
)


# =========================================================
# TOP DASHBOARD
# =========================================================

st.subheader("Today's Status")


col1, col2, col3, col4 = st.columns(4)


# ---------------------------------------------------------
# MEAL TIMER
# ---------------------------------------------------------

minutes_since_meal = current_state.get(
    "minutes_since_meal"
)

with col1:

    if minutes_since_meal is not None:

        st.metric(
            "🍽️ Time Since Meal",
            f"{minutes_since_meal} min",
        )

    else:

        st.metric(
            "🍽️ Time Since Meal",
            "—",
        )


# ---------------------------------------------------------
# WEEKLY SESSIONS
# ---------------------------------------------------------

with col2:

    st.metric(
        "🏊 Sessions This Week",
        training_load.get(
            "sessions_last_7_days",
            0,
        ),
    )


# ---------------------------------------------------------
# WEEKLY MINUTES
# ---------------------------------------------------------

with col3:

    st.metric(
        "⏱️ Minutes This Week",
        training_load.get(
            "total_minutes_last_7_days",
            0,
        ),
    )


# ---------------------------------------------------------
# TRAINING LOAD
# ---------------------------------------------------------

with col4:

    load_level = training_load.get(
        "training_load_level",
        "low",
    )

    st.metric(
        "⚡ Training Load",
        load_level.replace(
            "_",
            " ",
        ).title(),
    )


st.divider()


# =========================================================
# MAIN LAYOUT
# =========================================================

main_column, side_column = st.columns(
    [2, 1]
)


# =========================================================
# CHAT
# =========================================================

with main_column:

    st.subheader(
        "💬 Ask Swim Planner"
    )


    # -----------------------------------------------------
    # DISPLAY CHAT HISTORY
    # -----------------------------------------------------

    for message in (
        st.session_state.chat_messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    user_message = st.chat_input(
        "Tell me what you ate or ask for a swimming plan..."
    )


    if user_message:

        # Save user message

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )


        with st.chat_message(
            "user"
        ):

            st.markdown(
                user_message
            )


        # -------------------------------------------------
        # RUN AGENT
        # -------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Swim Planner is thinking..."
            ):

                try:

                    result = run_agent(
                        user_message
                    )

                    answer = result[
                        "answer"
                    ]

                    st.markdown(
                        answer
                    )


                    # -------------------------------------
                    # SAVE PERFORMANCE DATA
                    # -------------------------------------

                    st.session_state.last_latency = (
                        result.get(
                            "latency"
                        )
                    )

                    st.session_state.last_tool_results = (
                        result.get(
                            "tool_results"
                        )
                    )


                    # -------------------------------------
                    # SAVE CHAT
                    # -------------------------------------

                    st.session_state.chat_messages.append(
                        {
                            "role":
                                "assistant",

                            "content":
                                answer,
                        }
                    )


                    # -------------------------------------
                    # DEVELOPER DETAILS
                    # -------------------------------------

                    with st.expander(
                        "🔧 Developer Details"
                    ):

                        st.write(
                            "State Change"
                        )

                        st.json(
                            result.get(
                                "state_change",
                                {},
                            )
                        )


                        st.write(
                            "Current State"
                        )

                        st.json(
                            result.get(
                                "state",
                                {},
                            )
                        )


                        st.write(
                            "Tool Results"
                        )

                        st.json(
                            result.get(
                                "tool_results",
                                {},
                            )
                        )


                        st.write(
                            "Memory Decision"
                        )

                        st.json(
                            result.get(
                                "memory_decision",
                                {},
                            )
                        )


                except Exception as error:

                    st.error(
                        f"Something went wrong: "
                        f"{error}"
                    )


# =========================================================
# RIGHT-SIDE PANEL
# =========================================================

with side_column:

    # -----------------------------------------------------
    # CURRENT PLAN
    # -----------------------------------------------------

    st.subheader(
        "🎯 Current Plan"
    )


    duration = current_state.get(
        "swim_duration"
    )

    intensity = current_state.get(
        "swim_intensity"
    )

    level = current_state.get(
        "swimming_level"
    )

    goal = current_state.get(
        "swimming_goal"
    )

    stroke = current_state.get(
        "preferred_stroke"
    )

    pool_length = current_state.get(
        "pool_length"
    )


    if duration is not None:

        st.write(
            f"**Duration:** "
            f"{duration} min"
        )

    else:

        st.write(
            "**Duration:** —"
        )


    if intensity:

        st.write(
            f"**Requested intensity:** "
            f"{intensity.title()}"
        )

    else:

        st.write(
            "**Requested intensity:** —"
        )


    if level:

        st.write(
            f"**Level:** "
            f"{level.title()}"
        )


    if goal:

        st.write(
            f"**Goal:** "
            f"{goal.title()}"
        )


    if stroke:

        st.write(
            f"**Stroke:** "
            f"{stroke.title()}"
        )


    if pool_length:

        st.write(
            f"**Pool:** "
            f"{pool_length} m"
        )


    st.divider()


    # -----------------------------------------------------
    # USER PROFILE
    # -----------------------------------------------------

    st.subheader(
        "🧠 Preferences"
    )


    preferred_duration = profile.get(
        "preferred_swim_duration"
    )

    preferred_intensity = profile.get(
        "preferred_swim_intensity"
    )


    st.write(
        "**Usual duration:** "
        + (
            f"{preferred_duration} min"
            if preferred_duration
            is not None
            else "Not saved"
        )
    )


    st.write(
        "**Usual intensity:** "
        + (
            preferred_intensity.title()
            if preferred_intensity
            else "Not saved"
        )
    )


    st.divider()


    # -----------------------------------------------------
    # TRAINING LOAD
    # -----------------------------------------------------

    st.subheader(
        "📊 Training Analysis"
    )


    st.write(
        "**Recommended intensity:** "
        f"{training_load.get('recommended_intensity', 'moderate').title()}"
    )


    st.write(
        "**Hard sessions:** "
        f"{training_load.get('hard_sessions', 0)}"
    )


    st.write(
        "**Load score:** "
        f"{training_load.get('training_load_score', 0)}"
    )


    st.caption(
        training_load.get(
            "reason",
            "",
        )
    )


# =========================================================
# PERFORMANCE DASHBOARD
# =========================================================

st.divider()

st.subheader(
    "⚡ Agent Performance"
)


latency = (
    st.session_state.last_latency
)


if latency:

    perf1, perf2, perf3, perf4, perf5 = (
        st.columns(5)
    )


    with perf1:

        st.metric(
            "Memory",
            f"{latency.get('memory_analysis', 0):.2f}s",
        )


    with perf2:

        st.metric(
            "State",
            f"{latency.get('state_extraction', 0):.2f}s",
        )


    with perf3:

        st.metric(
            "Python Tools",
            f"{latency.get('python_tools', 0):.3f}s",
        )


    with perf4:

        st.metric(
            "Response",
            f"{latency.get('final_response', 0):.2f}s",
        )


    with perf5:

        st.metric(
            "Total",
            f"{latency.get('total', 0):.2f}s",
        )


    st.caption(
        "Python tools contribute negligible latency; "
        "local LLM inference is the primary bottleneck."
    )


else:

    st.info(
        "Ask Swim Planner a question to generate "
        "performance measurements."
    )


# =========================================================
# SWIMMING HISTORY
# =========================================================

st.divider()

st.subheader(
    "🏊 Recent Swimming History"
)


if history:

    recent_history = history[-7:]


    for record in reversed(
        recent_history
    ):

        history_col1, history_col2, history_col3 = (
            st.columns(
                [2, 1, 1]
            )
        )


        with history_col1:

            st.write(
                f"**{record.get('date', 'Unknown')}**"
            )


        with history_col2:

            st.write(
                f"{record.get('duration_minutes', 0)} min"
            )


        with history_col3:

            intensity_value = (
                record.get(
                    "intensity",
                    "moderate",
                )
            )

            st.write(
                intensity_value.title()
            )


else:

    st.caption(
        "No swimming sessions recorded yet."
    )


# =========================================================
# MEMORY CONTROLS
# =========================================================

st.divider()

st.subheader(
    "⚙️ Controls"
)


control1, control2 = (
    st.columns(2)
)


with control1:

    if st.button(
        "Clear Current Session",
        use_container_width=True,
    ):

        clear_session()

        st.session_state.chat_messages = []

        st.session_state.last_latency = None

        st.session_state.last_tool_results = None

        st.rerun()


with control2:

    if st.button(
        "Forget Long-Term Memory",
        use_container_width=True,
    ):

        forget_long_term_memory()

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Swim Planner V9 — Local prototype using "
    "Qwen3:4B, Ollama, Python tools, structured state, "
    "persistent memory, training-history analysis, "
    "and Streamlit."
)