from __future__ import annotations

import contextlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq, minimize_scalar


OUT = Path(r"C:\Users\ENAN\AppData\Local\Temp\junzi-economist-macro-x042")
LOG = OUT / "run_output.txt"
RESULTS = OUT / "results.json"
RESPONSE = OUT / "response.md"

SIGMA = 1.5
BETA = 0.95
ALPHA = 0.33
DELTA = 0.07
E_RAW = np.array([0.4, 1.0, 1.8])
P = np.array([[0.85, 0.12, 0.03], [0.08, 0.84, 0.08], [0.03, 0.12, 0.85]])

# Fixed before looking at any equilibrium result.
TAIL_MASS_LIMIT = 1.0e-7
CAPPED_MASS_LIMIT = 1.0e-10
CAP_NODE_SHARE_LIMIT = 0.02
POLICY_FP_LIMIT = 2.0e-7
DIST_LIMIT = 2.0e-11
ROOT_TOL = 2.0e-5
EXACT_ZERO_TOL = 1.0e-10  # numerical candidate only, never called an analytic exact zero


class Tee:
    def __init__(self, *files): self.files = files
    def write(self, x):
        for f in self.files: f.write(x); f.flush()
    def flush(self):
        for f in self.files: f.flush()


def stationary_markov():
    x = np.ones(3) / 3
    for _ in range(10000):
        y = x @ P
        if np.max(np.abs(y - x)) < 1e-15: break
        x = y
    ebar = float(x @ E_RAW)
    return x, E_RAW / ebar, ebar, float(np.max(np.abs(x @ P - x)))


PI_E, E, EBAR, PI_RESID = stationary_markov()


def prices(K):
    return ALPHA * K ** (ALPHA - 1.0) - DELTA, (1.0 - ALPHA) * K ** ALPHA


def grid(amax, n):
    x = np.linspace(0.0, 1.0, n)
    return amax * x ** 2.2


def interp_linear_extrap(x, xp, fp):
    y = np.interp(x, xp, fp)
    left = x < xp[0]
    right = x > xp[-1]
    if np.any(left): y[left] = fp[0] + (x[left] - xp[0]) * (fp[1] - fp[0]) / (xp[1] - xp[0])
    if np.any(right): y[right] = fp[-1] + (x[right] - xp[-1]) * (fp[-1] - fp[-2]) / (xp[-1] - xp[-2])
    return y


def solve_household(K, amax, n, tol=2e-10, maxit=4000):
    a = grid(amax, n)
    r, w = prices(K)
    R = 1.0 + r
    cash = R * a[:, None] + w * E[None, :]
    c = np.maximum(cash - np.minimum(0.05 * cash, 0.5), 1e-10)
    cap_raw = np.zeros_like(c)
    fp = np.inf
    for it in range(1, maxit + 1):
        emu = c ** (-SIGMA) @ P.T
        c_endo = (BETA * R * emu) ** (-1.0 / SIGMA)
        pol_raw = np.empty_like(c)
        for z in range(3):
            a_endo = (c_endo[:, z] + a - w * E[z]) / R
            pol_raw[:, z] = interp_linear_extrap(a, a_endo, a)
        pol = np.clip(pol_raw, 0.0, amax)
        c_new = np.maximum(cash - pol, 1e-12)
        fp = float(np.max(np.abs(c_new - c) / np.maximum(1.0, c)))
        c = c_new
        cap_raw = pol_raw
        if fp < tol: break
    if fp >= tol: raise RuntimeError(f"EGM failed K={K}, fp={fp}")
    pol = np.clip(cash - c, 0.0, amax)
    return a, c, pol, cap_raw, {"iterations": it, "policy_fp": fp, "r": r, "w": w}


