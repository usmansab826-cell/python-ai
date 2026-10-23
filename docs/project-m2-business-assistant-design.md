# Module 2 Final Project: AI Business Assistant

## Goal

Provide a local AI helper for business questions, menu prices, and approved
orders.

## Design

- **Business data:** `code/business.json` contains the business details and
  menu prices used by the tools.
- **Tools:** look up verified business information, look up a menu price, and
  request an order.
- **Order validation:** the tool rejects unknown items, non-positive/non-whole
  quantities, and missing customer names.
- **Approval:** an order is only written after an explicit `yes` confirmation.
- **Persistence:** approved order records are appended to
  `code/business_orders.jsonl`; the log is local runtime data.
- **Agent loop:** the local `qwen3.5:2b` model chooses tools, while a five-step
  limit prevents endless calls.
- **Run:** `uv run code/project_m2_business_assistant.py`

## Limits

The model can misunderstand a request. Read the proposed order details
carefully before approving, and verify the saved order ID and total.
