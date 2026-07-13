from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import least_squares


TRUE = {"alpha": 1.6, "beta_x": 1.1}
M, J, MARKET_SIZE = 40, 5, 200
PRICE_BOX_WIDTH = 4.0
START_OFFSETS = (0.05, 0.8, 2.5)
SOLVER_TOL = 1e-10


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def fail(out: Path, stage: str, reason: str, details: dict | None = None) -> int:
    record = {"status": "failed", "stage": stage, "reason": reason, "details": details or {}}
    write_json(out / "failure_diagnostic.json", record)
    print(json.dumps(record), file=sys.stderr)
    return 2


def shares(prices: np.ndarray, x: np.ndarray, xi: np.ndarray) -> tuple[np.ndarray, float]:
    util = TRUE["beta_x"] * x - TRUE["alpha"] * prices + xi
    e = np.exp(util)
    den = 1.0 + e.sum()
    return e / den, 1.0 / den


def foc(prices: np.ndarray, mc: np.ndarray, x: np.ndarray, xi: np.ndarray, subsidy: float) -> np.ndarray:
    s, _ = shares(prices, x, xi)
    return prices - (mc - subsidy) - 1.0 / (TRUE["alpha"] * (1.0 - s))


def solve_market(mc: np.ndarray, x: np.ndarray, xi: np.ndarray, subsidy: float) -> tuple[dict, list[dict]]:
    lo = mc - subsidy + 1e-8
    hi = mc - subsidy + PRICE_BOX_WIDTH
    traces: list[dict] = []
    candidates: list[dict] = []
    scale = max(1.0, float(np.max(np.abs(mc))))
    for start_id, offset in enumerate(START_OFFSETS):
        initial = np.clip(mc - subsidy + offset, lo + 1e-7, hi - 1e-7)
        result = least_squares(
            foc, initial, args=(mc, x, xi, subsidy), bounds=(lo, hi),
            xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=300,
        )
        raw = float(np.max(np.abs(foc(result.x, mc, x, xi, subsidy))))
        scaled = raw / scale
        row = {
            "start_id": start_id, "initial": initial.tolist(), "terminal": result.x.tolist(),
            "success_flag": bool(result.success), "status": int(result.status),
            "message": str(result.message), "nfev": int(result.nfev),
            "objective_half_sse": float(result.cost), "raw_max_foc": raw,
            "scaled_max_foc": scaled, "active_lower": bool(np.any(result.x - lo < 1e-7)),
            "active_upper": bool(np.any(hi - result.x < 1e-7)),
        }
        traces.append(row)
        if result.success and raw < SOLVER_TOL and not row["active_upper"]:
            candidates.append(row)
    if not candidates:
        raise RuntimeError("no accepted bounded equilibrium root across starts")
    best = min(candidates, key=lambda r: r["raw_max_foc"])
    accepted = np.asarray(best["terminal"])
    spread = max(float(np.max(np.abs(np.asarray(r["terminal"]) - accepted))) for r in candidates)
    return {"prices": accepted, "raw_max_foc": best["raw_max_foc"],
            "scaled_max_foc": best["scaled_max_foc"], "accepted_start": best["start_id"],
            "accepted_root_spread": spread, "root_claim": "accepted root found inside declared box; no global uniqueness claim"}, traces


def accounting(df: pd.DataFrame, subsidy: float) -> dict:
    q = MARKET_SIZE * df["share"].to_numpy()
    consumer_payment = float(np.sum(df["price"].to_numpy() * q))
    fiscal_payment = float(np.sum(subsidy * q))
    resource_cost = float(np.sum(df["mc"].to_numpy() * q))
    producer_receipts = consumer_payment + fiscal_payment
    profit = producer_receipts - resource_cost
    cs = 0.0
    for _, g in df.groupby("market", sort=True):
        u = TRUE["beta_x"] * g["x"].to_numpy() - TRUE["alpha"] * g["price"].to_numpy() + g["xi"].to_numpy()
        cs += MARKET_SIZE * np.log(1.0 + np.exp(u).sum()) / TRUE["alpha"]
    welfare = cs + profit - fiscal_payment
    direct_welfare = cs + consumer_payment - resource_cost
    return {
        "consumer_payment": consumer_payment, "fiscal_payment": fiscal_payment,
        "producer_receipts": producer_receipts, "real_resource_cost": resource_cost,
        "producer_profit": profit, "consumer_surplus_euler_zero_normalization": float(cs),
        "social_welfare": float(welfare), "direct_welfare_check": float(direct_welfare),
        "accounting_identity_abs_error": abs(welfare - direct_welfare),
    }


