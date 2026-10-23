# Module 1 Final Project: AI Front Desk

## Goal

Give a small bakery a simple front-desk assistant that answers routine customer
questions and refers sensitive or unsupported requests to staff.

## Design

- **Interface:** command-line chat in `code/project_m1_front_desk.py`.
- **Verified facts:** business hours, address, delivery rule, contact method,
  and menu prices are stored in the project code.
- **Known questions:** hours, address, delivery, contact, and listed prices are
  answered directly from those facts.
- **Other questions:** sent to the local Ollama model with a strict grounding
  instruction; the assistant must admit when information is not available.
- **Human handoff:** complaint, refund, manager, or human requests are routed to
  staff rather than answered with invented promises.
- **Privacy:** conversation history stays in memory and is not written to disk.
- **Run:** `uv run code/project_m1_front_desk.py`

## Limits

The keyword router covers common questions, not every way customers phrase
them. AI responses must be reviewed before being treated as business policy.
