# Semester Week 11 Progress Report

## Completed Work

- Updated the plan and the architecture in the proposal. The agent will be a LangGraph graph in Python, like the agent from the Week 10 lecture.
- Set up the Python environment and `requirements.txt`.
- Connected the model (`openai/gpt-5.6-luna` through OpenRouter) in `mailmate/model.py`.
- Wrote `mailmate/inbox.py` to load the test emails and find one by id.
- Made the first working request: `mailmate/summary.py` explains one email in simple words.
- Added a short "How to run" part at the top of the README.

## Important Commits

- Commit hash: bdae85d
- Description: updated plan and architecture
- Link: https://github.com/Asik456/ai-agents-final/commit/bdae85d

- Commit hash: this week's last commit (see git log)
- Description: connected the model and made the first request
- Link: https://github.com/Asik456/ai-agents-final/commits/main

## Current Functionality

`python -m mailmate.summary E-01` gives a short summary of an email. Real output:

- E-01: "Aigul Serikova says you have not submitted HW5 yet. It is due by 8 November at 23:59, and she wants to know by Friday if you need an extension."
- E-05 (the email that tries to give orders to the AI): the model did not follow it. It only said that the email asks to forward all emails and delete them.
- E-10 (no subject): works, the program writes "(no subject)".
- E-99: "no email with id E-99".
- No API key: "LLM_API_KEY is missing", the program does not crash.

## Problems Encountered

- My old API key was shown in a chat by mistake.
- The model client needed the right base URL and settings for OpenRouter.
- An email can contain text that looks like an order for the AI (E-05).

## Solutions

- I deleted the old key on OpenRouter and made a new one. The key is only in `.env`, which is in `.gitignore`.
- All settings come from `.env` (`LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`), with an example in `.env.example`.
- The email text is put between `<email>` and `</email>`, and the system prompt says this text is data, not instructions. This is only the first step: real checks in code come in week 15.

## What I Learned

- How to call a model through an OpenAI-compatible API with a different base URL.
- Errors must come back as clear messages, not crashes (missing email, missing key, failed call).
- A prompt alone cannot fully stop prompt injection, so later I need rules in code.

## Next Week

- Read and list emails, and sort them into urgent / needs_reply / info / spam / suspicious as JSON.
- Check the JSON from the model and handle bad answers.
- Write the first 5 tests.
