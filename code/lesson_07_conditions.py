
"""Lesson 1.7: Smart Model Router.

Choose a model based on task type, estimate cost,
and warn users about long requests.
"""

# Ask for the task and clean up the user's input.
task = input("Task (code / private / chat): ").strip().lower()
tokens = int(input("Estimated tokens: "))

# Stretch task: check whether the user has a paid plan.
paid_user = input("Is this a paid user? (yes/no): ").strip().lower()

# Why: Private data should stay on the user's own computer.
if task == "private":
    model = "llama3.2 (local, Ollama)"
    price_per_1k = 0.0

# Why: Code tasks may benefit from a stronger cloud model.
elif task == "code":
    model = "claude (cloud, strong at code)"
    price_per_1k = 0.01

else:
    model = "small cloud model (cheap for chat)"
    price_per_1k = 0.002

# Calculate estimated cost using the price per 1,000 tokens.
cost = (tokens / 1000) * price_per_1k

# Check request length and apply the free-user restriction.
if paid_user == "no" and tokens > 2000:
    warning = "Upgrade to send long requests."
elif tokens > 4000:
    warning = "Long request: consider shortening it."
else:
    warning = "Length is fine."

# Display the routing decision and estimated cost.
print("=" * 40)
print(f"Chosen model: {model}")
print(f"Estimated cost: ${cost:.2f}")
print(warning)

