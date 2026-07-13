#!/usr/bin/env python3
"""Validate the shared Junzi Economist package against Codex/Claude skill constraints."""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
errors: list[str] = []

text = SKILL.read_text(encoding="utf-8")
match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
if not match:
    errors.append("missing YAML frontmatter")
    frontmatter = ""
else:
    frontmatter = match.group(1)

fields = [line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if line and not line[0].isspace() and ":" in line]
if fields != ["name", "description"]:
    errors.append(f"shared frontmatter must contain only name and description; found {fields}")

name_match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", frontmatter)
name = name_match.group(1) if name_match else ""
if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
    errors.append("name is not Claude-compatible lowercase/hyphen form of at most 64 characters")

description_match = re.search(r'(?ms)^description:\s*"(.*?)"\s*$', frontmatter)
description = description_match.group(1) if description_match else ""
if not description:
    errors.append("description must be a quoted one-line string")
elif len(description) > 1536:
    errors.append(f"description exceeds Claude listing budget: {len(description)} characters")

if len(text.splitlines()) >= 500:
    errors.append("SKILL.md exceeds the shared 500-line guidance")

resource_pattern = re.compile(r"`((?:references|assets|scripts)/[^`]+)`")
for relative in sorted(set(resource_pattern.findall(text))):
    if not (ROOT / Path(relative)).exists():
        errors.append(f"referenced resource does not exist: {relative}")

for script in (ROOT / "scripts").glob("*.py"):
    try:
        compile(script.read_text(encoding="utf-8"), str(script), "exec")
    except SyntaxError as exc:
        errors.append(f"Python syntax error in {script.name}: {exc}")

if errors:
    print("Compatibility validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(
    "Shared skill compatibility passed: "
    f"name={name}, description_chars={len(description)}, skill_lines={len(text.splitlines())}, "
    f"referenced_resources={len(set(resource_pattern.findall(text)))}."
)
print("Runtime note: static compatibility does not substitute for a Claude Code invocation test.")
