#!/usr/bin/env python3
"""Compare an installed skill package with the repository source package."""
from __future__ import annotations
import argparse
import hashlib
import sys
from pathlib import Path

def manifest(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--installed", required=True)
    args = parser.parse_args()
    source = manifest(Path(args.source))
    installed = manifest(Path(args.installed))
    missing = sorted(source.keys() - installed.keys())
    extra = sorted(installed.keys() - source.keys())
    changed = sorted(key for key in source.keys() & installed.keys() if source[key] != installed[key])
    if missing or extra or changed:
        print(f"missing={missing}")
        print(f"extra={extra}")
        print(f"changed={changed}")
        return 1
    print(f"installation parity passed: {len(source)} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
