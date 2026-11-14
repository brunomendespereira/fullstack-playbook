# AI features

Read this when the product's `context.md` lists `ai`: the product calls language models (assistants, agents, classification, generation). Provider and model are product decisions, recorded with the reason.

## Responsibility

- **The model decides; code executes.** Publishing, charging, scheduling, retrying and validating are deterministic code with tests. The model only does what needs judgment or creation.
- **The model uses the same API as the screens,** through narrow tools with input validated by a schema. A validation error goes back to the model as a message so it can correct itself.
- **Code records each step** (tool started, tool finished, result), never relying on the model to report it.
- **The runtime sits behind the product's own interface,** so provider and model come from configuration.
- **Conversation is not a feature:** if the model can answer something only in words, do not count it as a product capability until the product actually does it.

## Robustness

- **Every model call has a timeout and limited retries,** and the user gets a friendly message when the provider fails.
- **A tool error goes back to the model,** never straight to the user, and a guard at the sending point blocks internal markup or system text from leaking into a reply.
- **A specialist agent gets only what it needs,** not the orchestrator's corrections and internal results.
- **What the model keeps forgetting to do in the turn** becomes a deterministic batch job.
- **Deterministic ids per object** (for example one conversation per item reviewed), so asking again returns to the same place instead of spending a new run.
- **Several agents on one request:** read-only work runs in parallel; changes and the answer to the user come from one of them, because parallel writers make conflicting decisions.

## Prompts and models

- **Static content at the top, dynamic data last,** so providers can cache the prompt prefix. Volatile data is fetched with a tool the prompt tells the model to call.
- **Keep the cached prefix byte-stable.** Providers cache from the start of the request in a fixed order (tool definitions, then system instructions, then messages), and one changed byte invalidates everything after it. List tools in a fixed order, keep dates, ids and user data out of the system instructions, and watch the cache hit rate the provider reports.
- **Every non-trivial prompt change is recorded** with the reason and the commit before and after, and checked before removing a section: a section may exist because of a bug already fixed.
- **The model choice for each call is recorded** with its reason and any comparison made.
- **The model must know what the product can do,** from a capabilities guide kept up to date in the same change that alters what users can do; an outdated guide makes the model promise what does not exist or deny what does.

## Untrusted input and what the model may do

- **Instructions live only in the system (or developer) role.** User messages, tool results, retrieved documents, web pages and files are data: mark where each one came from and tell the model it holds no instructions. Untrusted text never goes into the system instructions.
- **Assume an injected instruction will get through:** what the model can do is bounded by its tools. Each tool checks the same permissions as the screen for the user in the session, and an action that moves money, deletes, or sends something to other people needs the user's confirmation or a deterministic rule.
- **Model output is untrusted input** for the rest of the code: validate structured output against a schema (send the validation error back once, then fail safe), never run it as code, a query or a command, and sanitize it before rendering it as HTML (`principles/security.md`).
- **The system instructions hold no secrets** and can leak; whatever must hold is enforced in code. Send the provider only the personal data the task needs.

## Loops and budgets

- **Every agent loop has a stop the code checks:** a maximum number of steps, a done condition (the task is complete, no new tool call, the same call repeated), and a time and token budget per request. Reaching it ends with a clear message and a log entry, never a silent cut.
- **The conversation has a context budget:** keep the history within it by dropping or summarizing old turns and trimming large tool results to what the next step needs, without touching the cached prefix.
- **Measure each call** (tokens in, out and cached, latency, cost), alert on spikes, and limit use per user so a runaway loop or a flood of requests cannot run up the bill.
- The numbers (steps, budgets, limits) are product values in `context.md`.

## Where the records live

In the product's notebook, `docs/playbook/ai/`, created the first time one is needed:
- `conventions.md`: how this product writes prompts (section order, tone, what each agent receives).
- `prompts.md`: one dated entry per non-trivial change to a prompt section or a tool description: which prompt and section, the reason, the commit before and the commit of the change. Read it before removing or rewriting a section.
- `models.md`: every place the code calls a model (function, file, in the request or in the background), the model in use, why, and any comparison made, dated.

They are running logs, not decision records: one file per subject, newest entry first. Code and tests that point to them use these paths.

## Evaluating

Check behavior with the real model on recorded scenarios before and after each prompt or model change. A text-only proxy cannot confirm a visual bug: look at the real screen.

Sources: OWASP Top 10 for LLM Applications 2025 (LLM01 prompt injection, LLM02 sensitive information disclosure, LLM05 improper output handling, LLM06 excessive agency, LLM07 system prompt leakage, LLM10 unbounded consumption); Anthropic, "Building effective agents" and prompt caching documentation; OpenAI documentation on prompt caching, structured outputs and tool use.
