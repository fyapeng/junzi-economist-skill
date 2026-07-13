from __future__ import annotations

import json
import math
import platform
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar


BETA = 0.96
SIGMA = 2.0
ALPHA = 0.36
DELTA = 0.08
E = np.array([0.5, 1.5])
BASE_P = np.array([[0.9, 0.1], [0.1, 0.9]])
ROOT = Path(__file__).resolve().parent


@dataclass
class Config:
    name: str
    n: int
    a_min: float
    a_max: float
    curvature: float
    persistence: float


def utility(c: np.ndarray | float) -> np.ndarray | float:
    return -1.0 / np.asarray(c)


def transition(persistence: float) -> np.ndarray:
    return np.array([[persistence, 1.0 - persistence],
                     [1.0 - persistence, persistence]])


def grid_from(cfg: Config) -> np.ndarray:
    x = np.linspace(0.0, 1.0, cfg.n)
    return cfg.a_min + (cfg.a_max - cfg.a_min) * x ** cfg.curvature


def prices(K: float) -> tuple[float, float]:
    r = ALPHA * K ** (ALPHA - 1.0) - DELTA
    w = (1.0 - ALPHA) * K ** ALPHA
    return r, w


def interp_with_right_extrap(x: np.ndarray, xp: np.ndarray, fp: np.ndarray) -> np.ndarray:
    out = np.interp(x, xp, fp, left=fp[0], right=fp[-1])
    mask = x > xp[-1]
    if np.any(mask):
        slope = (fp[-1] - fp[-2]) / (xp[-1] - xp[-2])
        out[mask] = fp[-1] + slope * (x[mask] - xp[-1])
    return out


def solve_household(K: float, cfg: Config, tol: float = 2e-10, max_iter: int = 5000):
    agrid = grid_from(cfg)
    P = transition(cfg.persistence)
    r, w = prices(K)
    R = 1.0 + r
    if R <= 0:
        raise ValueError("Nonpositive gross return")

    cash = R * agrid[None, :] + w * E[:, None]
    ap = np.full((2, cfg.n), cfg.a_min)
    c = np.maximum(cash - ap, 1e-12)
    diff = math.inf
    for it in range(1, max_iter + 1):
        mu_next = c ** (-SIGMA)
        new_ap = np.empty_like(ap)
        for i in range(2):
            emu = P[i] @ mu_next
            c_endo = (BETA * R * emu) ** (-1.0 / SIGMA)
            a_endo = (c_endo + agrid - w * E[i]) / R
            pol = interp_with_right_extrap(agrid, a_endo, agrid)
            pol[agrid < a_endo[0]] = cfg.a_min
            new_ap[i] = np.clip(pol, cfg.a_min, cfg.a_max)
        new_c = cash - new_ap
        if np.min(new_c) <= 0:
            raise RuntimeError("EGM generated nonpositive consumption")
        diff = float(np.max(np.abs(new_ap - ap)))
        ap = 0.75 * new_ap + 0.25 * ap
        c = cash - ap
        if diff < tol:
            break
    else:
        raise RuntimeError(f"EGM failed at K={K}: diff={diff}")
    return {"agrid": agrid, "P": P, "r": r, "w": w, "ap": ap, "c": c,
            "egm_iterations": it, "egm_policy_diff": diff}


def stationary_distribution(sol: dict, tol: float = 2e-14, max_iter: int = 200000):
    agrid, P, ap = sol["agrid"], sol["P"], sol["ap"]
    n = agrid.size
    dist = np.full((2, n), 1.0 / (2.0 * n))
    for it in range(1, max_iter + 1):
        nxt = np.zeros_like(dist)
        for i in range(2):
            idx_hi = np.searchsorted(agrid, ap[i], side="right")
            idx_hi = np.clip(idx_hi, 1, n - 1)
            idx_lo = idx_hi - 1
            denom = agrid[idx_hi] - agrid[idx_lo]
            whi = np.clip((ap[i] - agrid[idx_lo]) / denom, 0.0, 1.0)
            wlo = 1.0 - whi
            mass = dist[i]
            for j in range(2):
                np.add.at(nxt[j], idx_lo, mass * P[i, j] * wlo)
                np.add.at(nxt[j], idx_hi, mass * P[i, j] * whi)
        diff = float(np.max(np.abs(nxt - dist)))
        dist = nxt
        if diff < tol:
            break
    else:
        raise RuntimeError("Distribution iteration failed")
    # One additional application for a directly measured invariant residual.
    check = np.zeros_like(dist)
    for i in range(2):
        idx_hi = np.clip(np.searchsorted(agrid, ap[i], side="right"), 1, n - 1)
        idx_lo = idx_hi - 1
        whi = np.clip((ap[i] - agrid[idx_lo]) /
                      (agrid[idx_hi] - agrid[idx_lo]), 0.0, 1.0)
        for j in range(2):
            np.add.at(check[j], idx_lo, dist[i] * P[i, j] * (1.0 - whi))
            np.add.at(check[j], idx_hi, dist[i] * P[i, j] * whi)
    residual = float(np.max(np.abs(check - dist)))
    return dist, it, diff, residual


