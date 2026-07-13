from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parent
BETA = 0.80
BOUNDS = [(-4.0, 4.0), (-4.0, 4.0)]
STARTS = [[-2.0, -1.0], [-1.0, 1.0], [0.0, 0.0], [1.0, 2.0], [2.0, -2.0]]
GRAD_STEP = 1e-5
ACCEPT_TOL = 2e-4
BELLMAN_TOL = 1e-11


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_bytes(canonical_bytes(obj))


def raw_primitives():
    transition_counts = {
        "s0_a0": [72, 18], "s0_a1": [24, 36],
        "s1_a0": [28, 42], "s1_a1": [12, 68],
    }
    choice_counts = {"s0": [70, 30], "s1": [25, 75]}
    return {
        "schema": "dynamic-ddc-primitives-v1",
        "states": [0, 1], "actions": [0, 1], "beta": BETA,
        "shock_normalization": "type-I-EV integrated value uses logsumexp with Euler constant removed",
        "transition_cells": [
            {"key": f"s{s}_a{a}", "state": s, "action": a,
             "next_state_counts": transition_counts[f"s{s}_a{a}"]}
            for s in [0, 1] for a in [0, 1]
        ],
        "choice_cells": [
            {"key": f"s{s}", "state": s, "action_counts": choice_counts[f"s{s}"]}
            for s in [0, 1]
        ],
        "initial_state_distribution": [0.60, 0.40],
        "parameter_names": ["action_intercept", "state1_action_return"],
        "parameter_bounds": BOUNDS,
        "starts": [{"start_key": f"start_{i:02d}", "initial": x} for i, x in enumerate(STARTS)],
        "numerics": {"gradient_step": GRAD_STEP, "accept_projected_gradient_tol": ACCEPT_TOL,
                     "bellman_tol": BELLMAN_TOL, "optimizer": "L-BFGS-B"},
        "policy_levels": [0.0, 0.25, 0.5, 0.75, 1.0],
        "observed_policy_levels": [0.0, 1.0],
        "restricted_grid": {
            "domain_label": "closed_finite_theta_grid_v1",
            "theta0_values": [-1.0, 0.0, 1.0], "theta1_values": [0.0, 1.0, 2.0],
            "restriction": "theta1-theta0-0.5>=0", "feasibility_tol": 1e-12,
        },
    }


def transition_matrix(raw):
    P = np.zeros((2, 2, 2))
    for row in raw["transition_cells"]:
        c = np.asarray(row["next_state_counts"], float)
        P[row["state"], row["action"]] = c / c.sum()
    return P


def observed_ccp(raw):
    p = np.zeros((2, 2))
    for row in raw["choice_cells"]:
        c = np.asarray(row["action_counts"], float)
        p[row["state"]] = c / c.sum()
    return p


def utility(theta, policy_level=0.0):
    u = np.zeros((2, 2))
    u[:, 1] = theta[0] + theta[1] * np.arange(2) - policy_level
    return u


def nfxp_solve(theta, P, policy_level=0.0):
    u = utility(theta, policy_level)
    V = np.zeros(2)
    for _ in range(10000):
        q = u + BETA * np.einsum("sak,k->sa", P, V)
        m = q.max(axis=1)
        Vn = m + np.log(np.exp(q - m[:, None]).sum(axis=1))
        if np.max(np.abs(Vn - V)) <= BELLMAN_TOL:
            V = Vn
            break
        V = Vn
    q = u + BETA * np.einsum("sak,k->sa", P, V)
    m = q.max(axis=1, keepdims=True)
    probs = np.exp(q - m); probs /= probs.sum(axis=1, keepdims=True)
    residual = float(np.max(np.abs(V - np.log(np.exp(q).sum(axis=1)))))
    return V, probs, residual


def nfxp_objective(theta, raw, P):
    _, probs, _ = nfxp_solve(theta, P)
    total = 0.0
    for row in raw["choice_cells"]:
        total -= float(np.dot(row["action_counts"], np.log(probs[row["state"]])))
    return total


