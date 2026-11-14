# Offline and instant open

Read this when the product's `context.md` lists `offline`: the product must keep working without a connection, or must open instantly from saved data. The tools (local storage, cache library, background sync) are chosen with the research rule in `principles/architecture.md` and recorded as decisions; lifetimes and limits are product values.

## Order of adoption

Build these in order; each step depends on the one before.
1. **Base:** pinned versions, layers, vendor adapters, canonical error codes.
2. **Network:** one client with timeouts, retry only for transient failures, idempotency on the server (`principles/data-integrity.md`). Idempotency comes before any queue, or replays duplicate data.
3. **Cache:** one key per piece of data, normalized entities, a version guard, freshness per kind of data, details opened from the list's copy.
4. **Persistence on the device:** per account, opt-in, versioned, with a maximum age, revalidated on restore.
5. **Screens:** the four states, one global "no connection" notice, totals from the server.
6. **Writes:** one mutation path with optimistic updates, undo only what is still yours, version conflicts, batches with per-item results.
7. **Real offline:** save on the device before sending; a queue that survives a reload.
8. **Isolation:** clear device data on sign-out and on account switch, before persisting data from more than one account.

## Reading

- **Open from the last good data** and refresh in the background. A failed refresh keeps the data and shows a notice; it never empties the screen.
- **Persist only what is marked** for persistence, and only successful results. Never persist tokens, search results or progress that must not be replayed.
- **Version and age:** every persisted cache has a version (raise it when the shape changes, and the old cache is dropped) and a maximum age. Keep data in memory at least as long as it may live on the device, or the next save erases it.
- **Revalidate what comes back from the device** against the current schema: new fields get defaults; what no longer fits is dropped and fetched again.
- **Store structured objects, not serialized text,** so dates and types survive. Write at most at a steady rate, only when the data changed, and immediately when the app goes to the background.
- **Long lists:** restore only what the first screen needs; how much is a product value.
- **Normalized cache:** keys per entity and per list, one list shape, one place that inserts or moves an entity between lists and fixes their totals. Read and write the cache only through these helpers.
- **Version guard:** data older than what the cache holds is ignored, whatever its source (response, live event, undo).
- **Instant filters:** show what the cache already has with the same rule and order the server uses, and hide totals and "empty" until the server confirms.
- **Totals come from the server,** never from counting a partial list.

## Writing

- **Save on the device first,** marked "not sent", then send. An old send clears the mark only if the device still holds exactly that content, so a newer change is never lost.
- **"Last one wins" queue** when the server keeps the latest value: one send at a time, and while one is in flight keep only the newest. The queue advances when the send finishes, even if the screen closed.
- **Retry with growing waits** and never give up while something is pending: with the server down and the device "online", the "back online" event never fires. Send immediately when the connection returns. This is the one exception to the retry limit in `principles/clean-code.md`, because the data exists only on this device.
- **One mutation path for everything:** optimistic update, an idempotency key created once per operation and kept on retries (`principles/data-integrity.md`), the server's answer written back to every place it appears, undo through the inverse action, single and batch actions handled the same way.
- **Undo only what is yours:** roll back only while the cached copy is still the one you wrote.
- **A queue that survives a reload:** register how to send each kind of write, persist paused writes, resume them after restoring.
- **Record "sending since" and "sent"** on the device for long sends, so a reload never reopens a form that may already have been sent.
- **Timers survive closing the app:** store the end time, not a countdown.
- **Status per item:** sending, saved, failed, visible next to the item.

## Session

- **Optimistic sign-in:** with a saved token, open right away and validate in the background. Only a refusal of the session signs out; a network failure keeps it.
- **A refused session is detected on any call** and signs out once, even when several calls fail together. Ignore answers for a token that is no longer the current one.
- **Per-device state is decided on the device** (for example "this device receives notifications"), and the server is told afterwards.
- **Sign-out:** send what is pending (with a time limit), then clear everything on the device, and ignore late writes from the account that left. Switching accounts without signing out clears memory before switching.

## Caching layers on the web

A service worker caches the app shell and static files (images, fonts). Server data stays in the application's cache, never in both, or the two disagree and an error page gets cached as data.

Sources: web.dev, "The offline cookbook"; Fowler, "Optimistic Offline Lock" (*Patterns of Enterprise Application Architecture*).
