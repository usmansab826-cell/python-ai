"""Lesson 2.2: A personal tutor that remembers recent conversation."""

import sys

from langchain.chat_models import init_chat_model

MODEL = "gemma3:1b"
MAX_MESSAGES = 8
SYSTEM = (
    "You are a friendly, patient personal tutor. Answer clearly and simply. "
    "Use the conversation history to remember details the learner has shared."
)

sys.stdout.reconfigure(encoding="utf-8")

llm = init_chat_model(
    MODEL,
    model_provider="ollama",
    temperature=0.2,
)

messages = [{"role": "system", "content": SYSTEM}]


def trim_history(history: list[dict[str, str]]) -> None:
    """Keep the system instructions and at most MAX_MESSAGES recent messages."""
    while len(history) > MAX_MESSAGES + 1:
        del history[1]


print("Personal Tutor: Ask me anything. Commands: /reset, /count, bye")

while True:
    text = input("You: ").strip()
    command = text.lower()

    if command == "bye":
        print("Tutor: Goodbye!")
        break
    elif command == "/reset":
        messages = [messages[0]]
        print("Tutor: Memory cleared.")
    elif command == "/count":
        print(f"Tutor: Memory has {len(messages)} messages, including system instructions.")
    elif text == "":
        print("Tutor: Please type a question.")
    else:
        messages.append({"role": "user", "content": text})

        # Why: A bounded history controls token use while retaining the tutoring rules.
        # Keep the system message and the newest conversation messages.
        trim_history(messages)

        response = llm.invoke(messages)
        answer = response.text
        messages.append({"role": "assistant", "content": answer})
        trim_history(messages)

        print(f"Tutor: {answer}")
        print(
            f"     (memory: {len(messages) - 1} messages, "
            f"{response.usage_metadata['input_tokens']} tokens sent)"
        )
