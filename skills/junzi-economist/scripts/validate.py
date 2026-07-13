#!/usr/bin/env python3
"""Validate the first Junzi Economist skill skeleton without third-party packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing file: {relative}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"not valid UTF-8: {relative}: {exc}")
        return ""


REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/ECONOMIC_FOUNDATIONS.md",
    "references/MICROECONOMIC_LAW.md",
    "references/MACROECONOMIC_LAW.md",
    "references/POLITICAL_ECONOMY_AND_HISTORY.md",
    "references/THEORY_ROUTER.md",
    "references/SITUATION_AND_FRONTIER.md",
    "references/EMPIRICAL_AND_STRUCTURAL_METHODS.md",
    "references/HUMAN_WELFARE_AND_INSTITUTIONS.md",
    "references/SOFTWARE_AND_COMPUTATION.md",
    "references/SOURCE_MAP.md",
    "references/BRANCH_AND_DECISION_PROTOCOL.md",
    "references/ECONOMIC_WRITING.md",
    "references/PAPER_READING.md",
    "assets/templates/RESEARCH_MAINLINE.yaml",
    "assets/templates/CLAIM_LEDGER.yaml",
    "assets/templates/MODEL_CARD.md",
    "assets/templates/BRANCH_LOG.yaml",
    "assets/templates/PAPER_EVIDENCE_MAP.yaml",
    "assets/templates/MANUSCRIPT_CLAIM_MAP.yaml",
    "evals/triggers.yaml",
    "evals/cases.yaml",
    "evals/legacy_capabilities.yaml",
    "evals/platform_compatibility.yaml",
    "scripts/check_citekeys.py",
    "scripts/prose_lint.py",
    "scripts/test_utilities.py",
    "scripts/validate_compatibility.py",
]

for relative in REQUIRED:
    read(relative)

skill = read("SKILL.md")
frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", skill, re.DOTALL)
if not frontmatter:
    fail("SKILL.md must begin with YAML frontmatter")
else:
    fields = [
        line.split(":", 1)[0].strip()
        for line in frontmatter.group(1).splitlines()
        if line and not line[0].isspace() and ":" in line
    ]
    if fields != ["name", "description"]:
        fail(f"frontmatter fields must be name and description; found {fields}")
    if not re.search(r"(?m)^name:\s*junzi-economist\s*$", frontmatter.group(1)):
        fail("skill name must be junzi-economist")

if len(skill.splitlines()) >= 300:
    fail("SKILL.md should stay below 300 lines")

for relative in REQUIRED[2:15]:
    if f"`{relative}`" not in skill:
        fail(f"SKILL.md does not route to {relative}")

for phrase in [
    "Dao 道",
    "Fa 法",
    "Shi 势",
    "Shu 术",
    "Qi 器",
    "Act first as an economist",
    "Do not use an estimator to conceal an undefined economic object",
    "Scale the visible response",
    "continue, pause, fork, backtrack, or abandon",
]:
    if phrase not in skill:
        fail(f"SKILL.md is missing core discipline: {phrase}")

foundations = read("references/ECONOMIC_FOUNDATIONS.md")
for phrase in ["Microeconomic foundations", "Macroeconomic foundations", "Institutions, distribution, and power"]:
    if phrase not in foundations:
        fail(f"economic foundations missing: {phrase}")

source_map = read("references/SOURCE_MAP.md")
for phrase in [
    "Karl Marx",
    "Mao Zedong",
    "Mas-Colell",
    "Ljungqvist",
    "Jean Tirole",
    "Amartya Sen",
    "Kenneth L. Judd",
    "Source-use protocol",
]:
    if phrase not in source_map:
        fail(f"source map missing lineage or protocol: {phrase}")

branch_protocol = read("references/BRANCH_AND_DECISION_PROTOCOL.md")
for phrase in ["Detect branch capture", "Name the failed premise", "Diagnose the deepest affected layer", "Preserve branch memory", "forbidden repetition"]:
    if phrase.casefold() not in branch_protocol.casefold():
        fail(f"branch protocol missing: {phrase}")

writing = read("references/ECONOMIC_WRITING.md")
for phrase in ["Gate writing by research state", "Build the paper spine", "Maintain claim, literature, and style separation", "Reconstruct formal claims before writing", "Review and stop"]:
    if phrase not in writing:
        fail(f"economic writing reference missing: {phrase}")

reading = read("references/PAPER_READING.md")
for phrase in ["Select the reading purpose", "Reconstruct the paper", "Separate four voices", "Audit by paper type", "Build a literature map"]:
    if phrase not in reading:
        fail(f"paper reading reference missing: {phrase}")

methods = read("references/EMPIRICAL_AND_STRUCTURAL_METHODS.md")
methods_folded = methods.casefold()
for phrase in ["Causal identification", "Structural modeling and estimation", "Numerical verification", "Exploration and confirmation"]:
    if phrase.casefold() not in methods_folded:
        fail(f"method reference missing: {phrase}")

cases = read("evals/cases.yaml")
case_count = len(re.findall(r"(?m)^  - id: JE-R\d{2}$", cases))
if case_count < 20:
    fail(f"need at least twenty core eval cases; found {case_count}")

triggers = read("evals/triggers.yaml")
trigger_count = len(re.findall(r"(?m)^  - id: JE-T\d{2}$", triggers))
if trigger_count < 10:
    fail(f"need at least ten trigger cases; found {trigger_count}")

interface = read("agents/openai.yaml")
for phrase in ["display_name:", "short_description:", "$junzi-economist", "allow_implicit_invocation: true"]:
    if phrase not in interface:
        fail(f"agents/openai.yaml missing: {phrase}")

if ERRORS:
    print("Junzi Economist validation failed:")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print(
    "Junzi Economist validation passed: "
    f"{len(REQUIRED)} required files, {case_count} core cases, "
    f"{trigger_count} trigger cases, and progressive reference routing."
)
