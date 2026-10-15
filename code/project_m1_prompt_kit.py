"""Build three ready-to-use AI prompts for a local business owner."""

business_name = input("Business name: ")
business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")

# Convert the budget to an integer so the prompt can use a numeric PKR amount.
monthly_budget = int(input("Monthly budget (PKR): "))

# Add the business name so the owner can recognize their prompt kit.
print()
print("=" * 41)
print(f"   AI Prompt Kit for {business_name}")
print("=" * 41)

# Name the audience and tone so the marketing post is specific and usable.
marketing_prompt = (
    f"Act as a social media marketer. Write one short Instagram post for "
    f"{business_name}, a {business_type} in {city}. Target {customers}. "
    f"Use a friendly tone and include one call to action."
)

# Set a clear customer-service role and situation to guide the reply.
service_prompt = (
    f"You are the manager of {business_name}. Write a polite reply to an "
    f"unhappy customer whose order arrived late. Apologise and offer a "
    f"small discount without inventing specific discount terms."
)

# Include the budget and ask the AI to flag uncertain prices to reduce made-up claims.
growth_prompt = (
    f"Suggest 3 low-cost AI ideas for a {business_type} in {city} that wants "
    f"to attract {customers}. Keep the total monthly budget within "
    f"{monthly_budget} PKR. Do not invent prices; label any estimates clearly."
)

print()
print("[1] Marketing")
print(marketing_prompt)
print()
print("[2] Customer Service")
print(service_prompt)
print()
print("[3] Growth")
print(growth_prompt)
