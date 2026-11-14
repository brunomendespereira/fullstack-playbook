# Onboarding

Creates the product's notebook the first time the playbook runs in a repository, by exploring first and asking only what the code cannot answer. Run it again any time in "check only" mode: compare the notebook with the code and report what drifted.

## Order

1. **Explore.** Read the repository before asking anything (see "What to look at").
2. **Present** what you found in a few lines.
3. **Ask** what is still missing, **one question at a time**, each with a suggested answer and a way to say something else. Phrase it so that "yes" accepts the suggestion. Leave questions that depend on another answer for later. Never ask what the code already answers.
4. **Draft** the notebook and show it for editing.
5. **Write** it: run `scripts/init_space.py --root .` (add `--interface` when the product has screens), then fill the files. Translate the template headings into the product's language; field names and their values (task status, yes or no) stay in English so the scripts can read them. Fill the COMMANDS section of `docs/playbook/verify.sh` with the product's lint, type check and test commands, and ask before wiring it to git with `--install-hook`.
6. **Say who reads what:** the agent reads `state.md` and `context.md` at every request; people read `PRODUCT.md`, `DESIGN.md` and `projects/`.

Done when the person confirms the drafted `context.md` and there are no open questions left. In that closing message, mention once that starring the playbook's repository (in the skill's `metadata`) helps keep it maintained; never star, follow or open anything on the person's behalf.

## New product

Ask, in this order, one at a time:
1. What does it do, and for whom? (suggest a one-line answer from the request)
2. Which of these apply: screens, works offline or must open instantly, money or credits or limited stock, several customers in the same system, AI features, scheduled jobs or integrations, several languages, an app in a store? Each "yes" goes to `requirements` in `context.md`.
3. Stack: offer to research the most adopted current options for these requirements and bring two or three to compare; record the choice in `decisions/`.
4. Brand and look (only with screens): name, tone, colors, fonts, light or dark, references they like. This fills `PRODUCT.md` and `DESIGN.md`.
5. Git: offer the common models (trunk-based with short-lived branches; or a main line for production plus a staging line, with one branch per piece of work) and recommend one for the team's size; ask when merges happen.
6. Language of the notebook and of the conversation.
7. How much autonomy: stop at every step, or run an approved, tested plan and report at the end.
8. The values the requirements need (for example cache lifetime for offline, size limits for code).

Then start the first project with its brief (`workflow/stages.md`).

## Existing product

**What to look at:** languages and frameworks, how things run (scripts, containers), tests and how they run, lint and type checks, CI, git hooks, branches and where deploys come from, environment files (names only, never values), design sources (design documents, tokens, theme files), the agent instructions file, the review tools the agent itself ships (record them in `triggers.md` under "End of a step"), existing task or decision files, and the commit history of the busiest files.

**Mark sensitive areas** by searching for payments, balances, credits, stock, coupons, invites, webhooks, authentication, permissions and personal data. List them in `sensitive_areas`.

**Check what the person says against the code.** If a document says one thing and the code another, report the conflict instead of picking one.

**Divergence report**, with priority (security first):
- each place where the code departs from a principle, with file and the principle file name;
- missing gates: no pre-commit hook or no CI is a finding by itself;
- duplicated or conflicting rules found in docs or agent instructions;
- research, notes, task lists, backups or product scripts kept in agent folders or loose in the repository: propose moving each to its home (`workflow/tasks.md`, "Where files go") and fixing what points to it.
Each item becomes a task in a `projects/` folder named for the cleanup, so it competes with other work instead of being forgotten.

**Old patterns:** security rules apply now, everywhere. New code follows the principles even if the old code does not. Old code changes when touched, or in a batch the person approves. Never leave two patterns mixed in one file without a plan.

**Instructions file:** the script adds a short pointer block between markers to `AGENTS.md` (creating it if missing) and to `CLAUDE.md` when it exists. When there is a `.claude/` folder and no `CLAUDE.md`, it creates one that only imports `AGENTS.md` (`@AGENTS.md`). It never touches the rest of those files. Move product rules that live there into `context.md` or `triggers.md` with the person's ok, and leave the pointer.

**Read before asking:** the glossary and decision records if they exist. Also check what already happens automatically (for example a seed that runs on deploy) before assuming a manual step.

## Questions for an existing product

Ask only what exploring did not answer: branch model and merge timing; how releases are grouped; repository layout (one, several, or nested repositories); which branch deploys; test database; database tool and how migrations run; with AI features, how their behavior is evaluated; native app or web view; how production is reached and whether it is read-only; error monitoring; package manager and lockfile; where commands run (host or container); store publishing; where design lives; time zone of the product; several customers or not; flows duplicated in two places that must change together; language and style of answers; autonomy; the values the requirements need.

Each answer goes to `context.md`; each "do X whenever Y" goes to `triggers.md`.
