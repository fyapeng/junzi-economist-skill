#!/usr/bin/env python3
"""Check Pandoc-style citation keys against a BibTeX database."""
from __future__ import annotations
import argparse
import re
from pathlib import Path

CITEKEY = re.compile(r"(?<![A-Za-z0-9._%+\-])@([A-Za-z][A-Za-z0-9_:.\-]*)")
BIBKEY = re.compile(r"@(?:article|book|inproceedings|incollection|techreport|phdthesis|mastersthesis|misc|unpublished|online|dataset)\s*\{\s*([^,\s]+)\s*,", re.I)

def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8-sig")

def cited_keys(text: str) -> set[str]:
    return set(CITEKEY.findall(text))

def bibliography_keys(text: str) -> set[str]:
    return set(BIBKEY.findall(text))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True)
    parser.add_argument("--bib", required=True)
    parser.add_argument("--fail-on-extra", action="store_true")
    args = parser.parse_args()
    used = cited_keys(read(args.text))
    available = bibliography_keys(read(args.bib))
    missing = sorted(used - available)
    extra = sorted(available - used)
    print(f"text_keys={len(used)}")
    print(f"bib_keys={len(available)}")
    print("missing=" + (", ".join(missing) if missing else "none"))
    print("extra_not_cited=" + (", ".join(extra) if extra else "none"))
    return 1 if missing or (args.fail_on_extra and extra) else 0

if __name__ == "__main__":
    raise SystemExit(main())
