# Changelog

Notable changes to the skill. Format: Keep a Changelog. Versions follow Semantic Versioning.
"Upgrading" says what an existing notebook needs; the agent does it on its own on the next
session (`skills/fullstack-playbook/workflow/upgrade.md`).

## 1.2.1 - 2026-11-17
### Added
- This changelog and the release checklist in `CONTRIBUTING.md`.
### Upgrading
- Nothing to decide. The agent records the new version in the notebook.

## 1.2.0 - 2026-11-17
### Added
- Upgrade path: `metadata.version` in `SKILL.md`, `playbook_version` in `context.md`,
  `workflow/upgrade.md` and `scripts/upgrade_space.py`. On the first request of a session the
  agent compares the versions and migrates an older notebook once.
- New notebooks are born with `playbook_version`; `check_space.py` warns when it is missing.
- READMEs: "Updating" section.
### Upgrading
- Automatic: the agent runs `upgrade_space.py` and commits the notebook on its own.

## 1.1.0 - 2026-11-17
### Added
- `principles/architecture.md`: from goals to structure (priority attributes as scenarios),
  code organization by size and phase, where a new file goes, keep and evolve.
- `code_structure` field and "Code structure" section in `context.md`. Onboarding asks the
  priority attributes and maps the real structure of an existing product. The reviewer checks
  where new files go.
### Changed
- Barrel files: one small entry point per boundary module, no index that re-exports everything.
### Upgrading
- The agent opens an "Architecture archaeology" task. You choose the code organization and it is
  recorded in `decisions/`.

## 1.0.0 - 2026-11-16
- First release.
