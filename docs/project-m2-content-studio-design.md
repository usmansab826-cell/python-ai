# Module 2 Checkpoint 1: AI Content Studio

## Goal

Turn a small-business brief into three short, reusable promotional drafts.

## Design

- **Inputs:** business name, business type, city, audience, and optional
  verified products/prices/offers.
- **Outputs:** Instagram caption, WhatsApp promotion, and promotional idea.
- **Model:** local `gemma3:1b` with a creative temperature.
- **Guardrails:** the prompt limits draft length, forbids invented facts and
  prices, and asks the model to label missing details.
- **Human review:** the app reminds the owner to check every output before
  publication.
- **Run:** `uv run code/project_m2_content_studio.py`

## Limits

Prompt instructions do not guarantee perfect compliance. Validate claims,
spelling, tone, and platform requirements before publication.
