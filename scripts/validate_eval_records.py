#!/usr/bin/env python3
"""Validate strict behavior execution records without third-party packages."""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXECUTIONS = ROOT / "evals" / "executions"
CASES = (ROOT / "evals" / "cases.yaml").read_text(encoding="utf-8")
TRIGGERS = (ROOT / "evals" / "triggers.yaml").read_text(encoding="utf-8")
VALID_CASES = set(re.findall(r"(?m)^  - id:\s*(JE-R\d+)\s*$", CASES))
VALID_CASES.update(re.findall(r"(?m)^  - id:\s*(JE-T\d+)\s*$", TRIGGERS))
REQUIRED = [
    "execution_id", "case_id", "timestamp_utc", "skill_commit", "platform",
    "client_version", "model", "evaluator", "isolation", "prompt", "expected",
    "forbidden", "loaded_files", "response_file", "response_sha256", "rubric", "verdict",
]
errors: list[str] = []
records = sorted(EXECUTIONS.glob("*/record.yaml")) if EXECUTIONS.exists() else []
if not records:
    errors.append("no strict execution records found")

TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".txt", ".yaml", ".yml"}


def valid_hash(path: Path, expected: str) -> bool:
    """Compare exact bytes; for text artifacts also tolerate CRLF/LF checkout conversion."""
    data = path.read_bytes()
    candidates = {hashlib.sha256(data).hexdigest()}
    if path.suffix.lower() in TEXT_SUFFIXES:
        lf = data.replace(b"\r\n", b"\n")
        crlf = lf.replace(b"\n", b"\r\n")
        candidates.update({hashlib.sha256(lf).hexdigest(), hashlib.sha256(crlf).hexdigest()})
    return expected.lower() in candidates

for record in records:
    text = record.read_text(encoding="utf-8")
    for field in REQUIRED:
        if not re.search(rf"(?m)^{re.escape(field)}:\s*", text):
            errors.append(f"{record}: missing field {field}")
    case_match = re.search(r"(?m)^case_id:\s*([^\s]+)\s*$", text)
    if not case_match or case_match.group(1) not in VALID_CASES:
        errors.append(f"{record}: unknown case_id")
    response_match = re.search(r"(?m)^response_file:\s*([^\s]+)\s*$", text)
    hash_match = re.search(r'(?m)^response_sha256:\s*"?([0-9a-fA-F]{64})"?\s*$', text)
    if response_match:
        response = record.parent / response_match.group(1)
        if not response.is_file():
            errors.append(f"{record}: response file missing: {response.name}")
        elif hash_match:
            if not valid_hash(response, hash_match.group(1)):
                errors.append(f"{record}: response hash mismatch")
        else:
            errors.append(f"{record}: invalid response_sha256")
    verdict_match = re.search(r"(?m)^verdict:\s*(\w+)\s*$", text)
    if not verdict_match or verdict_match.group(1) not in {"pass", "fail", "mixed", "invalid"}:
        errors.append(f"{record}: invalid verdict")
    artifacts = re.findall(
        r'(?m)^  - file:\s*([^\s]+)\s*\n\s+sha256:\s*"?([0-9a-fA-F]{64})"?\s*$', text
    )
    artifacts.extend(re.findall(
        r'(?m)^  - \{file:\s*([^,\s]+),\s*sha256:\s*"?([0-9a-fA-F]{64})"?\}\s*$', text
    ))
    for artifact_name, expected_hash in artifacts:
        artifact = record.parent / artifact_name
        if not artifact.is_file():
            errors.append(f"{record}: artifact missing: {artifact_name}")
            continue
        if not valid_hash(artifact, expected_hash):
            errors.append(f"{record}: artifact hash mismatch: {artifact_name}")

if errors:
    print("Behavior record validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print(f"Behavior record validation passed: {len(records)} strict execution record(s).")
