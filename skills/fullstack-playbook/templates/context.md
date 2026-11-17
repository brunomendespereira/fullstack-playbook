---
language:
requirements: []
sensitive_areas: []
open_fronts_limit:
code_structure:
playbook_version:
---
# Context

What an agent needs to know about this product. Changes rarely. Written by onboarding, edited by people. Write the content in the product's language (the `language` field); keep the field names as they are.

## The product
One paragraph: what it does, for whom. The longer version lives in `PRODUCT.md`.

## Requirements
Which of these apply (also listed in the `requirements` field above): interface, offline, ai, payments, multi-tenant, background-jobs, i18n, native-app. Each one turns on principles in the playbook.

## Stack and tools
Languages, frameworks, database, hosting. Each tool chosen after research is recorded in `decisions/`.

## Code structure
Read before creating any file or folder (`principles/architecture.md`, "Where a new file goes"). The `code_structure` field above points to the decision record that explains the choice.
- **Priority attributes:** at most three, each a scenario with a measure.
- **Organization:** the option chosen and why, in one or two lines.
- **Map:** the main modules and what each one hides; "where is the thing that does X?".
- **Placement:** one row per kind of thing: kind, folder, one-line decision test (for example "knows a business entity? its domain folder; only receives content? shared").
- **Allowed directions:** who may import whom, and the check in `verify` that enforces it.
- **Open exceptions:** known violations (the baseline) and migrations in progress, each with its task.

## Commands
How to run, test, lint and build. Say where commands run (host or container).

## Git
Branch model, where work starts, what deploys, when to merge, commit style.

## Environments and access
Environments, how to reach production (read-only by default), where errors are monitored.

## Values
Numbers and preferences this product chose: file and function size limits, timeouts, retry counts, cache lifetimes, status that means "done", autonomy level (stop at every step, or run a tested plan and report at the end).

## Sensitive areas
Code where a mistake costs money, data or trust (also in the `sensitive_areas` field). Touching them makes every risk question mandatory.

## Product rules
Rules that are true only for this product and win over the playbook's general principles. Say why.
