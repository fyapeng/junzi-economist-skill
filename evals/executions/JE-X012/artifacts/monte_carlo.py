import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import logsumexp


OUT = Path(__file__).resolve().parent
TRUE = np.array([0.7, 2.2])
BETA = 0.9
N_STATES = 5
T = 30
SAMPLE_SIZES = [100, 400]
REPLICATIONS = 60
BASE_SEED = 2026071300
BELLMAN_TOL = 1e-10
BOUNDS = [(1e-6, 5.0), (1e-6, 8.0)]
STARTS = [np.array([0.30, 1.00]), np.array([1.50, 4.50])]
BOUNDARY_TOL = 1e-4


def transition_matrices():
    keep = np.zeros((N_STATES, N_STATES))
    for x in range(N_STATES):
        keep[x, x] += 0.4
        keep[x, min(4, x + 1)] += 0.6
    replace = np.zeros((N_STATES, N_STATES))
    replace[:, 0] = 0.8
    replace[:, 1] = 0.2
    return keep, replace


P_KEEP, P_REPLACE = transition_matrices()


def solve_model(params, tol=BELLMAN_TOL, max_iter=100000):
    theta, rc = np.asarray(params, dtype=float)
    if theta < 0 or rc < 0:
        raise ValueError("negative parameter")
    u_keep = -theta * np.arange(N_STATES, dtype=float)
    u_replace = np.full(N_STATES, -rc)
    ev = np.zeros(N_STATES)
    for iteration in range(1, max_iter + 1):
        vk = u_keep + BETA * (P_KEEP @ ev)
        vr = u_replace + BETA * (P_REPLACE @ ev)
        new = logsumexp(np.column_stack([vk, vr]), axis=1)
        update = float(np.max(np.abs(new - ev)))
        ev = new
        if update < tol:
            break
    else:
        raise RuntimeError("Bellman failure")
    vk = u_keep + BETA * (P_KEEP @ ev)
    vr = u_replace + BETA * (P_REPLACE @ ev)
    indices = np.column_stack([vk, vr])
    log_ccp = indices - logsumexp(indices, axis=1)[:, None]
    residual = float(np.max(np.abs(ev - logsumexp(indices, axis=1))))
    return {"ev": ev, "ccp": np.exp(log_ccp), "log_ccp": log_ccp,
            "vk": vk, "vr": vr, "iterations": iteration,
            "update": update, "residual": residual}


TRUE_SOLVED = solve_model(TRUE, tol=1e-13)


def simulate_panel(n, seed):
    rng = np.random.default_rng(seed)
    states = np.zeros((n, T), dtype=np.int8)
    actions = np.zeros((n, T), dtype=np.int8)
    current = np.zeros(n, dtype=np.int8)
    for tt in range(T):
        states[:, tt] = current
        shocks = rng.gumbel(size=(n, 2))
        indices = np.column_stack([TRUE_SOLVED["vk"][current], TRUE_SOLVED["vr"][current]])
        action = np.argmax(indices + shocks, axis=1).astype(np.int8)
        actions[:, tt] = action
        draw = rng.random(n)
        nxt = np.empty(n, dtype=np.int8)
        keep = action == 0
        nxt[keep] = np.minimum(4, current[keep] + (draw[keep] < 0.6))
        nxt[~keep] = (draw[~keep] >= 0.8).astype(np.int8)
        current = nxt
    return states, actions


def nll(params, states, actions):
    try:
        log_ccp = solve_model(params)["log_ccp"]
        value = -float(np.sum(log_ccp[states.ravel(), actions.ravel()]))
        return value if np.isfinite(value) else 1e100
    except Exception:
        return 1e100


def finite_gradient(fun, x, step=1e-5):
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    for j in range(len(x)):
        h = step * max(1.0, abs(x[j]))
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        grad[j] = (fun(xp) - fun(xm)) / (2 * h)
    return grad


def finite_hessian(fun, x, step=2e-4):
    x = np.asarray(x, dtype=float)
    hess = np.zeros((len(x), len(x)))
    for j in range(len(x)):
        h = step * max(1.0, abs(x[j]))
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        hess[:, j] = (finite_gradient(fun, xp) - finite_gradient(fun, xm)) / (2 * h)
    return 0.5 * (hess + hess.T)


