import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize
from scipy.special import expit, logsumexp


OUT = Path(r"C:\Users\ENAN\AppData\Local\Temp\junzi-economist-struct-x044")
TRUE = {"theta": 0.65, "RC": 3.2, "p": 0.6, "beta": 0.9}
X = np.arange(6, dtype=float)
T = 25
TRAIN_T = 20
SEEDS = [1103, 2207, 3313, 4421, 5531]
SIZES = [400, 2000]
BOUNDS = [(0.02, 2.0), (0.2, 8.0)]
STARTS = [(0.25, 1.5), (0.65, 3.2), (1.2, 5.5), (1.8, 7.5)]


def trans(p):
    pk = np.zeros((6, 6))
    for x in range(6):
        pk[x, x] += 1 - p
        pk[x, min(x + 1, 5)] += p
    pr = np.zeros((6, 6))
    pr[:, 0] = 1 - p
    pr[:, 1] = p
    return pk, pr


def solve(theta, rc, p, beta, tol=1e-12, maxit=20000):
    pk, pr = trans(p)
    v = np.zeros(6)
    for it in range(1, maxit + 1):
        q0 = -theta * X + beta * pk.dot(v)
        q1 = -rc + beta * pr.dot(v)
        vn = logsumexp(np.vstack((q0, q1)), axis=0)
        if np.max(np.abs(vn - v)) < tol:
            v = vn
            break
        v = vn
    q0 = -theta * X + beta * pk.dot(v)
    q1 = -rc + beta * pr.dot(v)
    prob = expit(q1 - q0)
    residual = float(np.max(np.abs(v - logsumexp(np.vstack((q0, q1)), axis=0))))
    return v, prob, residual, it


def simulate(n, seed):
    rng = np.random.default_rng(seed)
    _, prob, _, _ = solve(TRUE["theta"], TRUE["RC"], TRUE["p"], TRUE["beta"])
    states = np.empty((n, T + 1), dtype=np.int8)
    actions = np.empty((n, T), dtype=np.int8)
    # Explicit initial-state law: iid discrete uniform over {0,...,5}, independent of shocks.
    states[:, 0] = rng.integers(0, 6, n)
    for t in range(T):
        x = states[:, t]
        a = (rng.random(n) < prob[x]).astype(np.int8)
        actions[:, t] = a
        d = (rng.random(n) < TRUE["p"]).astype(np.int8)
        states[:, t + 1] = np.where(a == 1, d, np.minimum(x + d, 5))
    return states, actions


def estimate_p(states, actions):
    x = states[:, :TRAIN_T].ravel()
    xn = states[:, 1:TRAIN_T + 1].ravel()
    a = actions[:, :TRAIN_T].ravel()
    informative = (a == 1) | ((a == 0) & (x < 5))
    inc = np.where(a == 1, xn == 1, xn == x + 1)
    k = int(inc[informative].sum())
    m = int(informative.sum())
    phat = k / m
    se = np.sqrt(phat * (1 - phat) / m)
    # Transition Bernoulli score residual at MLE.
    score = k / phat - (m - k) / (1 - phat)
    return phat, se, m, float(score)


def action_counts(states, actions, train=True):
    sl = slice(0, TRAIN_T) if train else slice(TRAIN_T, T)
    x = states[:, sl].ravel()
    a = actions[:, sl].ravel()
    n = np.bincount(x, minlength=6)
    r = np.bincount(x, weights=a, minlength=6)
    return n.astype(float), r.astype(float)


def nll(par, n, r, p, beta):
    theta, rc = par
    _, pr, _, _ = solve(theta, rc, p, beta)
    pr = np.clip(pr, 1e-12, 1 - 1e-12)
    return float(-(r * np.log(pr) + (n - r) * np.log1p(-pr)).sum())


def fit_nfxp(n, r, p, beta, starts=STARTS):
    runs = []
    for st in starts:
        res = minimize(nll, st, args=(n, r, p, beta), method="L-BFGS-B", bounds=BOUNDS,
                       options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 1000})
        runs.append({"start": list(st), "x": res.x.tolist(), "fun": float(res.fun),
                     "success": bool(res.success), "status": int(res.status),
                     "message": str(res.message), "nit": int(res.nit),
                     "jac_norm": float(np.linalg.norm(res.jac, ord=np.inf))})
    best_i = int(np.argmin([z["fun"] for z in runs]))
    return np.array(runs[best_i]["x"]), runs, best_i


