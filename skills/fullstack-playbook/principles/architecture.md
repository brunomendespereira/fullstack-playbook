# Architecture

How the code is shaped so it stays easy to change. The playbook imposes no structure: it derives one from the product's goals, records it in the notebook, follows it in every new file and checks it in the gate. Keep it as simple as the problem allows.

## From goals to structure

- **Pick at most three quality attributes** whose failure would sink the product (for example speed on a weak network, privacy of personal data, cost per user). Each extra one adds complexity. Aim for the least bad architecture for these, not the best in general.
- **Write each one as a scenario with a measure:** who or what triggers it, in which condition, and the expected response with a number ("on a slow mobile network, today's plan is usable in under 2 seconds"). A wish without a measure cannot guide a decision or be checked.
- **Only requirements that change the structure** deserve an architecture decision; the rest are implementation details.
- **Name the trade-off** the decision accepts ("we chose X over Y because...") in its decision record.

| Attribute | Structural decisions it pulls | Usually conflicts with |
|---|---|---|
| Speed | code split by route or domain, data near where it is used, slow work off the response path, bounded responses | maintainability (copies that go stale) |
| Security | explicit trust boundaries, one authorization point on the server, validation at the edge, least privilege | ease of use (more friction) |
| Ease of use | interfaces shaped by screens (one call per screen), optimistic updates with an error state, drafts that survive failure | security, consistency |
| Maintainability | domain modules, one-way dependencies, one adapter per vendor | speed, flexibility |
| Testability | pure business rules, dependencies passed in, injectable clock and randomness | rarely; it travels with maintainability |
| Offline | local data as the client's source of truth, a queue of changes with idempotency keys, conflict rule decided first | consistency, security |
| Reliability | timeouts, retries with backoff, explicit fail open or fail closed, health checks, reversible deploys | cost, simplicity |
| Cost | one deployable before several, managed services over own infrastructure, caching expensive calls, per-user limits | flexibility |

- **One-way and two-way doors.** A decision that is cheap to reverse is made quickly. A decision that is hard to reverse (data model, trust boundary, sync model, central vendor, code organization) waits for the last responsible moment and goes through "Before deciding".

Sources: ISO/IEC 25010:2023; Bass, Clements and Kazman, *Software Architecture in Practice* (quality attribute scenarios, tactics); Kazman, Klein and Clements, ATAM (SEI, 2000); Richards and Ford, *Fundamentals of Software Architecture*; Poppendieck, *Lean Software Development* (last responsible moment); Bezos, 2015 letter to shareholders (one-way and two-way doors).

## Before deciding

- **Research the industry standard** and the official documentation for the problem, and bring two or three options with pros and cons. Say which one you recommend and why, then decide with the person.
- **Fill the flow table** of the plan: each call or event, what it is for, when it happens, what the server does. It exposes duplicated requests and missing endpoints before any code exists.
- **Design an important interface more than once** with different constraints (smallest possible, most flexible, best for the common case), compare them by depth and by where the seam falls, then pick one or a hybrid.

Source: Ousterhout, *A Philosophy of Software Design* ("design it twice").

## Code organization

Choose by the product's size and phase, recommend one, and record the choice and its reason in `decisions/` and in the "Code structure" section of `context.md`.

| Option | Fits | Stops fitting when |
|---|---|---|
| By technical type (screens, components, services, helpers) | a prototype or a few features | a simple change touches four or five folders; "helpers" becomes a dump |
| Domain on top, technical segments inside each domain | several business areas; the common default from medium size | domains import each other in cycles; "shared" grows faster than the domains |
| Modular monolith: domains with declared interfaces, each owning its data | a grown product without the need to deploy parts separately | a part needs its own scale, failure isolation or team; extract it then, with a measured reason |

- **The top level names the business,** not the framework: a newcomer should see what the product does from the folder names.
- **Group what changes together** and separate what changes for different reasons. Divide by the decision each module hides, not by the steps of a flow.
- **Separate services only with a measured reason** (different scale, failure or security isolation, an autonomous team), recorded in a decision. A local call is far cheaper than a network call.

