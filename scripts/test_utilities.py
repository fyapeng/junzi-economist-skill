#!/usr/bin/env python3
"""Deterministic smoke tests for Junzi Economist manuscript utilities."""
from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = ROOT / "skills" / "junzi-economist" / "scripts"

def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], text=True, capture_output=True, encoding="utf-8")

def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        manuscript = folder / "稿件.md"
        bib = folder / "参考文献.bib"
        manuscript.write_text("联系 test@example.com。已有证据见 [@smith2020; @missing2021]。\n本文不是研究甲，而是研究乙。", encoding="utf-8-sig")
        bib.write_text("@article{smith2020,\n title={A}\n}\n", encoding="utf-8")
        cites = run(str(SKILL_SCRIPTS / "check_citekeys.py"), "--text", str(manuscript), "--bib", str(bib))
        assert cites.returncode == 1, cites.stdout + cites.stderr
        assert "missing=missing2021" in cites.stdout
        assert "example" not in cites.stdout
        lint = run(str(SKILL_SCRIPTS / "prose_lint.py"), "--text", str(manuscript), "--json")
        assert lint.returncode == 0, lint.stdout + lint.stderr
        assert "不是…而是" in lint.stdout
    print("utility tests passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
