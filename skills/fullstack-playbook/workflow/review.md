# Review

Machines check what can be measured; reviewers judge the rest. A review is done by someone who did not write the code, because a model tends to approve its own work.

## The gate first

`docs/playbook/verify.sh` runs before every commit and in CI: lint with the product's size and complexity limits, forbidden imports between layers, type checks, tests, unused code, dependency and secret scans, commit message format, design tokens, accessibility and visual regression checks where available, and the notebook check. Choose each tool for the product's stack during onboarding and record it as a decision. A lint finding is fixed, or gets the narrowest exception with a written reason; it is never silenced to pass.

## What stays with reviewers

Business rules, subtle access to other users' data, fidelity to the plan and acceptance criteria, names and module depth, visual hierarchy, and whether a test tests the right thing.

## Reviewers

- **Fresh context, closed scope, read-only.** One reviewer per area, run only when the diff touched it: correctness against the plan, security, interface, simplification. The ready brief for each role, the inputs and the report format are in `workflow/reviewers.md`.
- **Two axes, never merged:** standards (does the code follow the principles) and spec (what is missing, extra or wrong compared with the criteria, citing the line).
- **Code smells** (Fowler) are judgment calls; the product's rules win; skip what the lint already catches.
- **Separate hard violations from judgment,** and cap the findings per reviewer so the report stays readable.
- **Diff against the merge base;** confirm the base exists and the diff is not empty before reviewing.
- **No false positives:** verify each finding before reporting it. Separate systemic problems from one-off ones. Record what works, too.
- **The reviewer only reports;** the main session decides and fixes.
- **Use the review tools the agent already ships.** Many agents come with review skills or commands (code review, security review, simplification). When one fits a role above, it may play that reviewer with the same inputs and report format. The product's `triggers.md` ("End of a step") names which tool plays each role; without one, use the briefs in `workflow/reviewers.md`.

## Triage and report

Each finding becomes one of: fix now with a test that fails without the fix; keep, with the reason; out of scope, as a new task. Commit fixes separately from refactors. Write the result with `templates/review-report.md` in the project's `reviews/` folder (or the task, for a small change), never only in the conversation: OK, Fail with evidence, or N/A with a reason, for each item.

## Interface review

Open the screen at phone and desktop size, in each theme. Score Nielsen's ten heuristics from 0 to 4, give each finding a severity from P0 to P3 ("would a user contact support?" is at least P1), and walk the screen as a power user, a beginner, someone using assistive technology, someone stressed, and someone on a phone and distracted. Polish at the narrowest level: decide whether a deviation is a missing token, a one-off implementation, a conceptual mismatch or a local defect, and fix it there.

## Final review and evidence

The last review of a batch runs in a fresh context and inventories the target before reading the author's summary. Describing a fix is not evidence; a command output, a screenshot or a test is. The verdict (ship, fix, rebuild, recapture evidence) follows from the findings. After a batch, audit it: files and functions touched, and for each bug the commit where it entered and where it left.

## QA script

Each kind of change has a permanent scenario script (for example online, offline with saved data, server error showing saved data, leaving and returning). Keep it in `docs/playbook/qa/<kind of change>.md` and run it every time that kind of change happens, instead of an ad-hoc sweep.

## Learning from reviews

A finding that repeats becomes a written rule with its origin. A mechanical mistake becomes a check in `verify`; prove the check works (passes, then breaks on purpose, then passes). At the end of a project, hold a short retro: what went well, what hurt, what becomes a rule, a check, a template or a trigger.

Sources: Google engineering practices (code review); Fowler, *Refactoring*; Nielsen Norman Group, 10 usability heuristics; Panickssery et al. 2024 on self-preference.
