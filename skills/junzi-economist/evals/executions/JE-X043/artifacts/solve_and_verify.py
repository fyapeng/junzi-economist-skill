from __future__ import annotations

import json
import math
import platform
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq, minimize_scalar


OUT = Path(r"C:\Users\ENAN\AppData\Local\Temp\junzi-economist-macro-x043")
OUT.mkdir(parents=True, exist_ok=True)

# Primitives, entered directly from the task.
SIGMA = 2.0
BETA = 0.94
ALPHA = 0.35
DELTA = 0.075
E_RAW = np.array([0.6, 1.4], dtype=float)
P = np.array([[0.88, 0.12], [0.18, 0.82]], dtype=float)

# Predeclared numerical thresholds. These are not relaxed later.
THRESH = {
    "egm_iteration_tol": 2.0e-10,
    "policy_fixed_point": 2.0e-7,
    "distribution_iteration_tol": 2.0e-13,
    "distribution_stationarity": 2.0e-11,
    "distribution_mass": 2.0e-13,
    "euler_interior_max": 2.0e-2,
    "euler_kkt_max": 2.0e-8,
    "minimum_consumption": 1.0e-10,
    "tail_mass_last_2pct": 2.0e-7,
    "policy_top_ratio": 0.999,
    "policy_top_clip_share": 0.0,
    "transition_row_error": 2.0e-14,
    "resource_identity_consistency": 2.0e-10,
    "scan_market_residual_cap": 25.0,
    "scan_resource_residual_cap": 25.0,
    "root_market_clearing": 2.0e-7,
    "root_resource_clearing": 2.0e-7,
    "tangency_market_clearing": 2.0e-7,
}

SCAN_R = np.linspace(0.002, 0.060, 59)

CONFIGS = [
    # a_max=50 was rejected in a preliminary strict run because the root region
    # failed the predeclared tail/truncation tests. We backtrack the grid design,
    # not the thresholds, and use 100 as the common comparison baseline.
    {"name": "baseline", "n_assets": 700, "a_max": 100.0},
    {"name": "asset_grid_only", "n_assets": 1400, "a_max": 100.0},
    {"name": "asset_bound_only", "n_assets": 700, "a_max": 200.0},
]


def invariant_markov(p: np.ndarray) -> np.ndarray:
    a = np.vstack((p.T - np.eye(p.shape[0]), np.ones(p.shape[0])))
    b = np.r_[np.zeros(p.shape[0]), 1.0]
    pi, *_ = np.linalg.lstsq(a, b, rcond=None)
    return pi


PI_E = invariant_markov(P)
E = E_RAW / float(PI_E @ E_RAW)


def prices(r: float) -> tuple[float, float, float]:
    if not (-DELTA < r < 1.0 / BETA - 1.0):
        raise ValueError("price outside economically admissible interval")
    k = (ALPHA / (r + DELTA)) ** (1.0 / (1.0 - ALPHA))
    y = k**ALPHA
    w = (1.0 - ALPHA) * y
    return k, w, y


def interp_rows(x: np.ndarray, grid: np.ndarray, vals: np.ndarray) -> np.ndarray:
    out = np.empty_like(x)
    for z in range(x.shape[0]):
        out[z] = np.interp(x[z], grid, vals[z])
    return out


@dataclass
class HouseholdSolution:
    c: np.ndarray
    ap: np.ndarray
    iterations: int
    iteration_diff: float
    fixed_point: float


def egm_step(c_old: np.ndarray, grid: np.ndarray, r: float, w: float) -> tuple[np.ndarray, np.ndarray]:
    R = 1.0 + r
    emu = P @ (c_old ** (-SIGMA))
    c_endo = (BETA * R * emu) ** (-1.0 / SIGMA)
    a_endo = (c_endo + grid[None, :] - w * E[:, None]) / R
    ap = np.empty_like(c_old)
    resources = R * grid[None, :] + w * E[:, None]
    for z in range(P.shape[0]):
        ap[z] = np.interp(grid, a_endo[z], grid, left=0.0, right=grid[-1])
    ap = np.minimum(np.maximum(ap, 0.0), resources - THRESH["minimum_consumption"])
    c = resources - ap
    return c, ap


