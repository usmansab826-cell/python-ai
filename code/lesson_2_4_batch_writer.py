"""Lesson 2.4: Generate descriptions for every priced bakery product."""

import re
import sys

from langchain.chat_models import init_chat_model

MODEL = "gemma3:1b"

products = {
    "chocolate cake": 1500,
    "cupcake": 250,
    "brownie": 300,
    "old stock": 0,
    "donut": 200,
}

sys.stdout.reconfigure(encoding="utf-8")

writer = init_chat_model(
    MODEL,
    model_provider="ollama",
    temperature=0.7,
)

results = []
total_tokens = 0
total_seconds = 0.0

for name, price in products.items():
    if price <= 0:
        print(f"Skipping {name} (no price)")
        continue

    prompt = (
        f"Write exactly one tempting sentence of no more than 15 words for "
        f"'{name}' at {price} PKR for a Lahore bakery menu. "
        "Do not add a question, heading, or extra sentence."
    )
    response = writer.invoke([{"role": "user", "content": prompt}])
    description = re.split(
        r"(?<=[.!?])\s+", response.text.strip().replace("\n", " "), maxsplit=1
    )[0]
    description = " ".join(description.split()[:15])

    results.append(
        {"item": name, "price": price, "description": description}
    )
    total_tokens += response.usage_metadata["total_tokens"]
    total_seconds += (
        response.response_metadata["total_duration"] / 1_000_000_000
    )

print("=" * 50)
for number, result in enumerate(results, start=1):
    print(f"{number}. {result['item'].title()} ({result['price']} PKR)")
    print(f"   {result['description']}")
print("=" * 50)
print(
    f"{len(results)} descriptions, {total_tokens} tokens, "
    f"{total_seconds:.1f} seconds"
)
