# Python for AI

**Name:** Usman  
**Course:** Python for AI � Module 1: Python Basics for GenAI and Agentic AI  
**AI goal:** Become an AI Agent Developer.

## Run

`uv run main.py`

## Lessons completed

- Lesson 1.1: AI Career Intro
- Lesson 1.2: Toolkit Proof
- Lesson 1.3: Client-Ready Repo
- Lesson 1.4: Business Prompt Builder


## Module 1 Project: AI Prompt Kit

A Python tool that turns a local business's details into 3 ready-to-use AI prompts.

**Run:** `uv run code/project_m1_prompt_kit.py`

![Prompt Kit running](docs/project-m1-run.png)

**Who would pay for this:** Local small businesses that want AI help but are unsure what to ask.

## Lesson 1.8: Business Helper Bot — Sweet Crumbs Bakery

| Intent | Keywords | Reply |
|---|---|---|
| Complaint | refund, complaint, late | Manager will contact the customer within 1 hour |
| Human handover | agent, human | Connecting you to a human |
| Opening hours | hour, open, time | Open 9 am to 10 pm every day |
| Prices | price, cost, how much | Cakes from 1,500 PKR; cupcakes 250 PKR each |
| Location | where, location, address | Main Boulevard, Lahore |
| Ordering | order, delivery | Order on WhatsApp; free delivery over 3,000 PKR |
| Greeting | hi, hello, salam | Friendly greeting using the customer's name |
| Exit | bye, exit | Goodbye and chat summary |
| Other questions | No matching keywords | Print a future AI prompt and count unanswered questions |

The bot remembers the customer's name, counts messages and unanswered questions, and tracks complaints. The complaint rule runs before the order rule so late orders receive human support.