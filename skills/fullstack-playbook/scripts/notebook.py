"""Shared helpers for the product notebook (docs/playbook/).

Frontmatter is a small YAML subset, enough for the notebook files:
  key: value | key: [a, b] | key: {} | key: (then indented "sub: value" lines or "- item" lines)
No third-party packages: the scripts must run anywhere Python 3 runs.
"""
import pathlib
import re

NOTEBOOK = pathlib.Path("docs") / "playbook"
TASK_STATUSES = ("todo", "in-progress", "blocked", "review", "done", "dropped")
STARTED_STATUSES = ("in-progress", "review", "done")
PROJECT_STATUSES = ("active", "paused", "done", "dropped")
RISK_KEYS = ("duplicates", "external_events", "endpoint", "other_users_data", "auth_or_personal_data", "sensitive_area")
RISK_ANSWERS = ("yes", "no")
REQUIREMENTS = ("interface", "offline", "ai", "payments", "multi-tenant", "background-jobs", "i18n", "native-app")

_FM = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def _scalar(raw):
    v = raw.strip()
    if v in ("", "~", "null"):
        return ""
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v == "{}":
        return {}
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [_scalar(x) for x in inner.split(",")] if inner else []
    return v


def split(text):
    """Return (frontmatter dict, body text). Missing frontmatter gives ({}, text)."""
    m = _FM.match(text)
    if not m:
        return {}, text
    data, key = {}, None
    for line in m.group(1).split("\n"):
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            key = k.strip()
            data[key] = _scalar(v)
            continue
        item = line.strip()
        if key is None:
            continue
        if item.startswith("- "):
            if not isinstance(data[key], list):
                data[key] = []
            data[key].append(_scalar(item[2:]))
        else:
            sk, _, sv = item.partition(":")
            if not isinstance(data[key], dict):
                data[key] = {}
            data[key][sk.strip()] = _scalar(sv)
    return data, text[m.end():]


def _dump_value(v):
    if isinstance(v, list):
        return "[" + ", ".join(str(x) for x in v) + "]"
    if isinstance(v, dict) and not v:
        return "{}"
    return str(v)


def join(data, body):
    """Write frontmatter back in the same subset."""
    lines = ["---"]
    for k, v in data.items():
        if isinstance(v, dict) and v:
            lines.append(f"{k}:")
            lines += [f"  {sk}: {_dump_value(sv)}" for sk, sv in v.items()]
        else:
            lines.append(f"{k}: {_dump_value(v)}".rstrip())
    lines.append("---")
    return "\n".join(lines) + "\n" + body.lstrip("\n")


def read(path):
    return split(pathlib.Path(path).read_text())


def task_id(value):
    """Normalize a task reference: '001-coupon', '001', 1 and '1' all become '1'."""
    m = re.match(r"^\s*0*(\d+)", str(value))
    return str(int(m.group(1))) if m else None


def task_number(path):
    return task_id(pathlib.Path(path).name)