def estimate_replication(states, actions):
    runs = []
    for start in STARTS:
        try:
            res = minimize(nll, start, args=(states, actions), method="L-BFGS-B",
                           bounds=BOUNDS,
                           options={"ftol": 1e-11, "gtol": 1e-7, "maxiter": 600, "maxls": 50})
            runs.append({"start": start.tolist(), "success": bool(res.success),
                         "status": int(res.status), "message": str(res.message),
                         "x": res.x.tolist(), "fun": float(res.fun),
                         "nit": int(res.nit), "nfev": int(res.nfev),
                         "jac": np.asarray(res.jac).tolist()})
        except Exception as exc:
            runs.append({"start": start.tolist(), "success": False,
                         "status": -999, "message": repr(exc), "x": [None, None],
                         "fun": None, "nit": 0, "nfev": 0, "jac": [None, None]})
    valid = [r for r in runs if r["success"] and r["fun"] is not None
             and np.isfinite(r["fun"]) and all(v is not None and np.isfinite(v) for v in r["x"])]
    if not valid:
        return {"optimizer_success": False, "runs": runs}
    best = min(valid, key=lambda r: r["fun"])
    estimate = np.array(best["x"])
    fun = lambda z: nll(z, states, actions)
    try:
        hess = finite_hessian(fun, estimate)
        eig = np.linalg.eigvalsh(hess)
        if np.all(eig > 0) and np.all(np.isfinite(eig)):
            cov = np.linalg.inv(hess)
            se = np.sqrt(np.diag(cov))
            hessian_success = bool(np.all(np.isfinite(se)))
        else:
            se = np.array([np.nan, np.nan])
            hessian_success = False
    except Exception:
        hess = np.full((2, 2), np.nan)
        eig = np.array([np.nan, np.nan])
        se = np.array([np.nan, np.nan])
        hessian_success = False
    grad = finite_gradient(fun, estimate)
    boundary = [bool(abs(estimate[j] - BOUNDS[j][0]) <= BOUNDARY_TOL or
                     abs(estimate[j] - BOUNDS[j][1]) <= BOUNDARY_TOL) for j in range(2)]
    covered = [bool(estimate[j] - 1.96 * se[j] <= TRUE[j] <= estimate[j] + 1.96 * se[j])
               if hessian_success else None for j in range(2)]
    solved = solve_model(estimate)
    return {"optimizer_success": True, "hessian_success": hessian_success,
            "estimate": estimate.tolist(), "error": (estimate - TRUE).tolist(),
            "se": se.tolist(), "covered": covered, "boundary": boundary,
            "hessian_eigenvalues": eig.tolist(), "gradient": grad.tolist(),
            "bellman_residual": solved["residual"], "bellman_iterations": solved["iterations"],
            "best_nll": best["fun"], "runs": runs}


def summarize(records, n):
    subset = [r for r in records if r["n"] == n]
    valid = [r for r in subset if r.get("optimizer_success")]
    hvalid = [r for r in valid if r.get("hessian_success")]
    est = np.array([r["estimate"] for r in valid])
    err = est - TRUE
    se = np.array([r["se"] for r in hvalid]) if hvalid else np.empty((0, 2))
    coverage = np.array([r["covered"] for r in hvalid], dtype=float) if hvalid else np.empty((0, 2))
    result = {
        "n_physicians": n, "periods": T, "replications": len(subset),
        "optimizer_failures": len(subset) - len(valid),
        "optimizer_failure_rate": (len(subset) - len(valid)) / len(subset),
        "hessian_failures": len(valid) - len(hvalid),
        "hessian_failure_rate_among_optimizer_success": (len(valid) - len(hvalid)) / max(1, len(valid)),
        "successful_estimates": len(valid), "valid_hessian_estimates": len(hvalid),
        "bias": np.mean(err, axis=0).tolist(),
        "rmse": np.sqrt(np.mean(err ** 2, axis=0)).tolist(),
        "empirical_sd": np.std(est, axis=0, ddof=1).tolist(),
        "mean_hessian_se": np.mean(se, axis=0).tolist() if len(se) else [None, None],
        "wald_95_coverage": np.mean(coverage, axis=0).tolist() if len(coverage) else [None, None],
        "boundary_hits": np.sum(np.array([r["boundary"] for r in valid]), axis=0).tolist(),
        "max_abs_gradient": float(max(np.max(np.abs(r["gradient"])) for r in valid)),
        "max_bellman_residual": float(max(r["bellman_residual"] for r in valid)),
    }
    worst = []
    for j, name in enumerate(["theta", "RC"]):
        k = int(np.argmax(np.abs(err[:, j])))
        rec = valid[k]
        worst.append({"parameter": name, "replication": rec["replication"],
                      "seed": rec["seed"], "estimate": rec["estimate"][j],
                      "error": rec["error"][j], "se": rec["se"][j],
                      "covered": rec["covered"][j], "boundary": rec["boundary"][j]})
    result["worst_cases"] = worst
    return result


def ccp_vector(params):
    return solve_model(params, tol=1e-12)["ccp"][:, 1]


