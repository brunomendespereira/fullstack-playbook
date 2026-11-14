# Stages

How work moves from a request to production, the way a software company does it, sized for one person working with agents. The bottleneck is the person's attention, so every stage produces one short artifact and asks for approval only where it matters.

## Size decides the stages

| Stage | Small adjustment | Bug | Feature | New product |
|---|---|---|---|---|
| 1. Brief | no | no (the report is the brief) | 1 page | full |
| 2. Flow and mock | no | no | if a screen changes | yes |
| 3. Architecture | no | no | if a decision is hard to reverse | yes |
| 4. Plan (tasks with risks) | 1 line | 1 task | yes | yes, per phase |
| 5. Tests first, locked | if behavior changes | reproduction test | by a separate tester | by a separate tester |
| 6. Build | yes | yes | yes | yes |
| 7. Gate (`verify`) | yes | yes | yes | yes |
| 8. Review | correctness | correctness | full | full |
| 9. QA | if visible | if visible | yes | yes |
| 10. Release and close | yes | yes | yes | yes |
| Approvals | merge | plan and merge | brief, screen, plan, merge | every stage |

A critical bug (money, security, user data) follows the bug column plus a separate tester and the full review.

**Small path:** a text, color or config change with every risk answer "no" follows the small path in `SKILL.md`. If any answer is "yes", it is not small.

## The stages

1. **Brief.** Problem, outcome with a baseline, appetite, scope and out of scope, acceptance criteria (given, when, then), content ranges. Template: `templates/project-brief.md`. Rules for writing it: `principles/product.md`. Done when the owner confirms the criteria.
2. **Flow and mock.** Real user flows first (online and offline, leaving and coming back, first use). Then a mock built with the product's design system, shown to the person as a visual before approval. The mock is the specification: each correction made on it becomes an acceptance criterion. Text content is approved before code. Architecture waits for the wireframe, not for the final mock.
3. **Architecture.** Follow "Before deciding" in `principles/architecture.md`: research, two or three options, the flow table, decision records. Run the threat checklist when `principles/security.md` asks for it. For an outside integration, confirm endpoints, permissions and limits in its current documentation.
4. **Plan.** Vertical slices, each a task file with its own test and its risk answers (`workflow/tasks.md`). Say explicitly whether the plan creates a table, a migration, an endpoint or a screen, and what it costs. Plan phase by phase: detail only the phase you are about to build. Order that avoids rework: data infrastructure, then screen by screen, then optimization. Clarifying questions do not replace the plan: the plan is still shown and approved.
5. **Tests first.** Acceptance tests come from the criteria and are written before the code, then locked with `scripts/lock_tests.py`. For features, new products and critical bugs, a separate tester writes them per slice (see Roles). For a bug, the reproduction test. Details: `principles/testing.md`.
6. **Build.** One writer. Smallest change that solves it; look for what already exists and reuse it, or say why not. Test-driven, commit per step. Run the type check and the current test often; the full suite once at the end of the step.
7. **Gate.** `docs/playbook/verify.sh` passes (lint, types, tests, design tokens, notebook check). Red gate, no commit.
8. **Review.** By someone who did not write the code (`workflow/review.md`).
9. **QA.** The fixed scenario script for this kind of change, checked in a real browser or device at phone and desktop size, with evidence (screenshots, logs).
10. **Release and close.** Merge only with an ok (`workflow/release.md`). Update the task, the state and the resume phrase.

## Risk questions

Every task that changes code or data answers these with yes or no before it starts (`risks` field of the task; `scripts/check_space.py` refuses a started task with an empty answer). Ask about what the change does, not about its subject: a coupon, a seat, an invite and a payment all "write something that must not happen twice".

| Question | If yes, read | And add these tests |
|---|---|---|
| Does it write something that must not happen twice or get lost? | `principles/data-integrity.md` | same request twice in a row and twice at the same time; only one takes effect |
| Does it receive events from outside (webhook, queue, another system)? | `principles/data-integrity.md` | duplicate event, out-of-order event, event that fails and is retried |
| Does it add or change an endpoint or a public interface? | `principles/security.md` | wrong user, wrong role, invalid input |
| Can one user reach another user's data through it? | `principles/security.md` | user A reading and changing user B's data |
| Does it touch login, permissions or personal data? | `principles/security.md` | threat checklist from that file; attempt limits; secrets never logged |
| Does it touch a sensitive area listed in `context.md`? | all of the above | all of the above, even for a small bug |

## Roles

Evidence from multi-agent studies: a second agent pays off when it brings new information (tests actually executed, or eyes without the writer's reasoning); it is wasted when it is the same model giving opinions, or when several agents write the same code.

- **Researchers (2 or 3 in parallel), before architecture.** Read only; return a short summary or a file path, not the whole investigation. The main session saves the summary in the project's `research/` (`workflow/tasks.md`, "Where files go").
- **Tester, before building (features, new products, critical bugs).** Gets only the acceptance criteria, writes the tests slice by slice, and the tests are locked. Agents left alone with failing tests tend to change the test instead of the code.
- **One writer.** Parallel writers make conflicting decisions. Truly independent fronts get one worktree each.
- **Reviewers, read-only, at the end of a step.** Fresh context, closed scope, and only when the diff touched their area. Briefs in `workflow/reviewers.md`.
- **Not worth it:** an architect that debates the writer, company roles talking to each other, open-ended review loops.
- Give a subagent only the context it needs and pick the model for the job. Expected cost: three to five times a single session.
- Sources: Anthropic, "How we built our multi-agent research system" and "Building effective agents"; Panickssery et al. 2024 (self-preference, arXiv 2404.13076); Huang et al. 2024 (self-correction, arXiv 2310.01798); ImpossibleBench (arXiv 2510.20270); AgentCoder (arXiv 2312.13010); MAST (arXiv 2503.13657); Cognition, "Don't build multi-agents".

## While working

- **Check the real state before claiming a limit.** Say "I could not find it" instead of "it does not exist".
- **When fixing a symptom, name the invariant that broke** before adding another branch.
- **Read the commit history** of old code before changing it: it may exist because of a bug already fixed.
- **A finding outside the task becomes a task right away**, in the project in front, never a loose note.
- **Big change or change in a shared module: stop and talk** before doing it.
- **An outside prerequisite pending** (credential, approval, account): mark the task blocked and move to another front. Do not build on top of it.
- **An approved solution failed:** say whether your change caused it, give options with a recommendation, and wait for the ok before trying another.
- **An option that works:** keep it and compare alternatives afterwards, instead of stalling.
- **At an approval point,** hand over a decision-ready brief: what was done, what is being asked, the options with a recommendation.
- **A decision that depends on someone absent:** write the questions down for them and continue with the rest, instead of stopping.
- **Change context only at a phase boundary.** Prefer, in order: continue, clean, hand off with a written summary, delegate to a subagent, compact.
- **Measure what the plan promised.** Baseline before, the same measure after (requests per screen, time to open, the outcome metric).

## Prototype and foggy work

- **Prototype** when one question blocks the decision. Throwaway, the question written at the top, structurally different variants, kept on a branch outside the main line; the decision goes to real code, the prototype stays behind.
- **Foggy work** (the destination is clear, the path is not): write a map with the destination, the decisions to take, the fog, and what is out of scope. Take one decision per session and update the map.
- **Spec readiness:** a brief or spec is ready when the person implementing it would not need to ask anything. It synthesizes what was decided; it is not a new interview.

Sources: Google design docs; Shopify GSD; Basecamp Shape Up.
