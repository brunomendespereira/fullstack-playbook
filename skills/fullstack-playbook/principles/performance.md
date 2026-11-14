# Performance

Fast enough for real users on real devices. Measure before and after, and fix the biggest bottleneck first; an optimization without a measurement is a guess.

## Measure

- **Baseline first,** with the same measure repeated at the end: time to open each screen, requests per screen, the slowest routes, and the Core Web Vitals on the web (good: LCP under 2.5 s, INP under 200 ms, CLS under 0.1, at the 75th percentile).
- **Performance budgets** checked in `verify` or CI (bundle size, number of requests, a lab score), so a regression fails the build.
- **Test on a cheap device and a slow network,** and collect field metrics from real users when possible.
- **Time every route on the server** and track the slow ones.

Source: Google, web.dev (Core Web Vitals, performance budgets).

## Data on the client

- **One cache key per piece of data,** declared in one place; two declarations of the same data with different settings fight each other.
- **Independent requests run in parallel,** never one after another by accident. Never fetch inside a render or an effect when a data layer exists.
- **After a successful write, mark the affected lists as stale** instead of refetching everything; after an error or a partial batch, refetch the screen. Invalidate only on an unambiguous signal.
- **Open from what you already have:** a detail opened from a list starts with the list's copy and refreshes only if that copy is old.
- **Search runs on the server,** with a short pause after typing and results cached per term; do not copy the server's ranking logic to the client.
- **Freshness per kind of data:** how long each kind may be shown before refreshing is a product value, chosen by how fast it changes.

## Data on the server

- **Every list is paginated,** with an opaque cursor; never return an unbounded list.
- **No N+1 queries:** load related data in one query or a batch.
- **Index the columns that frequent queries filter and sort by,** and select only the columns used.
- **Limit the connection pool,** and compress responses.
- **Slow work (AI calls, reports, media) runs in the background;** the route answers right away with a "processing" status.
- **A shared cache or a CDN only when a measurement asks for it.**

## Loading and rendering

- **Load on demand** what the first screen does not need: heavy routes, rare panels, third-party scripts, analytics (in idle time).
- **Images** in a modern format, at the size they are shown, converted at upload; lazy loading only below the first fold; space reserved so the layout does not jump.
- **Fonts:** few weights, subsets, and a display strategy that shows text right away.
- **Long lists are virtualized** or windowed; do not redraw what did not change.
- **Small things that add up:** passive listeners for touch and scroll, never alternate layout reads and writes, use maps or sets for repeated lookups, await only in the branch that needs the value, and run the cheap check before the expensive call.
