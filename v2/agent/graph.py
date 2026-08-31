from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from v2.agent.state import (
    AgentState,
)

from v2.agent.nodes import (
    parse_user_input_node,
    analyze_meal_node,
    analyze_meal_image_node,
    calculate_meal_timing_node,
    save_completed_swim_node,
    load_history_node,
    training_load_node,
    intensity_decision_node,
    create_workout_node,
    final_response_node,
)


# =========================================================
# ROUTER — AFTER INPUT PARSING
# =========================================================

def route_after_input(
    state: AgentState,
) -> str:
    """
    Route according to user intent and available
    meal input.

    Priority:

    1. Completed swim
    2. Meal image
    3. Text meal
    4. Normal workout planning
    """

    intent = state.get(
        "intent",
        "other",
    )


    # =====================================================
    # COMPLETED SWIM
    # =====================================================

    if intent == "record_completed_swim":

        return "save_history"


    # =====================================================
    # IMAGE MEAL
    # =====================================================

    meal_image_path = state.get(
        "meal_image_path"
    )

    if meal_image_path:

        return "vision_nutrition"


    # =====================================================
    # TEXT MEAL
    # =====================================================

    meal_description = state.get(
        "meal_description"
    )

    if meal_description:

        return "text_nutrition"


    # =====================================================
    # NO MEAL
    # =====================================================

    return "load_history"


# =========================================================
# BUILD GRAPH
# =========================================================

def build_graph(
    checkpointer=None,
):
    """
    Build and compile Swim Planner V2.
    """

    builder = StateGraph(
        AgentState
    )


    # =====================================================
    # REGISTER NODES
    # =====================================================

    builder.add_node(
        "parse_input",
        parse_user_input_node,
    )

    builder.add_node(
        "text_nutrition",
        analyze_meal_node,
    )

    builder.add_node(
        "vision_nutrition",
        analyze_meal_image_node,
    )

    builder.add_node(
        "meal_timing",
        calculate_meal_timing_node,
    )

    builder.add_node(
        "save_history",
        save_completed_swim_node,
    )

    builder.add_node(
        "load_history",
        load_history_node,
    )

    builder.add_node(
        "training_load",
        training_load_node,
    )

    builder.add_node(
        "intensity_decision",
        intensity_decision_node,
    )

    builder.add_node(
        "workout",
        create_workout_node,
    )

    builder.add_node(
        "final_response",
        final_response_node,
    )


    # =====================================================
    # START
    # =====================================================

    builder.add_edge(
        START,
        "parse_input",
    )


    # =====================================================
    # PRIMARY ROUTING
    # =====================================================

    builder.add_conditional_edges(

        "parse_input",

        route_after_input,

        {
            "save_history":
                "save_history",

            "vision_nutrition":
                "vision_nutrition",

            "text_nutrition":
                "text_nutrition",

            "load_history":
                "load_history",
        },
    )


    # =====================================================
    # COMPLETED SWIM
    # =====================================================

    builder.add_edge(
        "save_history",
        "final_response",
    )


    # =====================================================
    # TEXT NUTRITION
    # =====================================================

    builder.add_edge(
        "text_nutrition",
        "meal_timing",
    )


    # =====================================================
    # VISION NUTRITION
    # =====================================================

    builder.add_edge(
        "vision_nutrition",
        "meal_timing",
    )


    # =====================================================
    # COMMON PLANNING PIPELINE
    # =====================================================

    builder.add_edge(
        "meal_timing",
        "load_history",
    )

    builder.add_edge(
        "load_history",
        "training_load",
    )

    builder.add_edge(
        "training_load",
        "intensity_decision",
    )

    builder.add_edge(
        "intensity_decision",
        "workout",
    )

    builder.add_edge(
        "workout",
        "final_response",
    )


    # =====================================================
    # END
    # =====================================================

    builder.add_edge(
        "final_response",
        END,
    )


    return builder.compile(
        checkpointer=checkpointer
    )