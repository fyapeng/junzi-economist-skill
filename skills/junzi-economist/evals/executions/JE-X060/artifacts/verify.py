"""Independent verifier. This file intentionally does not import production.py."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import root
from scipy.special import logsumexp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"
N_STATES = 5
BETA = 0.90
OBSERVED = (0.0, 1.0)
EVALUATION_POLICIES = (0.0, 0.25, 0.5, 0.75, 1.0)
BOUNDS = np.array([[0.15, 1.50], [1.00, 6.00]])


def load_json(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_hashes() -> dict[str, object]:
    manifest = load_json("production_hashes.json")
    mismatches = []
    for record in manifest:
        path = ROOT / record["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        size = path.stat().st_size if path.is_file() else None
        if digest != record["sha256"] or size != record["bytes"]:
            mismatches.append({"path": record["path"], "expected_hash": record["sha256"], "actual_hash": digest})
    return {"passed": not mismatches, "files_checked": len(manifest), "mismatches": mismatches}


def reconstruct_counts(panel: list[dict[str, str]]) -> tuple[np.ndarray, np.ndarray]:
    transitions = np.zeros((2, N_STATES, N_STATES), dtype=int)
    choices = np.zeros((len(OBSERVED), N_STATES, 2), dtype=int)
    regime = {value: index for index, value in enumerate(OBSERVED)}
    for row in panel:
        action, state, next_state = int(row["action"]), int(row["state"]), int(row["next_state"])
        transitions[action, state, next_state] += 1
        choices[regime[float(row["policy"])], state, action] += 1
    return transitions, choices


def compare_saved_counts(t_counts: np.ndarray, c_counts: np.ndarray) -> dict[str, object]:
    saved_t = read_csv(OUT / "transition_rows.csv")
    saved_c = read_csv(OUT / "ccp_rows.csv")
    t_mismatch, c_mismatch = [], []
    for row in saved_t:
        a, s, k = int(row["action"]), int(row["state"]), int(row["next_state"])
        expected_count = int(t_counts[a, s, k])
        expected_total = int(t_counts[a, s].sum())
        expected_probability = expected_count / expected_total
        if int(row["count"]) != expected_count or int(row["row_total"]) != expected_total or not math.isclose(
            float(row["probability"]), expected_probability, rel_tol=0.0, abs_tol=2e-15
        ):
            t_mismatch.append([a, s, k])
    for row in saved_c:
        ri = OBSERVED.index(float(row["policy"]))
        s = int(row["state"])
        expected = c_counts[ri, s]
        smooth = (expected[1] + 0.5) / (expected.sum() + 1.0)
        if (
            int(row["count_continue"]) != expected[0]
            or int(row["count_replace"]) != expected[1]
            or int(row["row_total"]) != expected.sum()
            or not math.isclose(float(row["smoothed_replace_ccp"]), smooth, rel_tol=0.0, abs_tol=2e-15)
        ):
            c_mismatch.append([float(row["policy"]), s])
    passed = not t_mismatch and not c_mismatch and len(saved_t) == 50 and len(saved_c) == 10
    return {
        "passed": passed,
        "transition_total_recomputed": int(t_counts.sum()),
        "ccp_total_recomputed": int(c_counts.sum()),
        "transition_rows_compared": len(saved_t),
        "ccp_rows_compared": len(saved_c),
        "transition_mismatches": t_mismatch,
        "ccp_mismatches": c_mismatch,
    }


def transition_probabilities(counts: np.ndarray) -> np.ndarray:
    totals = counts.sum(axis=2, keepdims=True)
    if np.any(totals == 0):
        raise ValueError("zero transition row")
    return counts / totals


def independent_policy_solve(theta: np.ndarray, transitions: np.ndarray, policy: float) -> dict[str, np.ndarray | float]:
    """Arbitrary-policy Newton/root path, algebraically distinct from production value iteration."""
    if not np.isscalar(policy) or not np.isfinite(float(policy)):
        raise ValueError("policy must be a finite scalar")
    states = np.arange(N_STATES, dtype=float)
    flow = np.vstack((-theta[0] * states, np.full(N_STATES, -theta[1] + float(policy))))

    def residual(value: np.ndarray) -> np.ndarray:
        q = flow + BETA * np.einsum("ask,k->as", transitions, value)
        return value - logsumexp(q, axis=0)

    def jacobian(value: np.ndarray) -> np.ndarray:
        q = flow + BETA * np.einsum("ask,k->as", transitions, value)
        sigma = np.exp(q - logsumexp(q, axis=0))
        induced = np.einsum("as,ask->sk", sigma, transitions)
        return np.eye(N_STATES) - BETA * induced

    answer = root(residual, np.zeros(N_STATES), jac=jacobian, method="hybr", options={"xtol": 1e-11, "maxfev": 2000})
    direct_residual = residual(answer.x)
    if not answer.success or np.max(np.abs(direct_residual)) > 1e-10:
        raise RuntimeError(f"independent root solve failed for policy={policy}: {answer.message}")
    q = flow + BETA * np.einsum("ask,k->as", transitions, answer.x)
    ccp = np.exp(q - logsumexp(q, axis=0))
    induced = np.einsum("as,ask->sk", ccp, transitions)
    augmented = np.eye(N_STATES) - induced.T
    augmented[-1] = 1.0
    rhs = np.zeros(N_STATES)
    rhs[-1] = 1.0
    stationary = np.linalg.solve(augmented, rhs)
    replacement_rate = float(stationary @ ccp[1])
    deterioration_cost = float(theta[0] * stationary @ states)
    replacement_cost = float(theta[1] * replacement_rate)
    transfer = float(policy * replacement_rate)
    return {
        "value": answer.x,
        "replacement_ccp": ccp[1],
        "stationary_distribution": stationary,
        "replacement_rate": replacement_rate,
        "deterioration_resource_cost": deterioration_cost,
        "replacement_resource_cost": replacement_cost,
        "fiscal_subsidy_transfer": transfer,
        "private_flow_cost": deterioration_cost + replacement_cost - transfer,
        "social_resource_cost": deterioration_cost + replacement_cost,
        "bellman_residual": float(np.max(np.abs(direct_residual))),
    }


def compare_policy_levels(theta: np.ndarray, transitions: np.ndarray) -> tuple[dict[str, object], dict[float, dict[str, object]]]:
    independently_solved = {p: independent_policy_solve(theta, transitions, p) for p in EVALUATION_POLICIES}
    saved = {float(row["policy"]): row for row in load_json("policy_levels.json")}
    comparisons = []
    vector_fields = ("value", "replacement_ccp", "stationary_distribution")
    scalar_fields = (
        "replacement_rate",
        "deterioration_resource_cost",
        "replacement_resource_cost",
        "fiscal_subsidy_transfer",
        "private_flow_cost",
        "social_resource_cost",
    )
    for policy in sorted(saved):
        independent = independently_solved[policy]
        vector_errors = {
            field: float(np.max(np.abs(np.asarray(independent[field]) - np.asarray(saved[policy][field])))) for field in vector_fields
        }
        scalar_errors = {field: abs(float(independent[field]) - float(saved[policy][field])) for field in scalar_fields}
        comparisons.append({"policy": policy, "vector_max_abs_errors": vector_errors, "level_abs_errors": scalar_errors})

    maximum_error = max(
        [value for row in comparisons for value in row["vector_max_abs_errors"].values()]
        + [value for row in comparisons for value in row["level_abs_errors"].values()]
    )
    midpoint = next(row for row in comparisons if row["policy"] == 0.5)
    midpoint_level_error = max(midpoint["level_abs_errors"].values())
    replacement_ccps = np.stack([independently_solved[p]["replacement_ccp"] for p in EVALUATION_POLICIES])
    replacement_rates = np.array([independently_solved[p]["replacement_rate"] for p in EVALUATION_POLICIES])
    private_costs = np.array([independently_solved[p]["private_flow_cost"] for p in EVALUATION_POLICIES])
    sanity = {
        "replacement_ccp_weakly_increases_with_state_each_policy": bool(np.all(np.diff(replacement_ccps, axis=1) >= -1e-11)),
        "replacement_ccp_weakly_increases_with_policy_each_state": bool(np.all(np.diff(replacement_ccps, axis=0) >= -1e-11)),
        "aggregate_replacement_rate_strictly_increases_with_policy": bool(np.all(np.diff(replacement_rates) > 0.0)),
        "private_flow_cost_strictly_decreases_with_subsidy": bool(np.all(np.diff(private_costs) < 0.0)),
        "stationary_distributions_valid": bool(
            all(np.min(independently_solved[p]["stationary_distribution"]) >= -1e-12 for p in EVALUATION_POLICIES)
            and all(abs(np.sum(independently_solved[p]["stationary_distribution"]) - 1.0) <= 1e-11 for p in EVALUATION_POLICIES)
        ),
    }
    residuals = {str(p): independently_solved[p]["bellman_residual"] for p in EVALUATION_POLICIES}
    result = {
        "passed": maximum_error <= 3e-9 and midpoint_level_error <= 3e-10 and all(sanity.values()) and max(residuals.values()) <= 1e-10,
        "method": "nonlinear root with analytic Newton Jacobian; production uses value iteration",
        "arbitrary_policy_values_evaluated": list(EVALUATION_POLICIES),
        "observed_policy_values": list(OBSERVED),
        "off_regime_interior_values": [0.25, 0.75],
        "saved_level_comparisons": comparisons,
        "maximum_saved_level_or_vector_error": maximum_error,
        "saved_midpoint_accounting_level_max_error": midpoint_level_error,
        "direct_bellman_residuals": residuals,
        "economic_sanity": sanity,
    }
    return result, independently_solved


def independent_local_rank(theta: np.ndarray, transitions: np.ndarray) -> dict[str, object]:
    jac = np.zeros((len(OBSERVED) * N_STATES, 2))
    for j in range(2):
        h = 5e-6 * max(1.0, abs(float(theta[j])))
        plus, minus = theta.copy(), theta.copy()
        plus[j] += h
        minus[j] -= h
        p_plus = np.concatenate([independent_policy_solve(plus, transitions, p)["replacement_ccp"] for p in OBSERVED])
        p_minus = np.concatenate([independent_policy_solve(minus, transitions, p)["replacement_ccp"] for p in OBSERVED])
        jac[:, j] = (p_plus - p_minus) / (2.0 * h)
    singular = np.linalg.svd(jac, compute_uv=False)
    saved = np.asarray(load_json("local_rank.json")["singular_values"])
    error = np.abs(singular - saved)
    return {
        "passed": bool(np.max(error) <= 2e-7 and np.sum(singular > 1e-8) == 2),
        "scope": "local rank at saved NFXP estimate only",
        "recomputed_singular_values": singular.tolist(),
        "saved_singular_values": saved.tolist(),
        "absolute_errors": error.tolist(),
        "recomputed_local_rank": int(np.sum(singular > 1e-8)),
    }


def verify_domain_and_starts(headline: dict[str, object]) -> dict[str, object]:
    domain = read_csv(OUT / "domain_rows.csv")
    corners = read_csv(OUT / "closed_domain_corners.csv")
    starts = read_csv(OUT / "optimizer_starts.csv")
    domain_ok = len(domain) == 4
    expected_parameters = {"theta_x": BOUNDS[0], "replacement_cost": BOUNDS[1]}
    for row in domain:
        lower, upper = expected_parameters[row["parameter"]]
        estimate = float(row["estimate"])
        domain_ok &= math.isclose(float(row["lower_inclusive"]), lower, abs_tol=0.0)
        domain_ok &= math.isclose(float(row["upper_inclusive"]), upper, abs_tol=0.0)
        domain_ok &= math.isclose(float(row["lower_slack"]), estimate - lower, rel_tol=0.0, abs_tol=2e-15)
        domain_ok &= math.isclose(float(row["upper_slack"]), upper - estimate, rel_tol=0.0, abs_tol=2e-15)
        domain_ok &= lower <= estimate <= upper
    expected_corners = {(BOUNDS[0, i], BOUNDS[1, j]) for i in range(2) for j in range(2)}
    actual_corners = {(float(row["theta_x"]), float(row["replacement_cost"])) for row in corners}
    corner_ok = len(corners) == 4 and actual_corners == expected_corners
    for row in corners:
        tx, rc = float(row["theta_x"]), float(row["replacement_cost"])
        corner_ok &= math.isclose(float(row["theta_x_lower_slack"]), tx - BOUNDS[0, 0], abs_tol=2e-15)
        corner_ok &= math.isclose(float(row["theta_x_upper_slack"]), BOUNDS[0, 1] - tx, abs_tol=2e-15)
        corner_ok &= math.isclose(float(row["replacement_cost_lower_slack"]), rc - BOUNDS[1, 0], abs_tol=2e-15)
        corner_ok &= math.isclose(float(row["replacement_cost_upper_slack"]), BOUNDS[1, 1] - rc, abs_tol=2e-15)
    pg_tol = float(headline["required_projected_gradient_tolerance"])
    start_logic = []
    for row in starts:
        criterion = row["optimizer_success"].lower() == "true" and float(row["projected_gradient_max"]) <= pg_tol
        saved_accept = row["accepted"].lower() == "true"
        start_logic.append(saved_accept == criterion and saved_accept)
    starts_ok = len(starts) == int(headline["optimizer_start_rows"]) == 10 and all(start_logic)
    return {
        "passed": bool(domain_ok and corner_ok and starts_ok),
        "inclusive_domain_rows_checked": len(domain),
        "all_closed_domain_corners_checked": len(corners),
        "optimizer_start_rows_checked": len(starts),
        "all_starts_pass_post_optimizer_projected_gradient_rule": starts_ok,
    }


def main() -> None:
    checks: dict[str, object] = {}
    try:
        checks["production_hashes"] = verify_hashes()
        panel = read_csv(OUT / "panel.csv")
        t_counts, c_counts = reconstruct_counts(panel)
        checks["saved_transition_and_ccp_counts"] = compare_saved_counts(t_counts, c_counts)
        headline = load_json("headline.json")
        headline_ok = (
            len(panel) == int(headline["sample_rows"])
            == int(headline["transition_count_total"])
            == int(headline["ccp_count_total"])
            == int(t_counts.sum())
            == int(c_counts.sum())
            and int(headline["transition_rows"]) == 50
            and int(headline["ccp_rows"]) == 10
            and int(headline["accepted_optimizer_starts"]) == int(headline["optimizer_start_rows"]) == 10
            and int(headline["closed_domain_rows"]) == 4
            and int(headline["closed_domain_corner_rows"]) == 4
            and int(headline["saved_policy_level_rows"]) == 3
            and headline["identification_scope"] == "local rank diagnostic only"
        )
        checks["headline_reconciliation"] = {"passed": bool(headline_ok), "sample_rows_recomputed": len(panel)}
        checks["closed_domain_and_optimizer_acceptance"] = verify_domain_and_starts(headline)
        transitions = transition_probabilities(t_counts)
        estimate = load_json("estimates.json")["NFXP"]
        theta = np.array([estimate["theta_x"], estimate["replacement_cost"]], dtype=float)
        checks["arbitrary_policy_and_saved_levels"], _ = compare_policy_levels(theta, transitions)
        checks["saved_local_singular_values"] = independent_local_rank(theta, transitions)
    except Exception as exc:
        checks["verifier_exception"] = {"passed": False, "type": type(exc).__name__, "message": str(exc)}

    passed = bool(checks) and all(bool(value.get("passed", False)) for value in checks.values())
    report = {
        "passed": passed,
        "independence": "verify.py does not import production.py and uses an algebraically different arbitrary-policy root solver",
        "coverage": {
            "covered": [
                "production file immutability",
                "transition and CCP row counts/probabilities",
                "headline count reconciliation",
                "inclusive closed domain, every corner, and all saved slacks",
                "all-start projected-gradient acceptance",
                "observed, midpoint, and two off-regime interior policy solutions",
                "direct Bellman residuals, economic monotonicity, and separate accounting levels",
                "saved midpoint levels and saved local singular values",
            ],
            "not_claimed": ["global identification", "out-of-support causal policy validity", "sampling uncertainty"],
        },
        "checks": checks,
    }
    (OUT / "verification.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "checks": {name: value.get("passed", False) for name, value in checks.items()}}, indent=2))
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
