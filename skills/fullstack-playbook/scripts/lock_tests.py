#!/usr/bin/env python3
"""Lock or unlock the tests of a task, so the code under test cannot quietly change them.

Usage:
  python3 <skill>/scripts/lock_tests.py lock   <task file> <test path>...
  python3 <skill>/scripts/lock_tests.py unlock <task file> <test path>... --by <person> --reason "<why>"

lock stores a SHA-256 of each test file in the task's `locked_tests`. check_space.py then fails
if a locked file changes. unlock needs the person who approved it and the reason, and logs both
in the task body. Paths are relative to the product root (the current folder).
"""
import argparse
import datetime
import hashlib
import pathlib
import sys

sys.dont_write_bytecode = True  # never leave __pycache__ inside the product
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import notebook as nbk  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("action", choices=("lock", "unlock"))
    p.add_argument("task")
    p.add_argument("tests", nargs="+")
    p.add_argument("--by")
    p.add_argument("--reason")
    a = p.parse_args()

    task = pathlib.Path(a.task)
    if not task.is_file():
        print(f"ERROR: task file {task} does not exist")
        return 1
    data, body = nbk.read(task)
    locked = data.get("locked_tests") if isinstance(data.get("locked_tests"), dict) else {}

    if a.action == "lock":
        for t in a.tests:
            f = pathlib.Path(t)
            if not f.is_file():
                print(f"ERROR: {t} does not exist")
                return 1
            locked[t] = hashlib.sha256(f.read_bytes()).hexdigest()
        data["locked_tests"] = locked
        task.write_text(nbk.join(data, body))
        print(f"locked {len(a.tests)} test file(s) in {task}")
        return 0

    if not a.by or not a.reason:
        print("ERROR: unlocking needs --by <person who approved> and --reason \"<why>\"")
        return 2
    removed = [t for t in a.tests if locked.pop(t, None) is not None]
    for t in a.tests:
        if t not in removed:
            print(f"WARNING: {t} was not locked in {task}")
    if not removed:
        print("ERROR: none of these tests were locked; nothing to unlock")
        return 1
    data["locked_tests"] = locked
    stamp = datetime.date.today().isoformat()
    log = "\n".join(f"- {stamp}: unlocked {t}, approved by {a.by}: {a.reason}" for t in removed)
    if "## Test lock log" in body:
        body = body.rstrip() + "\n" + log + "\n"
    else:
        body = body.rstrip() + "\n\n## Test lock log\n" + log + "\n"
    task.write_text(nbk.join(data, body))
    print(f"unlocked {len(removed)} test file(s) in {task}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
