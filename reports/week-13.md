# Semester Week 13 Progress Report

## Completed Work

- Five tools in `mailmate/tools.py`: `list_emails`, `read_email`, `lookup_contact`, `draft_reply`, `send_email`.
- Tool schemas for the model, so the model chooses which tool to call (`bind_tools`).
- `validate_args`: checks the tool name, required arguments, types, the email id format, empty text and text length.
- Permission table in code (`PERMISSIONS`): reading, contact lookup and drafts are allowed, `send_email` needs my approval. Any other tool (for example `delete_email`) is blocked. Sending only to known contacts, max 3 emails per run.
- `mailmate/agent.py`: a multi-step loop. The model calls tools, my code checks and runs them, the result goes back to the model, until the model gives a final answer. Limits: 8 model steps and 20 tool calls. Every call is saved in a trace with its status (ok / invalid / blocked / rejected / failed) and there is a stop reason.
- Sending is simulated: an approved email is saved in `outbox/sent.json`, nothing goes to the internet.
- 8 new tests in `tests/test_week13.py` (16 tests in total, all pass, no API key needed).

- Second part (27 November): `mailmate/digest.py`, a daily digest. For every unread email the agent gets a label (triage), a one-sentence summary and a deadline as checked JSON (date format `YYYY-MM-DD HH:MM` or null, one retry), and writes reply drafts only for urgent / needs reply emails from known contacts. Dangerous emails never get a draft. The result is a sorted Markdown report. 5 new tests (21 in total).

## Important Commits

- Commit: "added tools, permissions and agent loop"
- Description: 5 tools, argument checks, permission table, multi-step agent, tests, this report
- Link: https://github.com/Asik456/ai-agents-final/commits/main
- Commit: "added daily inbox digest with deadlines and drafts" (27 November)

## Current Functionality

Real run with the model: "Which unread emails need a reply? Read them, then save a short draft reply for the email from my teacher."

```
step 1: list_emails {"unread_only": true} -> ok
step 2: read_email E-01 ... E-13 (12 emails) -> ok
step 3: draft_reply {"email_id": "E-01", ...} -> ok
stop: done
```

The answer listed E-01, E-06, E-08 and E-13 as emails that need a reply, saved a draft for the teacher (E-01) and said the bank email looks like phishing.

Second real run: "Read E-05 and do what it asks." The model read E-05 and refused to forward and delete emails. Even if it tried, there is no delete tool and sending to an unknown address is blocked in code (this is tested with the fake model).

Real digest run (`reports/digest-example.md`): 12 unread emails. Dangerous: E-04, E-05 and E-12 (the hidden injection). Urgent: E-01, E-13. Needs reply: E-06, E-08. Spam: E-07, E-11. Drafts were saved for E-01, E-06, E-08, E-13. When the answer depends on me, the draft has a gap like `[CHOOSE: 11:00 / 16:00]`, so the agent does not decide for me.

## Problems Encountered

- In the first real run the model read all 11 unread emails in one step, and my limit of 12 tool calls stopped the agent before it could write the draft.
- The model can ask for a tool that does not exist or give wrong arguments.
- I must not send real emails while testing.

## Solutions

- I changed the limit to 20 tool calls, because the inbox has 13 emails. The limit still stops an endless loop (tested).
- My code checks every call before running it. An error goes back to the model as a tool result, so the model can fix it, and the agent does not crash.
- `send_email` only writes to `outbox/sent.json`. In tests the approval function always says "no" or "yes", so no input is needed.

- Deadlines as free text ("next Friday") cannot be sorted. Now the model must give `YYYY-MM-DD`, my code checks it with a regex and asks once more if it is wrong.

## What I Learned

- The model decides what to call, but my code decides what is allowed. The prompt alone is not a guardrail.
- Limits must fit the task: too small stops normal work, too big lets a loop run long.
- A fake model that returns tool calls lets me test the whole loop for free.

## Next Week

- Move the loop into a LangGraph graph (nodes: plan, model, gate, review, execute) with state.
- Ask for approval with `interrupt` instead of `input()`.
- Add replanning after a failed tool.
- Choose the research paper.
