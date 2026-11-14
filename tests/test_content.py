"""Content checks for the skill: frontmatter, routing, size, and words that must not appear.

Run: python3 -m unittest discover tests
"""
import pathlib
import py_compile
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "fullstack-playbook"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCE_DIRS = ("workflow", "principles", "requirements")

MAX_SKILL_LINES = 500
MAX_SKILL_CHARS = 9000
MAX_REFERENCE_CHARS = 16000

# Names of libraries, frameworks, vendors and of the products this skill was born in.
# Allowed only on lines that cite a source ("Source:" / "Sources:").
BANNED = [
    "react", "vue", "angular", "svelte", "next.js", "nextjs", "express", "prisma", "tailwind",
    "django", "rails", "laravel", "supabase", "firebase", "tanstack", "react query", "zod",
    "vitest", "jest", "cypress", "playwright", "docker", "kubernetes", "capacitor", "expo",
    "postgres", "postgresql", "mysql", "mongodb", "redis", "sentry", "notion", "trello", "jira",
    "linear", "whatsapp", "openai", "stripe", "pagar.me", "pagarme", "coolify", "vercel",
    "iagofit", "automatic content", "automatic-content", "bruno", "impeccable",
]


def reference_files():
    for d in REFERENCE_DIRS:
        yield from sorted((SKILL_DIR / d).glob("*.md"))


def skill_markdown_files():
    yield from sorted(SKILL_DIR.rglob("*.md"))


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    key = None
    for line in m.group(1).split("\n"):
        km = re.match(r"^([a-z][a-z0-9_-]*):\s?(.*)$", line)
        if km:
            key = km.group(1)
            fields[key] = km.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    for k, v in fields.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            fields[k] = v[1:-1]
    return fields


@unittest.skipUnless(SKILL_MD.exists(), "SKILL.md not written yet")
class SkillManifest(unittest.TestCase):
    def setUp(self):
        self.text = SKILL_MD.read_text()
        self.fm = frontmatter(self.text)

    def test_has_frontmatter(self):
        self.assertIsNotNone(self.fm, "SKILL.md must start with a --- frontmatter block")

    def test_only_open_standard_fields(self):
        allowed = {"name", "description", "license", "metadata", "compatibility"}
        self.assertTrue(set(self.fm) <= allowed, f"non-standard fields: {set(self.fm) - allowed}")

    def test_name_matches_folder_and_rules(self):
        name = self.fm.get("name", "")
        self.assertEqual(name, SKILL_DIR.name)
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        self.assertNotIn("claude", name)
        self.assertNotIn("anthropic", name)

    def test_declares_source_repository(self):
        # Agents use it to suggest a lesson upstream (workflow/tasks.md, "Memory, archive and cleanup").
        self.assertRegex(self.fm.get("metadata", ""), r"repository:\s*https://github\.com/[\w.-]+/fullstack-playbook")

    def test_description_size(self):
        desc = self.fm.get("description", "")
        self.assertTrue(desc, "description is required")
        self.assertLessEqual(len(desc), 1024)

    def test_size(self):
        self.assertLessEqual(len(self.text.splitlines()), MAX_SKILL_LINES)
        self.assertLessEqual(len(self.text), MAX_SKILL_CHARS)

    def test_every_route_exists(self):
        for rel in set(re.findall(r"\b((?:workflow|principles|requirements|templates|scripts)/[\w.-]+)", self.text)):
            self.assertTrue((SKILL_DIR / rel).exists(), f"SKILL.md points to a missing file: {rel}")

    def test_every_reference_is_routed(self):
        for path in reference_files():
            rel = f"{path.parent.name}/{path.name}"
            self.assertIn(rel, self.text, f"{rel} is not reachable from SKILL.md")


class ReferenceFiles(unittest.TestCase):
    def test_size(self):
        for path in reference_files():
            self.assertLessEqual(len(path.read_text()), MAX_REFERENCE_CHARS, f"{path} is too long to read whole")

    def test_no_agent_specific_variables(self):
        for path in skill_markdown_files():
            self.assertNotIn("${CLAUDE", path.read_text(), f"{path} uses an agent-specific variable")

    def test_no_banned_names(self):
        for path in skill_markdown_files():
            for n, line in enumerate(path.read_text().splitlines(), 1):
                if re.match(r"^\s*(?:[-*]\s*)?(?:\*\*)?Sources?:", line):
                    continue
                low = line.lower()
                for word in BANNED:
                    if re.search(rf"(?<![a-z0-9]){re.escape(word)}(?![a-z0-9])", low):
                        self.fail(f"{path.relative_to(ROOT)}:{n} names '{word}': {line.strip()[:120]}")


class Scripts(unittest.TestCase):
    def test_python_scripts_compile(self):
        for path in sorted((SKILL_DIR / "scripts").glob("*.py")):
            py_compile.compile(str(path), doraise=True)


class Helpers(unittest.TestCase):
    def test_frontmatter_parser(self):
        fm = frontmatter('---\nname: a-b\ndescription: "x: y"\n---\nbody')
        self.assertEqual(fm, {"name": "a-b", "description": "x: y"})

    def test_banned_word_boundary(self):
        # "expressive" must not match "express"; "Source:" lines are allowed.
        self.assertIsNone(re.search(r"(?<![a-z0-9])express(?![a-z0-9])", "expressive"))
        self.assertIsNotNone(re.match(r"^\s*(?:[-*]\s*)?(?:\*\*)?Sources?:", "Source: OWASP"))


if __name__ == "__main__":
    unittest.main()
