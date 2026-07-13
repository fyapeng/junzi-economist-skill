from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import least_squares


OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

SEEDS = [48101, 48102, 48103, 48104, 48105]
N_MARKETS = 120
J = 2
EXPECTED_ROWS = N_MARKETS * J
ALPHA = 1.20
BETA0 = 2.00
BETAX = 0.40
SUBSIDY = 0.20
OWNERSHIP = np.ones((J, J))
RAW_TOL = 1e-10
SCALED_TOL = 1e-9
ROOT_CLUSTER_TOL = 1e-6
START_MARKUPS = np.array([[0.15, 0.15], [0.5, 0.5], [1.0, 1.0],
                          [2.0, 2.0], [4.0, 4.0], [0.25, 3.0],
                          [3.0, 0.25], [6.0, 6.0]])


def shares(p: np.ndarray, x: np.ndarray, xi: np.ndarray) -> np.ndarray:
    util = BETA0 + BETAX * x + xi - ALPHA * p
    eu = np.exp(util)
    return eu / (1.0 + eu.sum())


def foc(p: np.ndarray, private_mc: np.ndarray, x: np.ndarray,
        xi: np.ndarray) -> np.ndarray:
    s = shares(p, x, xi)
    deriv = -ALPHA * (np.diag(s) - np.outer(s, s))  # ds_k / dp_j
    return s + (OWNERSHIP * deriv.T) @ (p - private_mc)


def scaled_foc(p: np.ndarray, private_mc: np.ndarray, x: np.ndarray,
               xi: np.ndarray) -> np.ndarray:
    s = shares(p, x, xi)
    return foc(p, private_mc, x, xi) / s


def numerical_jac(fun, p: np.ndarray, h: float = 1e-5) -> np.ndarray:
    ans = np.empty((J, J))
    for k in range(J):
        step = np.zeros(J)
        step[k] = h
        ans[:, k] = (fun(p + step) - fun(p - step)) / (2 * h)
    return ans


def solve_market(seed: int, market: int, scenario: str, x: np.ndarray,
                 xi: np.ndarray, real_mc: np.ndarray):
    subsidy = SUBSIDY if scenario == "subsidy" else 0.0
    private_mc = real_mc - subsidy
    lower = private_mc + 1e-8
    upper = private_mc + 10.0
    trace = []
    accepted = []
    for start_id, markup0 in enumerate(START_MARKUPS):
        p0 = np.clip(private_mc + markup0, lower + 1e-7, upper - 1e-7)
        sol = least_squares(lambda q: scaled_foc(q, private_mc, x, xi), p0,
                            bounds=(lower, upper), xtol=1e-13, ftol=1e-13,
                            gtol=1e-13, max_nfev=2500, x_scale="jac")
        raw = foc(sol.x, private_mc, x, xi)
        scaled = scaled_foc(sol.x, private_mc, x, xi)
        raw_max = float(np.max(np.abs(raw)))
        scaled_max = float(np.max(np.abs(scaled)))
        inside = bool(np.all(sol.x > lower) and np.all(sol.x < upper))
        accept = bool(sol.success and inside and raw_max <= RAW_TOL and
                      scaled_max <= SCALED_TOL)
        jac = numerical_jac(lambda q: scaled_foc(q, private_mc, x, xi), sol.x)
        rec = {"seed": seed, "market": market, "scenario": scenario,
               "start_id": start_id, "start_p1": p0[0], "start_p2": p0[1],
               "terminal_p1": sol.x[0], "terminal_p2": sol.x[1],
               "objective": float(np.dot(scaled, scaled)),
               "raw_foc_max": raw_max, "scaled_foc_max": scaled_max,
               "solver_success": bool(sol.success), "accepted": accept,
               "nfev": int(sol.nfev), "status": int(sol.status),
               "message": str(sol.message), "lower_p1": lower[0],
               "lower_p2": lower[1], "upper_p1": upper[0],
               "upper_p2": upper[1], "jacobian_condition": float(np.linalg.cond(jac))}
        trace.append(rec)
        if accept:
            accepted.append(sol.x.copy())

    roots = []
    for p in accepted:
        if not any(np.max(np.abs(p - q)) <= ROOT_CLUSTER_TOL for q in roots):
            roots.append(p)
    if not roots:
        return trace, [], None
    roots.sort(key=lambda q: tuple(q))
    return trace, roots, roots[0]