def iv_estimate(df: pd.DataFrame, invalid: bool = False) -> dict:
    y = np.log(df["share"].to_numpy()) - np.log(df["outside_share"].to_numpy())
    X = np.column_stack([np.ones(len(df)), df["x"].to_numpy(), df["price"].to_numpy()])
    z3 = df["z_invalid"].to_numpy() if invalid else df["z_cost"].to_numpy()
    Z = np.column_stack([np.ones(len(df)), df["x"].to_numpy(), z3])
    if np.linalg.matrix_rank(Z) < Z.shape[1] or np.linalg.matrix_rank(Z.T @ X) < X.shape[1]:
        raise RuntimeError("rank-deficient instrument system")
    theta = np.linalg.solve(Z.T @ X, Z.T @ y)
    resid = y - X @ theta
    return {
        "intercept": float(theta[0]), "beta_x": float(theta[1]), "price_coefficient": float(theta[2]),
        "alpha": float(-theta[2]), "max_abs_sample_moment": float(np.max(np.abs(Z.T @ resid / len(df)))),
        "instrument": "z_invalid_post_outcome" if invalid else "z_cost_pre_pricing",
        "rank_Z": int(np.linalg.matrix_rank(Z)), "rank_ZtX": int(np.linalg.matrix_rank(Z.T @ X)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--seed", type=int, default=73051)
    ap.add_argument("--force-failure", choices=["none", "simulation", "equilibrium", "estimation"], default="none")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "run_config.json", {"seed": args.seed, "markets": M, "products_per_market": J,
        "expected_rows": M * J, "market_size": MARKET_SIZE, "force_failure": args.force_failure,
        "price_box_width": PRICE_BOX_WIDTH, "starts": list(START_OFFSETS), "solver_tolerance": SOLVER_TOL})
    rng = np.random.default_rng(args.seed)
    n = M * J
    market = np.repeat(np.arange(M), J)
    product = np.tile(np.arange(J), M)
    x = rng.uniform(-0.8, 0.8, n)
    z_cost = rng.uniform(-0.7, 0.7, n)
    omega = rng.uniform(-0.12, 0.12, n)
    xi_raw = rng.uniform(-1.0, 1.0, n)
    A = np.column_stack([np.ones(n), x, z_cost])
    xi = xi_raw - A @ np.linalg.lstsq(A, xi_raw, rcond=None)[0]
    xi *= 0.35 / np.max(np.abs(xi))
    mc = 1.5 + 0.35 * x + 0.45 * z_cost + omega
    base = pd.DataFrame({"market": market, "product": product, "x": x, "z_cost": z_cost,
                         "omega": omega, "xi": xi, "mc": mc})
    if args.force_failure == "simulation":
        base = base.iloc[:-1].copy()
    if len(base) != n or not np.array_equal(base.groupby("market").size().to_numpy(), np.full(M, J)):
        return fail(out, "simulation", "declared exact-count DGP not realized",
                    {"expected_rows": n, "realized_rows": len(base), "no_redraw_attempted": True})
    if args.force_failure == "equilibrium":
        return fail(out, "equilibrium", "forced whole-replication equilibrium failure",
                    {"market": 0, "all_markets_required": True, "partial_sample_not_estimated": True})

    policy_frames: dict[str, pd.DataFrame] = {}
    all_traces: list[dict] = []
    equilibrium_summary = {}
    for label, subsidy in (("baseline", 0.0), ("subsidy", 0.12)):
        rows = []
        try:
            for m, g in base.groupby("market", sort=True):
                sol, traces = solve_market(g["mc"].to_numpy(), g["x"].to_numpy(), g["xi"].to_numpy(), subsidy)
                for t in traces:
                    all_traces.append({"policy": label, "market": int(m), **t})
                gg = g.copy()
                gg["price"] = sol["prices"]
                s, s0 = shares(sol["prices"], gg["x"].to_numpy(), gg["xi"].to_numpy())
                gg["share"], gg["outside_share"] = s, s0
                rows.append(gg)
        except Exception as exc:
            pd.DataFrame(all_traces).to_json(out / "equilibrium_starts.jsonl", orient="records", lines=True)
            return fail(out, "equilibrium", str(exc), {"policy": label, "all_markets_required": True})
        frame = pd.concat(rows, ignore_index=True)
        policy_frames[label] = frame
        equilibrium_summary[label] = {
            "markets": M, "raw_max_foc": max(t["raw_max_foc"] for t in all_traces if t["policy"] == label),
            "scaled_max_foc": max(t["scaled_max_foc"] for t in all_traces if t["policy"] == label),
            "max_root_spread_across_accepted_starts": max(
                max(np.max(np.abs(np.asarray(a["terminal"]) - np.asarray(b["terminal"])))
                    for b in all_traces if b["policy"] == label and b["market"] == a["market"] and b["success_flag"])
                for a in all_traces if a["policy"] == label and a["success_flag"]),
            "root_claim": "a root was recovered from every declared start in the bounded box; this finite search is not a uniqueness proof",
        }
    pd.DataFrame(all_traces).to_json(out / "equilibrium_starts.jsonl", orient="records", lines=True)

    baseline = policy_frames["baseline"].copy()
    # Deliberately invalid instrument: first constructed now, after xi, pricing, shares, and outcomes exist.
    # It was unavailable to and unused by the pricing solver, and violates demand exclusion by containing xi.
    invalid_noise = rng.uniform(-0.03, 0.03, n)
    invalid_merge = pd.DataFrame({"market": market, "product": product, "z_invalid": xi + invalid_noise})
    baseline = baseline.merge(invalid_merge, on=["market", "product"], how="left", validate="one_to_one")
    if args.force_failure == "estimation":
        baseline["z_cost"] = baseline["x"]
    try:
        valid_iv = iv_estimate(baseline, invalid=False)
        invalid_iv = iv_estimate(baseline, invalid=True)
    except Exception as exc:
        baseline.to_csv(out / "failed_estimation_input.csv", index=False, encoding="utf-8-sig")
        return fail(out, "estimation", str(exc), {"whole_replication_failed": True, "estimates_not_reported": True})
    if abs(valid_iv["alpha"] - TRUE["alpha"]) > 0.08 or abs(valid_iv["beta_x"] - TRUE["beta_x"]) > 0.08:
        return fail(out, "estimation", "valid-IV recovery tolerance exceeded", {"estimate": valid_iv, "truth": TRUE})

    baseline.to_csv(out / "baseline_data.csv", index=False, encoding="utf-8-sig")
    policy_frames["subsidy"].to_csv(out / "subsidy_data.csv", index=False, encoding="utf-8-sig")
    acct = {"baseline": accounting(baseline, 0.0), "subsidy": accounting(policy_frames["subsidy"], 0.12)}
    summary = {
        "status": "success", "dgp": {"declared_population": "40 markets x 5 products",
            "expected_rows": n, "realized_rows": len(baseline), "latent_conditioned_selection": False,
            "redraws": 0, "support": {"x": [-0.8, 0.8], "z_cost": [-0.7, 0.7], "omega": [-0.12, 0.12], "abs_xi_max": 0.35}},
        "timing": ["draw observed x and z_cost", "draw omega and xi; orthogonalize xi to valid instruments in this designed finite population",
            "merge z_cost into marginal cost before pricing", "solve prices and shares", "construct z_invalid = xi + noise after outcomes", "merge z_invalid only into estimation table"],
        "instrument_claims": {"valid": "z_cost is observed before pricing, shifts marginal cost and price, and is exactly orthogonal to designed xi",
            "invalid": "z_invalid is constructed after outcomes and contains xi, so it violates the demand exclusion; it is never input to pricing"},
        "truth": TRUE, "valid_iv": valid_iv, "deliberately_invalid_iv": invalid_iv,
        "equilibrium": equilibrium_summary, "accounting": acct,
        "claim_scope": "one designed finite-population recovery demonstration at one seed; no broad estimator-performance claim",
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__},
    }
    write_json(out / "summary.json", summary)
    write_json(out / "instrument_timing.json", {"events": summary["timing"], "claims": summary["instrument_claims"]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
