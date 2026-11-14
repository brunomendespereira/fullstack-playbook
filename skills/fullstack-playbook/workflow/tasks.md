# Projects and tasks

The notebook keeps the work, so any agent or person can pick it up without memory or an outside tool. Outside tools (issue trackers, docs) may mirror it through a trigger; the files in the repository are the source of truth.

## Model

- **Product:** the whole repository.
- **Project:** a front of work with a goal, a start and an end (for example "coupons", "offline mode"). Folder `docs/playbook/projects/YYYY-MM-name/` with `brief.md` (its `status`: active, paused, done or dropped), `plan.md` and `tasks/`. Small bugs and adjustments live in the standing project `projects/maintenance/`.
- **Task:** one step inside a project. One file per task, `tasks/NNN-short-name.md`, from `templates/task.md`.

## Tasks

- **Vertical slice:** each task delivers something a person can see or check, and fits in one context window. A preparatory refactor goes first, as its own task.
- **Fields:** `status` (todo, in-progress, blocked, review, done, dropped), `blocked_by` (task numbers only; a blocker outside the notebook, such as an answer, an access or a failing check, goes in the task's Notes and under "Waiting on" in `state.md`), `owner` (who is working on it; set it before starting so two sessions do not take the same task), `risks` (the six answers, required before starting), `locked_tests`. Field names and values stay in English whatever the product's language, so `scripts/check_space.py` can read them.
- **Each task has its test** defined before it starts, and "done when" lines a person can verify.
- **Refer to a task by its name**, not only by its number.
- **A checked box is not a manual check.** Before calling something finished, open it and confirm.
- **Done** means what `context.md` says (for example "in production"); otherwise done means merged.

## State and resuming

- `docs/playbook/state.md` holds the present: active project and task, next action, resume phrase, open fronts, what is waiting on whom. Replace it at the end of every session; do not append history to it.
- **Save progress during the session,** not only at the end: update the task file after each step.
- **Resume:** read `state.md`, then the active task, then `git status` and the last commits, then the latest plan. After a collision (another session worked here), read branch, status and log again before acting.
- **Handoff** (another session or person continues): point to the files, state the next action, remove secrets.

## Limits and priority

- **Limit open fronts** to the number in `context.md` (one or two per person is the usual Kanban limit). Finish or pause one before starting another; `scripts/check_space.py` warns when the limit is passed.
- **Appetite and circuit breaker** (Shape Up): when a project's appetite runs out, stop and decide again; never extend silently.
- **One goal per project,** specific and measurable, with its baseline.
- **Priority:** security, privacy and money problems come first. For the rest, any simple score works (impact, confidence, ease); write the reason in the brief.

## Triage

A new request or finding gets a category (bug, feature, question, chore) and a state. Before creating it, check whether it already exists and whether it was already refused. Keep refused ideas with a lasting reason in `archive/refused.md` (create it the first time), so they are not proposed again without new facts.

## Where files go

Every file the work produces has one home. Save it there the moment it exists, so the next session, another agent or a person finds it without asking.

| What | Where | In git |
|---|---|---|
| Research that supports a project's decisions: summaries, comparisons, maps, concept pages and the small images they need | `docs/playbook/projects/<project>/research/` | yes |
| Research about the whole product, not one project | `docs/playbook/research/` | yes |
| Review reports and QA results of a project | `docs/playbook/projects/<project>/reviews/` | yes |
| Full audits of the whole product | `docs/playbook/reviews/` | yes |
| Permanent QA scenario scripts, and test data that is public by design (a provider's sandbox card) | `docs/playbook/qa/` | yes |
| Raw dumps, large files, material from other products or people, anything with personal data, drafts not yet approved | `.playbook/<project>/` | no |
| Scripts the product uses (queries, one-off tools) | the product's own code (for example `scripts/`) | yes |

- **Each research file starts with its date, the question it answers and its sources.** A researcher returns a summary; the main session saves it here.
- **Use and delete outside material:** what was learned moves into a versioned file; the source in `.playbook/` goes when its task closes.
- **Agent folders hold only agent configuration** (`.claude/`, `.agents/` and similar: settings and skills). No research, notes, task lists or product scripts there.
- **Outside tools point here** (issue tracker, docs tool): link the path instead of copying the content, so the repository stays the source.
- **Never a secret in any of these files.** Real credentials live in the environment, not in the notebook.

## Memory, archive and cleanup

- `memory.md`: one dated entry per lesson, newest first, with the commit. Review it now and then; delete what stopped being true.
- **A lesson that may be universal:** when writing it, ask the three questions of the playbook's contribution filter: does it have a public source or industry consensus, does it make sense in a very different product, is it free of this product's values? If all three are yes, end the entry with `Playbook candidate: <file in the skill>` (for example `requirements/ai.md`). Prefer an existing file; a new `requirements/` file only for a product trait that changes the architecture and many products lack.
- **At session end, list the candidates** and ask the person: keep it only here, or take it to the playbook? The installed copy of the skill is never edited. Whoever maintains the skill changes it in its own repository, with a test, and reinstalls it. Anyone else gets the suggestion written (rule, why, source, target file) and, only with an ok, it is opened as an issue or pull request at the repository in the skill's `metadata`.
- **Archive, never delete:** a finished or dropped project moves to `archive/`. Something absorbed into another file keeps a pointer to where it went.
- **Periodic cleanup** (suggest it at session end when it applies): drafts in `.playbook/` older than the project, merged or dead branches, unused worktrees, stopped containers from tests. List them and ask before removing.

Sources: Kanban Guide (limits on work in progress); Basecamp, *Shape Up* (appetite, circuit breaker).