def invariant_distribution(a, pol, tol=2e-13, maxit=100000):
    n = len(a)
    idx_hi = np.searchsorted(a, pol, side="right")
    idx_hi = np.clip(idx_hi, 1, n - 1)
    idx_lo = idx_hi - 1
    whi = (pol - a[idx_lo]) / (a[idx_hi] - a[idx_lo])
    whi = np.clip(whi, 0.0, 1.0)
    mu = np.outer(np.ones(n) / n, PI_E)
    for it in range(1, maxit + 1):
        new = np.zeros_like(mu)
        for z in range(3):
            base = mu[:, z]
            for zp in range(3):
                wt = base * P[z, zp]
                np.add.at(new[:, zp], idx_lo[:, z], wt * (1.0 - whi[:, z]))
                np.add.at(new[:, zp], idx_hi[:, z], wt * whi[:, z])
        err = float(np.max(np.abs(new - mu)))
        mu = new
        if err < tol: break
    if err >= tol: raise RuntimeError(f"distribution failed, resid={err}")
    # Recompute the invariance residual once, independently of the stopping comparison.
    check = np.zeros_like(mu)
    for z in range(3):
        for zp in range(3):
            wt = mu[:, z] * P[z, zp]
            np.add.at(check[:, zp], idx_lo[:, z], wt * (1.0 - whi[:, z]))
            np.add.at(check[:, zp], idx_hi[:, z], wt * whi[:, z])
    return mu, {"iterations": it, "invariance_sup": float(np.max(np.abs(check - mu))),
                "state_marginal_sup": float(np.max(np.abs(mu.sum(axis=0) - PI_E)))}


def euler_diagnostics(a, c, pol, mu, r):
    R = 1.0 + r
    cp = np.empty((len(a), 3, 3))
    for z in range(3):
        for zp in range(3): cp[:, z, zp] = np.interp(pol[:, z], a, c[:, zp])
    rhs = BETA * R * np.sum(P[None, :, :] * cp ** (-SIGMA), axis=2)
    ratio = rhs / (c ** (-SIGMA))
    constrained = pol <= 1e-12
    err = np.where(constrained, np.maximum(ratio - 1.0, 0.0), np.abs(ratio - 1.0))
    positive_mass = mu > 1e-14
    return {"max_euler_kkt": float(np.max(err[positive_mass])),
            "mu_weighted_euler_kkt": float(np.sum(mu * err)),
            "max_borrowing_kkt_violation": float(np.max(np.maximum(ratio[constrained] - 1.0, 0.0))) if np.any(constrained) else 0.0,
            "borrowing_mass": float(mu[constrained].sum())}


def evaluate(K, cfg):
    a, c, pol, raw, hh = solve_household(K, cfg["amax"], cfg["n"])
    mu, dist = invariant_distribution(a, pol)
    A = float(np.sum(mu * a[:, None]))
    tail_mass = float(mu[-5:, :].sum())
    capped_nodes = raw >= cfg["amax"]
    capped_mass = float(mu[capped_nodes].sum())
    cap_node_share = float(np.mean(capped_nodes))
    r, w = hh["r"], hh["w"]
    C = float(np.sum(mu * c))
    Y = K ** ALPHA
    resource = Y - C - DELTA * K
    eul = euler_diagnostics(a, c, pol, mu, r)
    reliable = (tail_mass <= TAIL_MASS_LIMIT and capped_mass <= CAPPED_MASS_LIMIT
                and cap_node_share <= CAP_NODE_SHARE_LIMIT and hh["policy_fp"] <= POLICY_FP_LIMIT
                and dist["invariance_sup"] <= DIST_LIMIT)
    return {"K": float(K), "asset_supply": A, "excess_assets": A - K, "C": C, "Y": Y,
            "resource_residual": resource, "tail_mass_top5": tail_mass,
            "top_point_mass": float(mu[-1, :].sum()), "capped_policy_mass": capped_mass,
            "capped_policy_node_share": cap_node_share, "max_policy_ratio": float(np.max(pol) / cfg["amax"]),
            "reliable": bool(reliable), **hh, **dist, **eul}


