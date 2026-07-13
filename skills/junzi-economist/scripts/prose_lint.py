#!/usr/bin/env python3
"""Locate generic, inflated, or repetitive prose for human review."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

TERMS = [
    "delve", "landscape", "realm", "tapestry", "navigate", "underscore", "shed light",
    "pave the way", "pivotal", "vital role", "transformative", "game-changing",
    "ever-evolving", "it is important to note", "it should be noted", "fills a gap",
    "底层逻辑", "逻辑闭环", "多维视角", "现实关切", "深层机制", "具有重要现实意义",
    "丰富和拓展", "为政策制定提供参考", "推动高质量发展", "显著提升治理能力",
    "具有一定创新性", "研究结论具有启示意义", "赋能", "助力", "抓手",
]
PATTERNS = [
    ("不是…而是", re.compile(r"不是[\s\S]{0,80}?而是")),
    ("本文不…而是", re.compile(r"本文不[\s\S]{0,80}?而是")),
    ("既不是…也不是…而是", re.compile(r"既不是[\s\S]{0,80}?也不是[\s\S]{0,80}?而是")),
    ("not…but", re.compile(r"\bnot\b[\s\S]{0,120}?\bbut\b", re.I)),
]

def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1

def snippet(text: str, start: int, end: int, width: int) -> str:
    return " ".join(text[max(0, start-width):min(len(text), end+width)].split())

def scan(text: str, extra_terms: list[str], width: int) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for term in TERMS + extra_terms:
        flags = re.I if term.isascii() else 0
        for match in re.finditer(re.escape(term), text, flags):
            hits.append({"line": line_number(text, match.start()), "label": term, "context": snippet(text, match.start(), match.end(), width)})
    for label, pattern in PATTERNS:
        for match in pattern.finditer(text):
            hits.append({"line": line_number(text, match.start()), "label": label, "context": snippet(text, match.start(), match.end(), width)})
    return sorted(hits, key=lambda hit: (int(hit["line"]), str(hit["label"])))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True)
    parser.add_argument("--term", action="append", default=[])
    parser.add_argument("--context-chars", type=int, default=80)
    parser.add_argument("--max-hits", type=int, default=200)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.text)
    hits = scan(path.read_text(encoding="utf-8-sig"), args.term, args.context_chars)
    shown = hits[:args.max_hits]
    if args.json:
        print(json.dumps({"text": str(path), "hits": len(hits), "results": shown}, ensure_ascii=False, indent=2))
    else:
        print(f"text={path}")
        print(f"hits={len(hits)}")
        for hit in shown:
            print(f"line={hit['line']}\tterm={hit['label']}\tcontext={hit['context']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
