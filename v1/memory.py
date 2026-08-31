import json
import os
from datetime import datetime


# =========================================================
# MEMORY FILE
# =========================================================

MEMORY_FILE = "memory.json"


# =========================================================
# DEFAULT LONG-TERM MEMORY
# =========================================================

DEFAULT_MEMORY = {

    "user_profile": {

        "preferred_swim_duration": None,

        "preferred_swim_intensity": None
    },

    "swimming_history": []
}


# =========================================================
# LOAD MEMORY
# =========================================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):

        save_memory(DEFAULT_MEMORY)

        return DEFAULT_MEMORY.copy()


    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception:

        save_memory(DEFAULT_MEMORY)

        return DEFAULT_MEMORY.copy()


# =========================================================
# SAVE MEMORY
# =========================================================

def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=2,
            ensure_ascii=False
        )


# =========================================================
# UPDATE USER PREFERENCES
# =========================================================

def update_preferences(
    duration=None,
    intensity=None
):

    memory = load_memory()

    profile = memory["user_profile"]


    if duration is not None:

        profile[
            "preferred_swim_duration"
        ] = duration


    if intensity is not None:

        profile[
            "preferred_swim_intensity"
        ] = intensity


    save_memory(memory)

    return profile


# =========================================================
# GET USER PROFILE
# =========================================================

def get_user_profile():

    memory = load_memory()

    return memory["user_profile"]


# =========================================================
# ADD SWIM HISTORY
# =========================================================

def add_swim_history(
    duration,
    intensity
):

    memory = load_memory()

    record = {

        "date":
            datetime.now().strftime(
                "%Y-%m-%d"
            ),

        "duration_minutes":
            duration,

        "intensity":
            intensity
    }


    memory[
        "swimming_history"
    ].append(record)


    save_memory(memory)

    return record


# =========================================================
# GET SWIMMING HISTORY
# =========================================================

def get_swimming_history():

    memory = load_memory()

    return memory[
        "swimming_history"
    ]


# =========================================================
# CLEAR ALL LONG-TERM MEMORY
# =========================================================

def clear_long_term_memory():

    save_memory(
        DEFAULT_MEMORY
    )