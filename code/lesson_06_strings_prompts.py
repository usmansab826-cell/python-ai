"""Clean a user's question and build a short prompt for an AI tutor."""

name = input("Your name: ")
raw_question = input("Your question: ")

clean_name = name.strip().title()
clean_question = raw_question.strip().capitalize()

# Estimate tokens so the user can see roughly how long the prompt is.
estimated_tokens = round(len(clean_question) / 4)

# Check lowercase text so Python is detected regardless of capitalization.
mentions_python = "python" in clean_question.lower()

short_question = clean_question[:150]
prompt = f"""You are a helpful Python tutor.
Welcome, {clean_name}!
Answer in 3 lines.
Question: {short_question}"""

print("=" * 40)
print(f"Cleaned: {clean_question}")
print(f"Characters: {len(clean_question)}")
print(f"Estimated tokens: {estimated_tokens}")
print(f"Mentions Python: {mentions_python}")
print("=" * 40)
print(prompt)