def ccp_components(theta, raw, P):
    p = observed_ccp(raw)
    u = utility(theta)
    entropy = -(p * np.log(p)).sum(axis=1)
    Ppi = np.einsum("sa,sak->sk", p, P)
    upi = (p * u).sum(axis=1)
    V = np.linalg.solve(np.eye(2) - BETA * Ppi, upi + entropy)
    q = u + BETA * np.einsum("sak,k->sa", P, V)
    target = np.log(p[:, 1] / p[:, 0])
    gap = (q[:, 1] - q[:, 0]) - target
    weights = np.array([sum(r["action_counts"]) for r in raw["choice_cells"]], float)
    return V, gap, weights


def ccp_objective(theta, raw, P):
    _, gap, weights = ccp_components(theta, raw, P)
    return float(np.dot(weights, gap * gap))


def numerical_gradient(fun, x):
    x = np.asarray(x, float); g = np.zeros_like(x)
    for j, (lo, hi) in enumerate(BOUNDS):
        h = GRAD_STEP * max(1.0, abs(x[j]))
        xp = x.copy(); xm = x.copy()
        xp[j] = min(hi, x[j] + h); xm[j] = max(lo, x[j] - h)
        g[j] = (fun(xp) - fun(xm)) / (xp[j] - xm[j])
    return g


def projected_gradient(x, g):
    pg = np.asarray(g, float).copy()
    for j, (lo, hi) in enumerate(BOUNDS):
        if x[j] <= lo + 1e-8 and g[j] >= 0: pg[j] = 0.0
        if x[j] >= hi - 1e-8 and g[j] <= 0: pg[j] = 0.0
    return pg


def estimate(name, fun):
    records = []
    for i, x0 in enumerate(STARTS):
        res = minimize(fun, np.asarray(x0), method="L-BFGS-B", bounds=BOUNDS,
                       options={"ftol": 1e-13, "gtol": 1e-10, "maxiter": 2000, "maxls": 50})
        x = np.asarray(res.x); obj = float(fun(x))
        g = numerical_gradient(fun, x); pg = projected_gradient(x, g)
        accepted = bool(np.isfinite(obj) and np.max(np.abs(pg)) <= ACCEPT_TOL)
        records.append({"start_key": f"start_{i:02d}", "initial": x0, "terminal": x.tolist(),
                        "objective": obj, "raw_gradient": g.tolist(), "projected_gradient": pg.tolist(),
                        "projected_gradient_max_abs": float(np.max(np.abs(pg))),
                        "solver_success": bool(res.success), "solver_status": int(res.status),
                        "solver_message": str(res.message), "accepted": accepted})
    eligible = [r for r in records if r["accepted"]]
    if len(eligible) != len(records):
        raise RuntimeError(f"{name}: every declared start must pass recomputed projected-gradient acceptance")
    best = min(eligible, key=lambda r: r["objective"])
    for r in records: r["distance_from_best_objective"] = r["objective"] - best["objective"]
    return {"name": name, "starts": records, "selected_start_key": best["start_key"],
            "parameters": best["terminal"], "objective": best["objective"]}


def probability_jacobian(theta, P):
    J = np.zeros((2, 2))
    for j in range(2):
        h = 1e-5 * max(1.0, abs(theta[j])); xp = np.array(theta); xm = np.array(theta)
        xp[j] += h; xm[j] -= h
        J[:, j] = (nfxp_solve(xp, P)[1][:, 1] - nfxp_solve(xm, P)[1][:, 1]) / (2*h)
    return J


def policy_record(z, theta, P, raw):
    V, p, residual = nfxp_solve(theta, P, z)
    mu0 = np.asarray(raw["initial_state_distribution"], float)
    Ppi = np.einsum("sa,sak->sk", p, P)
    discounted_state = mu0 @ np.linalg.inv(np.eye(2) - BETA * Ppi)
    occ = discounted_state[:, None] * p
    activity = float(occ[:, 1].sum())
    intercept = float(theta[0] * activity)
    state_return = float(theta[1] * occ[1, 1])
    policy_cost = float(z * activity)
    entropy = float(np.sum(discounted_state * (-(p * np.log(p)).sum(axis=1))))
    total = intercept + state_return - policy_cost + entropy
    return {"policy_key": f"policy_{int(round(100*z)):03d}", "level": z,
            "support_label": "observed_regime" if z in raw["observed_policy_levels"] else "interior_model_interpolation",
            "is_midpoint": z == 0.5, "choice1_probabilities": p[:, 1].tolist(), "value_vector": V.tolist(),
            "bellman_residual_max_abs": residual,
            "accounting": {"discounted_activity": activity, "action_intercept_component": intercept,
                           "state1_action_return_component": state_return, "policy_cost_component": policy_cost,
                           "entropy_component": entropy, "total_model_value": total,
                           "initial_value_from_bellman": float(mu0 @ V),
                           "identity_residual": total - float(mu0 @ V)}}


