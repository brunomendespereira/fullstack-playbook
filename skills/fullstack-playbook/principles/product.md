# Product

What to build and how it should behave, written so that the person who builds it never has to guess.

## The spec

A brief or spec holds: the problem, the solution from the user's point of view, behavior as given/when/then criteria (or user stories with acceptance criteria), the implementation and testing decisions already taken, and what is out of scope. It never names files or functions: those change, the behavior does not. It is ready when the person implementing it would not need to ask anything.

Behavior statements are confirmed by the product owner before tests are written from them. The owner is the source of truth on expected behavior; when a statement looks wrong, ask.

## Real flows first

Discuss the change through real user journeys before screens: first use, returning user, leaving in the middle and coming back, no connection, a slow server, a second device. Each journey becomes criteria.

## Content ranges and anti-goals

For every screen or message, write the shortest, the typical and the longest real content it must handle (names, numbers, lists, languages). Write anti-goals too: what the change must not do, and what must stay untouched.

## Glossary

Keep the domain's words in `docs/playbook/glossary.md`, with the synonyms to avoid. Code, docs and conversation use the same term. Update it the moment a term is decided.

Source: Evans, *Domain-Driven Design* (ubiquitous language).

## Interface copy

Copy is its own pass, after the structure is right.
- Messages in order: the fact, the action, the context, then tone.
- A button says a verb and an object ("Save draft", not "OK").
- A destructive action names the object and the consequence; offering undo is better than asking for confirmation.
- A placeholder is not a label.
- An error says what failed, why, and how to get out of it, with no internal codes.
- Teach at the point of use. A tip the user dismissed does not come back.
- Measure time to first value: how long until a new user gets the thing they came for.

Source: Nielsen Norman Group, usability heuristics and error-message guidelines.

## Deleting data that others depend on

When deleting an account or a record would cascade into other people's data (comments, shared groups, history), the default is to anonymize instead of deleting, and the option shown to the user names the consequence.

## Metrics without new screens

When a project needs a metric, the default is recording it where it can be queried (an event or a table), not building a dashboard screen. A screen is a separate, explicit decision.
