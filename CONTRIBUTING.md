# Contributing

The skill is read by coding agents, so every line costs context and every vague line costs quality. These rules keep it small, universal and true.

## What a rule must pass

1. **It has a public source or is industry consensus.** Cite the source on a line that starts with `Source:`.
2. **It makes sense in a very different product.** Try it against a Python API with no screen and a mobile game. If it only fits one product, it belongs in that product's `docs/playbook/`, not here.
3. **It names no library, framework or vendor.** Write the principle ("persist server data on the device with a version and a maximum age"). The tool is chosen when the rule is applied: research the most adopted current option for the project's stack, check recent maintenance, compare two or three, and record the choice as a project decision.
4. **It holds no taste values.** Cache lifetimes, size limits, timeouts and retry counts are project values and live in `docs/playbook/context.md`. Only published norms stay in the skill, with their source (for example WCAG contrast 4.5:1).

## How a rule is written

- What to do, why, and the source. Positive instructions.
- Each step says how to know it is done.
- One source of truth: a rule lives in one file; other files point to it by name.
- The same guide words every time: manual, notebook, route, risk questions, verify, product, project, task.
- English, plain words, short sentences.
- When a stage or a file changes, update the routes in `SKILL.md` in the same change.

## Size and structure

- `SKILL.md` stays under 500 lines and routes to every reference file directly (one level deep).
- A reference file stays small enough to read whole (the content test enforces a limit).
- Only the open Agent Skills frontmatter fields (`name`, `description`, `license`, `compatibility`, `metadata`). Agent-specific features are described by capability, never required.

## Lessons from products

Products that use the skill mark universal lessons as `Playbook candidate` in their `docs/playbook/memory.md`. A suggestion that comes from there arrives as an issue or pull request with the rule, why, the source and the target file; it goes through the same four checks above. Values the product chose stay in its `context.md`.

## Before opening a pull request

```
python3 -m unittest discover tests
```
