"""Module 1 project: a grounded AI front desk for Sweet Crumbs bakery."""

import sys

import httpx
import ollama
from langchain.chat_models import init_chat_model

MODEL = "gemma3:1b"
MAX_HISTORY = 8
BUSINESS = {
    "name": "Sweet Crumbs",
    "city": "Lahore",
    "address": "Main Boulevard, Lahore",
    "hours": "9 am to 10 pm every day",
    "prices": {"chocolate cake": 1500, "cupcake": 250, "brownie": 300},
    "delivery": "Free delivery on orders over 3,000 PKR",
    "contact": "WhatsApp ordering is available",
}


def answer_from_facts(question: str) -> str | None:
    """Answer common front-desk questions directly from verified business facts."""
    text = question.casefold()
    if any(word in text for word in ("hour", "open", "close", "time")):
        return f"We are open {BUSINESS['hours']}."
    if any(word in text for word in ("where", "address", "location")):
        return f"We are at {BUSINESS['address']}."
    if "delivery" in text or "deliver" in text:
        return f"Our delivery policy: {BUSINESS['delivery']}."
    if "whatsapp" in text or "contact" in text or "order" in text:
        return f"{BUSINESS['contact']}. Please contact us there to place an order."
    if "price" in text or "cost" in text or "how much" in text:
        item = next((name for name in BUSINESS["prices"] if name in text), None)
        if item:
            return f"{item.title()} costs {BUSINESS['prices'][item]} PKR."
        prices = ", ".join(
            f"{name}: {price} PKR" for name, price in BUSINESS["prices"].items()
        )
        return f"Our menu prices are {prices}."
    return None


def make_system_message() -> dict[str, str]:
    """Build rules that ground AI answers in the business facts."""
    facts = "; ".join(
        (
            f"Business: {BUSINESS['name']}",
            f"City: {BUSINESS['city']}",
            f"Address: {BUSINESS['address']}",
            f"Hours: {BUSINESS['hours']}",
            f"Menu prices in PKR: {BUSINESS['prices']}",
            f"Delivery: {BUSINESS['delivery']}",
            f"Contact: {BUSINESS['contact']}",
        )
    )
    return {
        "role": "system",
        "content": (
            "You are a helpful front-desk assistant. Answer using only these "
            f"verified facts: {facts}. Do not invent names, prices, promises, or "
            "policies. If a fact is missing, say a staff member can help. "
            "Keep replies concise."
        ),
    }


def run() -> None:
    """Run the interactive front desk."""
    sys.stdout.reconfigure(encoding="utf-8")
    model = init_chat_model(MODEL, model_provider="ollama", temperature=0.2)
    system = make_system_message()
    history: list[dict[str, str]] = []

    print(f"{BUSINESS['name']} Front Desk — type 'bye' to finish.")
    print("Ask about opening hours, address, menu prices, delivery, or ordering.")
    while True:
        question = input("You: ").strip()
        if question.casefold() in {"bye", "exit"}:
            print("Front Desk: Thank you for contacting us. Goodbye!")
            return
        if not question:
            print("Front Desk: Please enter a question.")
            continue
        if any(word in question.casefold() for word in ("complaint", "refund", "human", "manager")):
            print("Front Desk: I will pass this to a staff member for help.")
            continue

        direct_answer = answer_from_facts(question)
        if direct_answer is not None:
            print(f"Front Desk: {direct_answer}")
            continue

        history.append({"role": "user", "content": question})
        try:
            response = model.invoke([system, *history])
        except httpx.ConnectError:
            history.pop()
            print("Front Desk: AI is offline. Start Ollama or ask about a listed business fact.")
            continue
        except ollama.ResponseError as error:
            history.pop()
            print(f"Front Desk: The model could not answer: {error.error}")
            continue

        answer = response.text.strip()
        history.append({"role": "assistant", "content": answer})
        history = history[-MAX_HISTORY:]
        print(f"Front Desk: {answer}")


if __name__ == "__main__":
    run()
