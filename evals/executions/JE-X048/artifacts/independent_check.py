from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import root

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
ALPHA, BETA0, BETAX = 1.2, 2.0, 0.4


def independent_share(p, x, xi):
    a = np.exp(BETA0 + BETAX * x + xi - ALPHA * p)
    return a / (1 + a[0] + a[1])


def independent_foc(p, c, x, xi):
    s = independent_share(p, x, xi)
    ans = np.zeros(2)
    for j in range(2):
        ans[j] = s[j]
        for k in range(2):
            ds_k_dp_j = -ALPHA * s[k] * ((1.0 if k == j else 0.0) - s[j])
            ans[j] += (p[k] - c[k]) * ds_k_dp_j
    return ans


def finite_difference_profit_gradient(p, c, x, xi, h=1e-6):
    def profit(q):
        return float(np.dot(q - c, independent_share(q, x, xi)))
    grad = np.zeros(2)
    for j in range(2):
        step = np.zeros(2); step[j] = h
        grad[j] = (profit(p + step) - profit(p - step)) / (2*h)
    return grad


def main():
    data = pd.read_parquet(OUT / "equilibrium_data.parquet")
    checks = []
    failures = 0
    for (seed, scenario, market), g in data.groupby(["seed", "scenario", "market"], sort=True):
        p = g.price.to_numpy(); x = g.x.to_numpy(); xi = g.xi.to_numpy()
        c = g.real_mc.to_numpy() - g.subsidy_rate.to_numpy()
        # Independent scipy.root solve from a fixed, non-production initialization.
        sol = root(lambda q: independent_foc(q, c, x, xi), c + np.array([1.3, 1.7]), method="hybr")
        raw = independent_foc(p, c, x, xi)
        fd = finite_difference_profit_gradient(p, c, x, xi)
        price_gap = float(np.max(np.abs(sol.x - p))) if sol.success else np.inf
        ok = bool(sol.success and np.max(np.abs(raw)) < 1e-10 and
                  np.max(np.abs(fd)) < 2e-9 and price_gap < 1e-7)
        failures += int(not ok)
        checks.append({"seed": seed, "scenario": scenario, "market": market,
                       "root_success": bool(sol.success), "independent_raw_foc_max": float(np.max(np.abs(raw))),
                       "finite_difference_profit_gradient_max": float(np.max(np.abs(fd))),
                       "independent_solve_price_gap": price_gap, "accepted": ok})
    pd.DataFrame(checks).to_csv(OUT / "independent_checks.csv", index=False, encoding="utf-8-sig")
    summary = {"checks": len(checks), "failures": failures,
               "status": "pass" if failures == 0 else "fail",
               "note": "Separate equation implementation, fresh root solve, and finite-difference profit gradient."}
    (OUT / "independent_check_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
