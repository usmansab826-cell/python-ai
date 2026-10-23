"""Lesson 2.8: Bakery agent that checks prices, orders, and approved purchases."""

import json
from pathlib import Path
import sys

import httpx
import ollama
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from pydantic import ValidationError

MAX_STEPS = 5
MODEL = "qwen3.5:2b"
ORDER_LOG = Path(__file__).with_name("agent_orders.jsonl")

PRICES = {
    "chocolate cake": 1500,
    "cupcake": 250,
    "brownie": 300,
}
ORDERS = {
    "A101": "baking",
    "A102": "out for delivery",
    "A103": "delivered",
}


def load_saved_orders() -> None:
    """Load previously placed orders so the status tool recognizes them."""
    try:
        with ORDER_LOG.open(encoding="utf-8") as order_file:
            for line in order_file:
                if not line.strip():
                    continue
                record = json.loads(line)
                if isinstance(record, dict) and isinstance(record.get("id"), str):
                    ORDERS[record["id"].upper()] = "received"
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Saved order log is damaged; older sample order statuses are still available.")
    except OSError:
        print("Saved order log could not be read; older sample order statuses are still available.")


load_saved_orders()

sys.stdout.reconfigure(encoding="utf-8")


@tool(parse_docstring=True)
def get_price(item: str) -> str:
    """Get the price of one bakery item.

    Args:
        item: The menu item name, for example "cupcake".
    """
    name = item.casefold().strip()
    if name in PRICES:
        return f"{name} costs {PRICES[name]} PKR"
    return f"{item} is not on the menu. Menu: {', '.join(PRICES)}"


@tool(parse_docstring=True)
def order_status(order_id: str) -> str:
    """Check the delivery status of an existing bakery order.

    Args:
        order_id: The order number, for example "A101".
    """
    key = order_id.upper().strip()
    if key not in ORDERS:
        return f"Order {order_id} not found"
    return f"Order {key} is {ORDERS[key]}"


def next_order_id() -> str | None:
    """Choose an order ID not already present in memory or the saved order log."""
    numbers = [
        int(order_id[1:])
        for order_id in ORDERS
        if order_id.startswith("A") and order_id[1:].isdigit()
    ]
    try:
        with ORDER_LOG.open(encoding="utf-8") as order_file:
            for line in order_file:
                if not line.strip():
                    continue
                record = json.loads(line)
                if not isinstance(record, dict):
                    return None
                order_id = record.get("id", "")
                if isinstance(order_id, str) and order_id.startswith("A"):
                    number = order_id[1:]
                    if number.isdigit():
                        numbers.append(int(number))
    except FileNotFoundError:
        pass
    except (OSError, json.JSONDecodeError):
        return None

    return f"A{max(numbers, default=100) + 1}"


@tool(parse_docstring=True)
def place_order(item: str, quantity: int, customer: str) -> str:
    """Prepare a new bakery order after the customer explicitly asks to order.

    Args:
        item: The menu item name, for example "cupcake".
        quantity: The positive whole-number quantity requested.
        customer: The customer's name.
    """
    name = item.casefold().strip()
    customer_name = customer.strip()
    if name not in PRICES:
        return f"{item} is not on the menu. Menu: {', '.join(PRICES)}"
    if type(quantity) is not int or quantity <= 0:
        return "Quantity must be a positive whole number."
    if not customer_name:
        return "Please provide the customer's name before placing the order."

    total = PRICES[name] * quantity
    approval = input(
        f"  [approve] {quantity} x {name} for {customer_name} = "
        f"{total} PKR. Place it? (yes/no) "
    )
    if approval.strip().casefold() != "yes":
        return "The owner did not approve this order."

    order_id = next_order_id()
    if order_id is None:
        return "Could not read the saved order log. Please ask the owner to check it."
    order_record = {
        "id": order_id,
        "item": name,
        "quantity": quantity,
        "customer": customer_name,
        "total": total,
    }
    try:
        with ORDER_LOG.open("a", encoding="utf-8") as order_file:
            order_file.write(json.dumps(order_record, ensure_ascii=False) + "\n")
    except OSError:
        return "Could not save the order. Please ask the owner to check the order log."
    ORDERS[order_id] = "received"
    return f"Order {order_id} placed: {quantity} x {name}, total {total} PKR"


TOOLS = {
    "get_price": get_price,
    "order_status": order_status,
    "place_order": place_order,
}

llm = init_chat_model(MODEL, model_provider="ollama")
llm_with_tools = llm.bind_tools(list(TOOLS.values()))

messages = [
    {
        "role": "system",
        "content": (
            "You are the Sweet Crumbs bakery agent. Use tools for prices, existing "
            "order statuses, and new orders. Never guess prices or statuses. "
            "Only call place_order when the customer clearly asks to place an order "
            "and provides both an item, positive quantity, and their name. "
            "Never claim an order was placed unless the tool confirms it. "
            "Answer in 2 short lines."
        ),
    }
]

print(
    "Sweet Crumbs Agent: Ask about prices or orders, or place an order. "
    "Type 'bye' to exit."
)

while True:
    text = input("You: ").strip()
    if text.casefold() == "bye":
        print("Agent: Goodbye!")
        break
    if not text:
        continue

    messages.append({"role": "user", "content": text})
    tool_results = []
    for step in range(MAX_STEPS):
        try:
            response = llm_with_tools.invoke(messages)
        except httpx.ConnectError:
            print("Agent: I am offline. Please start the Ollama app and try again.")
            messages.pop()
            break
        except ollama.ResponseError as error:
            print(f"Agent: The model could not complete that request: {error.error}")
            messages.pop()
            break

        if not response.tool_calls:
            answer = response.text.strip()
            if not answer:
                answer = (
                    tool_results[-1]
                    if tool_results
                    else "Sorry, I could not produce an answer. Please try again."
                )
            messages.append({"role": "assistant", "content": answer})
            print(f"Agent: {answer}")
            break

        messages.append(response)
        for call in response.tool_calls:
            name = call["name"]
            arguments = call["args"]
            if name not in TOOLS:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = TOOLS[name].invoke(arguments)
                except ValidationError as error:
                    result = f"Tool error: invalid arguments. {error}"

            print(f"  [tool] {name}({arguments}) -> {result}")
            tool_results.append(str(result))
            messages.append(
                {
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": call["id"],
                }
            )
    else:
        print("Agent: Sorry, I could not finish that. A human will help you.")
