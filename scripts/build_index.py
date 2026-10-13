#!/usr/bin/env python3
"""Build index.json: what the app's gallery and connection list read.

    python3 scripts/build_index.py <commit> > index.json

Every file of every skill and connection, with its sha256 and size, at the
commit the index is built from. The app fetches each file at that commit and
refuses one whose hash does not match.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import CONNECTIONS, ROOT, SKILLS, frontmatter  # noqa: E402


def files_of(folder: Path) -> list[dict]:
    out = []
    for p in sorted(folder.rglob("*")):
        if p.is_file():
            data = p.read_bytes()
            out.append({
                "path": p.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
            })
    return out


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[0-9a-f]{40}", sys.argv[1]):
        print("usage: build_index.py <40-character commit>", file=sys.stderr)
        return 2
    skills = []
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        top, meta, _, _ = frontmatter((folder / "SKILL.md").read_text(encoding="utf-8"))
        skills.append({
            "name": folder.name,
            "description": top.get("description", ""),
            "category": meta.get("category"),
            "suggested_trigger": meta.get("suggested_trigger"),
            "requires": [r.strip() for r in meta.get("requires", "").split(",") if r.strip()],
            "tested_with": [t.strip() for t in meta.get("tested_with", "").split(",") if t.strip()],
            "version": meta.get("version"),
            "files": files_of(folder),
        })
    connections = []
    for folder in sorted(p for p in CONNECTIONS.iterdir() if p.is_dir()) if CONNECTIONS.is_dir() else []:
        c = json.loads((folder / "connection.json").read_text(encoding="utf-8"))
        connections.append({**c, "files": files_of(folder)})
    json.dump({"spec": 1, "commit": sys.argv[1], "skills": skills, "connections": connections}, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
