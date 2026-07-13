from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    records = []
    for stage in ("simulation", "equilibrium", "estimation"):
        target = root / "results" / f"forced_{stage}"
        proc = subprocess.run([sys.executable, str(root / "run_simulation.py"), "--output", str(target),
                               "--force-failure", stage], capture_output=True, text=True)
        diag_path = target / "failure_diagnostic.json"
        diag = json.loads(diag_path.read_text(encoding="utf-8")) if diag_path.exists() else None
        records.append({"stage": stage, "exit_code": proc.returncode,
                        "diagnostic_written_before_exit": diag is not None, "diagnostic": diag})
    report = {"status": "passed" if all(r["exit_code"] != 0 and r["diagnostic_written_before_exit"] for r in records) else "failed",
              "requirement": "each isolated whole-replication failure writes diagnostics and exits nonzero",
              "records": records}
    (root / "results" / "process_failure_tests.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if report["status"] == "passed" else 4


if __name__ == "__main__":
    sys.exit(main())
