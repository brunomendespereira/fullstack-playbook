#!/usr/bin/env python3
"""Bring a notebook made by an older version of the skill up to this version. Safe to run twice.

Usage: python3 <skill>/scripts/upgrade_space.py [product folder]

Mechanical part only: adds the frontmatter fields that the current context.md template has and the
notebook lacks (empty, so a person or agent fills them), refreshes the managed checker copy in
docs/playbook/tools/, and records the skill's version in playbook_version. It never changes a
value the product wrote. It prints the versions crossed, so the agent can do the judgment part
listed for each one in workflow/upgrade.md.
"""
import pathlib
import re
import shutil
import sys

sys.dont_write_bytecode = True  # never leave __pycache__ inside the product
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import notebook as nbk  # noqa: E402

SKILL = pathlib.Path(__file__).resolve().parent.parent


def versions_crossed(old, new):
    """Version headings of workflow/upgrade.md newer than `old` and not newer than `new`."""
    text = (SKILL / "workflow" / "upgrade.md").read_text()
    found = re.findall(r"^### (\d+\.\d+\.\d+)\b", text, re.M)
    return [v for v in found if nbk.version_key(old) < nbk.version_key(v) <= nbk.version_key(new)]


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    nb = root / nbk.NOTEBOOK
    ctx = nb / "context.md"
    if not ctx.exists():
        print("no notebook here; run onboarding instead (workflow/onboarding.md)")
        return 1

    new = nbk.skill_version(SKILL)
    text = ctx.read_text()
    data, _ = nbk.split(text)
    old = str(data.get("playbook_version") or "")
    if old and nbk.version_key(old) >= nbk.version_key(new):
        print(f"notebook already at {old}; nothing to upgrade")
        return 0

    template, _ = nbk.read(SKILL / "templates" / "context.md")
    missing = [k for k in template if k not in data and k != "playbook_version"]
    text, changed = nbk.set_top_fields(text, {"playbook_version": new}, only_missing=missing)
    ctx.write_text(text)

    tools = nb / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    for name in ("check_space.py", "notebook.py"):
        shutil.copyfile(SKILL / "scripts" / name, tools / name)

    print(f"upgraded notebook from {old or 'before 1.1.0'} to {new}")
    for k in changed:
        print(f"context.md: {'set' if k == 'playbook_version' else 'added empty field'} {k}")
    print("refreshed: docs/playbook/tools/ (managed checker copy)")
    crossed = versions_crossed(old, new)
    if crossed:
        print("judgment steps to do now (workflow/upgrade.md): " + ", ".join(crossed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
