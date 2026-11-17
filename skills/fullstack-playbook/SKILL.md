---
name: fullstack-playbook
description: "Full-stack development workflow and engineering principles for building a product with a coding agent, from idea to release. Use for any change to a product's code, data or configuration, even a small text or color change: starting or onboarding a project, planning or building a feature, fixing a bug, writing tests, reviewing code or a screen, changing the database, or releasing; also when vibe coding and asked to build, fix, ship or make it production-ready. Runs the work like a software company (brief, design, architecture, plan, tests first, build, review, QA, release), keeps projects and tasks inside the repository, asks onboarding questions one at a time, and applies universal principles: architecture, clean code, data integrity (atomicity, race conditions, idempotency), security, testing against a real database, performance, interface design, offline-first and AI features."
license: MIT
metadata:
  repository: https://github.com/brunomendespereira/fullstack-playbook
  version: 1.2.1
---

# fullstack-playbook

Two parts work together:
- **This skill is the manual.** The same for every product. Never edit it inside a product.
- **The product keeps a notebook** that this skill creates and updates: `docs/playbook/` (context, state, triggers, projects and tasks, decisions, memory, glossary), plus `PRODUCT.md` and `DESIGN.md` at the repository root.

The manual says what is right. The notebook says how it applies here. When they disagree, a rule written in `docs/playbook/context.md` wins, because it was chosen for this product.

## Always

- **Plan, then wait for an explicit ok** at the approval points of the request's size (`workflow/stages.md`) and of the autonomy level in `context.md`. Understand the request, show a short plan, and act only after a clear yes. A request is not an approval. An ok that leaves something "to discuss later" does not approve that thing. A question left unanswered stays open.
- **Say what you are about to do** before each technical action, even inside an approved plan.
- **Find facts yourself; leave decisions to the person.** Never ask what the code or the notebook already answers.
- **Before writing to an outside service** (issue tracker, docs tool, chat, email), show what changes and where, and wait for the ok.
- **Never print or commit secrets.** Mask tokens, passwords and connection strings in every output.
- **If something must happen every time, make it a check** (git hook, CI, script), not a reminder.
- **Ask one question at a time**, with a suggested answer, in plain text.
- **Put new code where the product's structure says:** before creating a file or folder, read "Code structure" in `context.md`. When no row covers it, ask, then add the row (`principles/architecture.md`).
- **Save every file where it belongs** (research, reviews, QA, drafts): the table in `workflow/tasks.md`, "Where files go". Agent folders hold only agent configuration.
- **Write the notebook in the product's language** (`language` in `context.md`) and talk in the person's language. Keep field names and file names as they are.

## Start of every request

1. Read `docs/playbook/state.md`, then `docs/playbook/context.md`. If `docs/playbook/` does not exist, read `workflow/onboarding.md` and run onboarding first. A quick question that changes nothing can be answered without onboarding.
2. On the first request of a session, compare `playbook_version` in `context.md` with `version` in this file's `metadata`. If it is missing or older, upgrade the notebook first (`workflow/upgrade.md`), then go on.
3. Classify the request with the table below and read the files of its route.
4. If the request changes code or data, answer the **risk questions** (in `workflow/stages.md`) in the task file; a small adjustment gets a one-line task in `projects/maintenance/`. Each "yes" adds a principle file and required tests.
5. Read the principle files for the areas the change touches. Read nothing else.
6. Work through the stages for the request's size. Run the product's triggers at each moment (`docs/playbook/triggers.md`, mechanism in `workflow/triggers.md`).
7. Before stopping, also when blocked or waiting for an answer: update the task (status, and what blocks it), replace `docs/playbook/state.md` so it names that task and the next action, commit when verify passes, give the resume phrase, say which triggers ran (or that none applied), and list any memory entries marked `Playbook candidate` (`workflow/tasks.md`).

