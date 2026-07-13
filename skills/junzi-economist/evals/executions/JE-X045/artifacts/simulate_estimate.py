"""Simulated simple-logit differentiated-products IO exercise.

Creates data, estimates OLS/IV variants, recovers costs, solves tax and merger
counterfactuals, and runs a repeated-sample recovery study. All random-number
streams, failures, starts, and numerical diagnostics are written to disk.
"""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from numpy.linalg import cond, inv, lstsq, matrix_rank
from scipy.optimize import least_squares
from scipy.stats import f as f_dist

OUT = Path(__file__).resolve().parent
T, J, MARKET_SIZE = 180, 3, 1.0
TRUE = {"beta_x": 1.25, "alpha": 1.10, "gamma0": 2.25,
        "gamma_z": 0.65, "gamma_w": 0.28, "rho_xi_omega": 0.65}
BASE_OWN = np.array([[1, 1, 0], [1, 1, 0], [0, 0, 1]], dtype=float)
MERGER_OWN = np.ones((J, J))
SOLVER_TOL = 1e-10


def shares(delta):
    e = np.exp(np.clip(delta, -700, 700))
    den = 1.0 + e.sum()
    return e / den, 1.0 / den


def dsdp(s, alpha):
    return -alpha * (np.diag(s) - np.outer(s, s))


def foc(p, c, x, xi, alpha, beta, ownership, tax=0.0):
    s, _ = shares(beta * x - alpha * p + xi)
    d = dsdp(s, alpha)
    # Price k FOC: s_k + sum_j O[k,j]*(p_j-c_j-tax)*ds_j/dp_k = 0.
    return s + (ownership * d.T) @ (p - c - tax)


def scaled_foc(p, c, x, xi, alpha, beta, ownership, tax=0.0):
    """FOC normalized by own share, preventing vanishing-share false roots."""
    s, _ = shares(beta * x - alpha * p + xi)
    return foc(p, c, x, xi, alpha, beta, ownership, tax) / np.maximum(s, 1e-14)


def solve_market(c, x, xi, alpha, beta, ownership, tax=0.0,
                 starts=None, max_nfev=1500):
    if starts is None:
        starts = [c + tax + v for v in (0.15, 0.6, 1.2, 2.5)]
    attempts, roots = [], []
    for st in starts:
        sol = least_squares(lambda p: scaled_foc(p, c, x, xi, alpha, beta,
                                                 ownership, tax),
                            np.asarray(st), bounds=(-5.0, 25.0),
                            xtol=SOLVER_TOL, ftol=SOLVER_TOL,
                            gtol=SOLVER_TOL, max_nfev=max_nfev)
        scaled_res = float(np.max(np.abs(sol.fun)))
        raw_res = float(np.max(np.abs(foc(sol.x, c, x, xi, alpha, beta,
                                         ownership, tax))))
        economic = bool(np.all(sol.x >= c + tax - 1e-8))
        away_from_bound = bool(np.all(sol.x < 25.0-1e-7) and np.all(sol.x > -5.0+1e-7))
        ok = bool(sol.success and scaled_res < 1e-8 and raw_res < 1e-8 and
                  economic and away_from_bound)
        rec = {"start": np.asarray(st).tolist(), "price": sol.x.tolist(),
               "success_flag": bool(sol.success), "accepted": ok,
               "economic": economic, "away_from_bound": away_from_bound,
               "max_abs_foc": raw_res, "max_abs_scaled_foc": scaled_res,
               "nfev": int(sol.nfev), "message": sol.message}
        attempts.append(rec)
        if ok and not any(np.max(np.abs(sol.x-r)) < 1e-7 for r in roots):
            roots.append(sol.x.copy())
    return roots, attempts


def simulate(seed, n_markets=T, gamma_z=None):
    rng = np.random.default_rng(seed)
    gz = TRUE["gamma_z"] if gamma_z is None else gamma_z
    rows, solver_failures = [], []
    for t in range(n_markets):
        x = rng.normal(0.8, 0.65, J)
        z = rng.uniform(-1.0, 1.0, J)
        w = rng.normal(0.3, 0.55, J)
        u, eo = rng.normal(size=(2, J))
        xi = 0.55 * u
        omega = 0.18 * (TRUE["rho_xi_omega"] * u +
                        np.sqrt(1-TRUE["rho_xi_omega"]**2) * eo)
        c = TRUE["gamma0"] + gz*z + TRUE["gamma_w"]*w + omega
        if np.any(c <= 0.05):
            solver_failures.append({"market": t, "reason": "nonpositive DGP cost",
                                    "costs": c.tolist()})
            continue
        roots, att = solve_market(c, x, xi, TRUE["alpha"], TRUE["beta_x"], BASE_OWN)
        if not roots:
            solver_failures.append({"market": t, "attempts": att})
            continue
        p = roots[0]
        s, s0 = shares(TRUE["beta_x"]*x - TRUE["alpha"]*p + xi)
        qbad = xi + rng.normal(0, 0.10, J)  # deliberately invalid: correlated with xi.
        for j in range(J):
            rows.append({"market": t, "product": j+1, "firm": 1 if j < 2 else 2,
                         "x": x[j], "z": z[j], "w": w[j], "xi": xi[j],
                         "omega": omega[j], "mc_true": c[j], "price": p[j],
                         "share": s[j], "outside_share": s0,
                         "y": np.log(s[j])-np.log(s0), "qbad": qbad[j]})
    return pd.DataFrame(rows), solver_failures


