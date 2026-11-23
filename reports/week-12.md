# Semester Week 12 Progress Report

## Completed Work

I did not make any commits during week 12 (16–22 November). I was busy with HW5, HW6 and the quiz, and I did not plan my time well.

The work planned for week 12 was done on 23 November (the first day of week 13):

- `list_emails` and `read_email` in `mailmate/inbox.py`. `read_email` checks the id format (like `E-01`) and marks the email text as untrusted.
- `mailmate/triage.py`: the model sorts every email into urgent / needs_reply / info / spam / suspicious and returns JSON. My code checks the JSON and asks again once if the answer is wrong.
- The first 8 tests in `tests/test_week12.py`, with a fake model, so they run without an API key.

## Important Commits

- Commit hash: the commit "added email list, sorting and first tests" (see git log, 23 November)
- Description: inbox functions, triage with JSON checks, 8 tests, this report
- Link: https://github.com/Asik456/ai-agents-final/commits/main

## Current Functionality

`python -m mailmate.triage` sorts all 13 test emails. Real run with the model: 10 of 13 labels match my own labels. All three dangerous emails were found as `suspicious`: the phishing email (E-04), the open prompt injection (E-05) and the hidden one inside the IT email (E-12). The 3 differences: the model called E-01, E-06 and E-09 `urgent` because they have a date, but I labeled them `needs_reply` and `info`. The result is saved in `reports/triage-week12.json`.

## Problems Encountered

- I lost one week of regular work.
- The model sometimes wraps JSON in a code block, or could return a label that does not exist.
- "Urgent" is not clear: the model thinks every email with a date is urgent.

## Solutions

- I will work on the project on at least two different days each week.
- `parse_label` removes the code block, checks that the label is one of the 5 allowed and that there is a reason. If not, the code asks the model again once, then returns a clear error.
- I will make the meaning of "urgent" more exact in the prompt later (for example: "within 3 days").

## What I Learned

- Parsing JSON is not enough: I also have to check the values (allowed labels, non-empty reason).
- A fake model lets me test retries and API errors without paying for real calls.
- Measuring against my own labels shows where the prompt is unclear.

## Next Week

- Turn the functions into tools the model can choose (list, read, lookup contact, draft, send).
- Check tool arguments and add a permission table in code.
