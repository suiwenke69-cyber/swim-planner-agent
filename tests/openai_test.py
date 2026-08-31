import time
from openai import OpenAI


client = OpenAI()


start = time.perf_counter()


response = client.responses.create(
    model="gpt-5-mini",
    input="""
You are a swimming planning assistant.

A beginner wants a 40-minute moderate aerobic
freestyle swim in a 25-meter pool.

Give a short swimming plan.
"""
)


elapsed = time.perf_counter() - start


print()
print("🏊 OpenAI Response")
print("==============================")
print()

print(response.output_text)

print()
print("==============================")

print(
    f"⏱ Response time: "
    f"{elapsed:.3f} seconds"
)

print()