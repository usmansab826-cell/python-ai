# Module 1 Final Project: Test Results

Run offline checks with:

```powershell
uv run python -m unittest tests.test_coursework_projects -v
```

The automated checks cover direct answers for listed business facts, deferring
unknown facts to the AI path, and an explicit staff-handoff condition in the
interactive flow. Run the app itself with `uv run code/project_m1_front_desk.py`
after starting Ollama and confirm it answers a price question, an unknown
question without making a promise, a complaint/human request, and `bye`.

The test suite does not call the model. Record any model-generated answer
separately and verify every business claim before using it.
