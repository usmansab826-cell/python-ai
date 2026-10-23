"""Lesson 2.7: Extract, validate, total, and save bakery orders."""

import json
from pathlib import Path
import re
import sys

import httpx
import ollama
from langchain.chat_models import init_chat_model

PRICES = {
    "chocolate cake": 1500,
    "cupcake": 250,
    "brownie": 300,
}
ITEM_ALIASES = {
    "chocolate cake": ("chocolate cake", "chocolate cakes"),
    "cupcake": ("cupcake", "cupcakes"),
    "brownie": ("brownie", "brownies"),
}
NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "ek": 1,
    "do": 2,
    "teen": 3,
    "chaar": 4,
    "paanch": 5,
}
MODEL = "gemma3:1b"
ORDERS_FILE = Path(__file__).with_name("orders.json")

ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "customer": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
                "required": ["name", "quantity"],
            },
        },
        "address": {"type": "string"},
    },
    "required": ["customer", "items", "address"],
}

SYSTEM = (
    "Extract the bakery order from the customer message. "
    f"Return item names in singular form, exactly one of: {', '.join(PRICES)}. "
    "Use an empty customer name or address if it is not stated. "
    "If the message does not contain a clear order, return an empty items list. "
    "Never invent a name, address, menu item, or quantity. "
    "Convert English and Urdu number words to integers. In Roman Urdu, "
    "'do' immediately before a menu item means quantity 2."
)

MESSAGES_IN = [
    "Salam! 2 cupcakes aur 1 chocolate cake chahiye. Ali, house 12 Gulberg",
    "3 brownies please, Sara, DHA phase 5",
    "hi do you deliver to Johar Town?",
    "do cupcakes bhej dein",
    "1 pizza and 2 brownies",
    "same as last time please",
    "Bilal: 2 cakes, Model Town",
    "I want five brownies",
]


def canonical_item(name: str) -> str:
    """Return a menu item name for a known singular or plural alias."""
    candidate = name.strip().casefold()
    for menu_item, aliases in ITEM_ALIASES.items():
        if candidate in aliases:
            return menu_item
    return candidate


def source_mentions_item(message: str, name: str) -> bool:
    """Check whether the source message explicitly mentions a menu item."""
    return any(
        re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", message, re.IGNORECASE)
        for alias in ITEM_ALIASES[name]
    )


def explicit_quantity(message: str, name: str) -> int | None:
    """Read a digit or supported number word immediately before an item."""
    quantity_pattern = r"(?P<quantity>\d+|" + "|".join(NUMBER_WORDS) + r")"
    aliases = sorted(ITEM_ALIASES[name], key=len, reverse=True)
    for alias in aliases:
        match = re.search(
            rf"(?<!\w){quantity_pattern}\s+{re.escape(alias)}(?!\w)",
            message,
            re.IGNORECASE,
        )
        if match:
            quantity = match.group("quantity").casefold()
            return NUMBER_WORDS.get(quantity, int(quantity) if quantity.isdigit() else None)
    return None


def normalized_text(text: str) -> str:
    """Normalize punctuation and spacing for checking extracted text against a message."""
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def extracted_text(value: str) -> str:
    """Treat common model placeholders as missing values."""
    cleaned = value.strip()
    if normalized_text(cleaned) in {"not specified", "unknown", "none", "n a"}:
        return ""
    return cleaned


sys.stdout.reconfigure(encoding="utf-8")

extractor = init_chat_model(
    MODEL,
    model_provider="ollama",
    temperature=0,
    format=ORDER_SCHEMA,
)

saved = []

for message in MESSAGES_IN:
    try:
        response = extractor.invoke(
            [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": message},
            ]
        )
    except httpx.ConnectError:
        print("AI is offline. Please open the Ollama app and run the extractor again.")
        break
    except ollama.ResponseError as error:
        print(f"Model error: {error.error}")
        break

    try:
        order = json.loads(response.text)
    except json.JSONDecodeError as error:
        print(f"Could not read the AI JSON for this message: {error.msg}")
        continue

    if (
        not isinstance(order, dict)
        or not isinstance(order.get("customer"), str)
        or not isinstance(order.get("items"), list)
        or not isinstance(order.get("address"), str)
    ):
        print(f"AI returned an invalid order shape for: {message}")
        continue

    print(f"\nMessage: {message}")
    if not order["items"]:
        print("  Not an order: needs a human reply.")
        continue

    total = 0
    problems = []
    checked_items = []

    for item in order["items"]:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("name"), str)
            or type(item.get("quantity")) is not int
            or item["quantity"] <= 0
        ):
            problems.append("an item has an invalid name or positive whole quantity")
            continue

        name = canonical_item(item["name"])
        quantity = item["quantity"]
        if name not in PRICES:
            problems.append(f"'{item['name']}' is not on the menu")
            continue
        if not source_mentions_item(message, name):
            problems.append(f"'{item['name']}' is not mentioned in the message (invented?)")
            continue

        stated_quantity = explicit_quantity(message, name)
        if stated_quantity is not None and quantity != stated_quantity:
            problems.append(
                f"quantity for '{name}' was corrected to {stated_quantity} "
                "from the message"
            )
            quantity = stated_quantity

        line_total = PRICES[name] * quantity
        total += line_total
        checked_items.append({"name": name, "quantity": quantity})
        print(f"  {quantity} x {name} = {line_total} PKR")

    customer = extracted_text(order["customer"])
    if customer and customer.casefold() not in message.casefold():
        problems.append(f"customer '{customer}' is not in the message (invented?)")
    address = extracted_text(order["address"])
    if address and normalized_text(address) not in normalized_text(message):
        problems.append(f"address '{address}' is not in the message (invented?)")

    checked_order = {
        "customer": customer,
        "items": checked_items,
        "address": address,
        "total": total,
        "problems": problems,
        "source_message": message,
    }
    saved.append(checked_order)

    print(
        f"  Customer: {customer or '(missing)'}, "
        f"Address: {checked_order['address'] or '(missing)'}"
    )
    print(f"  Total: {total} PKR")
    for problem in problems:
        print(f"  CHECK: {problem}")

with ORDERS_FILE.open("w", encoding="utf-8") as orders_file:
    json.dump(saved, orders_file, indent=2, ensure_ascii=False)

print(f"\nSaved {len(saved)} checked orders to {ORDERS_FILE.name}")
