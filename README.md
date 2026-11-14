# fullstack-playbook

**An Agent Skill that runs your product like a software company, from idea to release, with any coding agent.** One skill for vibe coding and agentic engineering: brief, design, architecture, plan, tests first, build, review, QA and release, with universal engineering principles and the project's tasks kept inside the repository. Works with Claude Code and other agents that read the [Agent Skills](https://agentskills.io) standard.

[Português](README.pt-BR.md) · [License: MIT](LICENSE) · [Credits](CREDITS.md)

⭐ **If it helps your product, star the repository.** Stars are how this project finds new users and contributors, and they keep it maintained.

## Why

Coding agents write code fast and forget the rules just as fast. The usual fix is to install a skill for each concern (workflow, testing, design, React performance, composition, security), and soon they overlap, contradict each other and fill the context before the work starts. The product's own rules end up scattered across instruction files, agent memory and old task lists.

fullstack-playbook replaces that pile with one skill that:

- **loads on demand:** each request (feature, bug, small change, review, release, new product) reads only the few files of its route, so one skill costs less context than a pile of specialized ones (numbers below);
- **asks before it acts:** a short plan and an explicit ok at the approval points, one question at a time;
- **writes tests first** against a real test database, locks them while the code is written, and never loosens a failing test;
- **answers six risk questions** for every change (duplicates, outside events, endpoints, other users' data, login and personal data, sensitive areas), and each "yes" turns on the matching principles and required tests;
- **reviews with fresh eyes:** ready briefs for spec, standards, security, interface and final review, run as subagents or inline, on a diff or as a full audit of the codebase;
- **learns upstream:** a lesson that passes the contribution filter is marked in the product's memory and, with your ok, proposed back to this repository as an issue or pull request;
- **keeps projects and tasks in the repository,** with a state file and a resume phrase, so any session or agent can continue the work;
- **turns rules into checks:** a `verify.sh` gate for every commit and a notebook checker.

It names no framework, library or vendor. The principles hold for a React app, a Python API or a mobile game; tools are chosen per product, after research, and recorded as decisions.

## Loads on demand, one skill instead of many

Agent Skills load in three steps: the short description is always in context, the body loads when the skill is used, and reference files load only when a step needs them. fullstack-playbook is built around that:

- **Always in context:** one description of about 220 tokens.
- **When a request arrives:** the router (`SKILL.md`, about 2,000 tokens) sends it to the few files of its route. A typical feature reads about 6,700 tokens in all; a small text change reads the router and one template.
- **Never loaded for nothing:** offline and AI rules stay out unless the product needs them, and security, data integrity or interface rules load only when the change touches them.

Compare with keeping one skill per concern. In the product where this skill was born, seven skills covered workflow, front-end quality, design, React performance, component composition and module design. Their descriptions took about 600 tokens of context on every request, and a front-end change that triggered them together loaded about 15,600 tokens of skill bodies before reading a single reference file, with rules that overlapped and sometimes contradicted each other. Pages, security, data, testing, review and release now live in one skill with one set of rules, and each request pays only for what it uses.

## How it works

Two parts:

- **The skill is the manual.** The same for every product.
- **Each product keeps a notebook** that the skill creates on first use and updates as you work:

```
your-product/
├── PRODUCT.md                 what it is, for whom, voice and tone
├── DESIGN.md                  tokens and design rules (products with screens)
├── AGENTS.md / CLAUDE.md      a short pointer block to the notebook
└── docs/playbook/
    ├── context.md             stack, commands, git, environments, values, product rules
    ├── state.md               what is happening now and the resume phrase
    ├── triggers.md            what this product does at each moment (end of step, release...)
    ├── memory.md              lessons and gotchas, dated
    ├── glossary.md            the domain's words
    ├── decisions/             decision records
    ├── projects/<project>/    brief, plan and one file per task
    ├── verify.sh              the gate run before every commit and in CI
    └── tools/                 the notebook checker (managed by the skill)
```

The manual says what is right; the notebook says how it applies here. When they disagree, the product's rule in `context.md` wins.

## Install

Install it per product, inside the repository.

**With the skills CLI:**

```bash
npx skills add brunomendespereira/fullstack-playbook
```

**By hand:** copy `skills/fullstack-playbook/` into your repository:

- Claude Code: `.claude/skills/fullstack-playbook/`
- Most other agents that read Agent Skills: `.agents/skills/fullstack-playbook/` (check where your agent looks for skills)

The scripts need only Python 3 and a POSIX shell.

## First use

Open your agent in the repository and ask for anything, or say "Let's use the playbook here".

- **Existing product:** it explores the code first, asks only what the code does not answer, one question at a time with a suggested answer, shows the notebook as a draft, and writes it after your ok. It also reports what diverges from the playbook (no tests, no CI, rules in conflict) as tasks.
- **New product:** in an empty repository, say what you want to build ("a booking app for barbershops"). It asks about requirements, researches the stack and records the choice, and writes `PRODUCT.md` and `DESIGN.md` before any code.

## What is inside

| Folder | What it holds |
|---|---|
| `SKILL.md` | The router: rules that always apply, the start of every request, routes by request and by area |
| `workflow/` | Stages, onboarding, tasks and state, triggers, debugging, review, reviewers, release |
| `principles/` | Product, architecture, clean code, data integrity, security, performance, interface, testing |
| `requirements/` | Read only when the product needs them: offline-first and AI features |
| `templates/` | The notebook files, task, plan, brief, decision record, review report, pull request, `verify.sh` |
| `scripts/` | `init_space.py` (create the notebook), `check_space.py` (check it), `lock_tests.py` (lock tests written first) |

Every rule cites a public source or is industry consensus: OWASP ASVS and API Security Top 10, WCAG 2.2, Core Web Vitals, *Designing Data-Intensive Applications*, *Release It!*, *A Philosophy of Software Design*, *Refactoring*, Nielsen Norman Group, RFC 9457 and RFC 9110, Conventional Commits, SemVer and others, listed at the end of each file.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). In short: a rule needs a public source, must make sense in a very different product, names no library or vendor, and holds no taste values. Run the tests before opening a pull request:

```bash
python3 -m unittest discover tests
```

## Support

Star the repository, open an issue with a lesson your product taught you, or send a pull request (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Credits and license

MIT. Parts are adapted from open projects credited in [CREDITS.md](CREDITS.md).