def fit_ccp(n, r, p, beta):
    # Jeffreys smoothing avoids infinite logits; HM inversion then yields linear WLS.
    ccp = (r + 0.5) / (n + 1.0)
    pk, pr = trans(p)
    A = np.linalg.inv(np.eye(6) - beta * pk)
    # V(theta) = A[-theta*x - log(P_keep)] = V0 + theta*Vtheta.
    v0 = A.dot(-np.log1p(-ccp))
    vt = A.dot(-X)
    y = np.log(ccp / (1 - ccp)) - beta * (pr - pk).dot(v0)
    ztheta = X + beta * (pr - pk).dot(vt)
    Z = np.column_stack((ztheta, -np.ones(6)))
    w = n * ccp * (1 - ccp)
    coef = np.linalg.lstsq(Z * np.sqrt(w[:, None]), y * np.sqrt(w), rcond=None)[0]
    resid = y - Z.dot(coef)
    return coef, ccp, float(np.sqrt(np.average(resid**2, weights=w))), resid


def prediction(par, p, beta, n, r):
    _, prob, _, _ = solve(par[0], par[1], p, beta)
    obs = r / np.maximum(n, 1)
    brier = float(((r * (1 - prob)**2 + (n - r) * prob**2).sum()) / n.sum())
    logloss = nll(par, n, r, p, beta) / n.sum()
    calib = float(np.sqrt(np.average((obs - prob)**2, weights=n)))
    return {"brier": brier, "logloss": logloss, "state_rate_rmse": calib}


def fd_gradient(fun, x, h):
    g = np.empty_like(x, dtype=float)
    for j in range(len(x)):
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        g[j] = (fun(xp) - fun(xm)) / (2 * h)
    return g


def hessian(fun, x, h=2e-4):
    k = len(x)
    H = np.empty((k, k))
    for j in range(k):
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        H[:, j] = (fd_gradient(fun, xp, h) - fd_gradient(fun, xm, h)) / (2 * h)
    return (H + H.T) / 2


def stationary(policy, p):
    pk, pr = trans(p)
    P = (1 - policy)[:, None] * pk + policy[:, None] * pr
    A = np.vstack((P.T - np.eye(6), np.ones(6)))
    b = np.r_[np.zeros(6), 1.0]
    pi = np.linalg.lstsq(A, b, rcond=None)[0]
    return pi, P


def policy_metrics(theta, rc, p, beta, subsidy):
    v, pol, bell, _ = solve(theta, rc - subsidy, p, beta)
    pi, P = stationary(pol, p)
    rate = float(pi @ pol)
    private_value = float(np.mean(v))  # ex ante over the explicit uniform initial law
    fiscal = subsidy * rate
    # Real-resource accounting: theta*x while keeping, RC while replacing; subsidy is a transfer.
    flow_resource = float(pi @ ((1 - pol) * theta * X + pol * rc))
    disc_resource_uniform = float(np.mean(np.linalg.solve(np.eye(6) - beta * P,
                                                          (1 - pol) * theta * X + pol * rc)))
    return {"replacement_rate": rate, "private_inclusive_value_uniform_initial": private_value,
            "fiscal_outlay_per_period": fiscal, "resource_cost_per_period": flow_resource,
            "discounted_resource_cost_uniform_initial": disc_resource_uniform,
            "bellman_residual": bell}


def population_profile(beta_grid):
    _, qtrue, _, _ = solve(TRUE["theta"], TRUE["RC"], TRUE["p"], TRUE["beta"])
    pi, _ = stationary(qtrue, TRUE["p"])
    out = []
    for beta in beta_grid:
        def kl_obj(par):
            _, q, _, _ = solve(par[0], par[1], TRUE["p"], beta)
            q = np.clip(q, 1e-14, 1 - 1e-14)
            return float(np.sum(pi * (qtrue * np.log(qtrue / q) +
                                      (1 - qtrue) * np.log((1 - qtrue) / (1 - q)))))
        res = minimize(kl_obj, [TRUE["theta"], TRUE["RC"]], method="L-BFGS-B", bounds=BOUNDS,
                       options={"ftol": 1e-15, "gtol": 1e-11, "maxiter": 2000})
        _, q, _, _ = solve(res.x[0], res.x[1], TRUE["p"], beta)
        out.append({"beta": float(beta), "theta": float(res.x[0]), "RC": float(res.x[1]),
                    "population_KL_per_choice": float(res.fun),
                    "max_ccp_difference": float(np.max(np.abs(q - qtrue))),
                    "success": bool(res.success)})
    return out


