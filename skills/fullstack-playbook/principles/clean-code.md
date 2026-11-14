# Clean code

Rules for any line of code, on any side. Size and complexity limits are product values in `docs/playbook/context.md`; the linter enforces them.

## Shape

- **Small functions with one job.** A long function becomes an orchestrator that reads like a list of steps, plus small helpers. Return early instead of nesting.
- **One responsibility per file,** named with the domain's words (see the glossary).
- **Inner functions only for short callbacks;** anything with its own logic gets a name at module level.
- **A repeated condition becomes a named predicate.**
- **Types and defaults come from one schema** that also validates input, instead of being declared again in each layer.
- **Delete code that is proven unused** (no callers, no references, no dynamic use); version control keeps the history. If removing it reaches far outside the task, list it in the plan first. New code that nothing uses outside its tests does not go in.

Source: Martin, *Clean Code*.

## Errors

- **Never swallow an error.** Every catch either handles the error for real or reports it to the product's error monitoring, besides any local log.
- **A fallback logs the failure** with what was tried, so a silent degradation shows up somewhere.
- **One error shape** across the product: a stable code, a message for people, whether it is transient, and details for logs. The interface chooses its message from the code, never from a vendor's raw text. Bodies that are not in the expected format (a proxy page, an empty response) are handled, not parsed blindly.

Source: RFC 9457 (Problem Details for HTTP APIs).

## Calls to the network and to other services

- **Every outside call has a timeout.** A call without one can hang a request, a job or a screen forever.
- **One client for outside calls** applies the timeout, validates the response, translates failures to the product's error shape, and is the only place that retries.
- **Retry only transient failures** (network error, timeout, 429, 5xx), with exponential backoff and jitter, honoring `Retry-After`, up to the product's limit. A write is retried only with an idempotency key (`principles/data-integrity.md`); never retry a definite refusal.
- **Protect the system from a slow dependency** with circuit breakers (stop calling a failing service for a while) and bulkheads (a failing dependency cannot take every worker).

Sources: Nygard, *Release It!*; RFC 9110 (Retry-After).

## Time

- **Dates in one place:** one module formats and parses them, in the user's time zone.
- **Servers run in UTC.** Scheduled jobs declare their time zone explicitly.
- **APIs accept and return ISO 8601 with an offset.** Tests run in a fixed time zone so they do not depend on the machine.

Source: ISO 8601.

## Observability

- **Structured logs** (one event per line, key-value fields) with a correlation id that follows a request across services.
- **Temporary debug logs** follow `workflow/debugging.md` and never reach the main line.

Sources: W3C Trace Context; OpenTelemetry.

## Imports and fakes

Check what a module really exports before importing from it, and make a fake mirror the real shape. A fake that drifts from the real interface lets tests pass while production fails.
