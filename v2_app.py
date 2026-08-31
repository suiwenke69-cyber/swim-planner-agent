import os
import tempfile
import time
import uuid

import streamlit as st

from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from v2.agent.graph import (
    build_graph,
)

from v2.memory.store import (
    get_swimming_history,
    delete_swimming_session,
    clear_swimming_history,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Swim Planner",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

# ---------------------------------------------------------
# USER ID
#
# Represents one anonymous beta user.
#
# Long-term swimming history in Supabase is associated
# with this ID.
# ---------------------------------------------------------

if "user_id" not in st.session_state:

    st.session_state.user_id = (
        f"anonymous-{uuid.uuid4()}"
    )


# ---------------------------------------------------------
# THREAD ID
#
# Represents one LangGraph conversation.
#
# New conversation:
#     new thread_id
#
# Same user:
#     same user_id
# ---------------------------------------------------------

if "thread_id" not in st.session_state:

    st.session_state.thread_id = (
        str(uuid.uuid4())
    )


# ---------------------------------------------------------
# SESSION-LEVEL LANGGRAPH CHECKPOINTER
#
# One browser session keeps one InMemorySaver.
#
# Multiple thread IDs can live inside the same saver.
# ---------------------------------------------------------

if "checkpointer" not in st.session_state:

    st.session_state.checkpointer = (
        InMemorySaver()
    )


# ---------------------------------------------------------
# CHAT MESSAGES
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------------------------------------------
# LAST GRAPH RESULT
# ---------------------------------------------------------

if "last_result" not in st.session_state:

    st.session_state.last_result = None


# ---------------------------------------------------------
# FILE UPLOADER RESET KEY
# ---------------------------------------------------------

if "uploader_key" not in st.session_state:

    st.session_state.uploader_key = 0


# =========================================================
# HELPERS
# =========================================================

def start_new_conversation():
    """
    Start a fresh LangGraph conversation.

    Clears:
        chat UI
        current dashboard
        meal upload

    Preserves:
        anonymous user ID
        Supabase training history
        session-level checkpointer
    """

    st.session_state.thread_id = (
        str(uuid.uuid4())
    )

    st.session_state.messages = []

    st.session_state.last_result = None

    st.session_state.uploader_key += 1


def clear_meal_photo():
    """
    Reset the Streamlit meal-photo uploader.
    """

    st.session_state.uploader_key += 1


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 750;
        letter-spacing: -0.04em;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    .section-label {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .workout-card {
        padding: 1.4rem;
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 16px;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }

    .beta-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        border: 1px solid rgba(128,128,128,0.25);
        font-size: 0.78rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header(
        "🏊 Swim Planner"
    )


    # =====================================================
    # NEW CONVERSATION
    # =====================================================

    if st.button(
        "＋ New conversation",
        use_container_width=True,
    ):

        start_new_conversation()

        st.rerun()


    st.caption(
        "Starts a fresh conversation while preserving "
        "your training history."
    )


    st.divider()


    # =====================================================
    # MEAL PHOTO
    # =====================================================

    st.header(
        "📷 Meal photo"
    )


    uploaded_image = st.file_uploader(
        "Upload a meal",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
        ],
        key=(
            f"meal_uploader_"
            f"{st.session_state.uploader_key}"
        ),
        label_visibility="collapsed",
    )


    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Uploaded meal",
            use_container_width=True,
        )


        if st.button(
            "Remove meal photo",
            use_container_width=True,
        ):

            clear_meal_photo()

            st.rerun()


        st.caption(
            "AI will estimate visible foods, portions "
            "and nutrition."
        )


    else:

        st.info(
            "Optional — upload a meal photo for visual "
            "nutrition analysis."
        )


    st.divider()


    # =====================================================
    # TRAINING MEMORY
    # =====================================================

    st.header(
        "🧠 Training memory"
    )


    sidebar_history = (
        get_swimming_history(
            st.session_state.user_id
        )
    )


    st.metric(
        "Recorded swims",
        len(sidebar_history),
    )


    if sidebar_history:

        with st.expander(
            "Manage history"
        ):

            for session in reversed(
                sidebar_history
            ):

                left, right = (
                    st.columns(
                        [4, 1]
                    )
                )


                with left:

                    st.write(
                        f"**{session.date}**  \n"
                        f"{session.duration_minutes} min · "
                        f"{session.intensity.title()}"
                    )


                with right:

                    if st.button(
                        "✕",
                        key=(
                            "delete_session_"
                            f"{session.session_id}"
                        ),
                        help="Delete this swim",
                    ):

                        delete_swimming_session(
                            st.session_state.user_id,
                            session.session_id,
                        )

                        st.session_state.last_result = None

                        st.rerun()


            st.divider()


            if st.button(
                "Clear all training history",
                type="secondary",
                use_container_width=True,
            ):

                clear_swimming_history(
                    st.session_state.user_id
                )

                st.session_state.last_result = None

                st.rerun()


    st.caption(
        "Training history is stored separately from "
        "conversation state."
    )


    # =====================================================
    # SESSION DETAILS
    # =====================================================

    with st.expander(
        "Session details"
    ):

        st.write(
            "**Anonymous user**"
        )

        st.code(
            st.session_state.user_id[:18]
            + "..."
        )


        st.write(
            "**Conversation**"
        )

        st.code(
            st.session_state.thread_id[:12]
            + "..."
        )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="beta-badge">
        PUBLIC BETA · V2
    </div>

    <div class="hero-title">
        🏊 Swim Planner
    </div>

    <div class="hero-subtitle">
        AI-assisted swimming plans using your meal,
        recent training history, and workout goals.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MAIN CONTENT
