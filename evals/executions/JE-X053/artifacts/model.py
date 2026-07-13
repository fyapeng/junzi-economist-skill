from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import least_squares


ROOT = Path(__file__).resolve().parent
SEED = 20260713
M, J = 4000, 3
TRUE = np.array([18.0, 0.7, 4.0, 0.8])  # alpha, beta, c0, c1
LOWER = np.array([10.0, 0.2, 2.0, 0.1])
UPPER = np.array([25.0, 1.5, 6.0, 1.5])
STARTS = np.array([
    [18.0, 0.7, 4.0, 0.8],
    [11.0, 0.25, 2.2, 0.2],
    [24.0, 1.40, 5.8, 1.4],
    [15.0, 1.20, 3.0, 1.2],
    [22.0, 0.35, 5.0, 0.4],
    [19.5, 0.95, 3.5, 1.0],
])
RAW_TOL = 1e-9
SCALED_TOL = 1e-8


def dump(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")


def dgp() -> dict[str, np.ndarray]:
    rng = np.random.default_rng(SEED)
    market_id = np.arange(M, dtype=np.int64)
    z_cost = rng.uniform(-1.0, 1.0, size=(M, J))  # t=0, observed before shocks
    omega = rng.normal(0.0, 0.15, size=(M, J))    # t=1 cost shock
    eta = rng.normal(0.0, 0.40, size=M)           # t=1 demand shock
    alpha, beta, c0, c1 = TRUE
    mc = c0 + c1 * z_cost + omega
    intercept = alpha + eta
    q = (intercept[:, None] + mc.sum(axis=1)[:, None] - (J + 1) * mc) / (beta * (J + 1))
    if not np.all(q > 0):
        raise RuntimeError("DGP primitive domain failed: nonpositive Cournot quantity")
    Q = q.sum(axis=1)
    price = intercept - beta * Q
    # t=3: deliberately invalid instrument is created only after equilibrium outcomes exist.
    invalid_noise = rng.normal(0.0, 0.05, size=M)
    z_invalid_post = eta + invalid_noise
    return dict(market_id=market_id, z_cost=z_cost, omega=omega, eta=eta, mc=mc,
                q=q, Q=Q, price=price, z_invalid_post=z_invalid_post,
                planned_market_id=np.arange(M, dtype=np.int64))


def moments(theta: np.ndarray, d: dict[str, np.ndarray], invalid: bool = False) -> np.ndarray:
    alpha, beta, c0, c1 = theta
    zd = d["z_invalid_post"] if invalid else d["z_cost"].mean(axis=1)
    dem = d["price"] - alpha + beta * d["Q"]
    cost = d["price"][:, None] - beta * d["q"] - c0 - c1 * d["z_cost"]
    return np.array([dem.mean(), np.mean(zd * dem), cost.mean(), np.mean(d["z_cost"] * cost)])


def moment_scales(d: dict[str, np.ndarray], invalid: bool = False) -> np.ndarray:
    zd = d["z_invalid_post"] if invalid else d["z_cost"].mean(axis=1)
    return np.array([1.0, max(float(np.std(zd)), 0.1), 1.0, float(np.std(d["z_cost"]))])


def estimate(d: dict[str, np.ndarray], invalid: bool, label: str) -> tuple[list[dict], np.ndarray]:
    scales = moment_scales(d, invalid)
    records: list[dict] = []
    terminals = []
    for sid, x0 in enumerate(STARTS):
        trace = []
        def fun(x: np.ndarray) -> np.ndarray:
            raw = moments(x, d, invalid)
            scaled = raw / scales
            trace.append({"evaluation": len(trace), "theta": x.tolist(), "raw": raw.tolist(),
                          "scaled": scaled.tolist(), "raw_max": float(np.max(np.abs(raw))),
                          "scaled_max": float(np.max(np.abs(scaled)))})
            return scaled
        sol = least_squares(fun, x0, bounds=(LOWER, UPPER), xtol=1e-14, ftol=1e-14,
                            gtol=1e-14, max_nfev=1000)
        raw = moments(sol.x, d, invalid)
        scaled = raw / scales
        accepted = bool(sol.success and np.max(np.abs(raw)) < RAW_TOL and
                        np.max(np.abs(scaled)) < SCALED_TOL and
                        np.all(sol.x >= LOWER) and np.all(sol.x <= UPPER))
        rec = {"label": label, "start_id": sid, "start": x0.tolist(), "terminal": sol.x.tolist(),
               "terminal_hex": [float(v).hex() for v in sol.x], "objective": float(np.dot(scaled, scaled)),
               "raw": raw.tolist(), "scaled": scaled.tolist(), "raw_max": float(np.max(np.abs(raw))),
               "scaled_max": float(np.max(np.abs(scaled))), "active_lower": np.isclose(sol.x, LOWER, atol=1e-10).tolist(),
               "active_upper": np.isclose(sol.x, UPPER, atol=1e-10).tolist(),
               "success": bool(sol.success), "status": int(sol.status), "message": sol.message,
               "nfev": int(sol.nfev), "accepted": accepted, "trace_length": len(trace)}
        records.append(rec)
        terminals.append(sol.x.copy())
        with (ROOT / f"trace_estimation_{label}_start{sid}.jsonl").open("w", encoding="utf-8", newline="\n") as f:
            for row in trace:
                f.write(json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n")
    return records, np.vstack(terminals)


def equilibrium_checks(d: dict[str, np.ndarray]) -> tuple[list[dict], np.ndarray]:
    rng = np.random.default_rng(SEED + 1)
    records, terminals = [], []
    for m in [0, 17, 901, 2026, 3999]:
        a = TRUE[0] + d["eta"][m]
        beta = TRUE[1]
        mc = d["mc"][m]
        analytic = d["q"][m]
        matrix = beta * (np.eye(J) + np.ones((J, J)))
        # FOC residual is a - mc - beta*(Q + q_j).
        starts = [analytic, np.full(J, 0.1), np.full(J, 10.0), rng.uniform(0.0, 20.0, J)]
        for sid, x0 in enumerate(starts):
            trace = []
            scale = max(float(a), 1.0)
            def foc(qv: np.ndarray) -> np.ndarray:
                raw = a - mc - beta * (qv.sum() + qv)
                trace.append({"evaluation": len(trace), "q": qv.tolist(), "raw": raw.tolist(),
                              "scaled": (raw / scale).tolist(), "raw_max": float(np.max(np.abs(raw))),
                              "scaled_max": float(np.max(np.abs(raw / scale)))})
                return raw / scale
            sol = least_squares(foc, x0, bounds=(np.zeros(J), np.full(J, 20.0)),
                                xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=1000)
            raw = a - mc - beta * (sol.x.sum() + sol.x)
            scaled = raw / scale
            rec = {"market": m, "start_id": sid, "start": np.asarray(x0).tolist(),
                   "terminal": sol.x.tolist(), "terminal_hex": [float(v).hex() for v in sol.x],
                   "analytic": analytic.tolist(), "raw": raw.tolist(), "scaled": scaled.tolist(),
                   "raw_max": float(np.max(np.abs(raw))), "scaled_max": float(np.max(np.abs(scaled))),
                   "distance_to_analytic": float(np.max(np.abs(sol.x - analytic))),
                   "matrix_min_eigenvalue": float(np.linalg.eigvalsh(matrix).min()),
                   "within_bounds": bool(np.all(sol.x >= 0) and np.all(sol.x <= 20)),
                   "success": bool(sol.success), "accepted": bool(sol.success and np.max(np.abs(raw)) < RAW_TOL and np.max(np.abs(scaled)) < SCALED_TOL),
                   "trace_length": len(trace)}
            records.append(rec); terminals.append(sol.x.copy())
            with (ROOT / f"trace_equilibrium_market{m}_start{sid}.jsonl").open("w", encoding="utf-8", newline="\n") as f:
                for row in trace:
                    f.write(json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n")
    return records, np.vstack(terminals)


def iv_beta(d: dict[str, np.ndarray], z: np.ndarray) -> float:
    zc = z - z.mean(); qc = d["Q"] - d["Q"].mean(); pc = d["price"] - d["price"].mean()
    return float(-np.dot(zc, pc) / np.dot(zc, qc))


def main() -> None:
    d = dgp()
    np.savez(ROOT / "primitives.npz", **d)
    timeline = {
        "t0": "planned market IDs and z_cost drawn and observed",
        "t1": "omega and eta realized; marginal costs and demand intercept fixed",
        "t2": "Cournot quantities and price solved using only t0-t1 objects",
        "t3": "z_invalid_post = eta + independent noise constructed after outcomes; unavailable to and unused by the t2 decision rule",
        "valid_exclusion": "z_cost is independent of eta by construction and absent from inverse demand",
        "invalid_exclusion": "z_invalid_post contains eta directly, so E[z_invalid_post * eta] != 0",
    }
    dump(ROOT / "timing.json", timeline)
    valid_records, valid_terminal = estimate(d, False, "valid")
    invalid_records, invalid_terminal = estimate(d, True, "invalid")
    eq_records, eq_terminal = equilibrium_checks(d)
    np.savez(ROOT / "terminal_vectors_full_precision.npz", valid=valid_terminal,
             invalid=invalid_terminal, equilibrium=eq_terminal)
    # Mandatory actual reload: acceptance is recomputed from reloaded binary64 vectors.
    rt = np.load(ROOT / "terminal_vectors_full_precision.npz", allow_pickle=False)
    rt_checks = []
    for label, invalid in [("valid", False), ("invalid", True)]:
        source_records = valid_records if not invalid else invalid_records
        for sid, theta in enumerate(rt[label]):
            raw = moments(theta, d, invalid); scaled = raw / moment_scales(d, invalid)
            accepted = bool(np.max(np.abs(raw)) < RAW_TOL and np.max(np.abs(scaled)) < SCALED_TOL)
            rt_checks.append({"kind": label, "id": sid, "bitwise_equal": bool(np.array_equal(theta, (valid_terminal if not invalid else invalid_terminal)[sid])),
                              "raw_max": float(np.max(np.abs(raw))), "scaled_max": float(np.max(np.abs(scaled))),
                              "accepted": accepted, "expected_accepted": bool(source_records[sid]["accepted"]),
                              "diagnostic_reproduced": accepted == bool(source_records[sid]["accepted"])})
    eq_i = 0
    for rec in eq_records:
        qv = rt["equilibrium"][eq_i]; m = rec["market"]; a = TRUE[0] + d["eta"][m]; mc = d["mc"][m]
        raw = a - mc - TRUE[1] * (qv.sum() + qv); scale = max(float(a), 1.0)
        rt_checks.append({"kind": "equilibrium", "id": eq_i, "bitwise_equal": bool(np.array_equal(qv, eq_terminal[eq_i])),
                          "raw_max": float(np.max(np.abs(raw))), "scaled_max": float(np.max(np.abs(raw / scale))),
                          "accepted": bool(np.max(np.abs(raw)) < RAW_TOL and np.max(np.abs(raw / scale)) < SCALED_TOL),
                          "expected_accepted": True, "diagnostic_reproduced": bool(np.max(np.abs(raw)) < RAW_TOL and np.max(np.abs(raw / scale)) < SCALED_TOL)})
        eq_i += 1
    dump(ROOT / "roundtrip_diagnostics.json", rt_checks)

    Q, p, q, mc = d["Q"], d["price"], d["q"], d["mc"]
    revenue = p * Q; variable_cost = np.sum(mc * q, axis=1); profit = revenue - variable_cost
    consumer_surplus = 0.5 * TRUE[1] * Q ** 2; total_welfare = consumer_surplus + profit
    accounting = {
        "levels": {"consumer_expenditure": float(np.sum(p * Q)), "producer_revenue": float(revenue.sum()),
                   "variable_cost": float(variable_cost.sum()), "producer_profit": float(profit.sum()),
                   "consumer_surplus": float(consumer_surplus.sum()), "total_welfare": float(total_welfare.sum())},
        "identity_residuals": {"expenditure_minus_revenue": float(np.sum(p * Q) - revenue.sum()),
                               "profit_minus_revenue_plus_cost": float(profit.sum() - revenue.sum() + variable_cost.sum()),
                               "welfare_minus_cs_minus_profit": float(total_welfare.sum() - consumer_surplus.sum() - profit.sum())},
        "scope": "market totals summed over all planned markets; transfers absent; only variable production cost included"
    }
    dump(ROOT / "accounting.json", accounting)
    zvalid = d["z_cost"].mean(axis=1); zinvalid = d["z_invalid_post"]
    summary = {
        "dgp": {"seed": SEED, "planned_markets": M, "realized_markets": int(len(d["market_id"])),
                "firms_per_market": J, "realized_rows": int(q.size), "redraws": 0, "dropped_markets": 0,
                "market_ids_exact": bool(np.array_equal(d["planned_market_id"], d["market_id"])),
                "all_quantities_positive": bool(np.all(q > 0))},
        "true_parameters": TRUE.tolist(), "estimator_bounds": {"lower": LOWER.tolist(), "upper": UPPER.tolist()},
        "instrument_results": {"corr_valid_eta": float(np.corrcoef(zvalid, d["eta"])[0, 1]),
                               "corr_invalid_eta": float(np.corrcoef(zinvalid, d["eta"])[0, 1]),
                               "first_stage_corr_valid_Q": float(np.corrcoef(zvalid, Q)[0, 1]),
                               "iv_beta_valid": iv_beta(d, zvalid), "iv_beta_invalid": iv_beta(d, zinvalid)},
        "valid_estimation": valid_records, "invalid_estimation": invalid_records,
        "equilibrium": eq_records,
        "headline": {"all_valid_starts_accepted": all(r["accepted"] for r in valid_records),
                     "all_invalid_starts_accepted": all(r["accepted"] for r in invalid_records),
                     "all_equilibrium_starts_accepted": all(r["accepted"] for r in eq_records),
                     "valid_terminal_spread": float(np.ptp(valid_terminal, axis=0).max()),
                     "valid_max_abs_parameter_error": float(np.max(np.abs(valid_terminal[0] - TRUE))),
                     "all_roundtrip_diagnostics_reproduced": all(r["diagnostic_reproduced"] and r["bitwise_equal"] for r in rt_checks)}
    }
    dump(ROOT / "results.json", summary)
    dump(ROOT / "provenance.json", {"skill_commit": "539a1e8", "skill_files_read": [
        "skills/junzi-economist/SKILL.md", "skills/junzi-economist/references/EMPIRICAL_AND_STRUCTURAL_METHODS.md",
        "skills/junzi-economist/references/THEORY_MODELING.md", "skills/junzi-economist/references/SOFTWARE_AND_COMPUTATION.md"],
        "python": sys.version, "platform": platform.platform(), "numpy": np.__version__, "scipy": scipy.__version__,
        "seed": SEED, "float_serialization": "NumPy NPZ binary64 plus JSON float.hex terminals; NPZ was reloaded and acceptance recomputed"})
    if not (summary["headline"]["all_valid_starts_accepted"] and summary["headline"]["all_equilibrium_starts_accepted"] and summary["headline"]["all_roundtrip_diagnostics_reproduced"]):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
