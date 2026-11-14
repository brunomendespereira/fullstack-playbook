# Release

Git, deploy and closing the session. The product's branch model and merge timing live in `context.md`; these rules hold under any model.

## Git

- **Merge, push and deleting a branch need an explicit ok.** Force-deleting a branch is always confirmed separately. Undoing a commit does not authorize deleting its branch.
- **Commit per step,** after `verify` passes, with a semantic message (Conventional Commits). Check what is staged and what is not before committing, especially after moving files.
- **When to merge** (per step, per phase, or at the end of a project) is the product's choice in `context.md`.
- **Version what others depend on** (packages, public APIs) with Semantic Versioning.
- **Parallel work goes in its own worktree** (copy the environment files it needs). Never stash changes to switch branches.
- **Environments that should match:** compare them in both directions; "equal" means the same commit.
- **An instruction that names several branches:** confirm which one is the target before merging.
- **Production and destructive migrations** are a separate decision with their own ok.
- **Small changes** merge more safely than big ones; trunk-based or short-lived branches keep integration frequent.
- **No destructive git** (hard reset, force push, history rewrite) without an ok. If the agent supports command hooks, block these commands there; the rule holds without them.

## Database changes

- **Expand, migrate, contract:** add the new shape, move data and code in green batches, remove the old shape in a later deploy (parallel change).
- **Every migration is reviewed by the owner before it runs.** A new constraint first counts existing duplicates (`principles/data-integrity.md`).
- **A tool that uses a scratch database never points at a real one.**
- **Seed data is idempotent** and runs on deploy; it exits cleanly when its configuration is missing.
- **Damaged production data** is fixed as `principles/data-integrity.md` says, after the owner's ok.

## Dependencies and builds

- **Pin versions:** the latest stable version checked at install time, exact versions, a committed lockfile, frozen installs, an exact runtime version, and a minimum package age before adopting a new release. Dependency updates are their own task and commit.
- **When dependencies or the build change,** build the production artifact from scratch from committed files, on the server's architecture, before pushing.
- **Configuration in the environment, stateless processes, logs to standard output** (twelve-factor).

## Before pushing

Tests pass, the app runs without errors, no secrets in the diff, migrations reviewed, lint clean. An outside integration is validated by hand with a test account, because automated tests never call real outside services.

## Pull requests

Use `templates/pull-request.md`: the smallest visual or command that shows it working, evidence before and after, whether it is a one-way or two-way door, and its blast radius. A public comment written by an AI says so. High-risk changes ship behind a flag or to a small group first.

## Closing a session

Commit, replace `state.md` with the present, write the resume phrase, run the session-end trigger, and suggest cleanup of stale branches, worktrees and containers.

Sources: Conventional Commits; Fowler, "Parallel Change"; twelve-factor app (12factor.net); DORA research on trunk-based development; Google engineering practices on small changes; Semantic Versioning (semver.org).