def excess_assets(K: float, cfg: Config, detailed: bool = False):
    sol = solve_household(K, cfg)
    dist, dit, ddiff, dres = stationary_distribution(sol)
    supply = float(np.sum(dist * sol["agrid"][None, :]))
    if detailed:
        sol.update({"dist": dist, "dist_iterations": dit, "dist_diff": ddiff,
                    "dist_residual": dres, "asset_supply": supply})
        return supply - K, sol
    return supply - K


def bracket_root(cfg: Config):
    ra_K = (ALPHA / (1.0 / BETA - 1.0 + DELTA)) ** (1.0 / (1.0 - ALPHA))
    points = np.linspace(max(0.6, 0.35 * ra_K), 2.6 * ra_K, 18)
    vals = []
    for K in points:
        vals.append(excess_assets(float(K), cfg))
    for lo, hi, flo, fhi in zip(points[:-1], points[1:], vals[:-1], vals[1:]):
        if flo == 0 or flo * fhi < 0:
            return float(lo), float(hi), float(flo), float(fhi), points.tolist(), vals
    raise RuntimeError(f"No bracket for {cfg.name}: {list(zip(points, vals))}")


def policy_value(sol: dict, tol: float = 2e-11, max_iter: int = 5000):
    agrid, P, ap, c = sol["agrid"], sol["P"], sol["ap"], sol["c"]
    V = utility(c) / (1.0 - BETA)
    diff = math.inf
    for it in range(1, max_iter + 1):
        cont = np.empty_like(V)
        for i in range(2):
            cont[i] = sum(P[i, j] * np.interp(ap[i], agrid, V[j]) for j in range(2))
        Vn = utility(c) + BETA * cont
        diff = float(np.max(np.abs(Vn - V)))
        V = Vn
        if diff < tol:
            break
    else:
        raise RuntimeError("Value policy evaluation failed")
    return V, it, diff


def bellman_residual(sol: dict, V: np.ndarray):
    agrid, P, r, w = sol["agrid"], sol["P"], sol["r"], sol["w"]
    R = 1.0 + r
    residuals = []
    policy_gaps = []
    # Full state grid, continuous bounded scalar choice with interpolated continuation value.
    for i in range(2):
        EVgrid = P[i] @ V
        for m, a in enumerate(agrid):
            cash = R * a + w * E[i]
            upper = min(sol["agrid"][-1], cash - 1e-12)
            if upper <= sol["agrid"][0]:
                opt_ap = sol["agrid"][0]
                tv = utility(cash - opt_ap) + BETA * np.interp(opt_ap, agrid, EVgrid)
            else:
                def neg_obj(x):
                    return -(utility(cash - x) + BETA * np.interp(x, agrid, EVgrid))
                ans = minimize_scalar(neg_obj, bounds=(sol["agrid"][0], upper),
                                      method="bounded", options={"xatol": 2e-11, "maxiter": 300})
                opt_ap, tv = float(ans.x), float(-ans.fun)
            residuals.append(abs(tv - V[i, m]))
            policy_gaps.append(abs(opt_ap - sol["ap"][i, m]))
    return float(max(residuals)), float(max(policy_gaps))


def weighted_quantile(values: np.ndarray, weights: np.ndarray, probs):
    order = np.argsort(values)
    v, w = values[order], weights[order]
    cw = np.cumsum(w)
    cw /= cw[-1]
    return [float(np.interp(p, cw, v)) for p in probs]


def weighted_gini_nonnegative(values: np.ndarray, weights: np.ndarray):
    order = np.argsort(values)
    x, w = values[order], weights[order]
    total = np.sum(w * x)
    if total <= 0:
        return None
    cw = np.cumsum(w)
    cx = np.cumsum(w * x) / total
    cw0 = np.concatenate(([0.0], cw))
    cx0 = np.concatenate(([0.0], cx))
    return float(1.0 - np.sum((cx0[1:] + cx0[:-1]) * np.diff(cw0)))


