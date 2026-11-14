# Testing

Tests prove behavior with the real parts of the product, and nothing internal is faked. One standard for the whole product.

## The standard

- **Code that touches the database is tested through its entry point** (the route, the job, the message handler) against a real test database. Pure functions are called directly. **Only outside services are faked** (payment providers, email, messaging, AI providers, file storage, error monitoring). Never fake the database or the rule under test.
- **Test-driven:** write the test, see it fail for the right reason, make it pass, refactor. Confirm a regression test fails without the fix.
- **Agree on the seams first:** before the first test, list where tests will plug in, each with one line on what it catches and what it does not.
- **Verify through the public interface,** not through a side channel: read back with the module's own read function, not with a direct query that the code never makes.
- **No tautological tests:** the expected value comes from an independent source (a known literal, a worked example, the spec), never recalculated the way the code calculates it.
- **Vertical slices:** one test, the smallest implementation, repeat. Writing every test up front freezes the structure early and tests imagined behavior.
- **Design outside boundaries for simple fakes:** inject dependencies, one function per outside operation.
- **One level per behavior:** do not prove the same thing in a unit, an integration and an end-to-end test. Share fixtures and helpers.

Sources: Beck, *Test-Driven Development*; Fowler, "The Practical Test Pyramid"; Kent C. Dodds, "The Testing Trophy".

## Cases every risky route has

- **Repetition:** the same request twice in a row and twice at the same time; only one takes effect.
- **Access:** user A reading and changing user B's data; the wrong role.
- **Outside events:** duplicate, out of order, failed and retried.

## Locked tests and the tester

- **Tests written before the code are locked** (`scripts/lock_tests.py`) while the code is written; `verify` fails if they change. Unlocking needs the owner's ok and a reason, recorded in the task.
- **A separate tester** writes them from the acceptance criteria, slice by slice, for features, new products and critical bugs. For a common bug, the writer writes the reproduction, shows it failing and locks it before fixing.
- **Behavior statements are confirmed by the owner** before tests are written from them.

## When a test fails

- **A test failing because of a real bug stays failing** and goes on the bug list. Never delete, skip or loosen a test to make it pass. If a test looks wrong, stop and ask.
- **A failure that was already there gets fixed too,** or becomes a task; it is not "someone else's".
- **Where a regression test goes:** see `workflow/debugging.md`.

## Environment

- **A separate test database** that the setup refuses to use unless it is clearly local and clearly for tests; cleaned between test files.
- **The app is importable without starting a server;** scheduled jobs and outside connections do not start in tests.
- **No real time:** a slow dependency is a latch the test releases, not a sleep. A test that needs a long timeout needs a reason.
- **No real outside calls in automated tests:** use recorded responses that include real errors. A fake server follows the real contract (same rules, idempotency, conflicts, configurable latency). The real integration is validated by hand with a test account before release.
- **Tests run in a fixed time zone.**
- **One command runs the whole suite;** run it once per step, not in a loop.

Source: Pact (contract testing).

## Over time

- **Conventions become tests** (one definition per cache key, overlays lock scrolling, every route has authentication), so they cannot be forgotten.
- **Migrate an old test when you change its file;** delete the old one only when the new one covers the same cases.
- **Characterization tests before refactoring legacy code:** record what it does today, even if it looks wrong.
- **Mutation testing** on critical modules shows whether tests catch bugs, not just cover lines; **property-based tests** find edge cases in calculations.
- **Do not delete test data** someone else may be using, and **do not start parallel infrastructure** for tests without asking.

Sources: Feathers, *Working Effectively with Legacy Code*; mutation testing (Stryker); property-based testing (QuickCheck).
