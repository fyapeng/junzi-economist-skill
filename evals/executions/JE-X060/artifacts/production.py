"""Production pipeline for a compact dynamic discrete-choice replacement model."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import logsumexp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"
SEED = 60213
N_STATES = 5
BETA = 0.90
OBSERVED_POLICIES = (0.0, 1.0)
INTERPOLATION_POLICY = 0.5
BOUNDS = np.array([[0.15, 1.50], [1.00, 6.00]], dtype=float)
TRUE_THETA = np.array([0.62, 3.35], dtype=float)
STARTS = np.array(
    [[0.20, 1.20], [0.35, 5.50], [0.75, 3.00], [1.20, 2.00], [1.40, 5.70]],
    dtype=float,
)
PG_TOL = 2.0e-5
BELLMAN_TOL = 1.0e-12


def true_transitions() -> np.ndarray:
    p = np.zeros((2, N_STATES, N_STATES), dtype=float)
    for s in range(N_STATES):
        if s < N_STATES - 1:
            p[0, s, s] = 0.25
            p[0, s, s + 1] = 0.75
        else:
            p[0, s, s] = 1.0
        p[1, s, 0] = 0.85
        p[1, s, 1] = 0.15
    return p


def utilities(theta: np.ndarray, policy: float) -> np.ndarray:
    """Flow utilities; policy may be any finite scalar subsidy."""
    if not np.isscalar(policy) or not np.isfinite(float(policy)):
        raise ValueError("policy must be a finite scalar")
    deterioration, replacement_cost = np.asarray(theta, dtype=float)
    states = np.arange(N_STATES, dtype=float)
    return np.vstack((-deterioration * states, np.full(N_STATES, -replacement_cost + float(policy))))


def solve_policy(theta: np.ndarray, transitions: np.ndarray, policy: float) -> dict[str, np.ndarray | float | int]:
    """Production Bellman solver for an arbitrary scalar policy (value iteration)."""
    u = utilities(theta, policy)
    value = np.zeros(N_STATES, dtype=float)
    for iteration in range(1, 20001):
        choice_value = u + BETA * np.einsum("ask,k->as", transitions, value)
        updated = logsumexp(choice_value, axis=0)
        if np.max(np.abs(updated - value)) <= BELLMAN_TOL:
            value = updated
            break
        value = updated
    else:
        raise RuntimeError(f"Bellman iteration failed for policy={policy}")
    choice_value = u + BETA * np.einsum("ask,k->as", transitions, value)
    ccp = np.exp(choice_value - logsumexp(choice_value, axis=0))
    residual = float(np.max(np.abs(value - logsumexp(choice_value, axis=0))))
    return {"value": value, "choice_value": choice_value, "ccp": ccp, "residual": residual, "iterations": iteration}


def stationary_distribution(ccp: np.ndarray, transitions: np.ndarray) -> np.ndarray:
    induced = np.einsum("as,ask->sk", ccp, transitions)
    system = np.eye(N_STATES) - induced.T
    system[-1, :] = 1.0
    rhs = np.zeros(N_STATES)
    rhs[-1] = 1.0
    dist = np.linalg.solve(system, rhs)
    if np.min(dist) < -1e-11 or abs(dist.sum() - 1.0) > 1e-10:
        raise RuntimeError("invalid stationary distribution")
    return dist


def policy_levels(theta: np.ndarray, transitions: np.ndarray, policy: float) -> dict[str, object]:
    solved = solve_policy(theta, transitions, policy)
    ccp = np.asarray(solved["ccp"])
    dist = stationary_distribution(ccp, transitions)
    replacement_rate = float(dist @ ccp[1])
    deterioration_cost = float(theta[0] * (dist @ np.arange(N_STATES)))
    replacement_resource_cost = float(theta[1] * replacement_rate)
    fiscal_subsidy = float(policy * replacement_rate)
    private_flow_cost = deterioration_cost + replacement_resource_cost - fiscal_subsidy
    social_resource_cost = deterioration_cost + replacement_resource_cost
    return {
        "policy": float(policy),
        "value": np.asarray(solved["value"]).tolist(),
        "replacement_ccp": ccp[1].tolist(),
        "stationary_distribution": dist.tolist(),
        "replacement_rate": replacement_rate,
        "deterioration_resource_cost": deterioration_cost,
        "replacement_resource_cost": replacement_resource_cost,
        "fiscal_subsidy_transfer": fiscal_subsidy,
        "private_flow_cost": private_flow_cost,
        "social_resource_cost": social_resource_cost,
        "bellman_residual": solved["residual"],
        "bellman_iterations": solved["iterations"],
    }


def simulate_data() -> list[dict[str, int | float]]:
    rng = np.random.default_rng(SEED)
    transitions = true_transitions()
    true_solutions = {p: solve_policy(TRUE_THETA, transitions, p) for p in OBSERVED_POLICIES}
    rows: list[dict[str, int | float]] = []
    n_agents, periods = 500, 30
    for agent in range(n_agents):
        policy = OBSERVED_POLICIES[agent % len(OBSERVED_POLICIES)]
        state = int(rng.integers(N_STATES))
        ccp = np.asarray(true_solutions[policy]["ccp"])
        for period in range(periods):
            action = int(rng.random() < ccp[1, state])
            next_state = int(rng.choice(N_STATES, p=transitions[action, state]))
            rows.append(
                {"agent": agent, "period": period, "policy": policy, "state": state, "action": action, "next_state": next_state}
            )
            state = next_state
    return rows


def transition_counts(rows: list[dict[str, int | float]]) -> np.ndarray:
    counts = np.zeros((2, N_STATES, N_STATES), dtype=int)
    for row in rows:
        counts[int(row["action"]), int(row["state"]), int(row["next_state"])] += 1
    return counts


def estimate_transitions(counts: np.ndarray) -> np.ndarray:
    totals = counts.sum(axis=2, keepdims=True)
    if np.any(totals == 0):
        raise RuntimeError("an action-state transition row is unobserved")
    return counts / totals


def choice_counts(rows: list[dict[str, int | float]]) -> np.ndarray:
    counts = np.zeros((len(OBSERVED_POLICIES), N_STATES, 2), dtype=int)
    regime_index = {p: i for i, p in enumerate(OBSERVED_POLICIES)}
    for row in rows:
        counts[regime_index[float(row["policy"])], int(row["state"]), int(row["action"])] += 1
    return counts


def nfxp_objective(theta: np.ndarray, transitions: np.ndarray, counts: np.ndarray) -> float:
    nll = 0.0
    total = int(counts.sum())
    for ri, policy in enumerate(OBSERVED_POLICIES):
        ccp = np.asarray(solve_policy(theta, transitions, policy)["ccp"])
        nll -= float(np.sum(counts[ri].T * np.log(np.clip(ccp, 1e-300, None))))
    return nll / total


def empirical_ccp(counts: np.ndarray) -> np.ndarray:
    # Jeffreys smoothing makes the finite-sample log odds defined in every cell.
    return (counts[:, :, 1] + 0.5) / (counts.sum(axis=2) + 1.0)


def ccp_delta_model(theta: np.ndarray, transitions: np.ndarray, policy: float, empirical_p1: np.ndarray) -> np.ndarray:
    """Hotz-Miller forward mapping using empirical policy evaluation, not a Bellman fixed point."""
    sigma = np.vstack((1.0 - empirical_p1, empirical_p1))
    u = utilities(theta, policy)
    entropy = -np.sum(sigma * np.log(np.clip(sigma, 1e-300, None)), axis=0)
    p_sigma = np.einsum("as,ask->sk", sigma, transitions)
    u_sigma = np.sum(sigma * u, axis=0)
    ex_ante = np.linalg.solve(np.eye(N_STATES) - BETA * p_sigma, u_sigma + entropy)
    return u[1] - u[0] + BETA * ((transitions[1] - transitions[0]) @ ex_ante)


def ccp_objective(theta: np.ndarray, transitions: np.ndarray, counts: np.ndarray) -> float:
    p1 = empirical_ccp(counts)
    total = counts.sum()
    criterion = 0.0
    for ri, policy in enumerate(OBSERVED_POLICIES):
        observed_delta = np.log(p1[ri] / (1.0 - p1[ri]))
        modeled_delta = ccp_delta_model(theta, transitions, policy, p1[ri])
        weights = counts[ri].sum(axis=1) / total
        criterion += float(np.sum(weights * (observed_delta - modeled_delta) ** 2))
    return criterion


def finite_gradient(fun, x: np.ndarray, step: float = 2e-6) -> np.ndarray:
    gradient = np.zeros_like(x, dtype=float)
    for j in range(len(x)):
        h = step * max(1.0, abs(float(x[j])))
        xp, xm = x.copy(), x.copy()
        xp[j] = min(x[j] + h, BOUNDS[j, 1])
        xm[j] = max(x[j] - h, BOUNDS[j, 0])
        gradient[j] = (fun(xp) - fun(xm)) / (xp[j] - xm[j])
    return gradient


def projected_gradient(x: np.ndarray, gradient: np.ndarray) -> np.ndarray:
    projected = gradient.copy()
    for j, (lower, upper) in enumerate(BOUNDS):
        if x[j] <= lower + 1e-8 and gradient[j] > 0:
            projected[j] = 0.0
        elif x[j] >= upper - 1e-8 and gradient[j] < 0:
            projected[j] = 0.0
    return projected


def fit_estimator(name: str, objective) -> tuple[np.ndarray, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    candidates: list[tuple[float, np.ndarray]] = []
    for start_id, start in enumerate(STARTS):
        result = minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=[tuple(x) for x in BOUNDS],
            options={"ftol": 1e-14, "gtol": 1e-10, "maxiter": 2000, "maxls": 50},
        )
        gradient = finite_gradient(objective, result.x)
        projected = projected_gradient(result.x, gradient)
        pg_max = float(np.max(np.abs(projected)))
        accepted = bool(result.success and pg_max <= PG_TOL)
        records.append(
            {
                "estimator": name,
                "start_id": start_id,
                "start_theta_x": start[0],
                "start_replacement_cost": start[1],
                "theta_x": result.x[0],
                "replacement_cost": result.x[1],
                "objective": float(result.fun),
                "optimizer_success": bool(result.success),
                "optimizer_status": int(result.status),
                "optimizer_message": str(result.message),
                "raw_gradient_theta_x": gradient[0],
                "raw_gradient_replacement_cost": gradient[1],
                "projected_gradient_theta_x": projected[0],
                "projected_gradient_replacement_cost": projected[1],
                "projected_gradient_max": pg_max,
                "accepted": accepted,
            }
        )
        if accepted:
            candidates.append((float(result.fun), result.x.copy()))
    if len(candidates) != len(STARTS):
        raise RuntimeError(f"{name}: every start must pass post-optimizer projected-gradient acceptance")
    candidates.sort(key=lambda item: item[0])
    best = candidates[0][1]
    for record in records:
        record["objective_gap_from_best"] = float(record["objective"] - candidates[0][0])
    return best, records


def local_rank(theta: np.ndarray, transitions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    base = np.concatenate([np.asarray(solve_policy(theta, transitions, p)["ccp"])[1] for p in OBSERVED_POLICIES])
    jacobian = np.zeros((base.size, theta.size))
    for j in range(theta.size):
        h = 1e-5 * max(1.0, abs(float(theta[j])))
        xp, xm = theta.copy(), theta.copy()
        xp[j] += h
        xm[j] -= h
        plus = np.concatenate([np.asarray(solve_policy(xp, transitions, p)["ccp"])[1] for p in OBSERVED_POLICIES])
        minus = np.concatenate([np.asarray(solve_policy(xm, transitions, p)["ccp"])[1] for p in OBSERVED_POLICIES])
        jacobian[:, j] = (plus - minus) / (2.0 * h)
    return jacobian, np.linalg.svd(jacobian, compute_uv=False)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns = fieldnames or list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def json_dump(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = simulate_data()
    write_csv(OUT / "panel.csv", rows, ["agent", "period", "policy", "state", "action", "next_state"])

    t_counts = transition_counts(rows)
    transitions = estimate_transitions(t_counts)
    c_counts = choice_counts(rows)
    p1 = empirical_ccp(c_counts)

    transition_rows = []
    for action in range(2):
        for state in range(N_STATES):
            for next_state in range(N_STATES):
                transition_rows.append(
                    {
                        "action": action,
                        "state": state,
                        "next_state": next_state,
                        "count": int(t_counts[action, state, next_state]),
                        "probability": float(transitions[action, state, next_state]),
                        "row_total": int(t_counts[action, state].sum()),
                    }
                )
    write_csv(OUT / "transition_rows.csv", transition_rows)

    ccp_rows = []
    for ri, policy in enumerate(OBSERVED_POLICIES):
        for state in range(N_STATES):
            ccp_rows.append(
                {
                    "policy": policy,
                    "state": state,
                    "count_continue": int(c_counts[ri, state, 0]),
                    "count_replace": int(c_counts[ri, state, 1]),
                    "row_total": int(c_counts[ri, state].sum()),
                    "smoothed_replace_ccp": float(p1[ri, state]),
                }
            )
    write_csv(OUT / "ccp_rows.csv", ccp_rows)

    nfxp_fun = lambda x: nfxp_objective(np.asarray(x), transitions, c_counts)
    ccp_fun = lambda x: ccp_objective(np.asarray(x), transitions, c_counts)
    nfxp_theta, nfxp_starts = fit_estimator("NFXP", nfxp_fun)
    ccp_theta, ccp_starts = fit_estimator("CCP", ccp_fun)
    starts = nfxp_starts + ccp_starts
    write_csv(OUT / "optimizer_starts.csv", starts)

    domain_rows = []
    estimates = {"NFXP": nfxp_theta, "CCP": ccp_theta}
    names = ("theta_x", "replacement_cost")
    for estimator, estimate in estimates.items():
        for j, parameter in enumerate(names):
            lower, upper = BOUNDS[j]
            domain_rows.append(
                {
                    "estimator": estimator,
                    "parameter": parameter,
                    "lower_inclusive": lower,
                    "upper_inclusive": upper,
                    "estimate": estimate[j],
                    "lower_slack": estimate[j] - lower,
                    "upper_slack": upper - estimate[j],
                    "at_lower_boundary": bool(abs(estimate[j] - lower) <= 1e-8),
                    "at_upper_boundary": bool(abs(estimate[j] - upper) <= 1e-8),
                }
            )
    write_csv(OUT / "domain_rows.csv", domain_rows)

    boundary_rows = []
    for tx in (BOUNDS[0, 0], BOUNDS[0, 1]):
        for rc in (BOUNDS[1, 0], BOUNDS[1, 1]):
            boundary_rows.append(
                {
                    "theta_x": tx,
                    "replacement_cost": rc,
                    "theta_x_lower_slack": tx - BOUNDS[0, 0],
                    "theta_x_upper_slack": BOUNDS[0, 1] - tx,
                    "replacement_cost_lower_slack": rc - BOUNDS[1, 0],
                    "replacement_cost_upper_slack": BOUNDS[1, 1] - rc,
                    "boundary_count": 2,
                }
            )
    write_csv(OUT / "closed_domain_corners.csv", boundary_rows)

    jacobian, singular_values = local_rank(nfxp_theta, transitions)
    rank_payload = {
        "claim": "local rank at the accepted NFXP estimate only; no global identification claim",
        "observed_policy_support": list(OBSERVED_POLICIES),
        "jacobian_shape": list(jacobian.shape),
        "jacobian": jacobian.tolist(),
        "singular_values": singular_values.tolist(),
        "rank_tolerance": 1e-8,
        "local_rank": int(np.sum(singular_values > 1e-8)),
    }
    json_dump(OUT / "local_rank.json", rank_payload)

    # Only observed regimes and the declared model interpolation are saved as production policy claims.
    saved_levels = [policy_levels(nfxp_theta, transitions, p) for p in (*OBSERVED_POLICIES, INTERPOLATION_POLICY)]
    saved_levels.sort(key=lambda row: float(row["policy"]))
    json_dump(OUT / "policy_levels.json", saved_levels)

    estimates_payload = {
        "NFXP": {"theta_x": float(nfxp_theta[0]), "replacement_cost": float(nfxp_theta[1]), "objective": nfxp_fun(nfxp_theta)},
        "CCP": {"theta_x": float(ccp_theta[0]), "replacement_cost": float(ccp_theta[1]), "objective": ccp_fun(ccp_theta)},
    }
    json_dump(OUT / "estimates.json", estimates_payload)

    headline = {
        "model": "finite-state dynamic equipment replacement with type-I extreme-value shocks",
        "seed": SEED,
        "sample_rows": len(rows),
        "agents": 500,
        "periods": 30,
        "states": N_STATES,
        "beta": BETA,
        "observed_policy_regimes": list(OBSERVED_POLICIES),
        "model_interpolation_policy": INTERPOLATION_POLICY,
        "transition_count_total": int(t_counts.sum()),
        "ccp_count_total": int(c_counts.sum()),
        "transition_rows": len(transition_rows),
        "ccp_rows": len(ccp_rows),
        "optimizer_start_rows": len(starts),
        "accepted_optimizer_starts": int(sum(bool(x["accepted"]) for x in starts)),
        "required_projected_gradient_tolerance": PG_TOL,
        "closed_domain_rows": len(domain_rows),
        "closed_domain_corner_rows": len(boundary_rows),
        "local_rank": rank_payload["local_rank"],
        "local_rank_singular_values": rank_payload["singular_values"],
        "saved_policy_level_rows": len(saved_levels),
        "production_solver_contract": "solve_policy(theta, transitions, policy) accepts any finite scalar policy",
        "identification_scope": "local rank diagnostic only",
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
    }
    # Mechanical headline reconciliation against row-level objects.
    assert headline["sample_rows"] == headline["transition_count_total"] == headline["ccp_count_total"]
    assert headline["accepted_optimizer_starts"] == headline["optimizer_start_rows"] == 2 * len(STARTS)
    assert headline["transition_rows"] == 2 * N_STATES * N_STATES
    assert headline["ccp_rows"] == len(OBSERVED_POLICIES) * N_STATES
    assert headline["closed_domain_rows"] == 2 * len(names)
    assert headline["closed_domain_corner_rows"] == 4
    assert headline["saved_policy_level_rows"] == len(OBSERVED_POLICIES) + 1
    json_dump(OUT / "headline.json", headline)


if __name__ == "__main__":
    main()
