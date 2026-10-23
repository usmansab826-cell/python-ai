# Lesson 2.8 — Watch the Agent Think

Run `uv run code/lesson_2_8_first_agent.py` with Ollama running to observe the
tool-calling loop. Try a cupcake price question, an existing order-status
question, and a new order request.

For a new order, the `place_order` tool asks for explicit owner approval. A
declined order is not saved; an approved order is written to the local ignored
file `code/agent_orders.jsonl`. The agent prints each tool name, arguments,
and result so the user can see what happened before the final response.

This note describes the observable behavior implemented in the script. A
model-generated transcript should be recorded only after running the local
model; model output can vary between runs.
