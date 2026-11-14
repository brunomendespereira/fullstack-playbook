---
status: todo
blocked_by: []
owner:
risks:
  duplicates:
  external_events:
  endpoint:
  other_users_data:
  auth_or_personal_data:
  sensitive_area:
locked_tests: {}
---
# Task title

## What it delivers
One vertical slice a person can see or check.

## Risk questions
Answer every one with yes or no in the `risks` field before the task starts:
- duplicates: does it write something that must not happen twice or get lost?
- external_events: does it receive events from outside (webhook, queue, another system)?
- endpoint: does it add or change an endpoint or a public interface?
- other_users_data: can one user reach another user's data through it?
- auth_or_personal_data: does it touch login, permissions or personal data?
- sensitive_area: does it touch an area listed in `context.md`?

## Done when
- [ ] tests written first and locked
- [ ] verify passes
- [ ] reviewed

## Notes
What blocks the task from outside the notebook (an answer, an access, a failing check) goes here and in `state.md`; `blocked_by` holds only task numbers.