def scan(cfg):
    points = []
    for j, K in enumerate(np.linspace(cfg["Kmin"], cfg["Kmax"], cfg["Kpoints"])):
        q = evaluate(float(K), cfg)
        points.append(q)
        print(f"{cfg['name']} {j+1:03d}/{cfg['Kpoints']} K={K:.6f} excess={q['excess_assets']:+.6e} reliable={q['reliable']} tail={q['tail_mass_top5']:.2e}")
    brackets, exact_candidates = [], []
    for q in points:
        if q["reliable"] and abs(q["excess_assets"]) <= EXACT_ZERO_TOL: exact_candidates.append(q["K"])
    for x, y in zip(points[:-1], points[1:]):
        if x["reliable"] and y["reliable"] and x["excess_assets"] * y["excess_assets"] < 0:
            brackets.append([x["K"], y["K"]])
    roots = []
    for lo, hi in brackets:
        root = brentq(lambda k: evaluate(float(k), cfg)["excess_assets"], lo, hi, xtol=2e-10, rtol=2e-12)
        q = evaluate(float(root), cfg)
        if q["reliable"]: roots.append(q)
    # Tangency screen: bounded minimization of |excess| around every reliable discrete local minimum.
    tangency = []
    for i in range(1, len(points) - 1):
        triple = points[i-1:i+2]
        if all(q["reliable"] for q in triple):
            vals = [abs(q["excess_assets"]) for q in triple]
            if vals[1] <= vals[0] and vals[1] <= vals[2]:
                z = minimize_scalar(lambda k: abs(evaluate(float(k), cfg)["excess_assets"]),
                                    bounds=(triple[0]["K"], triple[2]["K"]), method="bounded",
                                    options={"xatol": 2e-7})
                qz = evaluate(float(z.x), cfg)
                tangency.append({"K": float(z.x), "abs_excess": abs(qz["excess_assets"]),
                                 "signed_excess": qz["excess_assets"], "reliable": qz["reliable"],
                                 "root_candidate": bool(qz["reliable"] and abs(qz["excess_assets"]) < ROOT_TOL)})
    return {"config": cfg, "points": points, "reliable_sign_change_brackets": brackets,
            "numerical_zero_candidates": exact_candidates, "roots": roots, "tangency_screens": tangency}


def ra_benchmark():
    rstar = 1.0 / BETA - 1.0
    K = (ALPHA / (rstar + DELTA)) ** (1.0 / (1.0 - ALPHA))
    r, w = prices(K)
    return {"conditional_assumptions": "deterministic representative household, interior steady state, L=1",
            "K": K, "r": r, "w": w, "note": "comparison only; no welfare or Pareto ordering"}


