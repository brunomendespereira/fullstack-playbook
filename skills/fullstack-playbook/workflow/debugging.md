# Debugging

No hypothesis before a failing command. Guessing first produces fixes for bugs that do not exist.

## Phases

1. **Reproduce.** Write a command or test that fails on the exact symptom reported (same input, same environment, same error). Show it failing. This becomes the reproduction test; lock it with `scripts/lock_tests.py` before fixing.
2. **Minimize.** Remove everything that is not needed for the failure until the case is as small as it gets.
3. **Hypothesize.** List a few hypotheses that can be proven false (three to five keeps the search focused), each with the experiment that would disprove it.
4. **Test one variable at a time.** Change one thing, rerun, write down the result. Mark temporary debug logs with a unique prefix so they are easy to find and remove.
5. **Intermittent failures:** run many times, record the failure rate, and look for time, order, concurrency and shared state. A test that waits on real time is a suspect.
6. **Clean up.** Remove the debug logs and experiments; keep the reproduction test.

Done when the reproduction test passes, the suite passes, and you can name the invariant that was broken.

## Where the regression test goes

Put it at the seam where the bug lives (the public interface of the module that was wrong), not in a test that happens to touch it. If no good seam exists, that is an architecture finding: record it as a task.

## Critical bugs

When the bug involves money, security or user data, a separate tester writes the reproduction from the report (`workflow/stages.md`, Roles), the full review runs, and data already damaged is fixed by reprocessing with the corrected code after the owner's ok (`principles/data-integrity.md`).

Source: Zeller, *Why Programs Fail* (scientific debugging).
