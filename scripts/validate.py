#!/usr/bin/env python3
"""Check every skill and connection against SPEC.md.

    python3 scripts/validate.py

Exits non-zero with one line per problem. Standard library only, so it runs
the same in CI and on a contributor's machine.
"""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
CONNECTIONS = ROOT / "connections"

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SCHEDULE = re.compile(
    r"^(hourly|(daily|weekdays|monday|tuesday|wednesday|thursday|friday|saturday|sunday) ([01]?\d|2[0-3]):[0-5]\d)$"
)
KNOWN_METADATA = {"accepts", "suggested_trigger", "requires", "tools", "document", "category", "tested_with", "version", "spec"}
# Keys from before automations: a new skill must not carry them.
RETIRED_METADATA = {"trigger", "schedule", "minutes_before", "title_contains"}
MAX_SKILL_MD = 20_000
MAX_SKILL_FOLDER = 1_000_000
MAX_FILES = 50
MAX_LOGO = 200_000
# Any square size in this range: a brand's file is kept exactly as the brand
# ships it (several brand guidelines forbid altering them), and the app
# scales it when drawing.
MIN_LOGO_PX = 128
MAX_LOGO_PX = 1024
# What a connection is for, as the app groups the Connections tab; the app
# shows a category it does not know under "Other".
CATEGORIES = ("tasks", "docs", "crm", "scheduling", "chat", "files")
MAX_DESCRIPTION = 120
# A word that reads like a tool name: verb_object.
TOOL_LIKE = re.compile(
    r"\b(?:read|list|search|create|edit|get|use|write|set|move|delete|add|check|digest|upcoming|remember|draft)_[a-z_]+\b"
)


CONNECTION_TOOL = re.compile(r"(?<![\w-])[a-z0-9-]+__[A-Za-z0-9_-]+")


def tools_in_spec() -> set[str]:
    """The tool names SPEC.md's table lists: its first column."""
    spec = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    return set(re.findall(r"^\| `([a-z_]+)` \|", spec, flags=re.M))