def solve_household(grid: np.ndarray, r: float, w: float, initial_c: np.ndarray | None) -> HouseholdSolution:
    R = 1.0 + r
    if initial_c is None or initial_c.shape != (2, grid.size):
        c = np.maximum(r * grid[None, :] + w * E[:, None] + 0.02, 1e-4)
    else:
        c = initial_c.copy()
    diff = math.inf
    for it in range(1, 10001):
        c_new, ap_new = egm_step(c, grid, r, w)
        diff = float(np.max(np.abs(c_new - c) / np.maximum(1.0, np.abs(c))))
        c = c_new
        if diff <= THRESH["egm_iteration_tol"]:
            break
    else:
        raise RuntimeError("EGM did not converge")
    c_check, ap_check = egm_step(c, grid, r, w)
    fixed = float(np.max(np.abs(ap_check - ap_new) / np.maximum(1.0, grid[-1])))
    return HouseholdSolution(c=c, ap=ap_new, iterations=it, iteration_diff=diff, fixed_point=fixed)


def policy_transition(grid: np.ndarray, ap: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    n = grid.size
    hi = np.searchsorted(grid, ap, side="right")
    hi = np.clip(hi, 1, n - 1)
    lo = hi - 1
    denom = grid[hi] - grid[lo]
    whi = np.divide(ap - grid[lo], denom, out=np.zeros_like(ap), where=denom > 0)
    whi = np.clip(whi, 0.0, 1.0)
    row_err = float(np.max(np.abs((1.0 - whi) + whi - 1.0)))
    return lo, hi, whi, row_err


def stationary_distribution(grid: np.ndarray, ap: np.ndarray) -> tuple[np.ndarray, dict]:
    n = grid.size
    lo, hi, whi, row_err = policy_transition(grid, ap)
    mu = PI_E[:, None] * np.ones((2, n)) / n

    def advance(x: np.ndarray) -> np.ndarray:
        nxt = np.zeros_like(x)
        for z in range(2):
            for zp in range(2):
                mass = x[z] * P[z, zp]
                np.add.at(nxt[zp], lo[z], mass * (1.0 - whi[z]))
                np.add.at(nxt[zp], hi[z], mass * whi[z])
        return nxt

    d = math.inf
    for it in range(1, 50001):
        nxt = advance(mu)
        d = float(np.max(np.abs(nxt - mu)))
        mu = nxt
        if d <= THRESH["distribution_iteration_tol"]:
            break
    else:
        raise RuntimeError("distribution iteration did not converge")
    stationarity = float(np.max(np.abs(advance(mu) - mu)))
    return mu, {
        "iterations": it,
        "iteration_diff": d,
        "stationarity": stationarity,
        "mass_error": float(abs(mu.sum() - 1.0)),
        "transition_row_error": row_err,
    }


def household_diagnostics(grid: np.ndarray, r: float, c: np.ndarray, ap: np.ndarray, mu: np.ndarray) -> dict:
    R = 1.0 + r
    c_next = interp_rows(np.broadcast_to(ap[:, None, :], (2, 2, grid.size)).reshape(4, grid.size), grid,
                         np.repeat(c[None, :, :], 2, axis=0).reshape(4, grid.size)).reshape(2, 2, grid.size)
    rhs = BETA * R * np.sum(P[:, :, None] * c_next ** (-SIGMA), axis=1)
    lhs = c ** (-SIGMA)
    ratio = rhs / lhs
    constrained = ap <= 1e-12
    # The two top grid nodes are governed by the separately executed tail/truncation tests.
    eligible_interior = (~constrained)
    eligible_interior[:, -2:] = False
    euler = np.abs(1.0 - ratio)
    interior_max = float(np.max(euler[eligible_interior])) if np.any(eligible_interior) else 0.0
    kkt_max = float(np.max(np.maximum(ratio[constrained] - 1.0, 0.0))) if np.any(constrained) else 0.0
    tail = grid >= 0.98 * grid[-1]
    top_clip = ap >= grid[-1] * (1.0 - 5e-14)
    return {
        "euler_interior_max": interior_max,
        "euler_mu_weighted_mean": float(np.sum(mu * euler)),
        "euler_kkt_max": kkt_max,
        "minimum_consumption": float(c.min()),
        "tail_mass_last_2pct": float(mu[:, tail].sum()),
        "policy_top_ratio": float(ap.max() / grid[-1]),
        "policy_top_clip_share": float(np.mean(top_clip)),
    }


class Evaluator:
    def __init__(self, config: dict):
        self.config = config
        self.grid = config["a_max"] * np.linspace(0.0, 1.0, config["n_assets"]) ** 2
        self.cache: dict[float, dict] = {}
        self.trace: list[dict] = []

    def evaluate(self, r: float, stage: str) -> dict:
        key = float(r)
        if key in self.cache:
            old = self.cache[key]
            self.trace.append({"stage": stage, "r": key, "cached": True, "reliable": old["reliable"],
                               "signed_market_residual": old["signed_market_residual"]})
            return old
        k_demand, w, y = prices(key)
        initial = None
        if self.cache:
            nearest = min(self.cache, key=lambda q: abs(q - key))
            initial = self.cache[nearest]["_c"]
        hh = solve_household(self.grid, key, w, initial)
        mu, ddiag = stationary_distribution(self.grid, hh.ap)
        hdiag = household_diagnostics(self.grid, key, hh.c, hh.ap, mu)
        assets = float(np.sum(mu * self.grid[None, :]))
        consumption = float(np.sum(mu * hh.c))
        market = (assets - k_demand) / max(1.0, k_demand)
        resource = (y - consumption - DELTA * k_demand) / max(1.0, y)
        # At arbitrary trial prices, resource and asset gaps need not vanish. Their exact
        # accounting link must hold: Y-C-delta Kd = r(Kd-A), using C=rA+wL.
        resource_identity = abs((y - consumption - DELTA * k_demand) - key * (k_demand - assets)) / max(1.0, y)
        checks = {
            "policy_fixed_point": hh.fixed_point <= THRESH["policy_fixed_point"],
            "distribution_stationarity": ddiag["stationarity"] <= THRESH["distribution_stationarity"],
            "distribution_mass": ddiag["mass_error"] <= THRESH["distribution_mass"],
            "transition_row_error": ddiag["transition_row_error"] <= THRESH["transition_row_error"],
            "euler_interior": hdiag["euler_interior_max"] <= THRESH["euler_interior_max"],
            "euler_kkt": hdiag["euler_kkt_max"] <= THRESH["euler_kkt_max"],
            "consumption_feasible": hdiag["minimum_consumption"] > THRESH["minimum_consumption"],
            "tail_mass": hdiag["tail_mass_last_2pct"] <= THRESH["tail_mass_last_2pct"],
            "policy_top_ratio": hdiag["policy_top_ratio"] <= THRESH["policy_top_ratio"],
            "policy_top_clip_share": hdiag["policy_top_clip_share"] <= THRESH["policy_top_clip_share"],
            "resource_identity": resource_identity <= THRESH["resource_identity_consistency"],
            "scan_market_finite_and_bounded": math.isfinite(market) and abs(market) <= THRESH["scan_market_residual_cap"],
            "scan_resource_finite_and_bounded": math.isfinite(resource) and abs(resource) <= THRESH["scan_resource_residual_cap"],
        }
        reliable = all(checks.values())
        rec = {
            "r": key, "w": w, "capital_demand": k_demand, "asset_supply": assets,
            "output": y, "consumption": consumption,
            "signed_market_residual": market, "signed_resource_residual": resource,
            "resource_identity_consistency": resource_identity,
            "household": {"iterations": hh.iterations, "iteration_diff": hh.iteration_diff,
                          "policy_fixed_point": hh.fixed_point, **hdiag},
            "distribution": ddiag, "checks": checks, "reliable": reliable,
            "_c": hh.c,
        }
        self.cache[key] = rec
        self.trace.append({"stage": stage, "r": key, "cached": False, "reliable": reliable,
                           "signed_market_residual": market, "failed_checks": [k for k, v in checks.items() if not v]})
        return rec

    def objective(self, r: float, stage: str) -> float:
        z = self.evaluate(float(r), stage)
        if not z["reliable"]:
            raise ValueError(f"unreliable internal evaluation at r={r}: {[k for k,v in z['checks'].items() if not v]}")
        return z["signed_market_residual"]


def cleaned(rec: dict) -> dict:
    return {k: v for k, v in rec.items() if not k.startswith("_")}


def run_config(config: dict) -> dict:
    ev = Evaluator(config)
    scan = [ev.evaluate(float(r), "scan") for r in SCAN_R]
    brackets = []
    invalid_adjacent = []
    for left, right in zip(scan[:-1], scan[1:]):
        if not (left["reliable"] and right["reliable"]):
            if left["signed_market_residual"] * right["signed_market_residual"] <= 0:
                invalid_adjacent.append([left["r"], right["r"]])
            continue
        fl, fr = left["signed_market_residual"], right["signed_market_residual"]
        if fl == 0.0 or fr == 0.0 or fl * fr < 0.0:
            brackets.append([left["r"], right["r"]])

    roots = []
    for j, (lo, hi) in enumerate(brackets):
        try:
            root = brentq(lambda x: ev.objective(x, f"root_{j}"), lo, hi, xtol=2e-10, rtol=2e-10, maxiter=100)
            rr = ev.evaluate(float(root), f"root_{j}_final")
            root_checks = {
                "point_reliable": rr["reliable"],
                "market_clearing": abs(rr["signed_market_residual"]) <= THRESH["root_market_clearing"],
                "resource_clearing": abs(rr["signed_resource_residual"]) <= THRESH["root_resource_clearing"],
            }
            roots.append({"bracket": [lo, hi], "r": float(root), "accepted": all(root_checks.values()),
                          "root_checks": root_checks, "evaluation": cleaned(rr)})
        except Exception as exc:
            roots.append({"bracket": [lo, hi], "accepted": False, "error": repr(exc)})

    # Non-crossing screen: exclude scan nodes in or adjacent to every sign-change bracket.
    excluded = set()
    for i, (left, right) in enumerate(zip(scan[:-1], scan[1:])):
        if [left["r"], right["r"]] in brackets:
            excluded.update({max(0, i - 1), i, i + 1, min(len(scan) - 1, i + 2)})
    tangent_candidates = []
    for i in range(1, len(scan) - 1):
        a, b, c = scan[i - 1:i + 2]
        if i in excluded or not (a["reliable"] and b["reliable"] and c["reliable"]):
            continue
        fa, fb, fc = (q["signed_market_residual"] for q in (a, b, c))
        same_positive = fa > 0 and fb > 0 and fc > 0 and fb <= fa and fb <= fc
        same_negative = fa < 0 and fb < 0 and fc < 0 and fb >= fa and fb >= fc
        if not (same_positive or same_negative):
            continue
        sign = 1.0 if same_positive else -1.0
        eval_failed = False
        try:
            opt = minimize_scalar(lambda x: sign * ev.objective(x, f"tangent_{i}"),
                                  bounds=(a["r"], c["r"]), method="bounded",
                                  options={"xatol": 2e-9, "maxiter": 100})
            rr = ev.evaluate(float(opt.x), f"tangent_{i}_final")
            accepted = (opt.success and rr["reliable"] and
                        abs(rr["signed_market_residual"]) <= THRESH["tangency_market_clearing"] and
                        abs(rr["signed_resource_residual"]) <= THRESH["root_resource_clearing"])
            tangent_candidates.append({"scan_triplet": [a["r"], b["r"], c["r"]],
                                       "kind": "positive_local_min" if same_positive else "negative_local_max",
                                       "r": float(opt.x), "signed_market_residual": rr["signed_market_residual"],
                                       "accepted_as_non_crossing_root": bool(accepted), "optimizer_success": bool(opt.success)})
        except Exception as exc:
            eval_failed = True
            tangent_candidates.append({"scan_triplet": [a["r"], b["r"], c["r"]],
                                       "accepted_as_non_crossing_root": False, "error": repr(exc),
                                       "rejected_due_to_unreliable_internal_point": eval_failed})

    serial_scan = [cleaned(x) for x in scan]
    serial_cache = [cleaned(ev.cache[k]) for k in sorted(ev.cache)]
    return {
        "config": config,
        "scan": serial_scan,
        "reliable_scan_count": sum(x["reliable"] for x in scan),
        "unreliable_scan_points": [{"r": x["r"], "failed_checks": [k for k, v in x["checks"].items() if not v]} for x in scan if not x["reliable"]],
        "sign_change_brackets": brackets,
        "invalid_sign_adjacent_to_unreliable_point": invalid_adjacent,
        "roots": roots,
        "noncrossing_screen": {
            "method": "same-sign signed-residual local extrema, excluding sign-change neighborhoods",
            "candidates": tangent_candidates,
            "limitation": "Finite grid and bounded local searches cannot rule out extrema between sampled intervals or outside the scanned reliable domain."
        },
        "evaluation_trace": ev.trace,
        "all_unique_evaluations": serial_cache,
    }


def main() -> None:
    results = {
        "task": "JE-X043",
        "primitives": {"sigma": SIGMA, "beta": BETA, "alpha": ALPHA, "delta": DELTA,
                       "efficiency_raw": E_RAW.tolist(), "transition": P.tolist()},
        "stationary_efficiency_distribution": PI_E.tolist(),
        "normalized_efficiency": E.tolist(),
        "effective_labor": float(PI_E @ E),
        "thresholds": THRESH,
        "scan_r": SCAN_R.tolist(),
        "software": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__,
                     "platform": platform.platform()},
        "configurations": [],
    }
    for config in CONFIGS:
        print(f"RUN {config['name']} n={config['n_assets']} amax={config['a_max']}", flush=True)
        out = run_config(config)
        results["configurations"].append(out)
        accepted = [x for x in out["roots"] if x.get("accepted")]
        print(f"  reliable scan {out['reliable_scan_count']}/{len(SCAN_R)}; brackets={out['sign_change_brackets']}", flush=True)
        print(f"  accepted roots={[x['r'] for x in accepted]}", flush=True)
    base_roots = [x for x in results["configurations"][0]["roots"] if x.get("accepted")]
    comparisons = []
    if len(base_roots) == 1:
        b = base_roots[0]
        for cfg in results["configurations"][1:]:
            rr = [x for x in cfg["roots"] if x.get("accepted")]
            if len(rr) == 1:
                q = rr[0]
                comparisons.append({
                    "configuration": cfg["config"]["name"],
                    "delta_r_vs_baseline": q["r"] - b["r"],
                    "delta_market_residual_vs_baseline": q["evaluation"]["signed_market_residual"] - b["evaluation"]["signed_market_residual"],
                    "delta_resource_residual_vs_baseline": q["evaluation"]["signed_resource_residual"] - b["evaluation"]["signed_resource_residual"],
                })
    results["one_dimension_comparisons"] = comparisons
    with (OUT / "results.json").open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("WROTE results.json", flush=True)


if __name__ == "__main__":
    main()