def diagnostics(cfg: Config):
    lo, hi, flo, fhi, scan_k, scan_res = bracket_root(cfg)
    K = float(brentq(lambda x: excess_assets(x, cfg), lo, hi,
                     xtol=2e-8, rtol=2e-10, maxiter=100))
    market_residual, sol = excess_assets(K, cfg, detailed=True)
    V, vit, vdiff = policy_value(sol)
    bres, policy_gap = bellman_residual(sol, V)

    agrid, dist, ap, c = sol["agrid"], sol["dist"], sol["ap"], sol["c"]
    r, w = sol["r"], sol["w"]
    R = 1.0 + r
    lhs = c ** (-SIGMA)
    rhs = np.empty_like(lhs)
    for i in range(2):
        rhs[i] = BETA * R * sum(
            sol["P"][i, j] * np.interp(ap[i], agrid, c[j]) ** (-SIGMA)
            for j in range(2)
        )
    ratio = rhs / lhs
    binding = ap <= cfg.a_min + 2e-8
    relevant = (dist > 1e-12) & (~binding) & (ap < cfg.a_max - 1e-6)
    euler_vals = np.abs(1.0 - ratio[relevant])
    euler_w = dist[relevant]
    euler_p95 = weighted_quantile(euler_vals, euler_w, [0.95])[0] if euler_vals.size else None
    kkt_violation = float(np.max(np.maximum(ratio[binding] - 1.0, 0.0))) if np.any(binding) else 0.0

    vals_a = np.tile(agrid, 2)
    weights = dist.ravel()
    vals_v = V.ravel()
    vals_c = c.ravel()
    asset_q = weighted_quantile(vals_a, weights, [0.1, 0.25, 0.5, 0.75, 0.9, 0.99])
    value_q = weighted_quantile(vals_v, weights, [0.1, 0.5, 0.9])
    consumption_q = weighted_quantile(vals_c, weights, [0.1, 0.5, 0.9])
    constrained_share = float(np.sum(dist[binding]))
    top_mass = float(np.sum(dist[:, -1]))
    mean_c = float(np.sum(dist * c))
    Y = K ** ALPHA
    resource_residual = mean_c + DELTA * K - Y
    stationary_e = np.sum(dist, axis=1)

    return {
        "config": asdict(cfg),
        "equilibrium": {"K": K, "r": r, "w": w, "Y": Y,
                        "asset_supply": sol["asset_supply"],
                        "asset_market_residual": float(market_residual),
                        "mean_consumption": mean_c,
                        "resource_residual_C_plus_deltaK_minus_Y": float(resource_residual)},
        "root": {"bracket": [lo, hi], "residual_at_bracket": [flo, fhi],
                 "scan_K": scan_k, "scan_residual": [float(x) for x in scan_res]},
        "convergence": {"egm_iterations": sol["egm_iterations"],
                        "egm_policy_sup_diff": sol["egm_policy_diff"],
                        "distribution_iterations": sol["dist_iterations"],
                        "distribution_sup_diff": sol["dist_diff"],
                        "distribution_invariance_residual": sol["dist_residual"],
                        "distribution_mass_error": float(abs(np.sum(dist) - 1.0)),
                        "value_policy_iterations": vit,
                        "value_policy_sup_diff": vdiff,
                        "continuous_bellman_residual_sup": bres,
                        "bellman_optimizer_vs_egm_policy_gap_sup": policy_gap},
        "optimality": {"nonbinding_euler_relative_max": float(np.max(euler_vals)),
                       "nonbinding_euler_relative_p95_weighted": euler_p95,
                       "borrowing_constraint_kkt_violation_max": kkt_violation},
        "distribution": {"efficiency_state_mass": stationary_e.tolist(),
                         "asset_quantiles_p10_p25_p50_p75_p90_p99": asset_q,
                         "asset_gini": weighted_gini_nonnegative(vals_a, weights) if cfg.a_min >= 0 else None,
                         "borrowing_constrained_share": constrained_share,
                         "top_grid_mass": top_mass,
                         "consumption_quantiles_p10_p50_p90": consumption_q,
                         "value_quantiles_p10_p50_p90": value_q,
                         "mean_value": float(np.sum(weights * vals_v)),
                         "mean_value_by_efficiency": [float(np.sum(dist[i] * V[i]) / stationary_e[i]) for i in range(2)]},
        "prices_identity": {"firm_labor": 1.0, "mean_efficiency": float(stationary_e @ E)},
    }


def main():
    configs = [
        Config("baseline", 600, 0.0, 40.0, 2.5, 0.9),
        Config("finer_wider_grid", 900, 0.0, 60.0, 2.5, 0.9),
        Config("smaller_grid", 400, 0.0, 25.0, 2.5, 0.9),
        Config("relaxed_borrowing", 600, -0.25, 40.0, 2.5, 0.9),
        Config("lower_persistence", 600, 0.0, 40.0, 2.5, 0.8),
    ]
    results = {"parameters": {"beta": BETA, "sigma": SIGMA, "alpha": ALPHA,
                               "delta": DELTA, "efficiency": E.tolist(),
                               "baseline_transition": BASE_P.tolist()},
               "representative_agent": {}}
    r_ra = 1.0 / BETA - 1.0
    K_ra = (ALPHA / (r_ra + DELTA)) ** (1.0 / (1.0 - ALPHA))
    results["representative_agent"] = {"r": r_ra, "K": K_ra}
    results["runs"] = []
    for cfg in configs:
        print(f"Solving {cfg.name} ...", flush=True)
        out = diagnostics(cfg)
        results["runs"].append(out)
        eq, cv = out["equilibrium"], out["convergence"]
        print(f"  K={eq['K']:.8f}, r={eq['r']:.8f}, market={eq['asset_market_residual']:.3e}, "
              f"dist={cv['distribution_invariance_residual']:.3e}, Bellman={cv['continuous_bellman_residual_sup']:.3e}", flush=True)
    (ROOT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote results.json with Python {platform.python_version()}")


if __name__ == "__main__":
    main()
