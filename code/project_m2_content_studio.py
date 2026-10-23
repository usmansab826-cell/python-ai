"""Module 2 project: create fact-grounded marketing content for a small business."""

import json
import re
import sys

import httpx
import ollama
from langchain.chat_models import init_chat_model

MODEL = "gemma3:1b"
MAX_WORDS = 60
DRAFTS_SCHEMA = {
    "type": "object",
    "properties": {
        "instagram_caption": {"type": "string"},
        "whatsapp_promotion": {"type": "string"},
        "promotional_idea": {"type": "string"},
    },
    "required": [
        "instagram_caption",
        "whatsapp_promotion",
        "promotional_idea",
    ],
}
DRAFT_LABELS = {
    "instagram_caption": "Instagram caption",
    "whatsapp_promotion": "WhatsApp promotion",
    "promotional_idea": "Promotional idea",
}
REVIEW_PHRASES = (
    "placeholder",
    "new favourite",
    "new favorite",
    "valid until",
    "expires",
    "special offer",
    "sale",
    "discount",
    "free gift",
    "freshly made",
    "homemade",
)


def build_prompt(
    business_name: str,
    business_type: str,
    city: str,
    audience: str,
    verified_facts: str,
) -> str:
    """Build a content brief that prevents unsupported business claims."""
    return (
        f"Create exactly three marketing drafts for {business_name}, a "
        f"{business_type} in {city}, for this audience: {audience}. "
        f"Use only these verified facts: {verified_facts or 'No additional facts provided.'} "
        "Draft 1: a friendly Instagram caption with one call to action. "
        "Draft 2: a short WhatsApp promotion. Draft 3: a concise promotional "
        f"idea. Return the drafts in the required structured fields. "
        f"Keep each draft to at most {MAX_WORDS} words. "
        "Do not invent prices, discounts, contact details, products, or claims. "
        "Label any missing information instead of guessing."
    )


def review_drafts(drafts: dict[str, str], verified_facts: str) -> list[str]:
    """Flag overlong drafts and numbers absent from the supplied facts."""
    allowed_numbers = {
        re.sub(r"[\s,]", "", number).casefold()
        for number in re.findall(
            r"\d[\d,]*(?:\s*(?:am|pm|PKR))?", verified_facts, re.IGNORECASE
        )
    }
    findings = []
    for field, label in DRAFT_LABELS.items():
        text = drafts[field]
        word_count = len(text.split())
        if word_count > MAX_WORDS:
            findings.append(
                f"{label} has {word_count} words; the limit is {MAX_WORDS}."
            )
        for number in re.findall(
            r"\d[\d,]*(?:\s*(?:am|pm|PKR))?", text, re.IGNORECASE
        ):
            if re.sub(r"[\s,]", "", number).casefold() not in allowed_numbers:
                findings.append(f"{label} contains unverified number {number}.")
        for phrase in REVIEW_PHRASES:
            if phrase in text.casefold() and phrase not in verified_facts.casefold():
                findings.append(f"{label} may contain an unsupported claim: {phrase}.")
    return findings


def main() -> None:
    """Collect a brief and generate the three content drafts."""
    sys.stdout.reconfigure(encoding="utf-8")
    print("AI Content Studio — provide a small business brief.")
    business_name = input("Business name: ").strip()
    business_type = input("Business type: ").strip()
    city = input("City: ").strip()
    audience = input("Target customers: ").strip()
    verified_facts = input("Verified products, prices, or offers (optional): ").strip()
    if not all((business_name, business_type, city, audience)):
        raise SystemExit("Business name, type, city, and target customers are required.")

    prompt = build_prompt(
        business_name, business_type, city, audience, verified_facts
    )
    model = init_chat_model(
        MODEL,
        model_provider="ollama",
        temperature=0.7,
        format=DRAFTS_SCHEMA,
    )
    try:
        response = model.invoke(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a careful small-business content writer. "
                        "Follow the brief exactly. Use only stated facts; do not "
                        "add quality claims, claims that a business is new, "
                        "placeholders, expiry times, discounts, or offers."
                    ),
                },
                {"role": "user", "content": prompt},
            ]
        )
    except httpx.ConnectError as error:
        raise SystemExit(
            "Ollama is offline. Start Ollama and run this script again."
        ) from error
    except ollama.ResponseError as error:
        raise SystemExit(f"The model could not generate content: {error.error}") from error

    try:
        drafts = json.loads(response.text)
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"The model returned unreadable structured output: {error.msg}"
        ) from error
    if not isinstance(drafts, dict) or any(
        not isinstance(drafts.get(field), str) for field in DRAFT_LABELS
    ):
        raise SystemExit("The model did not return all three required text drafts.")

    print(f"\nContent drafts for {business_name}")
    print("=" * 50)
    for field, label in DRAFT_LABELS.items():
        print(f"\n{label}:\n{drafts[field].strip()}")
    findings = review_drafts(drafts, verified_facts)
    if findings:
        print("\nReview flags:")
        for finding in findings:
            print(f"- {finding}")
    print("=" * 50)
    print("Review all claims and details before publishing.")


if __name__ == "__main__":
    main()