# =========================================================

chat_column, info_column = (
    st.columns(
        [1.7, 1],
        gap="large",
    )
)


# =========================================================
# CHAT COLUMN
# =========================================================

with chat_column:

    st.subheader(
        "💬 Plan your swim"
    )


    if not st.session_state.messages:

        st.markdown(
            """
            **Try one of these:**

            *“I'm a beginner and want a 40-minute moderate
            aerobic freestyle swim in a 25-meter pool.”*

            *“I ate chicken rice 45 minutes ago and want
            a 40-minute moderate swim.”*

            *Upload a meal photo and say:
            “I ate this 45 minutes ago.”*

            *“I just finished a 40-minute hard swim.”*
            """
        )


    for message in (
        st.session_state.messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


# =========================================================
# INFORMATION COLUMN
# =========================================================

with info_column:

    st.subheader(
        "How it works"
    )


    st.markdown(
        """
        **① Describe your goal**

        Tell the agent how long and how hard you want
        to swim.

        **② Add meal context**

        Describe your meal or upload a photo.

        **③ Use recent history**

        Completed swims can influence future plans.

        **④ Get a structured plan**

        The agent combines AI interpretation with
        deterministic planning tools.
        """
    )


    with st.expander(
        "Privacy & beta notes"
    ):

        st.markdown(
            """
            **Anonymous beta**

            This version does not use accounts or login.

            Training records are associated with an
            anonymous application identity.

            **Meal images**

            Uploaded meal images are used for the current
            nutrition analysis.

            **AI estimates**

            Food recognition, portion sizes and nutrition
            values may be inaccurate.

            **Exercise guidance**

            Swim Planner is an experimental planning tool,
            not a medical service.
            """
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "What did you eat, or how do you want to swim?"
)


# =========================================================
# EXECUTE AGENT
# =========================================================

if user_message:

    # =====================================================
    # STORE USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role":
                "user",

            "content":
                user_message,
        }
    )


    # =====================================================
    # INITIAL GRAPH STATE
    # =====================================================

    initial_state = {

        "user_id":
            st.session_state.user_id,

        "user_message":
            user_message,
    }


    # =====================================================
    # OPTIONAL MEAL IMAGE
    # =====================================================

    temporary_image_path = None


    if uploaded_image is not None:

        extension = (
            uploaded_image.name
            .split(".")[-1]
            .lower()
        )


        suffix = (
            f".{extension}"
        )


        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_image.getvalue()
            )


            temporary_image_path = (
                temp_file.name
            )


        initial_state[
            "meal_image_path"
        ] = temporary_image_path


    # =====================================================
    # LANGGRAPH THREAD CONFIG
    # =====================================================

    config = {

        "configurable": {

            "thread_id":
                st.session_state.thread_id
        }
    }


    # =====================================================
    # RUN AGENT
    # =====================================================

    try:

        with st.spinner(
            "Analyzing your plan..."
        ):

            start = (
                time.perf_counter()
            )


            # -------------------------------------------------
            # IMPORTANT:
            #
            # Reuse the SAME InMemorySaver throughout this
            # Streamlit browser session.
            # -------------------------------------------------

            graph = build_graph(
                checkpointer=(
                    st.session_state
                    .checkpointer
                )
            )


            result = graph.invoke(
                initial_state,
                config=config,
            )


            total_time = (
                time.perf_counter()
                - start
            )


        answer = result.get(
            "final_answer",
            "I couldn't generate a response.",
        )


        result[
            "total_execution_time"
        ] = total_time


        st.session_state.last_result = (
            result
        )


    except Exception as error:

        answer = (
            "I couldn't process that request. "
            "Please try again or start a new conversation."
        )


        st.session_state.last_result = {

            "error":
                str(error)
        }


    finally:

        # =================================================
        # CLEAN TEMP IMAGE
        # =================================================

        if (
            temporary_image_path
            and os.path.exists(
                temporary_image_path
            )
        ):

            try:

                os.remove(
                    temporary_image_path
                )

            except OSError:

                pass


    # =====================================================
    # STORE ASSISTANT RESPONSE
    # =====================================================

    st.session_state.messages.append(
        {
            "role":
                "assistant",

            "content":
                answer,
        }
    )


    st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

