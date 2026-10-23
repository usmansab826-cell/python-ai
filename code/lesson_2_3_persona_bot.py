"""Lesson 2.3: Bakery bot grounded in facts with switchable personas."""

import sys

from langchain.chat_models import init_chat_model

config = {
    "model": "gemma3:1b",
    "temperature": 0.3,
    "max_messages": 6,
}

facts = {
    "name": "Sweet Crumbs",
    "city": "Lahore",
    "hours": "9 am to 10 pm",
    "address": "Main Boulevard, Lahore",
    "delivery": "Free delivery on orders over 3,000 PKR",
    "prices": {
        "chocolate cake": 1500,
        "cupcake": 250,
        "brownie": 300,
    },
}

personas = {
    "friendly": "warm and cheerful, uses simple words",
    "formal": "polite and professional, no jokes",
    "sales": "excited, always suggests one extra item to buy",
}

sys.stdout.reconfigure(encoding="utf-8")

llm = init_chat_model(
    config["model"],
    model_provider="ollama",
    temperature=config["temperature"],
)

rules = (
    f"You are the assistant of {facts['name']} bakery in {facts['city']}. "
    f"Business facts: {facts}. "
    "Only use these facts. If you do not know, say you will check with the manager. "
    "Answer in 2 short lines."
)

style = "friendly"
messages = [
    {"role": "system", "content": f"{rules} Your style: {personas[style]}."}
]

print("Sweet Crumbs Bot: Commands: /persona friendly|formal|sales, /price <item>, bye")

while True:
    text = input("You: ").strip()
    command, _, argument = text.partition(" ")
    command = command.lower()
    argument = argument.strip()

    if command == "bye":
        print("Bot: Goodbye!")
        break
    elif command == "/persona":
        persona = argument.lower()
        # Why: The default keeps an invalid persona command usable and predictable.
        style = persona if persona in personas else "friendly"
        selected_style = personas.get(style, personas["friendly"])
        messages[0]["content"] = f"{rules} Your style: {selected_style}."
        if persona in personas:
            print(f"Bot: Style changed to {style}.")
        else:
            print(f"Bot: Unknown style; using {style}.")
    elif command == "/price":
        item = argument.lower()
        if not item:
            print("Bot: Usage: /price <item>.")
        elif item in facts["prices"]:
            print(f"Bot: {item.title()} costs {facts['prices'][item]} PKR.")
        else:
            print(f"Bot: Sorry, {item} is not on our menu.")
    elif not text:
        print("Bot: Please type a question or command.")
    else:
        messages.append({"role": "user", "content": text})

        while len(messages) > config["max_messages"] + 1:
            del messages[1:3]

        response = llm.invoke(messages)
        answer = response.text
        messages.append({"role": "assistant", "content": answer})
        print(f"Bot: {answer}")