**Small path** (a text, color or config value, all risk answers "no"): even here, create `docs/playbook/projects/maintenance/tasks/NNN-short-name.md` from `templates/task.md` with the six risk answers, make the change, run `verify`, run the "change visible to users" trigger when users will see it, and close the task. If something stops you from closing it, mark it `blocked` and do step 6. No brief, no plan.

## Routes by request

| The request is... | Read |
|---|---|
| A new product (empty repository, "let's build X") | `workflow/onboarding.md`, then `workflow/stages.md` |
| The first time in an existing product (no `docs/playbook/`) | `workflow/onboarding.md` |
| A feature | `workflow/stages.md`, `principles/product.md`, then the area files |
| A bug | `workflow/debugging.md`, `principles/testing.md` |
| A critical bug (money, security, user data) | `workflow/debugging.md`, `principles/testing.md`, plus `principles/data-integrity.md` or `principles/security.md` |
| A small adjustment (text, color, a config value) | the small path above |
| A review of code or of a screen | `workflow/review.md`, `workflow/reviewers.md`, then the area files |
| Unclear or exploratory work | the foggy-work section of `workflow/stages.md` |
| Merge, deploy, release, migration | `workflow/release.md` |
| "Continue", status, new project, cleanup | `workflow/tasks.md` |
| The notebook is older than the skill (`playbook_version`) | `workflow/upgrade.md` |
| A new idea, report or request to sort | the triage section of `workflow/tasks.md` |
| An automation or a "whenever X, do Y" rule | `workflow/triggers.md` |

## Areas the change touches

| If the change... | Read |
|---|---|
| writes code at all | `principles/clean-code.md` and `principles/testing.md` |
| creates a file or folder, adds a module, a vendor or a library | `principles/architecture.md` |
| writes something that must not happen twice or get lost, receives outside events, or runs on a schedule | `principles/data-integrity.md` |
| adds or changes an endpoint, login, permissions, personal data, or serves several customers; builds a query or command from input, renders user or model content, fetches a URL, accepts a file | `principles/security.md` |
| changes what users see or read | `principles/interface.md` (and the product's `DESIGN.md`) |
| defines behavior, acceptance criteria or copy | `principles/product.md` |
| affects speed, loading, lists or queries | `principles/performance.md` |
| touches a product whose context lists `offline` | `requirements/offline.md` |
| touches a product whose context lists `ai` | `requirements/ai.md` |

Requirements listed in `context.md` map to these files: `payments` and `background-jobs` to data-integrity; `multi-tenant` to security; `interface`, `i18n` and `native-app` to interface; `offline` and `ai` to `requirements/`.

The front-end or back-end view comes from these routes, not from folders: a screen reads interface, clean-code, performance and testing; an endpoint reads architecture, clean-code, data-integrity and security.

## Scripts and templates

Paths are relative to this skill's folder. Scripts need only Python 3 and print what they did.
- `scripts/init_space.py --root . [--interface] [--install-hook]`: creates the notebook from `templates/`, including the gate `docs/playbook/verify.sh`. It never overwrites the product's files; it refreshes only its own pointer block and the checker copy in `docs/playbook/tools/`. `--install-hook` wires the gate as the git pre-commit hook (it never replaces an existing hook); ask before using it.
- `scripts/upgrade_space.py .`: migrates a notebook from an older skill version: adds missing fields, refreshes the checker copy, records the version.
- `scripts/check_space.py .`: checks the notebook (statuses, blockers, risk answers, locked tests, state). Exit 1 on errors.
- `scripts/lock_tests.py lock|unlock <task> <test paths>`: locks tests written before the code; unlocking needs the approver and a reason.
- `templates/`: context, state, triggers, memory, glossary, project-brief, project-plan, task, decision, review-report, pull-request, PRODUCT, DESIGN, agent-block, verify.sh.

## Any agent

Instructions are written by capability. If your agent can run subagents, use them where a file says so; if not, do the same work in sequence in the main session. If it supports hooks, they may call the same scripts earlier, but the git hook and CI remain the real gate.
