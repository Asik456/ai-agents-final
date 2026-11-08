# Semester Week 10 Progress Report

## Completed Work

- Chose my project: MailMate, an email secretary agent, level A.
- Wrote the project proposal with functions, tools, architecture, examples and a plan for weeks 10–17.
- Made 13 test emails and 8 contacts. Some emails are tricky on purpose: one phishing email, two emails that try to give orders to the AI, and one email with no subject.
- Labeled every test email by hand (urgent, needs_reply, info, spam, suspicious) so I can check the agent later.
- Installed Node.js 22 and checked that the starter tests and `npm run proposal` pass.

## Important Commits

- Commit hash: 3eff38d
- Description: wrote the project proposal
- Link: https://github.com/Asik456/ai-agents-final/commit/3eff38d

- Commit hash: 8b08856
- Description: added 13 test emails, contacts and my own labels
- Link: https://github.com/Asik456/ai-agents-final/commit/8b08856

## Current Functionality

There is no agent code yet. The repository has the plan and the test data: `data/inbox.json`, `data/contacts.json` and `data/expected-labels.json`.

## Problems Encountered

- Node.js was not installed on my laptop.
- My first commits were not linked to my GitHub profile because git used my laptop name as the email.
- GitHub Actions did not run in my fork.
- It was hard to decide the label for some emails. For example, the IT support email is normal, but it has a hidden message for the AI inside.

## Solutions

- Installed Node.js 22 with Homebrew.
- Set my real email in the git settings of this project.
- Turned on Actions in the Actions tab of my fork.
- Wrote a short meaning for each label in `expected-labels.json`. Any email that tries to give orders to the AI is `suspicious`, even if the rest of it looks normal.

## What I Learned

- An email can attack an AI agent just with text (prompt injection). So the rules that stop the agent must be in my code, not only in the prompt.
- Reading an email is safe, but sending one is not. Sending must wait for my "yes".
- The `.example` domain is reserved for examples, so my test emails cannot belong to real people.

## Next Week

- Connect the model through OpenRouter.
- Make the first working request: a short summary of one email.
- Add setup steps to the README.
