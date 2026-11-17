"""Behavior tests for the notebook scripts (init_space, check_space, lock_tests).

Each test builds a throwaway product folder and calls the scripts the way an agent would:
python3 <skill>/scripts/<script>.py ...
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "fullstack-playbook" / "scripts"


def run(script, *args, cwd):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], cwd=cwd, capture_output=True, text=True)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip())


TASK_OK = """
---
status: in-progress
blocked_by: []
owner: agent
risks:
  duplicates: yes
  external_events: no
  endpoint: yes
  other_users_data: no
  auth_or_personal_data: no
  sensitive_area: no
locked_tests: {}
---
# Redeem a coupon
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q"], cwd=self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir)


class InitSpace(Base):
    def test_creates_notebook(self):
        r = run("init_space.py", "--root", ".", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        nb = self.dir / "docs" / "playbook"
        for f in ("context.md", "state.md", "triggers.md", "memory.md", "glossary.md"):
            self.assertTrue((nb / f).exists(), f)
        for d in ("projects/maintenance/tasks", "decisions", "archive"):
            self.assertTrue((nb / d).is_dir(), d)
        self.assertTrue((self.dir / "PRODUCT.md").exists())
        self.assertFalse((self.dir / "DESIGN.md").exists(), "DESIGN.md only when the product has an interface")
        self.assertIn(".playbook/", (self.dir / ".gitignore").read_text())
        self.assertIn("fullstack-playbook:start", (self.dir / "AGENTS.md").read_text())

    def test_agent_folder_without_claude_md_gets_an_import_of_agents_md(self):
        (self.dir / ".claude" / "skills").mkdir(parents=True)
        run("init_space.py", "--root", ".", cwd=self.dir)
        run("init_space.py", "--root", ".", cwd=self.dir)
        self.assertEqual((self.dir / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        self.assertIn("fullstack-playbook:start", (self.dir / "AGENTS.md").read_text())

    def test_no_agent_folder_creates_no_claude_md(self):
        run("init_space.py", "--root", ".", cwd=self.dir)
        self.assertFalse((self.dir / "CLAUDE.md").exists())

    def test_interface_flag_creates_design(self):
        run("init_space.py", "--root", ".", "--interface", cwd=self.dir)
        self.assertTrue((self.dir / "DESIGN.md").exists())

    def test_never_overwrites_and_is_idempotent(self):
        run("init_space.py", "--root", ".", cwd=self.dir)
        ctx = self.dir / "docs" / "playbook" / "context.md"
        ctx.write_text("mine")
        (self.dir / "CLAUDE.md").write_text("# Existing rules\nkeep me\n")
        run("init_space.py", "--root", ".", cwd=self.dir)
        run("init_space.py", "--root", ".", cwd=self.dir)
        self.assertEqual(ctx.read_text(), "mine")
        claude = (self.dir / "CLAUDE.md").read_text()
        self.assertIn("keep me", claude)
        self.assertEqual(claude.count("fullstack-playbook:start"), 1)
        self.assertEqual((self.dir / ".gitignore").read_text().count(".playbook/"), 1)

    def test_hook_only_when_asked(self):
        run("init_space.py", "--root", ".", cwd=self.dir)
        self.assertFalse((self.dir / ".githooks" / "pre-commit").exists())
        r = run("init_space.py", "--root", ".", "--install-hook", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.dir / ".githooks" / "pre-commit").exists())
        self.assertTrue((self.dir / "docs" / "playbook" / "verify.sh").exists())
        hooks = subprocess.run(["git", "config", "core.hooksPath"], cwd=self.dir, capture_output=True, text=True).stdout.strip()
        self.assertEqual(hooks, ".githooks")

    def test_verify_and_tools_always_present(self):
        run("init_space.py", "--root", ".", cwd=self.dir)
        nb = self.dir / "docs" / "playbook"
        self.assertTrue((nb / "verify.sh").exists(), "the gate must exist after a plain onboarding")
        self.assertTrue((nb / "tools" / "check_space.py").exists())
        self.assertTrue((nb / "tools" / "notebook.py").exists())
        r = subprocess.run(["sh", str(nb / "verify.sh")], cwd=self.dir, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("notebook ok", r.stdout)

    def test_verify_works_from_a_subfolder_product(self):
        sub = self.dir / "apps" / "web"
        sub.mkdir(parents=True)
        run("init_space.py", "--root", str(sub), cwd=self.dir)
        r = subprocess.run(["sh", "apps/web/docs/playbook/verify.sh"], cwd=self.dir, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("notebook ok", r.stdout)

    def test_hook_keeps_an_existing_git_hook(self):
        hook = self.dir / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\necho mine\n")
        r = run("init_space.py", "--root", ".", "--install-hook", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        hooks = subprocess.run(["git", "config", "core.hooksPath"], cwd=self.dir, capture_output=True, text=True).stdout.strip()
        self.assertEqual(hooks, "", "must not switch hooks path away from an existing hook")
        self.assertIn("pre-commit", r.stdout)

    def test_hook_respects_existing_hooks_path(self):
        subprocess.run(["git", "config", "core.hooksPath", ".husky"], cwd=self.dir)
        r = run("init_space.py", "--root", ".", "--install-hook", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        hooks = subprocess.run(["git", "config", "core.hooksPath"], cwd=self.dir, capture_output=True, text=True).stdout.strip()
        self.assertEqual(hooks, ".husky")
        self.assertIn("core.hooksPath", r.stdout)


class CheckSpace(Base):
    def setUp(self):
        super().setUp()
        run("init_space.py", "--root", ".", cwd=self.dir)
        self.tasks = self.dir / "docs" / "playbook" / "projects" / "maintenance" / "tasks"

    def check(self):
        return run("check_space.py", ".", cwd=self.dir)

    def test_fresh_notebook_passes(self):
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_installed_checker_leaves_no_bytecode_cache_in_the_product(self):
        import os
        env = {k: v for k, v in os.environ.items() if k != "PYTHONDONTWRITEBYTECODE"}
        tools = self.dir / "docs" / "playbook" / "tools"
        r = subprocess.run([sys.executable, str(tools / "check_space.py"), "."], cwd=self.dir,
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(list(tools.rglob("__pycache__")), [])

    def set_structure(self, value):
        ctx = self.dir / "docs" / "playbook" / "context.md"
        ctx.write_text(ctx.read_text().replace("code_structure:\n", f"code_structure: {value}\n", 1))

    def test_missing_code_structure_warns_without_failing(self):
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("code_structure is empty", r.stdout)

    def test_code_structure_pointing_to_a_record_passes_quietly(self):
        write(self.dir / "docs" / "playbook" / "decisions" / "001-code-structure.md", "# Code structure\n")
        self.set_structure("docs/playbook/decisions/001-code-structure.md")
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("code_structure", r.stdout)

    def test_code_structure_pointing_to_a_missing_record_fails(self):
        self.set_structure("docs/playbook/decisions/404.md")
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("code_structure points to", r.stdout)

    def test_valid_task_passes(self):
        write(self.tasks / "001-coupon.md", TASK_OK)
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_invalid_status_fails(self):
        write(self.tasks / "001-coupon.md", TASK_OK.replace("in-progress", "doing"))
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("status", r.stdout)

    def test_unknown_blocker_fails(self):
        write(self.tasks / "001-coupon.md", TASK_OK.replace("blocked_by: []", "blocked_by: [007]"))
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("007", r.stdout)

    def test_started_task_needs_every_risk_answered(self):
        write(self.tasks / "001-coupon.md", TASK_OK.replace("  endpoint: yes\n", "  endpoint:\n"))
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("endpoint", r.stdout)

    def test_todo_task_may_leave_risks_open(self):
        write(self.tasks / "001-coupon.md", TASK_OK.replace("in-progress", "todo").replace("  endpoint: yes\n", "  endpoint:\n"))
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_task_numbers_match_with_or_without_zeros_and_names(self):
        write(self.tasks / "001-coupon.md", TASK_OK.replace("in-progress", "todo"))
        write(self.tasks / "002-limit.md", TASK_OK.replace("blocked_by: []", "blocked_by: [1]"))
        state = self.dir / "docs" / "playbook" / "state.md"
        state.write_text(state.read_text().replace("active_project:", "active_project: maintenance", 1).replace("active_task:", "active_task: 002-limit", 1))
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_state_points_to_missing_task_fails(self):
        state = self.dir / "docs" / "playbook" / "state.md"
        state.write_text(state.read_text().replace("active_project:", "active_project: maintenance", 1).replace("active_task:", "active_task: 042", 1))
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("042", r.stdout)


class LockTests(Base):
    def setUp(self):
        super().setUp()
        run("init_space.py", "--root", ".", cwd=self.dir)
        self.task = self.dir / "docs" / "playbook" / "projects" / "maintenance" / "tasks" / "001-coupon.md"
        write(self.task, TASK_OK)
        self.test_file = self.dir / "tests" / "coupon_test.txt"
        write(self.test_file, "two redeems at once: only one counts\n")

    def test_lock_then_change_is_caught(self):
        r = run("lock_tests.py", "lock", str(self.task), "tests/coupon_test.txt", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(run("check_space.py", ".", cwd=self.dir).returncode, 0)
        self.test_file.write_text("weakened\n")
        r = run("check_space.py", ".", cwd=self.dir)
        self.assertEqual(r.returncode, 1)
        self.assertIn("coupon_test.txt", r.stdout)

    def test_missing_task_is_a_readable_error(self):
        r = run("lock_tests.py", "lock", "docs/playbook/projects/maintenance/tasks/999-none.md", "tests/coupon_test.txt", cwd=self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn("999-none.md", r.stdout)

    def test_unlock_ignores_tests_that_were_not_locked(self):
        run("lock_tests.py", "lock", str(self.task), "tests/coupon_test.txt", cwd=self.dir)
        r = run("lock_tests.py", "unlock", str(self.task), "tests/other.txt", "--by", "owner", "--reason", "x", cwd=self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("unlocked tests/other.txt", self.task.read_text())

    def test_unlock_needs_reason_and_person(self):
        run("lock_tests.py", "lock", str(self.task), "tests/coupon_test.txt", cwd=self.dir)
        r = run("lock_tests.py", "unlock", str(self.task), "tests/coupon_test.txt", cwd=self.dir)
        self.assertNotEqual(r.returncode, 0)
        r = run("lock_tests.py", "unlock", str(self.task), "tests/coupon_test.txt", "--by", "owner", "--reason", "the rule changed", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        text = self.task.read_text()
        self.assertIn("the rule changed", text)
        self.assertIn("owner", text)
        self.test_file.write_text("new rule\n")
        self.assertEqual(run("check_space.py", ".", cwd=self.dir).returncode, 0)


if __name__ == "__main__":
    unittest.main()