def main():
    summaries, starts_all, gradients = [], [], []
    saved = {}
    for n_agents in SIZES:
        for seed in SEEDS:
            states, actions = simulate(n_agents, seed)
            phat, pse, mtrans, tscore = estimate_p(states, actions)
            nt, rt = action_counts(states, actions, True)
            nh, rh = action_counts(states, actions, False)
            nfxp, runs, best_i = fit_nfxp(nt, rt, phat, TRUE["beta"])
            ccp, ccp_rates, ccp_rmse, ccp_resid = fit_ccp(nt, rt, phat, TRUE["beta"])
            _, _, bell, bit = solve(nfxp[0], nfxp[1], phat, TRUE["beta"])
            f = lambda z: nll(z, nt, rt, phat, TRUE["beta"])
            g4, g5, g6 = fd_gradient(f, nfxp, 1e-4), fd_gradient(f, nfxp, 1e-5), fd_gradient(f, nfxp, 1e-6)
            gradients.append({"n_agents": n_agents, "seed": seed, "g_h1e-4": g4.tolist(),
                              "g_h1e-5": g5.tolist(), "g_h1e-6": g6.tolist(),
                              "max_diff_1e4_1e5": float(np.max(np.abs(g4-g5))),
                              "max_diff_1e5_1e6": float(np.max(np.abs(g5-g6)))})
            summaries.append({"n_agents": n_agents, "train_choices": int(nt.sum()), "seed": seed,
                              "p_hat": phat, "p_se": pse, "transition_n": mtrans,
                              "transition_score_residual": tscore,
                              "nfxp_theta": nfxp[0], "nfxp_RC": nfxp[1],
                              "nfxp_nll": f(nfxp), "nfxp_success": runs[best_i]["success"],
                              "best_start_index": best_i, "bellman_residual": bell,
                              "bellman_iterations": bit,
                              "ccp_theta": ccp[0], "ccp_RC": ccp[1],
                              "ccp_equation_rmse": ccp_rmse,
                              **{"nfxp_" + k: v for k, v in prediction(nfxp, phat, TRUE["beta"], nh, rh).items()},
                              **{"ccp_" + k: v for k, v in prediction(ccp, phat, TRUE["beta"], nh, rh).items()}})
            starts_all.append({"n_agents": n_agents, "seed": seed, "runs": runs,
                               "empirical_ccp": ccp_rates.tolist(), "ccp_residuals": ccp_resid.tolist()})
            if n_agents == 2000 and seed == SEEDS[0]:
                saved = {"states": states, "actions": actions, "phat": phat, "pse": pse,
                         "nt": nt, "rt": rt, "nh": nh, "rh": rh, "nfxp": nfxp}

    df = pd.DataFrame(summaries)
    df.to_csv(OUT / "recovery_runs.csv", index=False, encoding="utf-8-sig")
    (OUT / "optimizer_starts.json").write_text(json.dumps(starts_all, indent=2), encoding="utf-8")
    (OUT / "gradient_checks.json").write_text(json.dumps(gradients, indent=2), encoding="utf-8")

    # Sample beta profile in the designated large sample; re-estimate theta and RC at every beta.
    beta_grid = np.round(np.linspace(0.50, 0.99, 50), 2)
    sample_profile = []
    for beta in beta_grid:
        par, runs, bi = fit_nfxp(saved["nt"], saved["rt"], saved["phat"], beta,
                                 starts=[tuple(saved["nfxp"]), (0.3, 1.5), (1.5, 6.0)])
        sample_profile.append({"beta": beta, "theta": par[0], "RC": par[1],
                               "nll": runs[bi]["fun"], "success": runs[bi]["success"],
                               "jac_norm": runs[bi]["jac_norm"]})
    sp = pd.DataFrame(sample_profile)
    sp["relative_nll"] = sp.nll - sp.nll.min()
    sp.to_csv(OUT / "sample_beta_profile.csv", index=False, encoding="utf-8-sig")

    pp = pd.DataFrame(population_profile(beta_grid))
    pp.to_csv(OUT / "population_beta_profile.csv", index=False, encoding="utf-8-sig")

    # Counterfactual at designated sample. Parametric local uncertainty conditional on beta and p-hat.
    par = saved["nfxp"]
    f = lambda z: nll(z, saved["nt"], saved["rt"], saved["phat"], TRUE["beta"])
    H = hessian(f, par)
    cov = np.linalg.inv(H)
    rng = np.random.default_rng(98761)
    draws = rng.multivariate_normal(par, cov, size=500)
    draws = draws[(draws[:, 0] > BOUNDS[0][0]) & (draws[:, 0] < BOUNDS[0][1]) &
                  (draws[:, 1] > BOUNDS[1][0]) & (draws[:, 1] < BOUNDS[1][1])]
    cf0 = policy_metrics(par[0], par[1], saved["phat"], TRUE["beta"], 0.0)
    cf1 = policy_metrics(par[0], par[1], saved["phat"], TRUE["beta"], 1.0)
    effects = []
    for d in draws:
        a = policy_metrics(d[0], d[1], saved["phat"], TRUE["beta"], 0.0)
        b = policy_metrics(d[0], d[1], saved["phat"], TRUE["beta"], 1.0)
        effects.append([b["replacement_rate"] - a["replacement_rate"],
                        b["private_inclusive_value_uniform_initial"] - a["private_inclusive_value_uniform_initial"],
                        b["resource_cost_per_period"] - a["resource_cost_per_period"]])
    effects = np.asarray(effects)
    uncertainty = {"accepted_draws": len(effects), "hessian_eigenvalues": np.linalg.eigvalsh(H).tolist(),
                   "effect_quantiles_5_50_95": {k: np.quantile(effects[:, j], [.05, .5, .95]).tolist()
                    for j, k in enumerate(["replacement_rate", "private_value", "resource_cost_per_period"])}}

    sensitivity = []
    for beta in [0.70, 0.90, 0.98]:
        row = sp.iloc[(sp.beta - beta).abs().argmin()]
        for pval in [max(.05, saved["phat"] - 2*saved["pse"]), saved["phat"], min(.95, saved["phat"] + 2*saved["pse"])]:
            base = policy_metrics(row.theta, row.RC, pval, beta, 0.0)
            sub = policy_metrics(row.theta, row.RC, pval, beta, 1.0)
            sensitivity.append({"beta": beta, "p": pval, "theta": row.theta, "RC": row.RC,
                                "rate_effect": sub["replacement_rate"] - base["replacement_rate"],
                                "private_value_effect": sub["private_inclusive_value_uniform_initial"] - base["private_inclusive_value_uniform_initial"],
                                "resource_cost_effect": sub["resource_cost_per_period"] - base["resource_cost_per_period"]})
    pd.DataFrame(sensitivity).to_csv(OUT / "counterfactual_sensitivity.csv", index=False, encoding="utf-8-sig")
    counter = {"designated_sample": {"n_agents": 2000, "seed": SEEDS[0]},
               "estimate": {"theta": par[0], "RC": par[1], "p": saved["phat"], "beta": TRUE["beta"]},
               "no_subsidy": cf0, "subsidy_1": cf1,
               "effects": {k: cf1[k] - cf0[k] for k in cf0 if k != "bellman_residual"},
               "conditional_parameter_uncertainty": uncertainty}
    (OUT / "counterfactual.json").write_text(json.dumps(counter, indent=2), encoding="utf-8")

    aggregate = df.groupby("n_agents").agg(
        runs=("seed", "count"), p_mean=("p_hat", "mean"), p_rmse=("p_hat", lambda z: np.sqrt(np.mean((z-TRUE["p"])**2))),
        nfxp_theta_mean=("nfxp_theta", "mean"), nfxp_theta_rmse=("nfxp_theta", lambda z: np.sqrt(np.mean((z-TRUE["theta"])**2))),
        nfxp_RC_mean=("nfxp_RC", "mean"), nfxp_RC_rmse=("nfxp_RC", lambda z: np.sqrt(np.mean((z-TRUE["RC"])**2))),
        ccp_theta_mean=("ccp_theta", "mean"), ccp_theta_rmse=("ccp_theta", lambda z: np.sqrt(np.mean((z-TRUE["theta"])**2))),
        ccp_RC_mean=("ccp_RC", "mean"), ccp_RC_rmse=("ccp_RC", lambda z: np.sqrt(np.mean((z-TRUE["RC"])**2))),
        nfxp_logloss=("nfxp_logloss", "mean"), ccp_logloss=("ccp_logloss", "mean"),
        nfxp_brier=("nfxp_brier", "mean"), ccp_brier=("ccp_brier", "mean"),
        failures=("nfxp_success", lambda z: int((~z).sum()))).reset_index()
    aggregate.to_csv(OUT / "recovery_summary.csv", index=False, encoding="utf-8-sig")
    metadata = {"true_parameters": TRUE, "T": T, "train_T": TRAIN_T,
                "initial_state_law": "iid discrete uniform on states 0,...,5",
                "timing": "observe x_t; draw EV1 shocks and choose; draw Bernoulli deterioration; realize x_{t+1}",
                "seeds": SEEDS, "sample_sizes_agents": SIZES,
                "versions": {"python": sys.version, "numpy": np.__version__, "pandas": pd.__version__,
                             "scipy": scipy.__version__, "platform": platform.platform()}}
    (OUT / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(aggregate.to_string(index=False))
    print("\nSample beta minimum and near-profile:\n", sp.nsmallest(8, "relative_nll").to_string(index=False))
    print("\nPopulation beta minimum and observationally close:\n", pp.nsmallest(8, "population_KL_per_choice").to_string(index=False))
    print("\nCounterfactual:\n", json.dumps(counter, indent=2))


if __name__ == "__main__":
    main()
