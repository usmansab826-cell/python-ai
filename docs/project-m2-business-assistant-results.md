# Module 2 Final Project: Test Results

Run offline checks with:

```powershell
uv run python -m unittest tests.test_coursework_projects -v
```

The automated tests check the trusted cupcake price, persistence of an
explicitly approved order, correct total calculation, and that declining an
order creates no file. These tests use a temporary directory and do not call
Ollama. For a live check, start Ollama, ask for an item price, then request an
order and verify both the approval prompt and saved record. The model must not
claim an order was placed unless the tool confirms it.
