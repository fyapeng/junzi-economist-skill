import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln, logsumexp, expit


HERE = Path(__file__).resolve().parent


def main():
    # Independence boundary: this program reads only primitives/config and defines its own likelihood,
    # derivatives, starts, acceptance logic, profile construction, and policy mapping.
    with (HERE / "raw_primitives.json").open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    m = int(spec["trials_per_unit"])
    y = np.arange(m + 1, dtype=float)
    freq = np.asarray(spec["success_count_frequencies"], dtype=float)
    choose = gammaln(m + 1) - gammaln(y + 1) - gammaln(m - y + 1)
    bounds3 = [tuple(spec["parameter_bounds"][key]) for key in ("pi", "p_a", "p_b")]

    def calc(x, fixed=None):
        if fixed is None:
            pi, a, b = x
        else:
            pi = float(fixed)
            a, b = x
        la = np.log(pi) + choose + y * np.log(a) + (m - y) * np.log1p(-a)
        lb = np.log1p(-pi) + choose + y * np.log(b) + (m - y) * np.log1p(-b)
        normalizer = logsumexp(np.stack([la, lb]), axis=0)
        wa = np.exp(la - normalizer)
        dpi = wa / pi - (1 - wa) / (1 - pi)
        da = wa * (y / a - (m - y) / (1 - a))
        db = (1 - wa) * (y / b - (m - y) / (1 - b))
        scores = -np.array([freq @ dpi, freq @ da, freq @ db])
        return -float(freq @ normalizer), scores if fixed is None else scores[1:], scores

    def pg(x, gradient, box):
        answer = np.array(gradient, copy=True)
        for j, (value, slope, (lower, upper)) in enumerate(zip(x, gradient, box)):
            if abs(value - lower) <= 1e-9 and slope >= 0:
                answer[j] = 0
            if abs(value - upper) <= 1e-9 and slope <= 0:
                answer[j] = 0
        return answer

    def solve(start, box, fixed=None):
        result = minimize(
            lambda x: calc(x, fixed)[:2],
            np.asarray(start, dtype=float),
            method="L-BFGS-B",
            jac=True,
            bounds=box,
            options={"gtol": 5e-11, "ftol": 5e-15, "maxiter": 5000, "maxls": 60},
        )
        value, free_grad, full_grad = calc(result.x, fixed)
        residual = float(np.max(np.abs(pg(result.x, free_grad, box))))
        return result, value, full_grad, residual

    # Fresh starts deliberately differ from production starts.
    u_starts = [
        [0.12, 0.04, 0.72], [0.88, 0.72, 0.04], [0.27, 0.25, 0.92],
        [0.73, 0.92, 0.25], [0.44, 0.12, 0.62], [0.56, 0.62, 0.12],
        [0.31, 0.94, 0.06], [0.69, 0.06, 0.94],
    ]
    candidates = [solve(start, bounds3) for start in u_starts]
    admissible = [row for row in candidates if row[0].success and row[3] <= spec["optimizer"]["accept_kkt_inf"]]
    if not admissible:
        raise SystemExit("Independent unrestricted solve failed acceptance.")
    u_result, u_nll, _, u_kkt = min(admissible, key=lambda row: row[1])

    c_starts = [[0.03, 0.66], [0.66, 0.03], [0.22, 0.93], [0.93, 0.22], [0.34, 0.58], [0.58, 0.34]]
    rows = []
    for pi in spec["profile_grid_pi"]:
        trials = [solve(start, bounds3[1:], fixed=pi) for start in c_starts]
        accepted = [row for row in trials if row[0].success and row[3] <= spec["optimizer"]["accept_kkt_inf"]]
        if not accepted:
            raise SystemExit(f"Independent conditional solve failed at pi={pi}.")
        result, nll, full_gradient, kkt = min(accepted, key=lambda row: row[1])
        a, b = (float(v) for v in result.x)
        lr = 2 * (nll - u_nll)
        chosen = bool(lr <= spec["lr_cutoff"])
        mapped = None
        if chosen:
            shift = spec["policy"]["log_odds_shift"]
            aa = expit(math.log(a / (1 - a)) + shift)
            bb = expit(math.log(b / (1 - b)) + shift)
            mapped = float(pi * aa + (1 - pi) * bb)
        rows.append({
            "pi": float(pi), "accepted": True, "nll": nll,
            "lr_from_unrestricted": lr, "p_a": a, "p_b": b,
            "support_low": min(a, b), "support_high": max(a, b),
            "profile_score_pi": float(full_gradient[0]), "kkt_inf_free": kkt,
            "selected_by_lr": chosen, "policy_probability": mapped,
        })

    selected = [row for row in rows if row["selected_by_lr"]]
    holes = [row["pi"] for row in rows if selected[0]["pi"] < row["pi"] < selected[-1]["pi"] and not row["selected_by_lr"]]
    policy = [row["policy_probability"] for row in selected]
    realized_n = int(freq.sum())
    declared_grid = [float(v) for v in spec["profile_grid_pi"]]
    evaluated_grid = [row["pi"] for row in rows]
    report = {
        "verifier_independence": {
            "imports_production_functions": False,
            "inputs_read": ["raw_primitives.json"],
            "stored_solutions_or_objectives_read": False,
            "fresh_unrestricted_start_count": len(u_starts),
            "fresh_conditional_starts_per_grid_point": len(c_starts),
        },
        "sample_count_check": {"intended": spec["intended_unit_count"], "realized": realized_n, "exact_match": realized_n == spec["intended_unit_count"]},
        "unrestricted": {
            "accepted": True, "nll": u_nll,
            "pi_coordinate_a": float(u_result.x[0]), "p_a": float(u_result.x[1]), "p_b": float(u_result.x[2]),
            "support_low": float(min(u_result.x[1], u_result.x[2])),
            "support_high": float(max(u_result.x[1], u_result.x[2])), "kkt_inf": u_kkt,
        },
        "grid_coverage": {
            "declared_grid": declared_grid, "evaluated_grid": evaluated_grid,
            "declared_count": len(declared_grid), "evaluated_count": len(evaluated_grid),
            "accepted_count": sum(row["accepted"] for row in rows),
            "exact_order_and_value_match": evaluated_grid == declared_grid,
            "missing_grid_points": [v for v in declared_grid if v not in evaluated_grid],
            "extra_grid_points": [v for v in evaluated_grid if v not in declared_grid],
        },
        "evaluated_grid_set": {
            "lr_reference": "independently accepted unrestricted optimum of the same likelihood",
            "selected_pi": [row["pi"] for row in selected], "selected_count": len(selected),
            "excluded_holes_inside_selected_span": holes,
            "lower_grid_censored": selected[0]["pi"] == declared_grid[0],
            "upper_grid_censored": selected[-1]["pi"] == declared_grid[-1],
        },
        "selected_only_policy_mapping": {
            "mapped_count": len(policy), "unselected_mapped_count": sum(row["policy_probability"] is not None for row in rows if not row["selected_by_lr"]),
            "minimum_probability": min(policy), "maximum_probability": max(policy),
        },
        "profile_recomputation": rows,
        "headline_coverage": {
            "unrestricted_optimum": "recomputed", "all_conditional_grid_optima": "recomputed",
            "projected_kkt_acceptance": "recomputed", "likelihood_ratios": "recomputed",
            "grid_holes_and_censoring": "recomputed", "selected_only_policy_mapping": "recomputed",
            "sample_and_grid_counts": "recomputed",
        },
        "verdict": "pass" if realized_n == spec["intended_unit_count"] and evaluated_grid == declared_grid and len(rows) == sum(row["accepted"] for row in rows) else "fail",
    }
    with (HERE / "verification_report.json").open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    if report["verdict"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
