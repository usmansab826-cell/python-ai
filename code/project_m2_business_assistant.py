"""Module 2 final project: a tool-using AI assistant for Sweet Crumbs."""

import json
from pathlib import Path
import sys

import httpx
import ollama
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from pydantic import ValidationError

MODEL = "qwen3.5:2b"
MAX_STEPS = 5
BUSINESS_FILE = Path(__file__).with_name("business.json")
ORDER_FILE = Path(__file__).with_name("business_orders.jsonl")

try:
    with BUSINESS_FILE.open(encoding="utf-8") as business_file:
        BUSINESS = json.load(business_file)
except FileNotFoundError as error:
    raise SystemExit(f"Missing business data file: {BUSINESS_FILE.name}") from error
except json.JSONDecodeError as error:
    raise SystemExit(
        f"{BUSINESS_FILE.name} has invalid JSON on line {error.lineno}: {error.msg}"
    ) from error

if (
    not isinstance(BUSINESS, dict)
    or not isinstance(BUSINESS.get("menu"), dict)
    or not isinstance(BUSINESS.get("name"), str)
):
    raise SystemExit(f"{BUSINESS_FILE.name} must have a name and menu object.")


@tool(parse_docstring=True)
def business_information(topic: str) -> str:
    """Look up verified business details.

    Args:
        topic: The requested detail, such as hours, address, delivery, or all.
    """
    key = topic.casefold().strip()
    available = {
        "hours": BUSINESS.get("hours", "Not provided"),
        "address": BUSINESS.get("address", "Not provided"),
        "city": BUSINESS.get("city", "Not provided"),
        "delivery": BUSINESS.get("delivery", "Not provided"),
    }
    if key in {"all", "business"}:
        return json.dumps(BUSINESS, ensure_ascii=False)
    if key in available:
        return f"{key.title()}: {available[key]}"
    return "That detail is not in the verified business data."


@tool(parse_docstring=True)
def get_price(item: str) -> str:
    """Check the price of a menu item.

    Args:
        item: The product name, for example cupcake.
    """
    name = item.casefold().strip()
    price = BUSINESS["menu"].get(name)
    if type(price) is not int or price < 0:
        return f"{item} is not on the verified menu."
    return f"{name.title()} costs {price} PKR."


def next_order_id() -> str:
    """Generate a unique order ID from the saved order log."""
    last_number = 100
    try:
        with ORDER_FILE.open(encoding="utf-8") as order_file:
            for line in order_file:
                if not line.strip():
                    continue
                record = json.loads(line)
                if isinstance(record, dict):
                    saved_id = record.get("id", "")
                    if isinstance(saved_id, str) and saved_id.startswith("SC"):
                        digits = saved_id[2:]
                        if digits.isdigit():
                            last_number = max(last_number, int(digits))
    except FileNotFoundError:
        pass
    return f"SC{last_number + 1}"


@tool(parse_docstring=True)
def place_order(item: str, quantity: int, customer: str) -> str:
    """Request an order; the customer must explicitly approve before saving.

    Args:
        item: A listed menu product.
        quantity: A positive whole-number quantity.
        customer: The customer's name.
    """
    name = item.casefold().strip()
    customer_name = customer.strip()
    price = BUSINESS["menu"].get(name)
    if type(price) is not int or price < 0:
        return f"{item} is not on the verified menu."
    if type(quantity) is not int or quantity < 1:
        return "Quantity must be a positive whole number."
    if not customer_name:
        return "Please provide a customer name before ordering."

    total = price * quantity
    confirmation = input(
        f"Approve {quantity} x {name} for {customer_name} ({total} PKR)? (yes/no): "
    ).strip().casefold()
    if confirmation != "yes":
        return "Order was not placed; customer approval was not received."

    order_id = next_order_id()
    record = {
        "id": order_id,
        "item": name,
        "quantity": quantity,
        "customer": customer_name,
        "total": total,
    }
    try:
        with ORDER_FILE.open("a", encoding="utf-8") as order_file:
            order_file.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as error:
        return f"Order could not be saved; ask the owner to check the order log. ({error})"
    return f"Order {order_id} placed: {quantity} x {name}, total {total} PKR."


TOOLS = {
    "business_information": business_information,
    "get_price": get_price,
    "place_order": place_order,
}


def run() -> None:
    """Run a bounded tool-calling chat with the business assistant."""
    sys.stdout.reconfigure(encoding="utf-8")
    model = init_chat_model(MODEL, model_provider="ollama")
    model_with_tools = model.bind_tools(list(TOOLS.values()))
    messages = [
        {
            "role": "system",
            "content": (
                f"You are the {BUSINESS['name']} business assistant. Use tools to "
                "look up information, prices, and place orders. Never invent facts "
                "or claim an order was placed unless its tool confirms it. Only "
                "place an order when the customer clearly requests it and provides "
                "a valid item, positive quantity, and customer name."
            ),
        }
    ]
    print(
        f"{BUSINESS['name']} Assistant — ask about the business, prices, or orders. "
        "Type 'bye' to exit."
    )

    while True:
        question = input("You: ").strip()
        if question.casefold() == "bye":
            print("Assistant: Goodbye!")
            return
        if not question:
            print("Assistant: Please enter a question.")
            continue
        messages.append({"role": "user", "content": question})

        tool_results: list[str] = []
        for _ in range(MAX_STEPS):
            try:
                response = model_with_tools.invoke(messages)
            except httpx.ConnectError:
                messages.pop()
                print("Assistant: Ollama is offline. Start the local model and retry.")
                break
            except ollama.ResponseError as error:
                messages.pop()
                print(f"Assistant: The model returned an error: {error.error}")
                break

            if not response.tool_calls:
                answer = response.text.strip()
                if not answer:
                    answer = tool_results[-1] if tool_results else "Please ask a staff member for help."
                messages.append({"role": "assistant", "content": answer})
                print(f"Assistant: {answer}")
                break

            messages.append(response)
            for call in response.tool_calls:
                tool = TOOLS.get(call["name"])
                if tool is None:
                    result = f"Unknown tool: {call['name']}"
                else:
                    try:
                        result = tool.invoke(call["args"])
                    except ValidationError as error:
                        result = f"Invalid tool arguments: {error}"
                result_text = str(result)
                tool_results.append(result_text)
                print(f"  [tool] {call['name']} -> {result_text}")
                messages.append(
                    {
                        "role": "tool",
                        "content": result_text,
                        "tool_call_id": call["id"],
                    }
                )
        else:
            print("Assistant: I could not finish this request; a staff member can help.")


if __name__ == "__main__":
    run()
