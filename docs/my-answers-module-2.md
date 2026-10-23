# Module 2 Quick Checks — Answer Key

Answers include short reasons so they can be reviewed before the class discussion.

## Checkpoint 1 — Lessons 2.1 to 2.4

- **2.1:** Q1 **b** (change the model/provider settings); Q2 **b** (`reply.text`); Q3 **b** (a low temperature is more repeatable); Q4 **a** (check that Ollama is running); Q5 **b** (streaming displays chunks as they arrive); Q6 `200 tokens in 3.5 seconds`.
- **2.2:** Q1 **b** (`-2` is the second-last item); Q2 **b** (`append()` mutates the list and returns `None`); Q3 **b** (the earlier messages were not sent to the model); Q4 **a** (preserve the system message/rules); Q5 **b** (long history costs more, is slower, and may exceed the context window); Q6 `['sys', 'u2', 'a2', 'u3'] 6`.
- **2.3:** Q1 **b** (`get()` returns its default); Q2 **c** (missing-key bracket access raises `KeyError`); Q3 **b** (assign a value to the new key); Q4 **b** (read the nested `city` key); Q5 **b** (ground the AI with trusted facts); Q6 `{'cupcake': 7, 'brownie': 0, 'donut': 8} 3 True`.
- **2.4:** Q1 **b** (`range` stops before 7); Q2 **b** (`.items()` yields key/value pairs); Q3 **b** (`total` resets each iteration, leaving 300); Q4 **b** (`continue` skips to the next item); Q5 **b** (create the model once and reuse it); Q6:

  ```text
  2: complaint
  3
  ```

  The empty review is skipped, while `"late again"` is counted and reported.

## Checkpoint 2 — Lessons 2.5 to 2.8

- **2.5:** Q1 **c** (a function without `return` gives `None`); Q2 **b** (required parameters must precede defaulted parameters); Q3 **b** (call the function with parentheses and its text argument); Q4 **b** (use the keyword argument to set `lines`); Q5 **b** (reuse an `ask_ai()` function); Q6:

  ```text
  Total: 1100.0
  None
  ```

  `add_tax()` returns `1100.0`; `show()` prints it but does not return a value.
- **2.6:** Q1 **c** (`"a"` appends); Q2 **b** (preserve Urdu and other characters as readable text); Q3 **b** (bare `except` can hide unrelated bugs); Q4 **b** (the app/server is unreachable); Q5 **b** (chat logs can contain private customer data); Q6:

  ```text
  Skipped abc
  550
  ```

- **2.7:** Q1 **b** (temperature zero makes extraction more consistent); Q2 **b** (the schema describes the required JSON shape); Q3 **b** (flag the unsupported customer name for human review); Q4 **b** (calculate with trusted Python prices); Q5 **b** (`json.JSONDecodeError`); Q6:

  ```text
  CHECK: pizza is not on the menu
  500 (missing)
  ```

- **2.8:** Q1 **b** (the model reads tool names and descriptions); Q2 **b** (`get_price.invoke({"item": "cupcake"})`); Q3 **b** (the tool result must match the request's ID); Q4 **b** (the step limit prevents an endless tool loop); Q5 **c** (placing an order changes data and needs approval); Q6:

  ```text
  step 0: tool
  step 1: tool
  step 2: tool
  Gave up: a human will help
  ```

  The loop uses all three steps without reaching `"answer"`, so its `else` runs.
