import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import gammaln, expit, logsumexp


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_primitives.json"


def load_primitives():
    with RAW.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def component_logpmf(y, m, p):
    return (
        gammaln(m + 1)
        - gammaln(y + 1)
        - gammaln(m - y + 1)
        + y * np.log(p)
        + (m - y) * np.log1p(-p)
    )


def objective_and_gradient(theta, y, counts, m, fixed_pi=None):
    if fixed_pi is None:
        pi, p_a, p_b = theta
    else:
        pi = float(fixed_pi)
        p_a, p_b = theta
    log_a = math.log(pi) + component_logpmf(y, m, p_a)
    log_b = math.log1p(-pi) + component_logpmf(y, m, p_b)
    denom = logsumexp(np.vstack((log_a, log_b)), axis=0)
    resp_a = np.exp(log_a - denom)
    score_pi = resp_a / pi - (1.0 - resp_a) / (1.0 - pi)
    score_a = resp_a * (y / p_a - (m - y) / (1.0 - p_a))
    score_b = (1.0 - resp_a) * (y / p_b - (m - y) / (1.0 - p_b))
    nll = -float(np.dot(counts, denom))
    if fixed_pi is None:
        grad = -np.array(
            [np.dot(counts, score_pi), np.dot(counts, score_a), np.dot(counts, score_b)]
        )
    else:
        grad = -np.array([np.dot(counts, score_a), np.dot(counts, score_b)])
    full_grad = -np.array(
        [np.dot(counts, score_pi), np.dot(counts, score_a), np.dot(counts, score_b)]
    )
    return nll, grad, full_grad


def projected_gradient(theta, gradient, bounds):
    result = np.asarray(gradient, dtype=float).copy()
    active = []
    for index, ((lower, upper), value, grad) in enumerate(zip(bounds, theta, gradient)):
        label = "none"
        if abs(value - lower) <= 1e-9:
            label = "lower"
            if grad >= 0.0:
                result[index] = 0.0
        elif abs(value - upper) <= 1e-9:
            label = "upper"
            if grad <= 0.0:
                result[index] = 0.0
        active.append(label)
    return result, active


def run_start(start_id, start, bounds, y, counts, m, fixed_pi=None):
    def fun(value):
        return objective_and_gradient(value, y, counts, m, fixed_pi)[:2]

    result = minimize(
        fun,
        np.asarray(start, dtype=float),
        method="L-BFGS-B",
        jac=True,
        bounds=bounds,
        options={"gtol": 1e-10, "ftol": 1e-14, "maxiter": 4000, "maxls": 50},
    )
    _, free_gradient, full_gradient = objective_and_gradient(
        result.x, y, counts, m, fixed_pi
    )
    projected, active = projected_gradient(result.x, free_gradient, bounds)
    return {
        "start_id": start_id,
        "profile_pi": fixed_pi,
        "initial": [float(value) for value in start],
        "terminal_free": [float(value) for value in result.x],
        "nll": float(result.fun),
        "raw_gradient_free": [float(value) for value in free_gradient],
        "raw_gradient_full_pi_pa_pb": [float(value) for value in full_gradient],
        "projected_gradient_free": [float(value) for value in projected],
        "kkt_inf_free": float(np.max(np.abs(projected))),
        "active_bounds_free": active,
        "solver_success": bool(result.success),
        "solver_status": int(result.status),
        "solver_message": str(result.message),
        "iterations": int(result.nit),
        "function_evaluations": int(result.nfev),
    }


