import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import logsumexp


OUT = Path(__file__).resolve().parent
SEED = 20260713
BETA = 0.9
N_STATES = 5
TRUE = np.array([0.7, 2.2])
N, T = 400, 30
N_TRAIN = 300


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


def solve_model(params, tol=1e-11, max_iter=100000):
    theta, rc = np.asarray(params, dtype=float)
    if theta < 0 or rc < 0:
        raise ValueError("parameters must be nonnegative")
    u_keep = -theta * np.arange(N_STATES, dtype=float)
    u_replace = np.full(N_STATES, -rc)
    ev = np.zeros(N_STATES)
    error = np.inf
    for iteration in range(1, max_iter + 1):
        vk = u_keep + BETA * (P_KEEP @ ev)
        vr = u_replace + BETA * (P_REPLACE @ ev)
        new_ev = logsumexp(np.column_stack([vk, vr]), axis=1)
        error = float(np.max(np.abs(new_ev - ev)))
        ev = new_ev
        if error < tol:
            break
    else:
        raise RuntimeError("Bellman iteration failed")
    vk = u_keep + BETA * (P_KEEP @ ev)
    vr = u_replace + BETA * (P_REPLACE @ ev)
    stacked = np.column_stack([vk, vr])
    log_ccp = stacked - logsumexp(stacked, axis=1)[:, None]
    bellman_rhs = logsumexp(stacked, axis=1)
    residual = float(np.max(np.abs(ev - bellman_rhs)))
    return {
        "ev": ev,
        "vk": vk,
        "vr": vr,
        "log_ccp": log_ccp,
        "ccp": np.exp(log_ccp),
        "iterations": iteration,
        "last_update": error,
        "bellman_residual": residual,
    }


def simulate_panel(params, seed=SEED):
    rng = np.random.default_rng(seed)
    solved = solve_model(params, tol=1e-13)
    states = np.zeros((N, T), dtype=np.int8)
    actions = np.zeros((N, T), dtype=np.int8)
    next_states = np.zeros((N, T), dtype=np.int8)
    current = np.zeros(N, dtype=np.int8)
    for tt in range(T):
        states[:, tt] = current
        shocks = rng.gumbel(size=(N, 2))
        indices = np.column_stack([solved["vk"][current], solved["vr"][current]])
        action = np.argmax(indices + shocks, axis=1).astype(np.int8)
        actions[:, tt] = action
        draw = rng.random(N)
        nxt = np.empty(N, dtype=np.int8)
        keep = action == 0
        nxt[keep] = np.minimum(4, current[keep] + (draw[keep] < 0.6))
        nxt[~keep] = (draw[~keep] >= 0.8).astype(np.int8)
        next_states[:, tt] = nxt
        current = nxt
    return states, actions, next_states


def neg_loglike(params, states, actions, tol=1e-11):
    try:
        log_ccp = solve_model(params, tol=tol)["log_ccp"]
    except (ValueError, RuntimeError, FloatingPointError):
        return 1e100
    return -float(np.sum(log_ccp[states.ravel(), actions.ravel()]))


def estimate(states, actions, tol=1e-11):
    starts = [
        np.array([0.15, 0.40]),
        np.array([0.40, 5.50]),
        np.array([1.20, 1.00]),
        np.array([2.50, 6.50]),
        np.array([4.00, 3.00]),
    ]
    runs = []
    for start in starts:
        result = minimize(
            neg_loglike,
            start,
            args=(states, actions, tol),
            method="L-BFGS-B",
            bounds=[(1e-6, 5.0), (1e-6, 8.0)],
            options={"ftol": 1e-12, "gtol": 1e-7, "maxiter": 1000, "maxls": 50},
        )
        runs.append({
            "start": start.tolist(),
            "x": result.x.tolist(),
            "fun": float(result.fun),
            "success": bool(result.success),
            "status": int(result.status),
            "message": str(result.message),
            "nit": int(result.nit),
            "nfev": int(result.nfev),
            "jac": np.asarray(result.jac).tolist(),
        })
    best = min(runs, key=lambda r: r["fun"])
    return np.array(best["x"]), runs


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
    n = len(x)
    hess = np.zeros((n, n))
    for j in range(n):
        h = step * max(1.0, abs(x[j]))
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        hess[:, j] = (finite_gradient(fun, xp) - finite_gradient(fun, xm)) / (2 * h)
    return 0.5 * (hess + hess.T)


def state_fit(states, actions, ccp):
    rows = []
    flat_s, flat_a = states.ravel(), actions.ravel()
    for x in range(N_STATES):
        mask = flat_s == x
        rows.append({
            "state": x,
            "n": int(mask.sum()),
            "observed_replace_rate": float(flat_a[mask].mean()) if mask.any() else None,
            "predicted_replace_rate": float(ccp[x, 1]),
        })
    return rows


def predictive_metrics(states, actions, ccp):
    s, a = states.ravel(), actions.ravel()
    prob = ccp[s, 1]
    eps = 1e-15
    logloss = -float(np.mean(a * np.log(prob + eps) + (1 - a) * np.log(1 - prob + eps)))
    brier = float(np.mean((a - prob) ** 2))
    accuracy = float(np.mean((prob >= 0.5) == a))
    return {"log_loss": logloss, "brier": brier, "accuracy": accuracy}


def stationary_outcomes(params):
    solved = solve_model(params, tol=1e-13)
    pr = solved["ccp"][:, 1]
    q = (1 - pr)[:, None] * P_KEEP + pr[:, None] * P_REPLACE
    dist = np.full(N_STATES, 1 / N_STATES)
    for iteration in range(1, 100000):
        new = dist @ q
        if np.max(np.abs(new - dist)) < 1e-14:
            dist = new
            break
        dist = new
    return {
        "distribution": dist.tolist(),
        "replacement_rate": float(dist @ pr),
        "mean_state": float(dist @ np.arange(N_STATES)),
        "ccp_replace": pr.tolist(),
        "stationary_residual": float(np.max(np.abs(dist @ q - dist))),
        "iterations": iteration,
        "value_at_state_0": float(solved["ev"][0]),
    }