Sources: Martin, *Clean Architecture* (common closure and common reuse principles) and "Screaming Architecture" (2011); Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (1972); Brown, "package by component"; Bogard, "Vertical Slice Architecture"; Fowler, "PresentationDomainDataLayering" and "MonolithFirst" (2015).

## Where a new file goes

Before creating a file or a folder, read the placement table in the "Code structure" section of `context.md` and follow it. When no row covers the case, ask the person, then add the row.

- **Three destinations:**
  - **A domain:** the piece knows a business entity (its fields, statuses or labels), calls a domain's data or rules, or carries a business word in its name. It stays in its domain even when two screens use it.
  - **Shared building blocks:** the piece carries no business vocabulary and receives content, callbacks and variants. A generic dialog is shared; a dialog that summarizes an order belongs to the orders domain.
  - **Core entities:** pure business rules that several domains use.
- **Decision test:** "if a business rule changes, does this file change?" Yes means a domain or the core.
- **Dependencies point one way:** composition (screens, routes, jobs) uses domains, domains use the core and shared blocks, shared blocks use nothing above them. Shared code never imports a domain. The domain never imports a framework.
- **A domain never reaches into another's internals.** When two domains must work together, the screen or use case above calls both (the default: explicit and easy to debug), or the shared rule moves down to the core. Use an event only when the sender does not care who reacts, and then make the handler idempotent and write the event in the same transaction as the change. Refer to another domain's records by id; never read its tables directly.
- **Public entry point:** a boundary module (a domain) exposes one small, deliberate entry point, and other modules import only from it. Inside a module, import from the file that owns the code. No index file that re-exports everything.

Sources: Evans, *Domain-Driven Design* (bounded contexts, anti-corruption layer); Vernon, "Effective Aggregate Design" (reference by id); Hohpe and Woolf, *Enterprise Integration Patterns* (orchestration and choreography); Richardson, *Microservices Patterns* (transactional outbox).

## Modules

- **Deep modules:** a small interface hiding a lot of behavior. The interface includes its invariants, the order of calls, its error modes and its cost, not just its signature. Shallow modules that only pass calls along add complexity without hiding any.
- **The deletion test:** if removing a module would only move its few lines elsewhere, it is not earning its place.
- **A seam (port) needs two real adapters.** One implementation behind an interface is speculation; add the seam when the second one exists or a test needs it.
- **Receive dependencies instead of creating them,** and return results instead of causing side effects deep inside. Both make the module testable through its interface.
- **Rule of three:** extract a shared abstraction when the same intention appears three times. Before that, duplication is cheaper than the wrong abstraction, unless the copies have already diverged by mistake. Two identical pieces that change for different reasons are not duplication.
- **Undo the wrong abstraction:** when a shared piece keeps gaining parameters and conditions for each caller, inline it back into the callers and extract again from what they really share.
- **Prioritize the hot spots:** deepen first the modules that change most often in the git history.

Sources: Ousterhout, *A Philosophy of Software Design*; Fowler, *Refactoring* (rule of three); Metz, "The Wrong Abstraction" (2016); Hunt and Thomas, *The Pragmatic Programmer* (DRY is about knowledge).

## Layers

- **Enforce the boundaries with a tool** (an import rule in the linter or a dependency check in `verify`), not with good intentions.
- **Business rules are pure functions** with tests, outside the user interface and outside the transport layer. When client and server need the same rule (whether an item belongs to a list, the effect of an action), write it once in a shared module and use it on both sides. Rules that depend on secrets, prices or permissions run only on the server, which sends the decision ready ("can edit: yes").
- **Derived values are computed, never stored.** If a state implies a label ("needs your attention"), compute it on read; a stored copy goes stale.
- **Request state never lives in a module-level variable** on the server: it leaks between users. Load static resources once per process; keep logging and analytics off the response path.