def main():
    started = utc_now()
    raw = raw_primitives(); raw_path = ROOT / "raw_primitives.json"; write_json(raw_path, raw)
    P = transition_matrix(raw); pobs = observed_ccp(raw)
    nfxp = estimate("NFXP_full_solution_likelihood", lambda x: nfxp_objective(x, raw, P))
    ccp = estimate("CCP_Hotz_Miller_policy_evaluation_minimum_distance", lambda x: ccp_objective(x, raw, P))
    theta = np.asarray(nfxp["parameters"])
    J = probability_jacobian(theta, P); sv = np.linalg.svd(J, compute_uv=False)
    grid = raw["restricted_grid"]; restricted = []
    for i, t0 in enumerate(grid["theta0_values"]):
        for j, t1 in enumerate(grid["theta1_values"]):
            slack = t1 - t0 - 0.5; feasible = slack >= -grid["feasibility_tol"]
            restricted.append({"row_key": f"grid_t0_{i:02d}_t1_{j:02d}", "domain_label": grid["domain_label"],
                               "theta0": t0, "theta1": t1,
                               "theta0_lower_boundary": i == 0, "theta0_upper_boundary": i == len(grid["theta0_values"])-1,
                               "theta1_lower_boundary": j == 0, "theta1_upper_boundary": j == len(grid["theta1_values"])-1,
                               "restriction_slack": slack, "feasible": feasible,
                               "nfxp_objective": nfxp_objective([t0, t1], raw, P)})
    feasible_rows = [r for r in restricted if r["feasible"]]
    selected_grid = min(feasible_rows, key=lambda r: r["nfxp_objective"])["row_key"]
    policies = [policy_record(z, theta, P, raw) for z in raw["policy_levels"]]
    monotonic = all(policies[k+1]["choice1_probabilities"][s] <= policies[k]["choice1_probabilities"][s] + 1e-12
                    for k in range(len(policies)-1) for s in [0, 1])
    output = {
        "schema": "dynamic-ddc-production-v1",
        "chronology": {"production_started_utc": started, "production_finished_utc": utc_now()},
        "production_source_sha256": sha256(ROOT / "production.py"), "raw_primitives_sha256": sha256(raw_path),
        "transition_estimates": [{"key": f"s{s}_a{a}", "probabilities": P[s,a].tolist(),
                                  "count_total": int(sum(next(r["next_state_counts"] for r in raw["transition_cells"] if r["key"]==f"s{s}_a{a}")))}
                                 for s in [0,1] for a in [0,1]],
        "observed_ccp_estimates": [{"key": f"s{s}", "probabilities": pobs[s].tolist(),
                                    "count_total": int(sum(next(r["action_counts"] for r in raw["choice_cells"] if r["key"]==f"s{s}")))}
                                   for s in [0,1]],
        "estimators": {"nfxp": nfxp, "ccp": ccp},
        "local_rank_diagnostic": {"object": "Jacobian of NFXP state-specific choice-1 probabilities",
                                  "jacobian": J.tolist(), "singular_values": sv.tolist(),
                                  "rank_threshold": 1e-6, "local_numerical_rank": int(np.sum(sv > 1e-6)),
                                  "claim_scope": "local numerical rank only; no global or population identification claim"},
        "restricted_grid_rows": restricted, "restricted_grid_selected_key": selected_grid,
        "policy_records": policies, "policy_choice1_monotone_nonincreasing": monotonic,
        "headlines": {"nfxp_parameters": nfxp["parameters"], "nfxp_objective": nfxp["objective"],
                      "ccp_parameters": ccp["parameters"], "ccp_objective": ccp["objective"],
                      "transition_cell_count": 4, "choice_cell_count": 2, "accepted_start_count_each": len(STARTS),
                      "restricted_row_count": len(restricted), "policy_record_count": len(policies),
                      "local_numerical_rank": int(np.sum(sv > 1e-6)), "monotonic_policy_sanity": monotonic},
    }
    write_json(ROOT / "production_output.json", output)


if __name__ == "__main__":
    main()