def population_identification():
    target = ccp_vector(TRUE)
    jac = np.zeros((N_STATES, 2))
    for j in range(2):
        h = 1e-5 * max(1.0, abs(TRUE[j]))
        xp, xm = TRUE.copy(), TRUE.copy()
        xp[j] += h
        xm[j] -= h
        jac[:, j] = (ccp_vector(xp) - ccp_vector(xm)) / (2 * h)
    singular = np.linalg.svd(jac, compute_uv=False)

    def scan(theta_grid, rc_grid, exclusion):
        best = None
        count = 0
        for theta in theta_grid:
            for rc in rc_grid:
                params = np.array([theta, rc])
                pdist = float(np.linalg.norm(params - TRUE))
                if pdist < exclusion:
                    continue
                diff = ccp_vector(params) - target
                d2 = float(np.linalg.norm(diff))
                maxabs = float(np.max(np.abs(diff)))
                count += 1
                if best is None or d2 < best["ccp_l2"]:
                    best = {"params": params.tolist(), "parameter_distance": pdist,
                            "ccp_l2": d2, "ccp_max_abs": maxabs,
                            "ccp": (target + diff).tolist()}
        return {"points_scanned": count, "exclusion_radius": exclusion, "closest": best}

    nearby = scan(np.linspace(TRUE[0] - 0.25, TRUE[0] + 0.25, 51),
                  np.linspace(TRUE[1] - 0.50, TRUE[1] + 0.50, 51), 0.02)
    broad = scan(np.linspace(0.05, 2.00, 60), np.linspace(0.20, 6.00, 80), 0.05)

    inverse_starts = [np.array([t, r]) for t in [0.05, 0.4, 1.0, 2.0]
                      for r in [0.2, 2.5, 6.0]]
    inverse_runs = []
    objective = lambda z: float(np.sum((ccp_vector(z) - target) ** 2))
    for start in inverse_starts:
        res = minimize(objective, start, method="L-BFGS-B", bounds=BOUNDS,
                       options={"ftol": 1e-15, "gtol": 1e-11, "maxiter": 1000, "maxls": 50})
        inverse_runs.append({"start": start.tolist(), "success": bool(res.success),
                             "x": res.x.tolist(), "objective": float(res.fun),
                             "parameter_distance_from_truth": float(np.linalg.norm(res.x - TRUE)),
                             "message": str(res.message)})
    return {"truth": TRUE.tolist(), "truth_ccp": target.tolist(),
            "jacobian": jac.tolist(), "singular_values": singular.tolist(),
            "rank_tolerance_1e-8": int(np.sum(singular > 1e-8)),
            "condition_number": float(singular[0] / singular[-1]),
            "nearby_grid": nearby, "broad_grid": broad,
            "inverse_mapping_runs": inverse_runs}


def main():
    jsonl = OUT / "replications.jsonl"
    expected_records = len(SAMPLE_SIZES) * REPLICATIONS
    if jsonl.exists():
        records = [json.loads(line) for line in jsonl.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        records = []
    if len(records) == expected_records:
        print(f"Reusing {len(records)} completed replication records", flush=True)
    else:
        records = []
        with jsonl.open("w", encoding="utf-8", newline="\n") as handle:
            for size_index, n in enumerate(SAMPLE_SIZES):
                for replication in range(REPLICATIONS):
                    seed = BASE_SEED + 10000 * size_index + replication
                    states, actions = simulate_panel(n, seed)
                    record = {"n": n, "periods": T, "replication": replication,
                              "seed": seed, "replace_count": int(actions.sum()),
                              "observations": int(actions.size)}
                    record.update(estimate_replication(states, actions))
                    records.append(record)
                    handle.write(json.dumps(record) + "\n")
                    handle.flush()
                    if (replication + 1) % 10 == 0:
                        print(f"n={n}: completed {replication+1}/{REPLICATIONS}", flush=True)

    summaries = [summarize(records, n) for n in SAMPLE_SIZES]
    identification = population_identification()
    output = {
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "protocol": {"sample_sizes": SAMPLE_SIZES, "periods": T,
                     "replications_per_size": REPLICATIONS, "starts": [x.tolist() for x in STARTS],
                     "bellman_tolerance": BELLMAN_TOL, "bounds": BOUNDS,
                     "base_seed": BASE_SEED},
        "truth": {"theta": TRUE[0], "RC": TRUE[1]},
        "monte_carlo_summaries": summaries,
        "population_identification": identification,
    }
    (OUT / "summary.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    lines = ["Repeated-sample dynamic replacement study"]
    for s in summaries:
        lines += [
            f"N={s['n_physicians']}, reps={s['replications']}, optimizer failures={s['optimizer_failures']}, Hessian failures={s['hessian_failures']}",
            f"  bias theta/RC={s['bias']}",
            f"  RMSE theta/RC={s['rmse']}",
            f"  empirical SD theta/RC={s['empirical_sd']}",
            f"  mean SE theta/RC={s['mean_hessian_se']}",
            f"  coverage theta/RC={s['wald_95_coverage']}",
            f"  boundary hits theta/RC={s['boundary_hits']}",
        ]
    lines += [
        f"Population Jacobian singular values={identification['singular_values']}",
        f"Population Jacobian rank={identification['rank_tolerance_1e-8']}, condition={identification['condition_number']}",
        f"Nearby closest={identification['nearby_grid']['closest']}",
        f"Broad closest={identification['broad_grid']['closest']}",
    ]
    (OUT / "run_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
