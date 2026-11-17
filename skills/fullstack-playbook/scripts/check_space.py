#!/usr/bin/env python3
"""Check the product notebook (docs/playbook/). Exit 1 on errors, 0 otherwise.

Usage: python3 <skill>/scripts/check_space.py [product folder]

Errors: unknown task or project status, blockers that do not exist, a started task with an
unanswered risk question, a locked test that changed, state.md pointing to a missing project or
task, unknown requirement in context.md, code_structure pointing to a missing decision record.
Warnings: more open fronts than the product allows, no code_structure recorded in context.md, no
playbook_version in context.md.
"""
import hashlib
import pathlib
import sys

sys.dont_write_bytecode = True  # never leave __pycache__ inside the product
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import notebook as nbk  # noqa: E402

errors, warnings = [], []


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_task(root, project, path, numbers):
    data, _ = nbk.read(path)
    rel = path.relative_to(root)
    status = data.get("status", "")
    if status not in nbk.TASK_STATUSES:
        errors.append(f"{rel}: status '{status}' is not one of {', '.join(nbk.TASK_STATUSES)}")
    for b in data.get("blocked_by") or []:
        if nbk.task_id(b) not in numbers:
            errors.append(f"{rel}: blocked_by {b} is not a task in project {project.name}")
    if status in nbk.STARTED_STATUSES:
        risks = data.get("risks") if isinstance(data.get("risks"), dict) else {}
        for key in nbk.RISK_KEYS:
            if str(risks.get(key, "")).lower() not in nbk.RISK_ANSWERS:
                errors.append(f"{rel}: risk question '{key}' must be answered yes or no before the task starts")
    locked = data.get("locked_tests") if isinstance(data.get("locked_tests"), dict) else {}
    for test_path, digest in locked.items():
        f = root / test_path
        if not f.exists():
            errors.append(f"{rel}: locked test {test_path} is missing")
        elif sha256(f) != digest:
            errors.append(f"{rel}: locked test {test_path} changed; unlock it with the owner's ok and a reason first")


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    nb = root / nbk.NOTEBOOK
    if not nb.is_dir():
        print(f"no notebook at {nb.relative_to(root)}; run onboarding first")
        return 1

    ctx, _ = nbk.read(nb / "context.md") if (nb / "context.md").exists() else ({}, "")
    for r in ctx.get("requirements") or []:
        if r not in nbk.REQUIREMENTS:
            errors.append(f"context.md: unknown requirement '{r}' (known: {', '.join(nbk.REQUIREMENTS)})")

    if not str(ctx.get("playbook_version") or "").strip():
        warnings.append("context.md: playbook_version is missing. The notebook predates the skill's upgrade path: "
                        "follow workflow/upgrade.md of the skill.")
    structure = str(ctx.get("code_structure") or "").strip()
    if not structure:
        warnings.append("context.md: code_structure is empty. Record the code organization (principles/architecture.md, "
                        "\"Code organization\") and point this field to its decision record.")
    elif not ((root / structure).exists() or (nb / structure).exists()):
        errors.append(f"context.md: code_structure points to '{structure}', which does not exist")

    projects = {}
    active = 0
    for project in sorted((nb / "projects").glob("*/")):
        brief = project / "brief.md"
        pdata, _ = nbk.read(brief) if brief.exists() else ({}, "")
        pstatus = pdata.get("status", "")
        if pstatus and pstatus not in nbk.PROJECT_STATUSES:
            errors.append(f"{brief.relative_to(root)}: status '{pstatus}' is not one of {', '.join(nbk.PROJECT_STATUSES)}")
        if pstatus == "active" and project.name != "maintenance":
            active += 1
        tasks = sorted((project / "tasks").glob("*.md"))
        numbers = {nbk.task_number(t) for t in tasks if nbk.task_number(t)}
        projects[project.name] = numbers
        for t in tasks:
            check_task(root, project, t, numbers)

    limit = str(ctx.get("open_fronts_limit", "")).strip()
    if limit.isdigit() and active > int(limit):
        warnings.append(f"{active} active projects; context.md allows {limit}. Finish or pause one before starting another.")

    state, _ = nbk.read(nb / "state.md") if (nb / "state.md").exists() else ({}, "")
    ap, at = str(state.get("active_project", "")), str(state.get("active_task", ""))
    if ap and ap not in projects:
        errors.append(f"state.md: active_project '{ap}' does not exist in projects/")
    if ap in projects and at and nbk.task_id(at) not in projects[ap]:
        errors.append(f"state.md: active_task {at} does not exist in project {ap}")

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if not errors:
        print("notebook ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
