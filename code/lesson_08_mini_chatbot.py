
"""Lesson 1.8: Rule-based chatbot for a local bakery."""

BOT = "Sweet Crumbs Bot"

print(f"{BOT}: Hi! I can help with hours, prices, location and orders.")
print(f"{BOT}: Type 'bye' to exit.")

# Why: Ask the name once so the bot remembers it throughout the chat.
name = input(f"{BOT}: What is your name? ").strip().title()

if name == "":
    name = "Friend"

print(f"{BOT}: Nice to meet you, {name}!")

count = 0
unanswered = 0
complaints = 0

while True:
    message = input(f"{name}: ").strip().lower()
    count += 1

    if message == "bye" or message == "exit":
        print(f"{BOT}: Goodbye, {name}! Thanks for visiting.")
        break

    # Why: Offer human help immediately for complaints or handover requests.
    elif "complaint" in message or "refund" in message or "late" in message:
        complaints += 1
        print(f"{BOT}: Sorry about that. A manager will contact you within 1 hour.")

    elif "agent" in message or "human" in message:
        print(f"{BOT}: Connecting you to a human...")
        break

    elif message == "":
        print(f"{BOT}: Please type a question.")

    elif "hour" in message or "open" in message or "time" in message:
        print(f"{BOT}: We are open from 9 am to 10 pm, every day.")

    elif "price" in message or "cost" in message or "how much" in message:
        print(f"{BOT}: Cakes start at 1,500 PKR. Cupcakes are 250 PKR each.")

    elif "where" in message or "location" in message or "address" in message:
        print(f"{BOT}: We are on Main Boulevard, Lahore.")

    elif "order" in message or "delivery" in message:
        print(f"{BOT}: Order on WhatsApp. Delivery is free over 3,000 PKR.")

    # Why: Exact greeting matches avoid triggering on words like "which".
    elif message == "hi" or message == "hello" or message.startswith("salam"):
        print(f"{BOT}: Hello, {name}! How can I help you?")

    else:
        unanswered += 1
        prompt = (
            "You are the friendly assistant of Sweet Crumbs bakery. "
            f"Answer this customer in 2 lines: {message}"
        )
        print(f"{BOT}: I don't know that answer yet.")
        print(f"{BOT}: Future AI prompt: {prompt}")

print("=" * 40)
print(f"Chat summary: {count} messages, {unanswered} unanswered.")
print(f"Complaints received: {complaints}")