def ols(y, X):
    b = lstsq(X, y, rcond=None)[0]
    e = y-X@b
    vc = inv(X.T@X) @ (X.T@(X*(e[:, None]**2))) @ inv(X.T@X)
    return b, e, vc


def iv_2sls(y, X, Z):
    zz = inv(Z.T@Z)
    xpzx = X.T@Z@zz@Z.T@X
    b = np.linalg.solve(xpzx, X.T@Z@zz@Z.T@y)
    e = y-X@b
    meat = X.T@Z@zz@(Z.T@(Z*(e[:, None]**2)))@zz@Z.T@X
    vc = inv(xpzx)@meat@inv(xpzx)
    g = Z.T@e/len(y)
    G = -(Z.T@X)/len(y)
    return b, e, vc, g, G, xpzx


def partial_first_stage(price, included, excluded):
    Xu = np.column_stack([included, excluded])
    _, eu, _ = ols(price, Xu)
    _, er, _ = ols(price, included)
    q = excluded.shape[1]; n = len(price); k = Xu.shape[1]
    sseu, sser = eu@eu, er@er
    F = ((sser-sseu)/q)/(sseu/(n-k))
    pval = float(f_dist.sf(F, q, n-k))
    return {"partial_F_homoskedastic": float(F), "df_num": q,
            "df_den": n-k, "p_value": pval}


def estimate(df, instrument_mode="valid"):
    y = df.y.to_numpy(); n = len(df)
    X = np.column_stack([np.ones(n), df.x, -df.price])
    bols, eols, v_ols = ols(y, X)
    included = np.column_stack([np.ones(n), df.x])
    if instrument_mode == "valid":
        excluded = np.column_stack([df.z, df.w])
    elif instrument_mode == "weak":
        excluded = np.column_stack([df.z])
    elif instrument_mode == "invalid":
        excluded = np.column_stack([df.z, df.qbad])
    else: raise ValueError(instrument_mode)
    Z = np.column_stack([included, excluded])
    biv, eiv, viv, g, G, xpzx = iv_2sls(y, X, Z)
    fs = partial_first_stage(df.price.to_numpy(), included, excluded)
    return {"mode": instrument_mode,
            "ols": {"coef_intercept_beta_alpha": bols.tolist(),
                    "se": np.sqrt(np.diag(v_ols)).tolist()},
            "iv": {"coef_intercept_beta_alpha": biv.tolist(),
                   "se": np.sqrt(np.diag(viv)).tolist()},
            "first_stage": fs,
            "moments": g.tolist(), "max_abs_moment": float(np.max(np.abs(g))),
            "jacobian_rank": int(matrix_rank(G)),
            "jacobian_condition": float(cond(G)),
            "normal_matrix_condition": float(cond(xpzx))}, biv


def recover_costs(df, b):
    alpha = float(b[2])
    out, failures = [], []
    if alpha <= 0:
        return None, [{"branch": "cost_recovery", "reason": "nonpositive alpha",
                       "alpha": alpha}]
    for t, g in df.groupby("market", sort=True):
        s = g.share.to_numpy(); p = g.price.to_numpy()
        H = -(BASE_OWN * dsdp(s, alpha).T)
        try:
            markup = np.linalg.solve(H, s)
            mc = p-markup
        except np.linalg.LinAlgError:
            failures.append({"market": int(t), "reason": "singular markup matrix"})
            continue
        for idx, m, c in zip(g.index, markup, mc):
            out.append((idx, m, c, cond(H)))
    if not out: return None, failures
    rec = pd.DataFrame(out, columns=["index","markup_hat","mc_hat","markup_matrix_cond"]).set_index("index")
    d = df.join(rec)
    invalid = d.loc[d.mc_hat <= 0, ["market","product","mc_hat"]]
    if len(invalid):
        failures.append({"branch":"nonpositive_recovered_mc", "count":len(invalid),
                         "rows":invalid.to_dict("records")})
    W = np.column_stack([np.ones(len(d)), d.z, d.w])
    bc, ec, vc = ols(d.mc_hat.to_numpy(), W)
    return {"cost_coef_intercept_z_w":bc.tolist(),
            "cost_se":np.sqrt(np.diag(vc)).tolist(),
            "mean_markup":float(d.markup_hat.mean()),
            "min_mc":float(d.mc_hat.min()), "negative_mc_count":int((d.mc_hat<=0).sum()),
            "mean_abs_mc_error":float(np.mean(np.abs(d.mc_hat-d.mc_true))),
            "max_markup_matrix_condition":float(d.markup_matrix_cond.max())}, failures