def simulate(seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    # Every support is closed and bounded; no redraw, clipping, or post-draw drop.
    market = np.repeat(np.arange(N_MARKETS), J)
    product = np.tile(np.arange(J), N_MARKETS)
    x = rng.uniform(-1.0, 1.0, EXPECTED_ROWS)
    w = rng.uniform(-1.0, 1.0, EXPECTED_ROWS)
    u = rng.uniform(-1.0, 1.0, EXPECTED_ROWS)
    v = rng.uniform(-1.0, 1.0, EXPECTED_ROWS)
    e = rng.uniform(-1.0, 1.0, EXPECTED_ROWS)
    xi = 0.30 * u + 0.10 * v                    # [-0.40, 0.40]
    omega = 0.12 * u + 0.05 * v                 # [-0.17, 0.17]
    real_mc = 1.60 + 0.15 * x + 0.25 * w + omega
    # z_bad is observed only after xi is realized and pricing occurs. Its direct
    # 0.8*xi component violates E[z_bad*xi]=0; it is never a valid instrument.
    z_bad = w + 0.80 * xi + 0.05 * e
    df = pd.DataFrame({"seed": seed, "market": market, "product": product,
                       "x": x, "w": w, "u": u, "v": v, "xi": xi,
                       "omega": omega, "real_mc": real_mc, "z_bad": z_bad})
    if len(df) != EXPECTED_ROWS or df.market.nunique() != N_MARKETS:
        raise RuntimeError("simulation_count_failure")
    if df.real_mc.min() < 1.03 - 1e-12:
        raise RuntimeError("primitive_support_failure")
    return df


def estimate_linear(df: pd.DataFrame, seed: int):
    y = np.log(df.share.to_numpy() / df.outside_share.to_numpy())
    X = np.column_stack([np.ones(len(df)), df.x, df.price])
    names = ["constant", "x", "price"]
    ols = np.linalg.lstsq(X, y, rcond=None)[0]

    Z = np.column_stack([np.ones(len(df)), df.x, df.w, df.w ** 2])
    ZZ = Z.T @ Z
    PZX = Z @ np.linalg.solve(ZZ, Z.T @ X)
    iv = np.linalg.solve(X.T @ PZX, X.T @ Z @ np.linalg.solve(ZZ, Z.T @ y))
    u1 = y - X @ iv
    S = (Z * u1[:, None]).T @ (Z * u1[:, None]) / len(df)
    W = np.linalg.pinv(S, rcond=1e-12)
    gmm = np.linalg.solve(X.T @ Z @ W @ Z.T @ X,
                          X.T @ Z @ W @ Z.T @ y)

    Zb = np.column_stack([np.ones(len(df)), df.x, df.z_bad, df.z_bad ** 2])
    Wb = np.linalg.pinv(Zb.T @ Zb)
    bad = np.linalg.solve(X.T @ Zb @ Wb @ Zb.T @ X,
                          X.T @ Zb @ Wb @ Zb.T @ y)
    out = []
    for method, b, z in [("OLS", ols, X), ("IV_2SLS", iv, Z),
                         ("GMM_2step", gmm, Z), ("INVALID_PROXY_IV", bad, Zb)]:
        resid = y - X @ b
        moments = z.T @ resid / len(df)
        cond = np.linalg.cond((z.T @ X) / len(df))
        for n, val, truth in zip(names, b, [BETA0, BETAX, -ALPHA]):
            out.append({"seed": seed, "method": method, "parameter": n,
                        "estimate": float(val), "truth": truth,
                        "error": float(val - truth),
                        "moment_max_abs": float(np.max(np.abs(moments))),
                        "design_condition": float(cond)})
    alpha_hat = -float(gmm[2])
    recovery = []
    for m, g in df.groupby("market", sort=True):
        s = g.share.to_numpy()
        deriv_hat = -alpha_hat * (np.diag(s) - np.outer(s, s))
        markup_hat = np.linalg.solve(-(OWNERSHIP * deriv_hat.T), s)
        mc_hat = g.price.to_numpy() - markup_hat
        true_markup = g.price.to_numpy() - g.real_mc.to_numpy()
        for k, (_, row) in enumerate(g.iterrows()):
            recovery.append({"seed": seed, "market": int(m),
                             "product": int(row["product"]),
                             "alpha_hat_GMM": alpha_hat,
                             "price": row["price"],
                             "true_markup": true_markup[k],
                             "recovered_markup": markup_hat[k],
                             "markup_error": markup_hat[k] - true_markup[k],
                             "true_mc": row["real_mc"],
                             "recovered_mc": mc_hat[k],
                             "mc_error": mc_hat[k] - row["real_mc"]})
    corr_w_xi = float(np.corrcoef(df.w, df.xi)[0, 1])
    corr_bad_xi = float(np.corrcoef(df.z_bad, df.xi)[0, 1])
    first_stage = np.linalg.lstsq(Z, df.price.to_numpy(), rcond=None)[0]
    diagnostics = {"seed": seed, "corr_valid_w_xi": corr_w_xi,
                   "corr_invalid_proxy_xi": corr_bad_xi,
                   "first_stage_w_coefficient": float(first_stage[2]),
                   "first_stage_w2_coefficient": float(first_stage[3]),
                   "valid_ZX_condition": float(np.linalg.cond((Z.T @ X) / len(df))),
                   "observed_min_real_mc": float(df.real_mc.min()),
                   "observed_max_real_mc": float(df.real_mc.max()),
                   "observed_min_share": float(df.share.min()),
                   "observed_max_share": float(df.share.max()),
                   "observed_min_outside_share": float(df.outside_share.min()),
                   "observed_max_outside_share": float(df.outside_share.max())}
    return out, recovery, diagnostics


def main():
    failure_counts = {"simulation": 0, "equilibrium": 0, "estimation": 0}
    all_data, all_traces, all_roots, all_est, all_welfare = [], [], [], [], []
    all_recovery, all_diagnostics = [], []
    replication_status = []
    for seed in SEEDS:
        try:
            primitive = simulate(seed)
        except Exception as exc:
            failure_counts["simulation"] += 1
            replication_status.append({"seed": seed, "status": "simulation_failure", "detail": repr(exc)})
            continue

        scenario_frames = {}
        equilibrium_failed = False
        for scenario in ["baseline", "subsidy"]:
            records = []
            for m, g in primitive.groupby("market", sort=True):
                x, xi, mc = g.x.to_numpy(), g.xi.to_numpy(), g.real_mc.to_numpy()
                trace, roots, selected = solve_market(seed, int(m), scenario, x, xi, mc)
                all_traces.extend(trace)
                for rid, root in enumerate(roots):
                    all_roots.append({"seed": seed, "market": int(m), "scenario": scenario,
                                      "root_id": rid, "p1": root[0], "p2": root[1]})
                if selected is None:
                    equilibrium_failed = True
                    continue
                s = shares(selected, x, xi)
                s0 = 1.0 - s.sum()
                subsidy = SUBSIDY if scenario == "subsidy" else 0.0
                for k, (_, row) in enumerate(g.iterrows()):
                    records.append({**row.to_dict(), "scenario": scenario,
                                    "price": selected[k], "share": s[k],
                                    "outside_share": s0, "subsidy_rate": subsidy})
            sf = pd.DataFrame(records)
            # Whole-replication acceptance: no estimator or welfare output if either
            # scenario has a missing equilibrium or unexpected row/market count.
            if equilibrium_failed or len(sf) != EXPECTED_ROWS or sf.market.nunique() != N_MARKETS:
                equilibrium_failed = True
            scenario_frames[scenario] = sf

        if equilibrium_failed:
            failure_counts["equilibrium"] += 1
            replication_status.append({"seed": seed, "status": "equilibrium_failure",
                                       "detail": "at least one scenario failed exact acceptance"})
            continue

        base = scenario_frames["baseline"]
        try:
            estimates, recovery, diagnostics = estimate_linear(base, seed)
            all_est.extend(estimates)
            all_recovery.extend(recovery)
            all_diagnostics.append(diagnostics)
        except Exception as exc:
            failure_counts["estimation"] += 1
            replication_status.append({"seed": seed, "status": "estimation_failure", "detail": repr(exc)})
            continue

        for scenario, sf in scenario_frames.items():
            all_data.append(sf)
            for m, g in sf.groupby("market", sort=True):
                payment = float((g.price * g.share).sum())
                subsidy_payment = float((g.subsidy_rate * g.share).sum())
                real_resource = float((g.real_mc * g.share).sum())
                producer_profit = float(((g.price - g.real_mc + g.subsidy_rate) * g.share).sum())
                cs = float(np.log(1.0 + np.exp(BETA0 + BETAX * g.x.to_numpy() +
                                               g.xi.to_numpy() - ALPHA * g.price.to_numpy()).sum()) / ALPHA)
                welfare = cs + producer_profit - subsidy_payment
                all_welfare.append({"seed": seed, "market": int(m), "scenario": scenario,
                                    "consumer_payment": payment, "producer_revenue": payment,
                                    "producer_profit": producer_profit, "tax_payment": 0.0,
                                    "subsidy_payment": subsidy_payment,
                                    "real_resource_cost": real_resource,
                                    "consumer_surplus": cs,
                                    "welfare_CS_plus_profit_minus_net_fiscal": welfare})
        replication_status.append({"seed": seed, "status": "complete", "detail": "exact counts accepted"})

    pd.DataFrame(all_traces).to_csv(OUT / "all_start_traces.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(all_roots).to_csv(OUT / "detected_roots.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(all_est).to_csv(OUT / "estimates.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(all_recovery).to_csv(OUT / "markup_cost_recovery.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(all_diagnostics).to_csv(OUT / "sample_diagnostics.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(all_welfare).to_csv(OUT / "welfare_market.csv", index=False, encoding="utf-8-sig")
    if all_data:
        pd.concat(all_data, ignore_index=True).to_parquet(OUT / "equilibrium_data.parquet", index=False)
    summary = {"predeclared": {"seeds": SEEDS, "markets_per_seed": N_MARKETS,
                                "products_per_market": J, "rows_per_seed": EXPECTED_ROWS,
                                "scenarios": ["baseline", "subsidy"],
                                "starts_per_market_scenario": len(START_MARKUPS),
                                "raw_foc_tolerance": RAW_TOL,
                                "scaled_foc_tolerance": SCALED_TOL},
               "primitive_support": {"x": [-1, 1], "w": [-1, 1], "u": [-1, 1],
                                     "v": [-1, 1], "e": [-1, 1], "xi": [-0.4, 0.4],
                                     "omega": [-0.17, 0.17], "real_mc": [1.03, 2.17],
                                     "private_mc_subsidy": [0.83, 1.97]},
               "failure_counts": failure_counts, "replication_status": replication_status,
               "versions": {"python": sys.version, "numpy": np.__version__,
                            "pandas": pd.__version__, "scipy": scipy.__version__,
                            "platform": platform.platform()}}
    (OUT / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
