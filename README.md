# Python for AI

**Name:** Usman

**Course:** Python for AI — Core Python for GenAI and Agentic AI

**AI goal:** Become an AI Agent Developer.

This repository follows my Python-for-AI lessons in order. Each lesson script is
kept in `code/`; lesson 1.3 is the project setup and structure task, so it does
not have a separate Python script.

## Project setup

```powershell
uv sync
uv run main.py
```

Run a lesson from the repository root with `uv run code/<file-name>.py`. `uv`
uses the project environment without requiring manual activation. The Python
version is pinned in `.python-version`; `uv.lock` records the exact dependency
versions. The `.venv/` directory is local and ignored by Git.

## Lessons, in order

### Module 1 — Python basics

| Lesson | Topic | Run |
|---|---|---|
| 1.1 | AI career introduction | `uv run code/lesson_01_intro.py` |
| 1.2 | AI development toolkit | `uv run code/lesson_02_toolkit.py` |
| 1.3 | Client-ready project setup and GitHub | Project structure task; see this README and the repository files |
| 1.4 | Business prompt builder | `uv run code/lesson_04_print_input.py` |
| 1.5 | Variables, types, and cost estimates | `uv run code/lesson_05_variables.py` |
| 1.6 | Strings and prompt cleanup | `uv run code/lesson_06_strings_prompts.py` |
| 1.7 | Conditions and smart model routing | `uv run code/lesson_07_conditions.py` |
| 1.8 | Sweet Crumbs rule-based chatbot | `uv run code/lesson_08_mini_chatbot.py` |

**Module 1 project — AI Prompt Kit:**

`uv run code/project_m1_prompt_kit.py`

A small-business tool that turns business details into three ready-to-use AI
prompts. See [the project run screenshot](docs/project-m1-run.png) and
[project results](docs/project-m1-results.md).

### Module 2 — Core Python for LLM apps

| Lesson | Topic / assignment | Run |
|---|---|---|
| 2.1 | First AI call — AI Tutor | `uv run code/lesson_2_1_first_ai_call.py` |
| 2.2 | Chat history — Personal Tutor with Memory | `uv run code/lesson_2_2_chat_memory.py` |
| 2.3 | Dictionaries — Persona Bot with Real Facts | `uv run code/lesson_2_3_persona_bot.py` |
| 2.4 | Loops — Batch Product Writer | `uv run code/lesson_2_4_batch_writer.py` |
| 2.5 | Functions — AI Skills Toolkit | `uv run code/lesson_2_5_ai_skills.py` |
| 2.6 | Files, JSON, and errors — Saved Bot | `uv run code/lesson_2_6_saved_bot.py` |
| 2.7 | Structured output — Order Extractor | `uv run code/lesson_2_7_extractor.py` |
| 2.8 | Tools and agent loop — First Agent | `uv run code/lesson_2_8_first_agent.py` |

The AI lessons use local Ollama models. Start Ollama and download the model
specified in each script before running it.

## Repository layout

```text
python-ai/
├── code/         # lesson scripts and project code
├── docs/         # notes, setup evidence, and project results
├── notebooks/    # Jupyter notebooks
├── main.py
├── pyproject.toml
├── uv.lock
└── .python-version
```

The generated chat histories, error logs, order data, and `.venv/` are ignored
by Git so private/runtime files are not pushed to GitHub.

## Sweet Crumbs Bakery chatbot

The Module 1 rule-based chatbot covers:

| Intent | Example response |
|---|---|
| Complaints and refunds | A manager will contact the customer within 1 hour |
| Opening hours | Open 9 am to 10 pm every day |
| Prices | Cakes from 1,500 PKR; cupcakes 250 PKR each |
| Location | Main Boulevard, Lahore |
| Ordering | WhatsApp ordering; free delivery over 3,000 PKR |
| Other questions | Provides a future AI prompt and counts unanswered questions |

The bot also remembers the customer's name, counts messages, and tracks
complaints.