def derivative_check(df):
    g = df[df.market==df.market.min()].sort_values("product")
    p=g.price.to_numpy(); x=g.x.to_numpy(); xi=g.xi.to_numpy(); h=1e-6
    s,_=shares(TRUE["beta_x"]*x-TRUE["alpha"]*p+xi)
    ana=dsdp(s, TRUE["alpha"]); num=np.zeros((J,J))
    for k in range(J):
        pp=p.copy(); pm=p.copy(); pp[k]+=h; pm[k]-=h
        sp,_=shares(TRUE["beta_x"]*x-TRUE["alpha"]*pp+xi)
        sm,_=shares(TRUE["beta_x"]*x-TRUE["alpha"]*pm+xi)
        num[:,k]=(sp-sm)/(2*h)
    return {"max_abs_dsdp_error":float(np.max(np.abs(ana-num))),
            "step":h}


def counterfactual(df, ownership, tax, label):
    markets, all_attempts, failures, root_counts = [], [], [], []
    for t,g in df.groupby("market",sort=True):
        g=g.sort_values("product"); c=g.mc_true.to_numpy(); x=g.x.to_numpy(); xi=g.xi.to_numpy()
        base=g.price.to_numpy()
        starts=[base, c+tax+0.2, c+tax+1.0, c+tax+3.0,
                np.array([0.5,2.0,4.0])+c+tax]
        roots, att=solve_market(c,x,xi,TRUE["alpha"],TRUE["beta_x"],ownership,tax,starts)
        all_attempts.append({"market":int(t),"attempts":att})
        root_counts.append(len(roots))
        if not roots:
            failures.append({"market":int(t),"reason":"no accepted equilibrium","attempts":att})
            continue
        p=roots[0]; s,s0=shares(TRUE["beta_x"]*x-TRUE["alpha"]*p+xi)
        delta=TRUE["beta_x"]*x-TRUE["alpha"]*p+xi
        cs=MARKET_SIZE/TRUE["alpha"]*np.log1p(np.exp(delta).sum())
        producer_profit=MARKET_SIZE*np.sum((p-c-tax)*s)
        revenue=MARKET_SIZE*tax*np.sum(s)
        real_cost=MARKET_SIZE*np.sum(c*s)
        markets.append({"market":int(t),"prices":p.tolist(),"shares":s.tolist(),
                        "outside_share":float(s0),"consumer_surplus":float(cs),
                        "producer_profit_net_of_tax":float(producer_profit),
                        "tax_revenue":float(revenue),"real_cost":float(real_cost),
                        "max_abs_foc":float(np.max(np.abs(foc(p,c,x,xi,TRUE["alpha"],TRUE["beta_x"],ownership,tax)))),
                        "max_abs_scaled_foc":float(np.max(np.abs(scaled_foc(p,c,x,xi,TRUE["alpha"],TRUE["beta_x"],ownership,tax)))),
                        "detected_equilibria":len(roots)})
    agg={k:float(sum(m[k] for m in markets)) for k in
         ["consumer_surplus","producer_profit_net_of_tax","tax_revenue","real_cost"]}
    agg.update({"mean_price":float(np.mean([q for m in markets for q in m["prices"]])),
                "mean_inside_share":float(np.mean([q for m in markets for q in m["shares"]])),
                "max_abs_foc":float(max([m["max_abs_foc"] for m in markets],default=np.nan)),
                "max_abs_scaled_foc":float(max([m["max_abs_scaled_foc"] for m in markets],default=np.nan)),
                "markets_solved":len(markets),"markets_failed":len(failures),
                "max_detected_equilibria":max(root_counts,default=0),
                "markets_multiple_detected":int(sum(r>1 for r in root_counts))})
    return {"label":label,"aggregate":agg,"markets":markets,
            "failures":failures,"all_start_attempts":all_attempts}


