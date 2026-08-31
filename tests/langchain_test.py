import time

from langchain_openai import ChatOpenAI


# =========================================================
# CREATE MODEL
# =========================================================

model = ChatOpenAI(
    model="gpt-5-mini"
)


# =========================================================
# TEST PROMPT
# =========================================================

prompt = """
You are a swimming planning assistant.

A beginner wants a 40-minute moderate aerobic
freestyle swim in a 25-meter pool.

Give a short swimming plan.
"""


# =========================================================
# CALL MODEL
# =========================================================

start = time.perf_counter()


response = model.invoke(
    prompt
)


elapsed = (
    time.perf_counter()
    - start
)


# =========================================================
# OUTPUT
# =========================================================

print()

print("🏊 LangChain + OpenAI Response")

print(
    "================================"
)

print()

print(
    response.content
)

print()

print(
    "================================"
)

print(
    f"⏱ Response time: "
    f"{elapsed:.3f} seconds"
)

print()