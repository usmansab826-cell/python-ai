"""Lesson 2.6: Bakery bot that saves chat history and handles common errors."""

import json
from pathlib import Path
import sys

import httpx
import ollama
from langchain.chat_models import init_chat_model

FAQ_FILE = Path(__file__).with_name("faq.json")
HISTORY_FILE = Path(__file__).with_name("chat_history.json")
LOG_FILE = Path(__file__).with_name("errors.log")
MODEL = "gemma3:1b"
MAX_MESSAGES = 6

sys.stdout.reconfigure(encoding="utf-8")

try:
    with FAQ_FILE.open(encoding="utf-8") as faq_file:
        facts = json.load(faq_file)
except FileNotFoundError:
    raise SystemExit(f"Missing {FAQ_FILE.name}. Create the bakery facts JSON file first.")
except json.JSONDecodeError as error:
    raise SystemExit(
        f"{FAQ_FILE.name} contains invalid JSON on line {error.lineno}: {error.msg}"
    ) from error

if not isinstance(facts, dict) or not all(
    key in facts for key in ("name", "city", "hours", "prices")
):
    raise SystemExit(
        f"{FAQ_FILE.name} must contain name, city, hours, and prices fields."
    )
if not isinstance(facts["prices"], dict):
    raise SystemExit(f"The prices field in {FAQ_FILE.name} must be a JSON object.")

system = {
    "role": "system",
    "content": (
        f"You are the assistant of {facts['name']} in {facts['city']}. "
        f"Facts: {json.dumps(facts, ensure_ascii=False)}. "
        "Only use these facts. If you do not know, say you will check with the manager. "
        "Answer in 2 short lines."
    ),
}

messages = [system]
try:
    with HISTORY_FILE.open(encoding="utf-8") as history_file:
        saved_messages = json.load(history_file)
    if not isinstance(saved_messages, list) or any(
        not isinstance(message, dict)
        or message.get("role") not in ("user", "assistant")
        or not isinstance(message.get("content"), str)
        for message in saved_messages
    ):
        print("History file has an invalid format. Starting a fresh chat.")
    else:
        # Why: Only user and assistant messages are saved; system rules stay in code.
        messages.extend(saved_messages[-MAX_MESSAGES:])
        print(f"Loaded {len(messages) - 1} old messages.")
except FileNotFoundError:
    pass
except json.JSONDecodeError as error:
    print(
        f"History file was damaged on line {error.lineno}. "
        "Starting a fresh chat."
    )

llm = init_chat_model(MODEL, model_provider="ollama")

print(f"{facts['name']} Bot: Ask me anything. Commands: /reset, bye")

while True:
    text = input("You: ").strip()
    command = text.lower()

    if command == "bye":
        print("Bot: Goodbye! Your chat is saved.")
        break
    elif command == "":
        continue
    elif command == "/reset":
        messages = [system]
        with HISTORY_FILE.open("w", encoding="utf-8") as history_file:
            # Why: UTF-8 preserves Urdu and other non-ASCII customer messages.
            json.dump([], history_file, indent=2, ensure_ascii=False)
        print("Bot: Memory cleared.")
        continue

    messages.append({"role": "user", "content": text})

    try:
        response = llm.invoke([system] + messages[1:][-MAX_MESSAGES:])
    except httpx.ConnectError:
        print("Bot: I am offline right now. Please open the Ollama app and try again.")
        messages.pop()
        # Why: A log helps diagnose an unavailable local Ollama service later.
        with LOG_FILE.open("a", encoding="utf-8") as log_file:
            log_file.write("ConnectError: Ollama not running\n")
        continue
    except ollama.ResponseError as error:
        print("Bot: Sorry, something went wrong on my side.")
        messages.pop()
        with LOG_FILE.open("a", encoding="utf-8") as log_file:
            log_file.write(f"ResponseError: {error.error}\n")
        continue

    messages.append({"role": "assistant", "content": response.text})
    print(f"Bot: {response.text}")

    while len(messages) > MAX_MESSAGES + 1:
        del messages[1:3]

    with HISTORY_FILE.open("w", encoding="utf-8") as history_file:
        # Why: UTF-8 keeps multilingual conversation history readable on disk.
        json.dump(messages[1:], history_file, indent=2, ensure_ascii=False)
