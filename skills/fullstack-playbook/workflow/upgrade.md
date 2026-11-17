# Upgrade

A notebook remembers the skill version that wrote it (`playbook_version` in `context.md`). When the skill is newer, the notebook is migrated once, in order, the way a database applies only the migrations it has not run yet. A missing field means the notebook predates 1.1.0.

## When

On the first request of a session, after reading `state.md` and `context.md`: compare `playbook_version` with `metadata.version` in `SKILL.md`. Equal: go on. Missing or older: do the steps below first, then go on with the request.

## Steps

1. **Say it in one line:** "The notebook was written by playbook X and the skill is now Y; updating the notebook first."
2. **Mechanical part:** run `scripts/upgrade_space.py .`. It touches only the notebook's own fields and its managed checker copy, and prints the versions crossed.
3. **Judgment part:** for each version crossed, do what its section below lists. Anything that needs the person's decision becomes a task in `projects/maintenance/` (or its own project when it is large), with the six risk answers, so it competes with other work instead of blocking this request.
4. **Tell the person** in a few lines what changed in the playbook and which tasks were opened. Ask nothing yet unless the current request depends on it.
5. **Commit the notebook** on its own (`chore: notebook upgraded to playbook Y`) when `verify` passes, then go on with the request.

Done when `playbook_version` equals the skill's version, `check_space.py` prints no upgrade warning, and every judgment step is done or has its task.

## Versions

Newest last. Each section lists what an existing notebook needs; new notebooks are born with it.

### 1.1.0

- **Code structure.** Field `code_structure` (added empty by the script) and the "Code structure" section in `context.md`. Open a task "Architecture archaeology" that follows `workflow/onboarding.md` ("Architecture archaeology"): import graph, hot spots, each kind of thing found in more than one place, the attributes the current structure favors. Its outcome is a decision record with the chosen organization, the filled section with its placement table, and the field pointing to the record. Until it is done, new files follow the most common existing place for their kind.

### 1.2.0

- **Upgrade path.** Field `playbook_version` in `context.md` (set by the script). Nothing to decide.