def policy_probability(pi, p_a, p_b, shift):
    moved_a = expit(math.log(p_a / (1.0 - p_a)) + shift)
    moved_b = expit(math.log(p_b / (1.0 - p_b)) + shift)
    return float(pi * moved_a + (1.0 - pi) * moved_b)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    cfg = load_primitives()
    y = np.arange(cfg["trials_per_unit"] + 1, dtype=float)
    counts = np.asarray(cfg["success_count_frequencies"], dtype=float)
    realized_n = int(counts.sum())
    intended_n = int(cfg["intended_unit_count"])
    if realized_n != intended_n:
        raise RuntimeError(f"Intended {intended_n} units but frequencies imply {realized_n}.")

    parameter_bounds = [tuple(cfg["parameter_bounds"][name]) for name in ("pi", "p_a", "p_b")]
    unrestricted_starts = [
        [0.20, 0.08, 0.78],
        [0.80, 0.78, 0.08],
        [0.35, 0.15, 0.70],
        [0.65, 0.70, 0.15],
        [0.50, 0.05, 0.90],
        [0.50, 0.90, 0.05],
    ]
    conditional_starts = [
        [0.08, 0.78],
        [0.78, 0.08],
        [0.15, 0.70],
        [0.70, 0.15],
        [0.40, 0.85],
    ]
    if len(unrestricted_starts) != cfg["intended_starts"]["unrestricted"]:
        raise RuntimeError("Unrestricted start declaration does not match implementation.")
    if len(conditional_starts) != cfg["intended_starts"]["per_profile_grid_point"]:
        raise RuntimeError("Conditional start declaration does not match implementation.")

    all_starts = []
    unrestricted_runs = []
    for index, start in enumerate(unrestricted_starts):
        record = run_start(
            f"u{index + 1:02d}", start, parameter_bounds, y, counts, cfg["trials_per_unit"]
        )
        unrestricted_runs.append(record)
        all_starts.append(record)
    unrestricted = min(unrestricted_runs, key=lambda row: row["nll"])
    accept_tol = cfg["optimizer"]["accept_kkt_inf"]
    unrestricted_accepted = unrestricted["solver_success"] and unrestricted["kkt_inf_free"] <= accept_tol
    if not unrestricted_accepted:
        raise RuntimeError("No accepted unrestricted optimum.")

    grid_records = []
    conditional_bounds = parameter_bounds[1:]
    for grid_index, pi in enumerate(cfg["profile_grid_pi"]):
        runs = []
        for start_index, start in enumerate(conditional_starts):
            record = run_start(
                f"g{grid_index + 1:02d}s{start_index + 1:02d}",
                start,
                conditional_bounds,
                y,
                counts,
                cfg["trials_per_unit"],
                fixed_pi=pi,
            )
            runs.append(record)
            all_starts.append(record)
        accepted_runs = [
            row for row in runs if row["solver_success"] and row["kkt_inf_free"] <= accept_tol
        ]
        if not accepted_runs:
            raise RuntimeError(f"No accepted conditional optimum at pi={pi}.")
        best = min(accepted_runs, key=lambda row: row["nll"])
        p_a, p_b = best["terminal_free"]
        low, high = sorted((p_a, p_b))
        lr = 2.0 * (best["nll"] - unrestricted["nll"])
        selected = bool(lr <= cfg["lr_cutoff"])
        grid_records.append(
            {
                "record_type": "conditional_profile",
                "pi": float(pi),
                "accepted": True,
                "selected_by_lr": selected,
                "best_start_id": best["start_id"],
                "nll": best["nll"],
                "lr_from_unrestricted": float(lr),
                "p_a": p_a,
                "p_b": p_b,
                "support_low": low,
                "support_high": high,
                "profile_score_pi": best["raw_gradient_full_pi_pa_pb"][0],
                "projected_gradient_free": best["projected_gradient_free"],
                "kkt_inf_free": best["kkt_inf_free"],
                "active_bounds_free": best["active_bounds_free"],
                "policy_probability": policy_probability(pi, p_a, p_b, cfg["policy"]["log_odds_shift"])
                if selected
                else None,
            }
        )

    intended_start_count = len(unrestricted_starts) + len(cfg["profile_grid_pi"]) * len(conditional_starts)
    realized_start_count = len(all_starts)
    if intended_start_count != realized_start_count:
        raise RuntimeError("Intended and realized optimizer-start counts differ.")
    selected = [row for row in grid_records if row["selected_by_lr"]]
    excluded_inside_span = [
        row["pi"]
        for row in grid_records
        if selected[0]["pi"] < row["pi"] < selected[-1]["pi"] and not row["selected_by_lr"]
    ]
    lower_censored = selected[0]["pi"] == cfg["profile_grid_pi"][0]
    upper_censored = selected[-1]["pi"] == cfg["profile_grid_pi"][-1]
    u_pi, u_pa, u_pb = unrestricted["terminal_free"]
    ranked_unrestricted = sorted((u_pa, u_pb))

    profile_rows = [
        {
            "record_type": "unrestricted",
            "accepted": True,
            "best_start_id": unrestricted["start_id"],
            "nll": unrestricted["nll"],
            "pi": u_pi,
            "p_a": u_pa,
            "p_b": u_pb,
            "support_low": ranked_unrestricted[0],
            "support_high": ranked_unrestricted[1],
            "projected_gradient_free": unrestricted["projected_gradient_free"],
            "kkt_inf_free": unrestricted["kkt_inf_free"],
            "active_bounds_free": unrestricted["active_bounds_free"],
        }
    ] + grid_records
    with (ROOT / "start_records.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in all_starts:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    with (ROOT / "profile_records.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in profile_rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

    policy_values = [row["policy_probability"] for row in selected]
    response = {
        "claim_status": "provisional_structural_grid_evidence",
        "economic_object": "Latent heterogeneity in repeated binary success and the model-implied response to a common log-odds policy shift.",
        "sample_count_check": {"intended": intended_n, "realized": realized_n, "exact_match": True},
        "start_count_check": {
            "intended": intended_start_count,
            "realized": realized_start_count,
            "exact_match": True,
        },
        "unrestricted": {
            "accepted": True,
            "nll": unrestricted["nll"],
            "pi_coordinate_a": u_pi,
            "p_a": u_pa,
            "p_b": u_pb,
            "support_labels": {"low": ranked_unrestricted[0], "high": ranked_unrestricted[1]},
            "kkt_inf": unrestricted["kkt_inf_free"],
        },
        "evaluated_grid_set": {
            "label": "evaluated-grid LR set; not a continuous confidence set",
            "lr_reference": "accepted unrestricted optimum of the same binomial-mixture likelihood",
            "cutoff": cfg["lr_cutoff"],
            "evaluated_count": len(grid_records),
            "accepted_count": sum(row["accepted"] for row in grid_records),
            "selected_count": len(selected),
            "selected_pi": [row["pi"] for row in selected],
            "excluded_holes_inside_selected_span": excluded_inside_span,
            "lower_grid_censored": lower_censored,
            "upper_grid_censored": upper_censored,
        },
        "selected_only_policy_mapping": {
            "mapped_count": len(policy_values),
            "unselected_mapped_count": 0,
            "log_odds_shift": cfg["policy"]["log_odds_shift"],
            "minimum_probability": min(policy_values),
            "maximum_probability": max(policy_values),
        },
        "support_interpretation": "Coordinate A/B labels switch across observationally equivalent branches; economic labels are the ranked low and high success-probability supports.",
        "branch_decision": {
            "decision": "retain_both_coordinate_branches_interpret_ranked_supports_only",
            "evidence": "The two selected profile components are label-switched likelihood branches, while ranked supports and the policy mixture are invariant up to numerical error.",
            "scope": "No coordinate-label identification or continuous-set claim is made; grid-edge inclusion is reported as censoring.",
        },
    }
    with (ROOT / "response.json").open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(response, handle, indent=2, sort_keys=True)
        handle.write("\n")

    provenance = {
        "entrypoint": "run_profile.py",
        "raw_primitives": "raw_primitives.json",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "raw_sha256": sha256(RAW),
        "production_code_sha256": sha256(ROOT / "run_profile.py"),
        "randomness": "none; deterministic declared starts",
        "likelihood": "two-support binomial mixture including binomial coefficients",
        "serialization": "JSON numeric values use Python round-trip-safe float representation",
    }
    with (ROOT / "provenance.json").open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(provenance, handle, indent=2, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    main()
