# Reviewers

Ready-to-use briefs for the review roles in `workflow/review.md`. Each brief is self-contained: hand it to a reviewer that did not write the code, together with the inputs below.

## How to run them

- **With subagents:** start one subagent per role the diff touched, in parallel, each with its brief and the inputs. Give it nothing else from the session: a reviewer that knows the author's reasoning tends to agree with it.
- **Without subagents:** run the roles one after another in the main session. Before each one, set the work aside, read only the brief and the inputs, and say in one line that the review ran inline.
- **With a review tool the agent ships** (a code review, security review or simplification skill or command): it may play a role when it covers the brief's checks. Pass it the same inputs and bring its findings into the report format below. The product's `triggers.md` says which tool plays which role.
- **Which roles:** spec and standards on every change that writes code; security when the diff touches an endpoint, login, permissions, personal data, money, outside events or another user's data; interface when users will see the change. The final review closes a batch.

## Inputs for every role

1. The diff against the merge base (`git diff <base>...HEAD`), after confirming the base exists and the diff is not empty.
2. The task file (what it delivers, done-when, risk answers) and the plan or brief it belongs to.
3. `docs/playbook/context.md` (the product's rules win over the playbook) and the principle files of the role.
4. For interface: `DESIGN.md`, the mock if there is one, and screenshots at phone and desktop size.

## Report format (every role)

```
Role: <role> · Scope: <diff range or screen>
| # | Kind (hard rule / judgment) | Severity (P0-P3) | Where (file:line) | Evidence | Suggestion | Effort (S/M/L) |
What works: <one or two lines>
```
- At most 8 findings, the most important first. Hard rule = a written rule (playbook or `context.md`) is broken; judgment = a smell or a risk.
- Verify each finding before reporting it (open the line, run the command). No finding without evidence.
- Report only. Do not edit files, commit or run anything that changes state.

## Brief: spec

You check the change against what was asked. Read the task and the plan first, then the diff.
- What is **missing** or only partly done compared with each done-when item and acceptance criterion? Cite the criterion.
- What was **added** that nobody asked for?
- What **looks done but is wrong** (a branch never reached, a state not handled, a value hardcoded where a rule was asked)?
- Every "yes" in the task's risk answers has its required tests (`workflow/stages.md`); the tests check behavior through the public entry point and would fail without the change.
- Docs and guides the product requires in the same change (`triggers.md`, "Change visible to users") were updated.

## Brief: standards and simplification

You check the code against the playbook and the product's rules. Read `principles/clean-code.md` and `principles/architecture.md`, then the diff.
- Hard rules: layer direction, size limits from `context.md`, errors never swallowed, no secrets, one source of truth for each value, dates and money handled at one point.
- Simpler is possible: duplicated logic that already exists elsewhere (name the existing function), a new abstraction with fewer than three uses, a flag that should be two components, code with no caller.
- Code smells as judgment: mysterious names, long parameter lists, feature envy, shotgun surgery, speculative generality.
- Skip what the linter already reports.

## Brief: security

You look for ways the change lets the wrong person do or see something, or lets a write happen twice or get lost. Read `principles/security.md` and `principles/data-integrity.md`, then the diff.
- Every new or changed entry point: who can call it, and is ownership checked on each object it reads or writes (one user reaching another's data by changing an id)?
- Input validated on the server; errors that do not leak internals; no secret, token or personal data in logs, URLs or responses.
- Read-then-write sequences that two simultaneous requests can break; repeated requests and repeated outside events (idempotency); status changes that can move backwards.
- Queries and commands built from input are parameterized; user or model content rendered as HTML is sanitized; cookie sessions have forgery protection; addresses the user chooses are checked before the server fetches them; uploads are checked (`principles/security.md`, "Injection and output").
- Outside events authenticated and failing closed; outside calls with a timeout.
- With `ai` in the context: untrusted text kept out of the system instructions, tools limited to the user's permissions, model output validated before use, agent loops with a stop (`requirements/ai.md`).
- For each finding, write the attack or the race in one line (who does what, what happens).

## Brief: interface

You check what users will see. Read `principles/interface.md` and the product's `DESIGN.md`, then look at the screenshots and the diff.
- Every state of each screen touched: loading, empty, error with saved data, error without data, offline when the product lists it.
- Only tokens from `DESIGN.md`; a raw value has a comment saying why.
- Accessibility (WCAG 2.2 AA): contrast, target size, focus visible and in order, labels, nothing conveyed by color alone, reduced motion respected.
- Phone and desktop size; long text and translations do not break the layout; repeated taps cannot submit twice.
- Copy: the product's words (glossary), actions named by what they do.
- Rate each finding with the usability heuristic it breaks and a severity from P0 (blocks the task) to P3 (cosmetic).

## Full audit

The same briefs, with the whole codebase as the scope instead of a diff. Run it when the person asks, before a first release, or periodically for security.
1. List every entry point first (routes, handlers, scheduled jobs, webhooks, tools given to a model), so the report proves what was covered.
2. Check each one against the brief, area by area, and record what is correct with its evidence too.
3. Save the report in `docs/playbook/reviews/<date>-<area>-audit.md`. Each finding that needs work becomes a task; when the product uses an issue tracker, also write each one as a ready-to-paste issue (title, evidence, impact, fix, acceptance criteria). A visual page or a PDF only if the person asks.

## Brief: final review

You close a batch in a fresh context. Before reading the author's summary, list what the diff actually changed (files, behaviors). Then check each claim in the summary against that list and against evidence: a test name and its output, a command output, a screenshot. A described fix without evidence counts as not done. End with the verdict: ship, fix, rebuild or recapture evidence.

Sources: Google engineering practices (code review); OWASP ASVS and API Security Top 10; WCAG 2.2; Nielsen Norman Group, usability heuristics and severity ratings; Fowler, *Refactoring*; Panickssery et al. 2024 on self-preference in model evaluation.