def monte_carlo(seeds):
    recs=[]
    for seed in seeds:
        df, sf=simulate(seed)
        row={"seed":seed,"simulation_solver_failures":len(sf),"n":len(df)}
        for mode in ["valid","invalid"]:
            try:
                est,b=estimate(df,mode)
                row[f"{mode}_beta"]=b[1]; row[f"{mode}_alpha"]=b[2]
                row[f"{mode}_F"]=est["first_stage"]["partial_F_homoskedastic"]
                row[f"{mode}_failed"]=False
            except Exception as e:
                row[f"{mode}_failed"]=True; row[f"{mode}_error"]=repr(e)
        recs.append(row)
    r=pd.DataFrame(recs)
    summary={"draws":len(r),"raw":recs}
    for mode in ["valid","invalid"]:
        ok=r[~r[f"{mode}_failed"]]
        summary[mode]={"successful":len(ok),"failures":int(r[f"{mode}_failed"].sum()),
                       "beta_mean":float(ok[f"{mode}_beta"].mean()),
                       "beta_bias":float(ok[f"{mode}_beta"].mean()-TRUE["beta_x"]),
                       "alpha_mean":float(ok[f"{mode}_alpha"].mean()),
                       "alpha_bias":float(ok[f"{mode}_alpha"].mean()-TRUE["alpha"]),
                       "alpha_rmse":float(np.sqrt(np.mean((ok[f"{mode}_alpha"]-TRUE["alpha"])**2))),
                       "F_median":float(ok[f"{mode}_F"].median())}
    return summary


def main():
    df, sim_fail=simulate(45045)
    valid,bv=estimate(df,"valid")
    # A separate DGP makes z genuinely weak, rather than relabeling a strong design.
    dfweak, weak_sim_fail=simulate(45046,gamma_z=0.015)
    weak,bw=estimate(dfweak,"weak")
    invalid,bi=estimate(df,"invalid")
    cost_valid,cost_fail_valid=recover_costs(df,bv)
    cost_invalid,cost_fail_invalid=recover_costs(df,bi)
    basecf=counterfactual(df,BASE_OWN,0.0,"baseline_re-solve")
    taxcf=counterfactual(df,BASE_OWN,0.35,"per-unit tax 0.35")
    mergecf=counterfactual(df,MERGER_OWN,0.0,"full merger")
    mc=monte_carlo(list(range(45100,45130)))
    raw={"design":{"markets_requested":T,"products":J,"market_size":MARKET_SIZE,
                   "true_parameters":TRUE,"base_ownership":BASE_OWN.tolist(),
                   "merger_ownership":MERGER_OWN.tolist(),"solver_tolerance":SOLVER_TOL,
                   "main_seed":45045,"weak_seed":45046,"monte_carlo_seeds":[45100,45129]},
         "sample":{"rows":len(df),"markets":int(df.market.nunique()),
                   "price_min":float(df.price.min()),"share_min":float(df.share.min()),
                   "share_max":float(df.share.max()),
                   "outside_share_min":float(df.outside_share.min()),
                   "outside_share_max":float(df.outside_share.max()),
                   "true_corr_price_xi":float(df[["price","xi"]].corr().iloc[0,1]),
                   "true_corr_xi_omega":float(df[["xi","omega"]].corr().iloc[0,1]),
                   "simulation_failures":sim_fail},
         "valid":valid,"weak":weak,"invalid":invalid,
         "weak_sample":{"rows":len(dfweak),"simulation_failures":weak_sim_fail},
         "cost_recovery_valid":cost_valid,"cost_failures_valid":cost_fail_valid,
         "cost_recovery_invalid":cost_invalid,"cost_failures_invalid":cost_fail_invalid,
         "derivative_check":derivative_check(df),
         "counterfactuals":{"baseline":basecf,"tax":taxcf,"merger":mergecf},
         "monte_carlo":mc,
         "software":{"python":sys.version,"platform":platform.platform(),
                     "numpy":np.__version__,"pandas":pd.__version__,"scipy":scipy.__version__}}
    df.to_csv(OUT/"simulated_data.csv",index=False,encoding="utf-8-sig")
    with open(OUT/"raw_results.json","w",encoding="utf-8") as f:
        json.dump(raw,f,ensure_ascii=False,indent=2)
    # Compact output is preserved separately from the complete JSON traces.
    compact={"sample":raw["sample"],"valid":valid,"weak":weak,"invalid":invalid,
             "cost_recovery_valid":cost_valid,"cost_failures_valid":cost_fail_valid,
             "derivative_check":raw["derivative_check"],
             "counterfactual_aggregates":{k:v["aggregate"] for k,v in raw["counterfactuals"].items()},
             "monte_carlo":{k:v for k,v in mc.items() if k!="raw"}}
    print(json.dumps(compact,indent=2))


if __name__ == "__main__":
    main()
