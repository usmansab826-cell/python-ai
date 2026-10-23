"""Lesson 2.5: Reusable AI skills for Sweet Crumbs bakery."""

import sys

from langchain.chat_models import init_chat_model

BUSINESS = "Sweet Crumbs"
MODEL = "gemma3:1b"

sys.stdout.reconfigure(encoding="utf-8")

precise = init_chat_model(
    MODEL,
    model_provider="ollama",
    temperature=0.2,
)
creative = init_chat_model(
    MODEL,
    model_provider="ollama",
    temperature=0.8,
)


def estimate_tokens(text: str) -> int:
    """Estimate English token count using about four characters per token."""
    return round(len(text) / 4)


def ask_ai(
    prompt: str,
    system: str = "You are a helpful assistant. Answer in 2 short lines.",
    creative_mode: bool = False,
) -> str:
    """Send a prompt to the selected AI model and return its answer."""
    model = creative if creative_mode else precise
    response = model.invoke(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
    )
    return response.text.strip()


def summarize(text: str, max_words: int = 30) -> str:
    """Summarize text in no more than max_words words."""
    return ask_ai(f"Summarize in at most {max_words} words:\n{text}")


def translate(text: str, language: str = "Urdu") -> str:
    """Translate text into the requested language."""
    return ask_ai(
        f"Translate faithfully into {language}. "
        "For Urdu, use Urdu script, not Devanagari. Return only the translation:\n"
        f"{text}",
        system=(
            f"You are a careful translator. Write the translation in {language}. "
            "If translating into Urdu, use Urdu script."
        ),
    )


def reply_to_review(review: str, business: str) -> str:
    """Write a short, polite reply to a customer review."""
    return ask_ai(
        f"Write a 2-line polite reply from {business} to this review:\n{review}",
        creative_mode=True,
    )


assert estimate_tokens("Hello AI") == 2
assert estimate_tokens("") == 0
assert estimate_tokens("Python") == 2

usage = {"summarize": 0, "translate": 0, "reply": 0}

print(f"{BUSINESS} AI Toolkit. Commands: /summarize, /translate, /reply, bye")

while True:
    command = input("Command: ").strip().lower()

    if command == "bye":
        break
    elif command == "/summarize":
        text = input("Text to summarize: ").strip()
        print(f"AI: {summarize(text)}")
        usage["summarize"] += 1
    elif command == "/translate":
        text = input("Text to translate: ").strip()
        language = input("Language (Enter for Urdu): ").strip()
        if language:
            answer = translate(text, language)
        else:
            answer = translate(text)
        print(f"AI: {answer}")
        usage["translate"] += 1
    elif command == "/reply":
        review = input("Customer review: ").strip()
        print(f"AI: {reply_to_review(review, BUSINESS)}")
        print(f"    (review was about {estimate_tokens(review)} tokens)")
        usage["reply"] += 1
    else:
        print("Unknown command. Try /summarize, /translate, /reply or bye.")

print("Skills used today:")
for skill, count in usage.items():
    print(f"  {skill}: {count}")
