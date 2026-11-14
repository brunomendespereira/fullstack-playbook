# Data integrity

Anything that must not happen twice or get lost: charging, crediting, stock, coupons, seats, invites, counters, records that may exist only once, and events received from outside. Read this whenever a task answers "yes" to the first two risk questions.

## Concurrent writes (race conditions)

Two identical requests can arrive in the same millisecond. Code that reads, decides and then writes lets both pass the check and both write: a duplicate order, negative stock, a coupon used twice. Fix it in the database, in this order of preference:

1. **A unique constraint** that makes the duplicate impossible. Design it around the legitimate case (two different orders on the same day are fine; the same order twice is not).
2. **One atomic statement** that checks and writes together, then check the number of affected rows (for example `UPDATE stock SET qty = qty - 1 WHERE id = ? AND qty > 0`; zero rows means it was not available).
3. **A transaction that locks the row** (`SELECT ... FOR UPDATE`) when the rule needs several reads.

Do not add an in-memory lock, a cache or a queue when the database can do it: they break with a second instance. If you think something beyond the database is needed, explain why the database is not enough before proposing it.

Before creating a constraint, count existing duplicates with a read-only query. If they exist, report them and propose how to clean them up; delete nothing without the owner's ok.

Test: fire the same request twice at the same time and prove only one had an effect.

Source: Kleppmann, *Designing Data-Intensive Applications*, chapter 7.

## Related rules

- **Reserve before calling outside.** When an action calls a payment provider or another service, write a pending row first (the reservation), so a second request finds it; complete or release it after the call. Release reservations stuck longer than the product's limit.
- **Status changes are conditional:** `UPDATE ... SET status = 'paid' WHERE id = ? AND status = 'pending'`, and only the request that changed a row triggers the side effects (notifications, credits, emails). A final status is never downgraded by a late event.
- **Balances:** read and debit in the same transaction, with a lock.
- **Writes that belong together** happen in one transaction.
- **Version conflicts:** send the version the user saw; the server answers 409 if it changed, and the screen reloads instead of offering a retry that would fail again. Data arriving from any source (response, live event, undo) never overwrites a newer version.

## Idempotency

- **Calls to providers:** send an idempotency key generated once per business operation and reused on every retry of that operation. A new operation gets a new key.
- **Endpoints that charge, credit or create:** accept an `Idempotency-Key` header. A repeated key that finished returns the same response; a repeated key still running returns 409; the same key with a different body returns 422; keys expire after the product's window.
- **The key is a random UUID** created by the client once per operation, when the user starts it (the form opens or the action begins), and reused on every retry of that operation. Never use personal data (email, document number) as a key.
- **Disabling the button while sending** is a comfort for the user, never the protection. The protection is on the server and in the database.

Sources: IETF draft "The Idempotency-Key HTTP Header Field"; Stripe API, idempotent requests.

## Events from outside (webhooks, queues)

- **Verify authenticity before any processing,** with the provider's signature or credentials, comparing in constant time. Missing configuration means refuse (fail closed), never accept.
- **Record the event id first,** in a table with the id as a unique key. If it already exists, answer 2xx and do nothing more.
- **Do not trust arrival order:** when the current state matters, fetch the object from the provider instead of trusting the event payload.
- **Answer fast** and process in the background if the product already has a job mechanism; a failed processing is recorded and retried by a job, because the provider will not resend an event it already got a 2xx for.
- **If the event id is not reliable,** keep a second guard: the conditional status change above.

Source: Stripe documentation on webhooks (best practices).

## Asynchronous payments and confirmations

No error is not success. A payment, a transfer or any asynchronous confirmation is final only when a webhook or a polling of the provider confirms it. When polling gives up, tell the user and do not charge again.

## Batches, events and schedules

- **A batch operation answers per item:** which succeeded and which failed, with a code for each.
- **Publish domain events after the transaction commits,** through one place, carrying ids rather than whole objects, one aggregated event per transaction (outbox pattern).
- **Scheduled jobs never overlap** themselves, declare their time zone, and isolate the failure of one item from the rest of the batch. An in-memory guard only works with a single instance; say so where it is used.

## Fixing data already damaged

Fix production data by reprocessing with the corrected code, or with a surgical update limited to the affected rows, always after the owner's ok and after counting what will change.