def frontmatter(text: str) -> tuple[dict[str, str], dict[str, str], str, list[str]]:
    """Top-level keys, metadata keys and the body. A block splitter, not a
    YAML parser — the same reading the app does."""
    problems: list[str] = []
    if not text.startswith("---\n"):
        return {}, {}, text, ["SKILL.md must start with a --- header"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, {}, text, ["the --- header is never closed"]
    head, body = text[4:end], text[end + 5 :]
    top: dict[str, str] = {}
    meta: dict[str, str] = {}
    in_meta = False
    for line in head.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if not in_meta:
                continue  # a continuation of a top-level value
            key, sep, value = line.strip().partition(":")
            if not sep or not value.strip():
                problems.append(f"metadata line is not `key: \"value\"`: {line.strip()}")
                continue
            meta[key.strip()] = unquote(value)
            continue
        key, sep, value = line.partition(":")
        if not sep:
            problems.append(f"header line is not `key: value`: {line}")
            continue
        key = key.strip()
        in_meta = key == "metadata"
        if in_meta and value.strip():
            problems.append("metadata must be one level of indented `key: \"value\"` lines, not {…} or a list")
        top[key] = unquote(value)
    return top, meta, body, problems


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value.split(" #")[0].strip()


def check_suggested_trigger(raw: str) -> str | None:
    words = raw.split(None, 1)
    head, rest = (words[0].lower().replace("-", "_"), words[1].strip() if len(words) > 1 else "")
    if head == "after_meeting":
        return None if not rest else "after_meeting takes nothing after it"
    if head == "before_meeting":
        return None if not rest or rest.isdigit() else f'"{rest}" is not a number of minutes'
    if head == "schedule":
        return None if SCHEDULE.match(rest.lower()) else f'"{rest}" is not like "monday 09:00", "daily 08:00" or "hourly"'
    return f'"{head}" is not after_meeting, before_meeting or schedule'


def png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


def connection_ids() -> set[str]:
    return {p.name for p in CONNECTIONS.iterdir() if p.is_dir()} if CONNECTIONS.is_dir() else set()


ACCEPTS = {"meeting", "calendar_event", "none"}
# Named in SPEC.md for a later version; a skill may not use one yet.
ACCEPTS_RESERVED = {"notebook", "note", "folder"}


def check_accepts(raw: str | None) -> str | None:
    """Why `accepts` is wrong, or None. Every library skill must declare it:
    without it the app guesses."""
    if raw is None:
        return "has no accepts: say what it runs on (meeting, calendar_event, none)"
    words = [w.strip() for w in raw.split(",") if w.strip()]
    if not words:
        return "accepts is empty: say what it runs on (meeting, calendar_event, none)"
    for w in words:
        if w in ACCEPTS_RESERVED:
            return f"accepts: {w} is reserved for a later version of the app"
        if w not in ACCEPTS:
            return f"accepts: {w} is not something a skill can run on (meeting, calendar_event, none)"
    if len(set(words)) != len(words):
        return "accepts names something twice"
    return None


def check_skill(folder: Path, tools: set[str], connections: set[str]) -> list[str]:
    where = f"skills/{folder.name}"
    out: list[str] = []
    if not NAME.match(folder.name) or len(folder.name) > 64:
        out.append(f"{where}: the folder name must be lowercase letters, digits and single hyphens, at most 64")
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return out + [f"{where}: no SKILL.md"]
    files = [p for p in folder.rglob("*") if p.is_file()]
    if len(files) > MAX_FILES:
        out.append(f"{where}: {len(files)} files; at most {MAX_FILES}")
    if sum(p.stat().st_size for p in files) > MAX_SKILL_FOLDER:
        out.append(f"{where}: larger than {MAX_SKILL_FOLDER // 1000} KB")
    if any(part.startswith(".") for p in files for part in p.relative_to(folder).parts):
        out.append(f"{where}: hidden files are not allowed")
    text = skill_md.read_text(encoding="utf-8")
    if len(text.encode()) > MAX_SKILL_MD:
        out.append(f"{where}: SKILL.md is larger than {MAX_SKILL_MD // 1000} KB")
    top, meta, body, problems = frontmatter(text)
    out += [f"{where}: {p}" for p in problems]
    if top.get("name") != folder.name:
        out.append(f'{where}: name is "{top.get("name", "")}" but the folder is "{folder.name}"')
    if not top.get("description"):
        out.append(f"{where}: needs a description saying what it does and when to use it")
    if not body.strip():
        out.append(f"{where}: has no instructions")
    for key in meta:
        if key in RETIRED_METADATA:
            out.append(f"{where}: `{key}` is from before automations; use suggested_trigger instead")
        elif key not in KNOWN_METADATA:
            print(f"note: {where}: metadata `{key}` is not one Samurai Scribe reads (kept as written)")
    if why := check_accepts(meta.get("accepts")):
        out.append(f"{where}: {why}")
    if "suggested_trigger" in meta and (why := check_suggested_trigger(meta["suggested_trigger"])):
        out.append(f"{where}: suggested_trigger: {why}")
    required = [r.strip() for r in meta.get("requires", "").split(",") if r.strip()]
    for r in required:
        if r not in connections:
            out.append(f'{where}: requires "{r}", which is not in connections/')
    tested = [t.strip() for t in meta.get("tested_with", "").split(",") if t.strip()]
    if any(t not in ("local", "cloud") for t in tested):
        out.append(f"{where}: tested_with is local, cloud, or both")
    if meta.get("spec", "1") != "1":
        out.append(f'{where}: spec "{meta["spec"]}" is not one this repository knows (1)')
    # A connection's tool (`calendly__users-get_current_user`) is checked
    # below, against `tools`; its pieces are not the app's tools.
    own_words = CONNECTION_TOOL.sub(" ", body)
    for word in sorted(set(TOOL_LIKE.findall(own_words))):
        if word not in tools:
            out.append(f"{where}: names `{word}`, which is not a tool in SPEC.md")
    listed = [t.strip() for t in meta.get("tools", "").split(",") if t.strip()]
    for t in listed:
        prefix, _, tool = t.partition("__")
        if not tool or prefix not in required:
            out.append(f"{where}: tools lists {t}, which is not a tool of a connection in requires")
    # Services name tools in every style — add-tasks, createJiraIssue,
    # save_issue — so the tool part takes letters, digits, _ and -; a
    # trailing hyphen is punctuation, not the name.
    for name in sorted({m.rstrip("-") for m in CONNECTION_TOOL.findall(body)}):
        prefix = name.split("__")[0]
        if prefix not in required:
            out.append(f"{where}: uses {prefix}'s tools but does not list it in requires")
        elif name not in listed:
            out.append(f"{where}: names {name} but does not list it in tools; a run is offered only the tools listed")
    return out


def check_connection(folder: Path) -> list[str]:
    where = f"connections/{folder.name}"
    out: list[str] = []
    if not NAME.match(folder.name):
        out.append(f"{where}: the folder name must be lowercase letters, digits and single hyphens")
    path = folder / "connection.json"
    try:
        c = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return out + [f"{where}: connection.json cannot be read ({e})"]
    allowed = {"id", "name", "url", "auth", "client_id", "description", "category", "suggested"}
    for key in set(c) - allowed:
        out.append(f"{where}: unknown key `{key}`")
    if c.get("id") != folder.name:
        out.append(f'{where}: id is "{c.get("id")}" but the folder is "{folder.name}"')
    if not isinstance(c.get("name"), str) or not c["name"].strip():
        out.append(f"{where}: needs a name")
    if not isinstance(c.get("url"), str) or not c["url"].startswith("https://"):
        out.append(f"{where}: url must be the service's own https:// MCP address")
    if c.get("auth") not in ("oauth", "api_key"):
        out.append(f"{where}: auth is oauth or api_key")
    if "client_id" in c and not isinstance(c["client_id"], str):
        out.append(f"{where}: client_id is a string")
    description = c.get("description")
    if not isinstance(description, str) or not description.strip():
        out.append(f"{where}: needs a description, one line on what it is for")
    elif len(description) > MAX_DESCRIPTION:
        out.append(f"{where}: description is longer than {MAX_DESCRIPTION} characters")
    if c.get("category") not in CATEGORIES:
        out.append(f"{where}: category is one of {', '.join(CATEGORIES)}")
    suggested = c.get("suggested", {})
    if not isinstance(suggested, dict) or any(v not in ("allow", "ask") for v in suggested.values()):
        out.append(f"{where}: suggested maps tool names to allow or ask — never anything that runs unattended")
    for logo, required in (("logo.png", True), ("logo-dark.png", False)):
        p = folder / logo
        if not p.exists():
            if required:
                out.append(f"{where}: needs {logo}, a square PNG from {MIN_LOGO_PX} to {MAX_LOGO_PX} px")
            continue
        size = png_size(p)
        if size is None or size[0] != size[1] or not MIN_LOGO_PX <= size[0] <= MAX_LOGO_PX:
            out.append(f"{where}: {logo} must be a square PNG from {MIN_LOGO_PX} to {MAX_LOGO_PX} px")
        if p.stat().st_size > MAX_LOGO:
            out.append(f"{where}: {logo} is larger than {MAX_LOGO // 1000} KB")
    return out


def main() -> int:
    tools = tools_in_spec()
    if not tools:
        print("SPEC.md lists no tools")
        return 1
    connections = connection_ids()
    problems: list[str] = []
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.is_dir() else []:
        problems += check_skill(folder, tools, connections)
    for folder in sorted(p for p in CONNECTIONS.iterdir() if p.is_dir()) if CONNECTIONS.is_dir() else []:
        problems += check_connection(folder)
    for p in problems:
        print(p)
    count = len([p for p in SKILLS.iterdir() if p.is_dir()]) if SKILLS.is_dir() else 0
    print(f"{count} skills, {len(connections)} connections: {'ok' if not problems else f'{len(problems)} problems'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
