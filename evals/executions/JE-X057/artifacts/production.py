from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parent
SEED = 57013
BETA = 0.90
N_AGENTS = 240
T_PERIODS = 20
TRUE_THETA = np.array([0.75, 1.25, 0.85])  # state harm, maintenance cost, subsidy loading
BOUNDS = np.array([[0.10, 2.00], [0.20, 3.00], [0.00, 2.00]])
NAMES = ["state_harm", "maintenance_cost", "subsidy_loading"]
P_TRUE = np.array(
    [
        [[0.72, 0.25, 0.03], [0.08, 0.72, 0.20], [0.02, 0.18, 0.80]],
        [[0.90, 0.09, 0.01], [0.62, 0.33, 0.05], [0.40, 0.48, 0.12]],
    ]
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def solve_dp(theta: np.ndarray, regime: float, ptrans: np.ndarray, tol: float = 1e-12):
    alpha, cost, subsidy = theta
    u0 = -alpha * np.arange(3, dtype=float)
    u1 = u0 - cost + subsidy * regime
    ev = np.zeros(3)
    for it in range(20000):
        v0 = u0 + BETA * ptrans[0].dot(ev)
        v1 = u1 + BETA * ptrans[1].dot(ev)
        m = np.maximum(v0, v1)
        new_ev = m + np.log(np.exp(v0 - m) + np.exp(v1 - m))
        if np.max(np.abs(new_ev - ev)) < tol:
            ev = new_ev
            break
        ev = new_ev
    else:
        raise RuntimeError("Bellman iteration did not converge")
    v0 = u0 + BETA * ptrans[0].dot(ev)
    v1 = u1 + BETA * ptrans[1].dot(ev)
    p1 = 1.0 / (1.0 + np.exp(np.clip(v0 - v1, -700, 700)))
    residual = float(np.max(np.abs(ev - np.logaddexp(v0, v1))))
    return ev, p1, residual, it + 1


def simulate() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    policies = {r: solve_dp(TRUE_THETA, float(r), P_TRUE)[1] for r in (0, 1)}
    for i in range(N_AGENTS):
        regime = 0 if i < N_AGENTS // 2 else 1
        state = int(rng.integers(0, 3))
        for t in range(T_PERIODS):
            action = int(rng.random() < policies[regime][state])
            next_state = int(rng.choice(3, p=P_TRUE[action, state]))
            rows.append((i, t, regime, state, action, next_state))
            state = next_state
    return pd.DataFrame(rows, columns=["agent_id", "period", "regime", "state", "action", "next_state"])


def estimate_transitions(data: pd.DataFrame):
    counts = np.zeros((2, 3, 3), dtype=int)
    for row in data.itertuples(index=False):
        counts[row.action, row.state, row.next_state] += 1
    if np.any(counts.sum(axis=2) == 0):
        raise RuntimeError("An action-state transition cell is empty")
    phat = counts / counts.sum(axis=2, keepdims=True)
    records = []
    for a in range(2):
        for x in range(3):
            denom = int(counts[a, x].sum())
            for xp in range(3):
                records.append({"action": a, "state": x, "next_state": xp,
                                "count": int(counts[a, x, xp]), "cell_total": denom,
                                "probability": float(phat[a, x, xp])})
    return phat, pd.DataFrame(records)


def empirical_cells(data: pd.DataFrame) -> pd.DataFrame:
    g = data.groupby(["regime", "state"])["action"].agg(["sum", "count"]).reset_index()
    g["p1_jeffreys"] = (g["sum"] + 0.5) / (g["count"] + 1.0)
    g["log_odds"] = np.log(g["p1_jeffreys"] / (1.0 - g["p1_jeffreys"]))
    return g


def nfxp_objective(theta: np.ndarray, data: pd.DataFrame, ptrans: np.ndarray) -> float:
    ll = 0.0
    for r in (0, 1):
        p1 = solve_dp(theta, float(r), ptrans)[1]
        d = data[data.regime == r]
        p = p1[d.state.to_numpy()]
        a = d.action.to_numpy()
        ll += np.log(np.where(a == 1, p, 1.0 - p) + 1e-300).sum()
    return float(-ll)


def ccp_predicted_logodds(theta: np.ndarray, cells: pd.DataFrame, ptrans: np.ndarray) -> np.ndarray:
    alpha, cost, subsidy = theta
    u0 = -alpha * np.arange(3, dtype=float)
    out = []
    for r in (0, 1):
        cr = cells[cells.regime == r].sort_values("state")
        p0 = 1.0 - cr.p1_jeffreys.to_numpy()
        # Hotz-Miller-style inversion: V = u0 - log(P0) + beta P0_transition V.
        v = np.linalg.solve(np.eye(3) - BETA * ptrans[0], u0 - np.log(p0))
        delta = (-cost + subsidy * r) + BETA * (ptrans[1] - ptrans[0]).dot(v)
        out.extend(delta.tolist())
    return np.asarray(out)


def ccp_objective(theta: np.ndarray, cells: pd.DataFrame, ptrans: np.ndarray) -> float:
    ordered = cells.sort_values(["regime", "state"])
    resid = ordered.log_odds.to_numpy() - ccp_predicted_logodds(theta, ordered, ptrans)
    weights = ordered["count"].to_numpy(dtype=float)
    weights /= weights.sum()
    return float(np.sum(weights * resid * resid))


def projected_gradient(theta, grad):
    pg = np.asarray(grad, dtype=float).copy()
    active = []
    for j, (lo, hi) in enumerate(BOUNDS):
        if theta[j] <= lo + 1e-7:
            active.append(f"{NAMES[j]}:lower")
            if pg[j] > 0:
                pg[j] = 0.0
        if theta[j] >= hi - 1e-7:
            active.append(f"{NAMES[j]}:upper")
            if pg[j] < 0:
                pg[j] = 0.0
    return pg, "|".join(active) if active else "none"


def run_multistart(label, objective, starts):
    rows, results = [], []
    for sid, start in enumerate(starts):
        res = minimize(objective, np.asarray(start, dtype=float), method="L-BFGS-B",
                       bounds=[tuple(x) for x in BOUNDS], options={"ftol": 1e-13, "gtol": 1e-8, "maxiter": 2000})
        pg, active = projected_gradient(res.x, res.jac)
        row = {"estimator": label, "start_id": sid}
        for j, n in enumerate(NAMES):
            row[f"initial_{n}"] = float(start[j])
            row[f"terminal_{n}"] = float(res.x[j])
            row[f"raw_gradient_{n}"] = float(res.jac[j])
            row[f"projected_gradient_{n}"] = float(pg[j])
        row.update({"objective": float(res.fun), "success": bool(res.success), "status": int(res.status),
                    "message": str(res.message), "iterations": int(res.nit), "active_bounds": active,
                    "projected_gradient_inf": float(np.max(np.abs(pg)))})
        rows.append(row)
        results.append(res)
    eligible = [i for i, r in enumerate(rows) if r["success"] and math.isfinite(r["objective"])]
    if not eligible:
        raise RuntimeError(f"No successful {label} start")
    best_i = min(eligible, key=lambda i: rows[i]["objective"])
    best_obj = rows[best_i]["objective"]
    for i, row in enumerate(rows):
        row["selected"] = i == best_i
        row["objective_gap"] = float(row["objective"] - best_obj)
    return results[best_i].x.copy(), pd.DataFrame(rows)


def predicted_ccp_vector(theta, ptrans):
    return np.concatenate([solve_dp(theta, float(r), ptrans)[1] for r in (0, 1)])


def local_rank(theta, ptrans):
    h = 1e-5
    jac = np.empty((6, 3))
    for j in range(3):
        up, dn = theta.copy(), theta.copy()
        up[j] += h
        dn[j] -= h
        jac[:, j] = (predicted_ccp_vector(up, ptrans) - predicted_ccp_vector(dn, ptrans)) / (2 * h)
    sv = np.linalg.svd(jac, compute_uv=False)
    return {"claim_scope": "continuous local rank at the NFXP estimate, conditional on estimated transitions and normalization",
            "global_identification_claim": False, "finite_difference_step": h, "jacobian": jac.tolist(),
            "singular_values": sv.tolist(), "rank_tolerance": 1e-6,
            "rank": int(np.sum(sv > 1e-6)), "full_column_rank": bool(np.sum(sv > 1e-6) == 3)}


def restricted_grid(theta_hat, ptrans):
    axes = [np.linspace(lo, hi, 17) for lo, hi in BOUNDS]
    target = predicted_ccp_vector(theta_hat, ptrans)
    delta, tol = 0.35, 1e-12
    rows = []
    rid = 0
    for alpha in axes[0]:
        for cost in axes[1]:
            for subsidy in axes[2]:
                th = np.array([alpha, cost, subsidy])
                diffs = np.abs(th - theta_hat)
                slack = float(np.max(diffs) - delta)
                slabs = []
                for j, n in enumerate(NAMES):
                    if th[j] <= theta_hat[j] - delta + tol:
                        slabs.append(f"{n}_low")
                    if th[j] >= theta_hat[j] + delta - tol:
                        slabs.append(f"{n}_high")
                accepted = slack >= -tol
                if accepted != bool(slabs):
                    raise AssertionError("Slab union and L-infinity restriction disagree")
                pred = predicted_ccp_vector(th, ptrans)
                rows.append({"row_id": rid, "state_harm": alpha, "maintenance_cost": cost,
                             "subsidy_loading": subsidy, "objective_ccp_sse": float(np.sum((pred - target) ** 2)),
                             "linf_distance": float(np.max(diffs)), "restriction_delta": delta,
                             "restriction_slack": slack, "acceptance_tolerance": tol,
                             "restricted_accept": accepted, "slab_membership": "|".join(slabs) if slabs else "none",
                             "is_domain_boundary": bool(any(abs(th[j] - BOUNDS[j, 0]) < 1e-14 or abs(th[j] - BOUNDS[j, 1]) < 1e-14 for j in range(3)))})
                rid += 1
    return pd.DataFrame(rows)


def stationary_policy(theta, regime, ptrans):
    _, p1, bellman_resid, iterations = solve_dp(theta, regime, ptrans)
    q = (1.0 - p1)[:, None] * ptrans[0] + p1[:, None] * ptrans[1]
    dist = np.full(3, 1 / 3)
    for _ in range(100000):
        new = dist.dot(q)
        if np.max(np.abs(new - dist)) < 1e-14:
            dist = new
            break
        dist = new
    action_rate = float(dist.dot(p1))
    expected_state = float(dist.dot(np.arange(3)))
    alpha, cost, subsidy = theta
    transfer = subsidy * regime * action_rate
    resource_cost = cost * action_rate
    state_harm = alpha * expected_state
    private = -state_harm - resource_cost + transfer
    welfare = -state_harm - resource_cost
    return {"regime": regime, "support_status": "observed" if regime in (0.0, 1.0) else "model_interpolation",
            "stationary_state0": dist[0], "stationary_state1": dist[1], "stationary_state2": dist[2],
            "maintenance_rate": action_rate, "expected_deterioration": expected_state,
            "private_payoff": private, "transfer_outlay": transfer, "state_harm": state_harm,
            "resource_cost": resource_cost, "social_welfare": welfare,
            "accounting_error_private_minus_transfer": welfare - (private - transfer),
            "accounting_error_resource_identity": welfare + state_harm + resource_cost,
            "bellman_residual": bellman_resid, "bellman_iterations": iterations}


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    produced_at = utc_now()
    data = simulate()
    data.to_csv(ROOT / "model_data.csv", index=False, encoding="utf-8")
    ptrans, transitions = estimate_transitions(data)
    transitions.to_csv(ROOT / "transition_estimates.csv", index=False, encoding="utf-8")
    cells = empirical_cells(data)
    cells.to_csv(ROOT / "choice_cells.csv", index=False, encoding="utf-8")

    starts = [
        [0.10, 0.20, 0.00], [2.00, 3.00, 2.00], [0.10, 3.00, 2.00], [2.00, 0.20, 0.00],
        [0.50, 1.00, 0.50], [1.20, 2.20, 1.40], [1.80, 0.70, 1.80], [0.80, 2.80, 0.20],
    ]
    nfxp_theta, nfxp_starts = run_multistart("NFXP", lambda th: nfxp_objective(th, data, ptrans), starts)
    nfxp_starts.to_csv(ROOT / "nfxp_starts.csv", index=False, encoding="utf-8")
    ccp_theta, ccp_starts = run_multistart("CCP-WMD", lambda th: ccp_objective(th, cells, ptrans), starts)
    ccp_starts.to_csv(ROOT / "ccp_starts.csv", index=False, encoding="utf-8")

    rank = local_rank(nfxp_theta, ptrans)
    write_json(ROOT / "local_rank.json", rank)
    search = restricted_grid(nfxp_theta, ptrans)
    search.to_csv(ROOT / "restricted_search.csv", index=False, encoding="utf-8")
    policy = pd.DataFrame([stationary_policy(nfxp_theta, r, ptrans) for r in (0.0, 0.5, 1.0)])
    policy.to_csv(ROOT / "policy_results.csv", index=False, encoding="utf-8")

    # Re-open final row-level files so every reported count/rate is mechanically derived from saved artifacts.
    d = pd.read_csv(ROOT / "model_data.csv")
    ns = pd.read_csv(ROOT / "nfxp_starts.csv")
    cs = pd.read_csv(ROOT / "ccp_starts.csv")
    rs = pd.read_csv(ROOT / "restricted_search.csv")
    pr = pd.read_csv(ROOT / "policy_results.csv")
    tr = pd.read_csv(ROOT / "transition_estimates.csv")
    nsel = ns.loc[ns.selected].iloc[0]
    csel = cs.loc[cs.selected].iloc[0]
    best_alt = rs.loc[rs.restricted_accept].sort_values(["objective_ccp_sse", "row_id"]).iloc[0]
    summary = {
        "generated_at_utc": produced_at, "seed": SEED, "beta": BETA,
        "sample": {"rows": int(len(d)), "agents": int(d.agent_id.nunique()), "periods_per_agent": T_PERIODS,
                   "action_rate": float(d.action.mean()),
                   "action_rate_by_regime": {str(int(k)): float(v) for k, v in d.groupby("regime").action.mean().items()}},
        "estimated_transitions": {"rows": int(len(tr)), "action_state_cells": int(tr.groupby(["action", "state"]).ngroups),
                                  "minimum_cell_total": int(tr.cell_total.min()), "maximum_row_sum_error": float(tr.groupby(["action", "state"]).probability.sum().sub(1).abs().max())},
        "nfxp": {"theta": {n: float(nsel[f"terminal_{n}"]) for n in NAMES}, "objective": float(nsel.objective),
                 "starts": int(len(ns)), "successful_starts": int(ns.success.sum()), "selected_start_id": int(nsel.start_id),
                 "projected_gradient_inf": float(nsel.projected_gradient_inf)},
        "ccp_wmd": {"theta": {n: float(csel[f"terminal_{n}"]) for n in NAMES}, "objective": float(csel.objective),
                    "starts": int(len(cs)), "successful_starts": int(cs.success.sum()), "selected_start_id": int(csel.start_id),
                    "projected_gradient_inf": float(csel.projected_gradient_inf)},
        "local_rank": {"rank": rank["rank"], "singular_values": rank["singular_values"], "claim_scope": rank["claim_scope"],
                       "global_identification_claim": False},
        "restricted_search": {"domain": {n: BOUNDS[j].tolist() for j, n in enumerate(NAMES)}, "nodes_per_axis": 17,
                              "total_rows": int(len(rs)), "accepted_rows": int(rs.restricted_accept.sum()),
                              "boundary_rows": int(rs.is_domain_boundary.sum()), "delta": float(best_alt.restriction_delta),
                              "tolerance": float(best_alt.acceptance_tolerance), "best_row_id": int(best_alt.row_id),
                              "best_objective_ccp_sse": float(best_alt.objective_ccp_sse),
                              "best_slack": float(best_alt.restriction_slack),
                              "interpretation": "exact exhaustive result on the declared closed 17^3 lattice; not continuous global identification"},
        "policy": {"rows": int(len(pr)), "observed_regime_rows": int((pr.support_status == "observed").sum()),
                   "interpolation_rows": int((pr.support_status == "model_interpolation").sum()),
                   "maximum_accounting_error": float(pr[["accounting_error_private_minus_transfer", "accounting_error_resource_identity"]].abs().to_numpy().max())},
    }
    write_json(ROOT / "summary.json", summary)

    response = f"""# Compact dynamic discrete-choice result

## Economic object and status

The artifact models households choosing whether to maintain a deteriorating durable asset. The controlled state transition is estimated from the simulated panel rather than imposed in estimation. The sample has **{summary['sample']['rows']} decision rows from {summary['sample']['agents']} agents**; the overall maintenance rate is **{summary['sample']['action_rate']:.4f}** (regime 0: **{summary['sample']['action_rate_by_regime']['0']:.4f}**; regime 1: **{summary['sample']['action_rate_by_regime']['1']:.4f}**).

NFXP estimates `(state harm, maintenance cost, subsidy loading)` as **({nfxp_theta[0]:.6f}, {nfxp_theta[1]:.6f}, {nfxp_theta[2]:.6f})** from {summary['nfxp']['successful_starts']}/{summary['nfxp']['starts']} successful starts. The genuinely distinct CCP-WMD estimator uses empirical CCP inversion and no nested Bellman likelihood; it estimates **({ccp_theta[0]:.6f}, {ccp_theta[1]:.6f}, {ccp_theta[2]:.6f})** from {summary['ccp_wmd']['successful_starts']}/{summary['ccp_wmd']['starts']} successful starts.

## Identification and restricted alternatives

The continuous claim is **local only**: the six observed-regime CCPs have a numerical Jacobian of rank {rank['rank']} at the NFXP estimate, conditional on the estimated transitions, logit shocks, discount factor, and utility normalization. This is not a global population-identification claim.

The restricted alternative exercise exhausts all **{summary['restricted_search']['total_rows']}** points of the declared closed 17-by-17-by-17 lattice, including **{summary['restricted_search']['boundary_rows']}** boundary points. Exactly **{summary['restricted_search']['accepted_rows']}** rows satisfy the hard L-infinity distance restriction `distance >= {summary['restricted_search']['delta']}` at tolerance `{summary['restricted_search']['tolerance']}`. The best accepted row has CCP SSE **{summary['restricted_search']['best_objective_ccp_sse']:.8g}** and slack **{summary['restricted_search']['best_slack']:.8g}**. This is exact for the evaluated lattice only and supplies no continuous global-separation theorem.

## Policy and welfare

Regimes 0 and 1 are observed supports. Regime 0.5 is explicitly labeled model-based interpolation, not observed support. `policy_results.csv` keeps private payoff, government transfer outlay, real maintenance resources, state harm, and social welfare separate. Social welfare equals private payoff minus transfers and also equals negative state harm minus real maintenance cost; the maximum saved accounting error is **{summary['policy']['maximum_accounting_error']:.3e}**.

## Limits

Results are a deterministic simulated-data recovery exercise, conditional on the specified dynamic logit and estimated transition law. The local rank check, finite-lattice restricted search, and policy interpolation do not establish global population identification, external validity, or policy invariance outside the two observed regimes.
"""
    (ROOT / "response.md").write_text(response, encoding="utf-8")

    stdout_text = (f"production_complete rows={len(d)} nfxp_starts={len(ns)} ccp_starts={len(cs)} "
                   f"restricted_rows={len(rs)} accepted={int(rs.restricted_accept.sum())} "
                   f"max_accounting_error={summary['policy']['maximum_accounting_error']:.17g}\n")
    (ROOT / "production_stdout.txt").write_text(stdout_text, encoding="utf-8")
    print(stdout_text, end="")

    artifact_names = ["production.py", "model_data.csv", "transition_estimates.csv", "choice_cells.csv",
                      "nfxp_starts.csv", "ccp_starts.csv", "local_rank.json", "restricted_search.csv",
                      "policy_results.csv", "summary.json", "response.md", "production_stdout.txt"]
    provenance = {
        "production_completed_at_utc": utc_now(), "workspace": str(ROOT),
        "source_instruction_commit": "f120979", "random_seed": SEED,
        "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
        "scipy": scipy.__version__,
        "artifacts": {name: {"sha256": sha256(ROOT / name),
                              "mtime_utc": datetime.fromtimestamp((ROOT / name).stat().st_mtime, timezone.utc).isoformat(),
                              "bytes": (ROOT / name).stat().st_size} for name in artifact_names},
    }
    write_json(ROOT / "provenance.json", provenance)


if __name__ == "__main__":
    main()