result = (
    st.session_state.last_result
)


if result:

    # =====================================================
    # ERROR STATE
    # =====================================================

    if result.get(
        "error"
    ):

        st.error(
            "The request could not be completed."
        )


        with st.expander(
            "Technical details"
        ):

            st.code(
                result[
                    "error"
                ]
            )


    else:

        st.divider()


        # =================================================
        # NUTRITION
        # =================================================

        meal = result.get(
            "meal_analysis"
        )


        if meal:

            st.markdown(
                (
                    '<div class="section-label">'
                    '🍽 Nutrition estimate'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )


            c1, c2, c3, c4, c5 = (
                st.columns(5)
            )


            c1.metric(
                "Calories",
                (
                    f"{meal.calories_kcal.low:.0f}"
                    f"–"
                    f"{meal.calories_kcal.high:.0f}"
                    " kcal"
                ),
            )


            c2.metric(
                "Protein",
                (
                    f"{meal.protein_g.low:.0f}"
                    f"–"
                    f"{meal.protein_g.high:.0f}"
                    " g"
                ),
            )


            c3.metric(
                "Carbs",
                (
                    f"{meal.carbohydrates_g.low:.0f}"
                    f"–"
                    f"{meal.carbohydrates_g.high:.0f}"
                    " g"
                ),
            )


            c4.metric(
                "Fat",
                (
                    f"{meal.fat_g.low:.0f}"
                    f"–"
                    f"{meal.fat_g.high:.0f}"
                    " g"
                ),
            )


            c5.metric(
                "Fiber",
                (
                    f"{meal.fiber_g.low:.0f}"
                    f"–"
                    f"{meal.fiber_g.high:.0f}"
                    " g"
                ),
            )


            with st.expander(
                "Food recognition details"
            ):

                for item in (
                    meal.food_items
                ):

                    st.write(
                        f"**{item.name}** — "
                        f"{item.estimated_portion} "
                        f"({item.confidence} confidence)"
                    )


                st.write(
                    "**Overall confidence:**",
                    meal.confidence,
                )


                st.write(
                    "**Uncertainty:**",
                    meal.uncertainty_reason,
                )


            st.caption(
                "Nutrition values are AI estimates."
            )


        # =================================================
        # MEAL TIMING
        # =================================================

        timing = result.get(
            "meal_timing"
        )


        if timing:

            st.markdown(
                (
                    '<div class="section-label">'
                    '⏱ Pre-swim timing'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )


            c1, c2, c3 = (
                st.columns(3)
            )


            c1.metric(
                "Recommended wait",
                (
                    f"{timing.recommended_wait_minutes}"
                    " min"
                ),
            )


            c2.metric(
                "Already waited",
                (
                    f"{timing.minutes_since_meal}"
                    " min"
                ),
            )


            c3.metric(
                "Remaining",
                (
                    f"{timing.remaining_wait_minutes}"
                    " min"
                ),
            )


            if timing.status == "ready":

                st.success(
                    "Planner status: Ready"
                )

            else:

                st.warning(
                    "Planner status: Wait"
                )


            st.caption(
                "Current timing recommendations use "
                "prototype planning heuristics."
            )


        # =================================================
        # WORKOUT
        # =================================================

        workout = result.get(
            "workout"
        )


        if workout:

            st.markdown(
                (
                    '<div class="section-label">'
                    '🏊 Today’s workout'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )


            c1, c2, c3, c4 = (
                st.columns(4)
            )


            c1.metric(
                "Duration",
                (
                    f"{workout.duration_minutes}"
                    " min"
                ),
            )


            c2.metric(
                "Intensity",
                workout.intensity.title(),
            )


            c3.metric(
                "Goal",
                workout.goal.title(),
            )


            c4.metric(
                "Distance",
                (
                    f"{workout.estimated_total_distance_m}"
                    " m"
                ),
            )


            st.markdown(
                f"""
                <div class="workout-card">

                <b>
                Warm-up · {workout.warmup.distance_m} m
                </b><br>
                {workout.warmup.instruction}

                <br><br>

                <b>
                Main Set · {workout.main_set.distance_m} m
                </b><br>
                {workout.main_set.instruction}

                <br><br>

                <b>
                Cool-down · {workout.cooldown.distance_m} m
                </b><br>
                {workout.cooldown.instruction}

                </div>
                """,
                unsafe_allow_html=True,
            )


        # =================================================
        # TRAINING
        # =================================================

        training = result.get(
            "training_load"
        )


        decision = result.get(
            "intensity_decision"
        )


        if training:

            st.markdown(
                (
                    '<div class="section-label">'
                    '📈 Recent training'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )


            c1, c2, c3 = (
                st.columns(3)
            )


            c1.metric(
                "Sessions · 7 days",
                training.sessions_last_7_days,
            )


            c2.metric(
                "Minutes · 7 days",
                training.total_minutes_last_7_days,
            )


            c3.metric(
                "Training load",
                (
                    training
                    .training_load_level
                    .replace(
                        "_",
                        " ",
                    )
                    .title()
                ),
            )


            if decision:

                recommended = (
                    decision
                    .recommended_intensity
                )


                recommendation_text = (
                    recommended.title()
                    if recommended
                    else "No adjustment"
                )


                st.write(
                    "**Intensity decision:** "
                    f"Requested "
                    f"`{decision.requested_intensity}` "
                    f"→ Recommended "
                    f"`{recommendation_text}` "
                    f"→ Final "
                    f"`{decision.final_intensity}`"
                )


        # =================================================
        # SWIMMING HISTORY
        # =================================================

        history = (
            get_swimming_history(
                st.session_state.user_id
            )
        )


        if history:

            with st.expander(
                "🗂 Swimming history"
            ):

                for session in reversed(
                    history[-10:]
                ):

                    st.write(
                        f"**{session.date}** · "
                        f"{session.duration_minutes} min · "
                        f"{session.intensity.title()}"
                    )


        # =================================================
        # DEVELOPER DETAILS
        # =================================================

        with st.expander(
            "⚡ Developer details"
        ):

            st.write(
                "**Architecture:** "
                "OpenAI + LangChain + LangGraph"
            )


            st.write(
                "**Long-term memory:** "
                "Supabase PostgreSQL"
            )


            st.write(
                "**Conversation memory:** "
                "LangGraph InMemorySaver"
            )


            latency = result.get(
                "latency",
                {},
            )


            for name, value in (
                latency.items()
            ):

                st.write(
                    f"**{name}:** "
                    f"{value:.3f} s"
                )


            st.write(
                "**Total execution:** "
                f"{result.get('total_execution_time', 0):.3f} s"
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "Swim Planner V2 Public Beta · Experimental AI "
    "planning tool. Nutrition, meal timing and training "
    "recommendations are estimates and are not medical "
    "advice."
)