# Architecture

How the code is shaped so it stays easy to change. Decide structure before code, discuss it before implementing, and keep it as simple as the problem allows.

## Before deciding

- **Research the industry standard** and the official documentation for the problem, and bring two or three options with pros and cons. Decide with the person.
- **Fill the flow table** of the plan: each call or event, what it is for, when it happens, what the server does. It exposes duplicated requests and missing endpoints before any code exists.
- **Design an important interface more than once** with different constraints (smallest possible, most flexible, best for the common case), compare them by depth and by where the seam falls, then pick one or a hybrid.

Source: Ousterhout, *A Philosophy of Software Design* ("design it twice").

## Modules

- **Deep modules:** a small interface hiding a lot of behavior. The interface includes its invariants, the order of calls, its error modes and its cost, not just its signature. Shallow modules that only pass calls along add complexity without hiding any.
- **The deletion test:** if removing a module would only move its few lines elsewhere, it is not earning its place.
- **A seam (port) needs two real adapters.** One implementation behind an interface is speculation; add the seam when the second one exists or a test needs it.
- **Receive dependencies instead of creating them,** and return results instead of causing side effects deep inside. Both make the module testable through its interface.
- **Rule of three:** extract a shared abstraction when the same intention appears three times. Before that, duplication is cheaper than the wrong abstraction, unless the copies have already diverged by mistake.
- **Prioritize the hot spots:** deepen first the modules that change most often in the git history.

Sources: Ousterhout, *A Philosophy of Software Design*; Fowler, *Refactoring* (rule of three).

## Layers

- **Dependencies point one way.** Features use domain entities, entities use shared building blocks, building blocks use nothing above them. The domain never imports a framework.
- **Enforce the boundary with a tool** (an import rule in the linter or a dependency check in `verify`), not with good intentions. No barrel files that re-export everything: import from the file that owns the code.
- **Business rules are pure functions** with tests, outside the user interface and outside the transport layer. When client and server need the same rule (whether an item belongs to a list, the effect of an action), write it once in a shared module and use it on both sides.
- **Derived values are computed, never stored.** If a state implies a label ("needs your attention"), compute it on read; a stored copy goes stale.
- **Request state never lives in a module-level variable** on the server: it leaks between users. Load static resources once per process; keep logging and analytics off the response path.

Source: Martin, *Clean Architecture* (dependency rule).

## Outside vendors

- **One adapter per vendor** (payments, email, storage, AI providers, maps): it is the only code that knows the vendor, translates to the product's own vocabulary and errors, and makes a second vendor a new file instead of a rewrite. It is a step of its own in the plan.
- **A canonical vocabulary** also applies inside the product wherever several options feed one place (a list of providers, of channels, of formats).
- **An outside reference** (a repository, an example app) becomes knowledge in the notebook, never a dependency of the product.

Source: Evans, *Domain-Driven Design* (anti-corruption layer).

## Choosing a library or tool

The playbook never names one. When the product needs one: search for the most adopted current options for this stack, check recent maintenance and open issues, compare two or three on the product's real constraints, and record the choice and the reason in `docs/playbook/decisions/`. A library that removes code is adopted in its own commit. A library that reshapes state or data flow is adopted only after a small spike proves it fits.

## Decision records

Write one only when the decision is hard to reverse, would surprise someone new, and came from a real trade-off. One to three sentences per section; template `templates/decision.md`. A rejected proposal can be a record too, so it is not proposed again without new facts.

Sources: Nygard, "Documenting Architecture Decisions"; MADR.

## Component interfaces (for products with screens)

- **Explicit variants instead of boolean props:** a set of flags multiplies hidden combinations; a named variant per real case does not.
- **Composed components** (a container with named parts such as header, body and footer) instead of one component with many options.
- **Shared state exposes an interface** of state, actions and metadata, so the parts that read it do not depend on how it is implemented.
- A parent never styles the inside of a child; the child exposes a variant.

## Simplicity and failure

- **No overengineering:** build what the current phase needs, modular enough that the next phase does not require a rewrite.
- **Plan the fallback** for anything that can fail (a device feature, a vendor, the network), and log each failure.
- **Fail open or fail closed is an explicit decision,** written next to the code: for example, a spam filter that is down might let messages through and rely on reports, while an email sender without a provider must refuse so that nothing is lost silently.
