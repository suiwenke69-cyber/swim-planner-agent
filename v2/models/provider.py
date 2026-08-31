import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# DEFAULT MODEL
# =========================================================

DEFAULT_MODEL = "gpt-5-mini"


# =========================================================
# MODEL PROVIDER
# =========================================================

def get_model(
    model_name: str = DEFAULT_MODEL,
):
    """
    Return the default LangChain OpenAI model.
    """

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "OPENAI_API_KEY was not found. "
            "Add it to the project's .env file."
        )

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
    )