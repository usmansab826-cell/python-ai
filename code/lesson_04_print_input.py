"""Lesson 1.4: Build an AI prompt from user input."""

# Ask for details so the prompt fits the user's business.
name = input("What is your name? ")
business = input("What type of business do you have? ")
problem = input("What problem does your business face? ")

# Include the user's details so an AI can give relevant suggestions.
prompt = f"Suggest 3 AI solutions for a {business} that struggles with {problem}."

print(f"\nWelcome, {name}!")
print("\n--- Your Prompt ---")
print(prompt)