def make_response(res):
    coarse, fine = res["scans"]
    roots = fine["roots"]
    if roots:
        rows = "\n".join(f"- K={q['K']:.8f}, r={q['r']:.8f}, w={q['w']:.8f}, A-K={q['excess_assets']:+.3e}, C={q['C']:.8f}" for q in roots)
        verdict = f"可靠细网格扫描检出 {len(roots)} 个带符号变化的稳态：\n\n{rows}"
    else:
        verdict = "可靠扫描未检出稳态；不能据此断言不存在均衡。"
    maxres = max([abs(q["resource_residual"]) for q in roots], default=float('nan'))
    maxe = max([q["max_euler_kkt"] for q in roots], default=float('nan'))
    return f"""# JE-X042 异质性主体生产经济稳态

## 结论

{verdict}

这是“检出的均衡集合”，不是全局唯一性定理。完整可靠域内的全部相邻符号变化均已收集；另做了数值零点和离散局部极小值的切点筛查，但有限扫描无法排除未采到的偶重根、极窄根或可靠域之外的根。

## 经济环境与递归闭合

状态为 `(a,e)`，家庭在 `a' >= 0` 下解
`V(a,e)=max_{{a'>=0}} u(c)+beta E[V(a',e')|e]`，其中
`c+a'=(1+r)a+w e`，`u(c)=c^(1-sigma)/(1-sigma)`。效率状态先按给定转移矩阵求平稳概率，再把效率除以平稳均值，使总有效劳动 `L=1`。

内点 Euler 条件为 `u'(c)=beta(1+r)E[u'(c')|e]`；在借款约束 `a'=0` 处为 `u'(c)>=beta(1+r)E[u'(c')|e]`，并满足互补松弛。企业竞争价格为 `r=alpha K^(alpha-1)-delta`、`w=(1-alpha)K^alpha`。不变分布由政策与 `P` 联合诱导；资产市场为 `sum mu(a,e)a=K`；资源约束为 `Y=C+delta K`。

## 验证摘要

- 平稳效率概率：{np.array2string(PI_E, precision=10)}；原始平均效率 `{EBAR:.10f}`；归一化效率 {np.array2string(E, precision=10)}。
- 粗扫描：`K in [{coarse['config']['Kmin']},{coarse['config']['Kmax']}]`，{coarse['config']['Kpoints']} 点，资产网格 {coarse['config']['n']} 点、上界 {coarse['config']['amax']}；可靠括根 {coarse['reliable_sign_change_brackets']}。
- 更宽更细复验：`K in [{fine['config']['Kmin']},{fine['config']['Kmax']}]`，{fine['config']['Kpoints']} 点，资产网格 {fine['config']['n']} 点、上界 {fine['config']['amax']}；可靠括根 {fine['reliable_sign_change_brackets']}。
- 均衡最大 Euler/KKT 残差 `{maxe:.3e}`；最大资源残差 `{maxres:.3e}`。逐根的分布残差、市场残差、边界质量、借款约束质量均在 `results.json`。
- 可靠阈值在求解前固定：top-5 资产质量 `<= {TAIL_MASS_LIMIT}`，被上界截断政策的分布质量 `<= {CAPPED_MASS_LIMIT}`，截断节点比例 `<= {CAP_NODE_SHARE_LIMIT}`，政策固定点 `<= {POLICY_FP_LIMIT}`，分布残差 `<= {DIST_LIMIT}`。每个扫描点均保存这些量。
- Bellman 的等价最优性检查采用 EGM Euler/KKT：内点等式、借款角点不等式，并报告有正分布质量状态上的最大和加权残差。

## 有条件的 RA 比较

确定性、内点、`L=1` 的代表性家庭稳态给出 `r=1/beta-1` 和 `K={res['ra_benchmark']['K']:.8f}`。它只用于数值尺度比较；市场完备性、可实施配置和福利权重并未建立，因此不推出福利或 Pareto 排序。

## 技能评估

技能有效。它直接促成了四个关键约束：家庭—分布—价格—资源同时闭合；把“一个计算根”降格为“一个检出均衡”；把尾部污染纳入执行选择规则；并把 Euler/KKT、分布、市场、资源和网格敏感性置于同一可重跑入口。局限是技能本身不能提供全局唯一性证明；本报告也不作该声明。
"""


def main():
    start = time.time()
    coarse_cfg = {"name": "coarse", "Kmin": 2.5, "Kmax": 10.0, "Kpoints": 61, "amax": 80.0, "n": 450}
    fine_cfg = {"name": "fine", "Kmin": 1.5, "Kmax": 14.0, "Kpoints": 201, "amax": 140.0, "n": 850}
    coarse = scan(coarse_cfg)
    fine = scan(fine_cfg)
    res = {"task": "JE-X042", "fresh_recompute": True,
           "primitives": {"sigma": SIGMA, "beta": BETA, "alpha": ALPHA, "delta": DELTA,
                          "e_raw": E_RAW.tolist(), "P": P.tolist()},
           "stationary_efficiency": {"pi": PI_E.tolist(), "raw_mean": EBAR,
                                     "normalized_e": E.tolist(), "markov_residual": PI_RESID,
                                     "normalized_mean": float(PI_E @ E)},
           "preset_reliability_thresholds": {"tail_mass_top5": TAIL_MASS_LIMIT,
                  "capped_policy_mass": CAPPED_MASS_LIMIT, "capped_policy_node_share": CAP_NODE_SHARE_LIMIT,
                  "policy_fp": POLICY_FP_LIMIT, "distribution_sup": DIST_LIMIT},
           "scans": [coarse, fine], "ra_benchmark": ra_benchmark(),
           "limitations": ["finite scans cannot rule out tangencies between points",
                           "numerical zero tolerance is not analytic exact equality",
                           "no global uniqueness claim without proof"],
           "software": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__,
                        "platform": platform.platform()}, "elapsed_seconds": time.time() - start}
    RESULTS.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    RESPONSE.write_text(make_response(res), encoding="utf-8")
    print(f"completed elapsed={res['elapsed_seconds']:.2f}s results={RESULTS}")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    with LOG.open("w", encoding="utf-8") as lf, contextlib.redirect_stdout(Tee(sys.__stdout__, lf)), contextlib.redirect_stderr(Tee(sys.__stderr__, lf)):
        main()
