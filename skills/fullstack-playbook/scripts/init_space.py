#!/usr/bin/env python3
"""Create the product notebook from the templates. Never overwrites a file the product owns.

Usage: python3 <skill>/scripts/init_space.py --root <product folder> [--interface] [--install-hook]

Creates docs/playbook/ (context, state, triggers, memory, glossary, verify.sh, projects/maintenance,
decisions, archive), PRODUCT.md (and DESIGN.md with --interface), adds .playbook/ to .gitignore,
and writes the short pointer block into AGENTS.md (created if missing) and into CLAUDE.md when it
exists. Files it manages itself are refreshed on every run: the pointer block between its markers
and the notebook checker copied to docs/playbook/tools/. With --install-hook it wires verify.sh as
the git pre-commit hook, unless the repository already has a pre-commit hook or another hooks
path: then it prints the one line to add there instead of replacing anything.
"""
import argparse
import pathlib
import shutil
import stat
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
START, END = "<!-- fullstack-playbook:start -->", "<!-- fullstack-playbook:end -->"

created, kept = [], []


def copy(template, dest):
    if dest.exists():
        kept.append(str(dest))
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TEMPLATES / template, dest)
    created.append(str(dest))


def ensure_dir(path):
    if not path.exists():
        path.mkdir(parents=True)
        created.append(str(path) + "/")


def ensure_gitignore(root):
    gi = root / ".gitignore"
    lines = gi.read_text().splitlines() if gi.exists() else []
    if ".playbook/" not in [line.strip() for line in lines]:
        with gi.open("a") as f:
            if lines and lines[-1].strip():
                f.write("\n")
            f.write("# fullstack-playbook drafts and research (not versioned)\n.playbook/\n")
        created.append(".gitignore entry .playbook/")


def write_block(path, block, create):
    if not path.exists() and not create:
        return
    text = path.read_text() if path.exists() else ""
    if START in text and END in text:
        before, rest = text.split(START, 1)
        after = rest.split(END, 1)[1]
        new = before + block.strip() + after
    else:
        new = (text.rstrip() + "\n\n" if text.strip() else "") + block.strip() + "\n"
    if new != text:
        path.write_text(new)
        created.append(f"{path.name} pointer block")


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True).stdout.strip()


def install_tools(notebook):
    """Managed copies of the notebook checker, refreshed on every run (never edited by hand)."""
    tools = notebook / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    for name in ("check_space.py", "notebook.py"):
        shutil.copyfile(SKILL / "scripts" / name, tools / name)
    created.append(str(tools) + "/ (managed copy of the notebook checker)")
    copy("verify.sh", notebook / "verify.sh")
    verify = notebook / "verify.sh"
    verify.chmod(verify.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_hook(root, notebook):
    top = pathlib.Path(git(root, "rev-parse", "--show-toplevel") or root)
    verify_rel = (notebook / "verify.sh").relative_to(top)
    line = f"sh {verify_rel}"
    current = git(root, "config", "core.hooksPath")
    existing = top / git(root, "rev-parse", "--git-path", "hooks/pre-commit") if not current else top / current / "pre-commit"
    if current and current != ".githooks":
        print(f"NOTE: this repository already uses core.hooksPath={current}. Add this line to its pre-commit hook:\n  {line}")
        return
    if not current and existing.exists():
        print(f"NOTE: a pre-commit hook already exists at {existing}. Add this line to it:\n  {line}")
        return
    hook = top / ".githooks" / "pre-commit"
    if hook.exists() and line not in hook.read_text():
        print(f"NOTE: {hook} already exists. Add this line to it:\n  {line}")
        return
    if not hook.exists():
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text(f"#!/bin/sh\n# Runs the product verification gate (fullstack-playbook).\nexec {line}\n")
        hook.chmod(0o755)
        created.append(str(hook))
    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=top, check=True)
    created.append("git config core.hooksPath .githooks")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--root", default=".")
    p.add_argument("--interface", action="store_true", help="the product has a user interface: also create DESIGN.md")
    p.add_argument("--install-hook", action="store_true", help="wire docs/playbook/verify.sh as the git pre-commit hook")
    a = p.parse_args()
    root = pathlib.Path(a.root).resolve()
    nb = root / "docs" / "playbook"

    for name in ("context.md", "state.md", "triggers.md", "memory.md", "glossary.md"):
        copy(name, nb / name)
    copy("project-brief.md", nb / "projects" / "maintenance" / "brief.md")
    for d in (nb / "projects" / "maintenance" / "tasks", nb / "decisions", nb / "archive"):
        ensure_dir(d)
    copy("PRODUCT.md", root / "PRODUCT.md")
    if a.interface:
        copy("DESIGN.md", root / "DESIGN.md")
    ensure_gitignore(root)
    block = (TEMPLATES / "agent-block.md").read_text()
    write_block(root / "AGENTS.md", block, create=True)
    claude_md = root / "CLAUDE.md"
    if not claude_md.exists() and (root / ".claude").is_dir():
        # This agent reads CLAUDE.md, not AGENTS.md: import it instead of keeping a second copy.
        claude_md.write_text("@AGENTS.md\n")
        created.append("CLAUDE.md (imports AGENTS.md)")
    elif claude_md.exists() and "@AGENTS.md" not in claude_md.read_text():
        write_block(claude_md, block, create=False)
    install_tools(nb)
    if a.install_hook:
        install_hook(root, nb)

    for item in created:
        print(f"created: {item}")
    for item in kept:
        print(f"kept (already existed): {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
