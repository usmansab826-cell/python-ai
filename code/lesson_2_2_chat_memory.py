"""Lesson 2.2: A personal tutor that remembers recent conversation."""

import sys

from langchain.chat_models import init_chat_model

MODEL = "gemma3:1b"
MAX_MESSAGES = 6
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
        conversation = messages[1:]
        turns = sum(message["role"] == "user" for message in conversation)
        print(
            f"Tutor: Memory has {turns} turns "
            f"({len(conversation)} messages, system message not included)."
        )
    elif text == "":
        print("Tutor: Please type a question.")
    else:
        messages.append({"role": "user", "content": text})

        # Remove complete old user/assistant pairs, keeping the system message.
        while len(messages) > MAX_MESSAGES + 1:
            del messages[1:3]

        response = llm.invoke(messages)
        answer = response.text
        messages.append({"role": "assistant", "content": answer})

        print(f"Tutor: {answer}")
        print(
            f"     (memory: {len(messages) - 1} messages, "
            f"{response.usage_metadata['input_tokens']} tokens sent)"
        )