def main():
    states, actions, next_states = simulate_panel(TRUE)
    np.savez_compressed(OUT / "simulated_panel.npz", states=states, actions=actions, next_states=next_states)
    train_s, train_a = states[:N_TRAIN], actions[:N_TRAIN]
    test_s, test_a = states[N_TRAIN:], actions[N_TRAIN:]

    estimate_main, start_runs = estimate(train_s, train_a, tol=1e-11)
    solution = solve_model(estimate_main, tol=1e-11)
    objective = lambda z: neg_loglike(z, train_s, train_a, tol=1e-11)
    grad_fd = finite_gradient(objective, estimate_main)
    hess = finite_hessian(objective, estimate_main)
    eig = np.linalg.eigvalsh(hess)
    covariance = np.linalg.inv(hess)
    se = np.sqrt(np.diag(covariance))
    corr = covariance / np.outer(se, se)

    tolerance_runs = []
    for tol in [1e-8, 1e-10, 1e-12]:
        est, runs = estimate(train_s, train_a, tol=tol)
        tolerance_runs.append({
            "bellman_tolerance": tol,
            "estimate": est.tolist(),
            "nll": float(neg_loglike(est, train_s, train_a, tol=tol)),
            "best_success": bool(min(runs, key=lambda r: r["fun"])["success"]),
        })

    fitted = solve_model(estimate_main, tol=1e-13)
    train_metrics = predictive_metrics(train_s, train_a, fitted["ccp"])
    heldout_metrics = predictive_metrics(test_s, test_a, fitted["ccp"])

    baseline_cf = stationary_outcomes(estimate_main)
    policy_params = estimate_main.copy()
    policy_params[1] *= 0.75
    policy_cf = stationary_outcomes(policy_params)

    empirical_transition = np.zeros((2, N_STATES, N_STATES))
    empirical_counts = np.zeros((2, N_STATES))
    for a in [0, 1]:
        for x in range(N_STATES):
            mask = (states.ravel() == x) & (actions.ravel() == a)
            empirical_counts[a, x] = mask.sum()
            if mask.any():
                empirical_transition[a, x] = np.bincount(next_states.ravel()[mask], minlength=N_STATES) / mask.sum()

    diagnostics = {
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "seed": SEED,
        "sample": {"physicians": N, "periods": T, "train_physicians": N_TRAIN, "heldout_physicians": N-N_TRAIN},
        "true_params": {"theta": TRUE[0], "RC": TRUE[1]},
        "estimate": {"theta": estimate_main[0], "RC": estimate_main[1]},
        "recovery_error": (estimate_main - TRUE).tolist(),
        "standard_errors_hessian": se.tolist(),
        "hessian": hess.tolist(),
        "hessian_eigenvalues": eig.tolist(),
        "hessian_condition_number": float(eig.max() / eig.min()),
        "parameter_correlation": corr.tolist(),
        "start_runs": start_runs,
        "bellman": {k: solution[k] for k in ["iterations", "last_update", "bellman_residual"]},
        "finite_difference_gradient": grad_fd.tolist(),
        "finite_difference_gradient_max_abs": float(np.max(np.abs(grad_fd))),
        "tolerance_sensitivity": tolerance_runs,
        "train_predictive": train_metrics,
        "heldout_predictive": heldout_metrics,
        "train_state_fit": state_fit(train_s, train_a, fitted["ccp"]),
        "heldout_state_fit": state_fit(test_s, test_a, fitted["ccp"]),
        "baseline_stationary": baseline_cf,
        "counterfactual_params": {"theta": policy_params[0], "RC": policy_params[1]},
        "counterfactual_stationary": policy_cf,
        "counterfactual_changes": {
            "replacement_rate": policy_cf["replacement_rate"] - baseline_cf["replacement_rate"],
            "mean_state": policy_cf["mean_state"] - baseline_cf["mean_state"],
            "value_at_state_0": policy_cf["value_at_state_0"] - baseline_cf["value_at_state_0"],
        },
        "choice_counts": {"train_replace": int(train_a.sum()), "train_total": int(train_a.size), "test_replace": int(test_a.sum()), "test_total": int(test_a.size)},
        "empirical_transition_counts": empirical_counts.tolist(),
        "empirical_transition_probabilities": empirical_transition.tolist(),
    }
    (OUT / "diagnostics.json").write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")

    summary_lines = [
        "Dynamic replacement NFXP run",
        f"estimate theta={estimate_main[0]:.6f}, RC={estimate_main[1]:.6f}",
        f"true theta={TRUE[0]:.6f}, RC={TRUE[1]:.6f}",
        f"Bellman residual={solution['bellman_residual']:.3e}, iterations={solution['iterations']}",
        f"FD gradient={grad_fd.tolist()}",
        f"Hessian eigenvalues={eig.tolist()}, condition={eig.max()/eig.min():.3f}",
        f"heldout logloss={heldout_metrics['log_loss']:.6f}, brier={heldout_metrics['brier']:.6f}",
        f"baseline replacement={baseline_cf['replacement_rate']:.6f}, mean state={baseline_cf['mean_state']:.6f}",
        f"policy replacement={policy_cf['replacement_rate']:.6f}, mean state={policy_cf['mean_state']:.6f}",
    ]
    (OUT / "run_summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print("\n".join(summary_lines))


if __name__ == "__main__":
    main()
