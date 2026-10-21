"""Lesson 2.1: Ask a local AI model to explain a topic."""

import sys

from langchain.chat_models import init_chat_model

MODEL = "gemma3:1b"

sys.stdout.reconfigure(encoding="utf-8")

topic = input("What topic would you like to learn about? ").strip()
level = input("What is your level (beginner, intermediate, or advanced)? ").strip()

tutor = init_chat_model(
    MODEL,
    model_provider="ollama",
    temperature=0.2,
)

response = tutor.invoke(
    [
        {
            "role": "system",
            "content": (
                "You are a friendly, patient AI tutor. Explain "
                f"{topic} to a learner at the {level} level. "
                "Use clear language, answer in 3-5 sentences, and include a simple example."
            ),
        },
        {"role": "user", "content": f"Teach me about {topic}."},
    ]
)

print(f"\nAI Tutor's answer about {topic}:")
print(response.text)

usage = response.usage_metadata
print(f"\nInput tokens: {usage['input_tokens']}")
print(f"Output tokens: {usage['output_tokens']}")
print(f"Total tokens: {usage['total_tokens']}")

seconds = response.response_metadata["total_duration"] / 1_000_000_000
print(f"Time: {seconds:.1f} seconds")
