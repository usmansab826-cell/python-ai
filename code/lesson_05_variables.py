"""Lesson 1.5: Store an AI model profile and estimate token cost."""

model_name: str = "local-demo-model"
context_window_tokens: int = 8192
price_per_1k_tokens: float = 0.50  # Practice price in PKR, not a real model price.
runs_locally: bool = True

# Show each setting's type so type mistakes are easier to spot.
print(f"Model: {model_name} ({type(model_name).__name__})")
print(f"Context window: {context_window_tokens} tokens ({type(context_window_tokens).__name__})")
print(f"Price per 1K tokens: {price_per_1k_tokens} PKR ({type(price_per_1k_tokens).__name__})")
print(f"Runs locally: {runs_locally} ({type(runs_locally).__name__})")

# Convert input text to an integer before doing cost maths.
tokens_used = int(input("Tokens used: "))
estimated_cost = tokens_used / 1000 * price_per_1k_tokens
print(f"Estimated cost: {round(estimated_cost, 2)} PKR")

# Multiply by 30 to estimate a month's usage.
chats_per_day = int(input("Chats per day: "))
monthly_cost = chats_per_day * 30 * (tokens_used / 1000) * price_per_1k_tokens
print(f"Estimated monthly cost: {round(monthly_cost, 2)} PKR")
