from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parent

def write(mode: str, diagnostic: dict) -> None:
    diagnostic.update({"mode": mode, "required_unit_failed": True, "process_must_exit_nonzero": True})
    (ROOT / f"failure_{mode}.json").write_text(json.dumps(diagnostic, indent=2, allow_nan=False), encoding="utf-8")

p = argparse.ArgumentParser(); p.add_argument("mode", choices=["simulation", "equilibrium", "estimation"]); a = p.parse_args()
if a.mode == "simulation":
    planned, realized = 4000, 3999
    write(a.mode, {"planned_markets": planned, "realized_markets": realized, "invariant": "realized == planned", "accepted": realized == planned})
    raise SystemExit(31)
if a.mode == "equilibrium":
    beta = 0.0; matrix = beta * (np.eye(3) + np.ones((3, 3)))
    write(a.mode, {"beta": beta, "matrix_rank": int(np.linalg.matrix_rank(matrix)), "required_rank": 3,
                   "accepted": bool(np.linalg.matrix_rank(matrix) == 3)})
    raise SystemExit(32)
if a.mode == "estimation":
    # Deliberately one evaluation: cannot meet the declared root tolerance.
    sol = least_squares(lambda x: np.array([x[0] - 18.0, x[1] - 0.7]), np.array([11.0, 1.4]), max_nfev=1)
    residual = np.array([sol.x[0] - 18.0, sol.x[1] - 0.7])
    accepted = bool(sol.success and np.max(np.abs(residual)) < 1e-9)
    write(a.mode, {"max_nfev": 1, "solver_success": bool(sol.success), "terminal": sol.x.tolist(),
                   "raw_max": float(np.max(np.abs(residual))), "tolerance": 1e-9, "accepted": accepted})
    raise SystemExit(33)