Source: Martin, *Clean Architecture* (dependency rule).

## Keep and evolve

- **Find the real structure, not the declared one.** Folders show intent; the import graph shows the truth. For each kind of thing (screen, route, business rule, adapter, component, script), list the places where it lives today; more than one place is a finding, with files and counts. Add the hot spots (size times change frequency in the git history) and the files that always change together in the same commit.
- **One fitness function per priority attribute,** run by `verify`: the dependency rule, no import cycles, a size budget per route, a response-time limit, every route requiring authorization. An attribute that no check watches is only a wish. Keep them few and meaningful: too many checks freeze the code.
- **Baseline for an existing mess:** list the violations that exist today and fail the gate only on new ones. The list only shrinks.
- **Migrate without stopping the product.** Grow the new shape around the old one and move one domain at a time (strangler fig); for an interface, add the new form beside the old, move the callers, then remove the old (expand, migrate, contract). Write characterization tests before moving code that has none.
- **Local cleanups when touched; pattern changes in an approved batch** with a scope, an order and an end. Pattern changes started one file at a time and never finished leave layer on layer of half-done patterns. One module, one pattern; a temporary mix is written in the plan with its end.
- **Do not migrate** stable code outside the hot spots, code about to be deleted, or code whose migration costs more than the friction it causes. Record a "do not migrate" decision so it is not proposed again without new facts.

Sources: Tornhill, *Your Code as a Crime Scene* (hot spots, change coupling); Ford, Parsons and Kua, *Building Evolutionary Architectures* (fitness functions); Fowler, "StranglerFigApplication" and Sato, "ParallelChange" (martinfowler.com); Feathers, *Working Effectively with Legacy Code* (characterization tests); Hadlow, "The Lava Layer Anti-Pattern" (2014).

## Outside vendors

- **One adapter per vendor** (payments, email, storage, AI providers, maps): it is the only code that knows the vendor, translates to the product's own vocabulary and errors, and makes a second vendor a new file instead of a rewrite. It is a step of its own in the plan.
- **A canonical vocabulary** also applies inside the product wherever several options feed one place (a list of providers, of channels, of formats).
- **An outside reference** (a repository, an example app) becomes knowledge in the notebook, never a dependency of the product.

Source: Evans, *Domain-Driven Design* (anti-corruption layer).

## Choosing a library or tool

The playbook never names one. When the product needs one: search for the most adopted current options for this stack, check recent maintenance and open issues, compare two or three on the product's real constraints, and record the choice and the reason in `docs/playbook/decisions/`. A library that removes code is adopted in its own commit. A library that reshapes state or data flow is adopted only after a small spike proves it fits.

## Decision records

Write one only when the decision is hard to reverse, would surprise someone new, and came from a real trade-off. One to three sentences per section; template `templates/decision.md`. A rejected proposal can be a record too, so it is not proposed again without new facts. The code organization always gets one: `context.md` points to it in the `code_structure` field.

Sources: Nygard, "Documenting Architecture Decisions"; MADR.

## Component interfaces (for products with screens)

- **Explicit variants instead of boolean props:** a set of flags multiplies hidden combinations; a named variant per real case does not.
- **Composed components** (a container with named parts such as header, body and footer) instead of one component with many options.
- **Shared state exposes an interface** of state, actions and metadata, so the parts that read it do not depend on how it is implemented.
- A parent never styles the inside of a child; the child exposes a variant.

## Simplicity and failure

- **No overengineering:** build what the current phase needs, modular enough that the next phase does not require a rewrite. Full layered rings (ports, use cases, mappers) only for a rich, long-lived business core.
- **Plan the fallback** for anything that can fail (a device feature, a vendor, the network), and log each failure.
- **Fail open or fail closed is an explicit decision,** written next to the code: for example, a spam filter that is down might let messages through and rely on reports, while an email sender without a provider must refuse so that nothing is lost silently.
