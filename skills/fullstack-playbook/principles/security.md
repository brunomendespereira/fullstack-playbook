# Security

Read this for any endpoint, login, permission, personal data, product that serves several customers, anything that builds a query or command from input, renders user or model content, fetches a URL or accepts a file, and anything that touches production. These rules apply immediately, even in old code that does not follow them yet.

## Input and access

- **Validate everything on the server,** with a schema and an allow-list. The client is controlled by whoever attacks it; client-side validation is only comfort.
- **Deny by default.** A route is closed unless a rule opens it.
- **Authorize per object on every route:** the resource belongs to the user in the session (or the user has the role that allows it). Checking only that the user is logged in is the most common API flaw.
- **Test it:** user A reading and changing user B's data, and the wrong role, for every route that takes an id or a role.

Sources: OWASP ASVS; OWASP API Security Top 10 (API1, broken object level authorization); OWASP Top 10:2025 (broken access control).

## Injection and output

- **Queries and commands are parameterized.** Never build a database query, a shell command, a file path or a search filter by joining text that came from outside; use the driver's placeholders or the query builder, and bound parameters even in raw queries. Test with a value that contains a quote.
- **Output is encoded for where it lands.** The interface's normal text rendering escapes; any way of inserting raw HTML takes only content cleaned by an allow-list sanitizer, including Markdown turned into HTML and text written by a model. Links from users keep an allowed scheme (no `javascript:`). A content security policy limits which scripts can run.
- **Sessions kept in cookies need forgery protection:** same-site cookies plus a token on every request that changes state. State never changes on a GET.
- **The server never fetches an address the user chose without checks:** an allow-list of hosts or schemes, private and internal addresses blocked after resolving the name, and no redirect followed into them.
- **Uploaded files** are checked by content and size, stored under generated names away from the code, and served with an explicit content type.
- **Errors sent to the client** carry no stack trace, query or internal path; the detail goes to the logs.

Sources: OWASP Top 10:2025 (injection; SSRF within broken access control; mishandling of exceptional conditions); OWASP Cheat Sheet Series (SQL injection, cross-site scripting, CSRF, SSRF and file upload prevention).

## Several customers in one system

Every record carries the customer it belongs to, and every query goes through one function that answers "may this user see this?". Each feature has a test proving one customer cannot see another's data. When teams or roles arrive later, only that function changes. Device caches and local storage are separated per customer too.

## Login and secrets

- **Attempt limits are consumed atomically before comparing** (one statement that increments and checks the limit), so parallel guesses cannot pass the limit. Rate-limit authentication routes.
- **One-time codes are deleted atomically** when used; a second use answers "invalid", not an error.
- **Secrets never appear** in the repository, in logs, in reports, in handoffs or in the conversation. Never print environment variables or connection strings; mask them.
- **Incoming webhooks are authenticated before processing** and refuse everything when the secret is not configured (`principles/data-integrity.md`).

Source: OWASP ASVS, V2 (authentication).

## Personal data

Collect the minimum. Reports, handoffs and logs carry no personal data beyond what the task needs. Never use it as a key, an identifier in a URL, or a lookup value shared with outside services. Prefer anonymizing over deleting when others depend on the record (`principles/product.md`).

## Threats at design time

A change that touches login, personal data or money runs the STRIDE checklist during architecture: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. Each "possible" becomes a mitigation or a test.

Source: Microsoft Security Development Lifecycle, threat modeling.

## Production

- **Read-only by default.** Logs, status and read-only queries are free. Anything that changes state (restart, deploy, migration, editing files, changing configuration) is shown as the exact command first and runs only after an explicit ok.
- **Monitoring only observes and reports;** the fix is proposed and waits.

## Supply chain

Audit dependencies for known vulnerabilities, adopt new package releases only after a minimum age, keep the lockfile committed, and scan commits for secrets in `verify`.

## Outside accounts

When work happens in an outside service on the person's behalf (a store console, a payment dashboard, a cloud panel), stop and hand over at payments, contracts, terms and logins. Those are the person's to do.
