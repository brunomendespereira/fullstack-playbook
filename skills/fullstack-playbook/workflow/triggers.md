# Triggers

"Whenever X happens, do Y" rules, kept in one structured place instead of scattered notes. The moments are fixed here; the actions belong to each product, in `docs/playbook/triggers.md`.

## Moments

| Moment | When it fires |
|---|---|
| Session start | before the first action of a session |
| End of a step | after a step's `verify` passes and before its commit |
| Change visible to users | anything a user sees or can do changed (screen, flow, message, automatic behavior) |
| Change in an AI prompt or model | a prompt, a tool description or a model choice changed |
| Database change | a schema or migration changed |
| Periodic | on a schedule the product defines (weekly review, monthly maintenance) |
| Session end | before handing back to the person |
| Release | before and after code reaches production |

## Running them

1. At each moment, read the product's section for it and run what is there: an instruction is done by the agent; a command is run in the terminal.
2. If an action fails, say so and stop that action. Never swallow the failure, and do not retry more than the product allows.
3. If an action writes to an outside service (mirror tasks to a tracker, send a summary), it follows the "show what changes and where" rule from `SKILL.md` unless the person approved that trigger to run unattended.
4. Monitoring triggers follow the production rules in `principles/security.md`: they observe and report.

## Adding an automation

Before adding one, answer: what fires it, what it does, what happens after, where a person comes back in, and what stops it from running twice. Give it the three brakes: a deterministic check, a cold review, and a human. Turn on one automation at a time and watch it before adding the next.
