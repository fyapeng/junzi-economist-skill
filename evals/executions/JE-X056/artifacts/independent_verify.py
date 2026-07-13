"""Independent reconstruction: intentionally imports no production module or result."""
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
primitive = json.loads((HERE / "raw_primitives.json").read_text(encoding="utf-8"))
rows = primitive["observations"]
xx = np.fromiter((float(z["x"]) for z in rows), dtype=float)
yy = np.fromiter((int(z["y"]) for z in rows), dtype=float)
px = float(primitive["design"]["policy_x"])
grouped = []
for level in sorted(set(xx.tolist())):
    mask = xx == level
    grouped.append((float(level), int(mask.sum()), int(yy[mask].sum())))
box4 = [(-3.0, 2.0), (0.05, 2.5), (0.0, 5.0), (0.08, 0.92)]
grid = [round(v, 2) for v in np.arange(0, 5.0001, 0.10)]
cut = 3.841458820694124


def logistic_scalar(t):
    if t >= 0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def criterion(par):
    # Separately coded observation loop, not the production vectorized function.
    aa, bb, sep, share = [float(z) for z in par]
    total = 0.0
    # Reconstruct sufficient counts from raw rows, then evaluate a separately coded
    # grouped Bernoulli likelihood (algebraically identical to the row likelihood).
    for xi, nn, successes in grouped:
        low = logistic_scalar(aa + bb * xi - sep)
        high = logistic_scalar(aa + bb * xi + sep)
        prob = max(1e-14, min(1 - 1e-14, (1 - share) * low + share * high))
        total -= successes * math.log(prob) + (nn - successes) * math.log(1 - prob)
    return total


def central_grad(fun, z, bounds):
    z = np.asarray(z, float)
    g = np.empty(z.size)
    for j in range(z.size):
        h = 2e-6 * max(1.0, abs(z[j]))
        lo, hi = bounds[j]
        zp, zm = z.copy(), z.copy()
        zp[j] = min(hi, z[j] + h); zm[j] = max(lo, z[j] - h)
        g[j] = (fun(zp) - fun(zm)) / (zp[j] - zm[j])
    return g


def kkt(z, g, bounds):
    pg = g.copy()
    for j, (lo, hi) in enumerate(bounds):
        if z[j] <= lo + 2e-6 and g[j] > 0: pg[j] = 0
        if z[j] >= hi - 2e-6 and g[j] < 0: pg[j] = 0
    return float(np.max(np.abs(pg)) / (1 + np.max(np.abs(g))))


def verifier_starts(bounds, count, offset):
    # An independently chosen cosine lattice; no stored terminal enters this list.
    out = []
    for k in range(count):
        vals = []
        for j, (lo, hi) in enumerate(bounds):
            frac = 0.5 * (1 + math.cos((k + 1) * (j + 2) * 1.173 + offset))
            vals.append(lo + (0.04 + 0.92 * frac) * (hi - lo))
        out.append(vals)
    return out


def reconstruct(fun, bounds, offset, count=9):
    records = []
    for sid, start in enumerate(verifier_starts(bounds, count, offset)):
        # Powell supplies a derivative-free basin search; SLSQP independently polishes constraints.
        p = minimize(fun, start, method="Powell", bounds=bounds,
                     options={"xtol": 1e-10, "ftol": 1e-11, "maxiter": 2500})
        s = minimize(fun, p.x, method="SLSQP", bounds=bounds,
                     options={"ftol": 1e-11, "maxiter": 1800})
        gg = central_grad(fun, s.x, bounds)
        kr = kkt(s.x, gg, bounds)
        records.append({"start_id": sid, "initial": start, "terminal": s.x.tolist(),
                        "objective": float(fun(s.x)), "finite_difference_gradient": gg.tolist(),
                        "kkt_scaled_inf": kr, "powell_success": bool(p.success),
                        "slsqp_success": bool(s.success), "accepted": bool(np.isfinite(fun(s.x)) and kr <= 8e-5)})
    ok = [z for z in records if z["accepted"]]
    return (min(ok, key=lambda z: z["objective"]) if ok else None), records


unr, unruns = reconstruct(criterion, box4, 0.744, 12)
if unr is None:
    raise SystemExit("independent unrestricted reconstruction failed")

profiles = []
for sep in grid:
    b3 = [box4[0], box4[1], box4[3]]

    def fixed(v, d=sep):
        return criterion([v[0], v[1], d, v[2]])

    best, runs = reconstruct(fixed, b3, 1.219 + sep * 0.13, 20)
    if best is None:
        profiles.append({"delta": sep, "status": "hole_unresolved", "all_starts": runs})
        continue
    a, b, w = best["terminal"]
    low = logistic_scalar(a + b * px - sep)
    high = logistic_scalar(a + b * px + sep)
    lr = max(0.0, 2 * (best["objective"] - unr["objective"]))
    profiles.append({"delta": sep, "status": "accepted", "objective": best["objective"], "lr": lr,
                     "in_evaluated_grid_set": bool(lr <= cut), "policy_adoption": (1 - w) * low + w * high,
                     "selected_terminal": [a, b, sep, w], "kkt_scaled_inf": best["kkt_scaled_inf"],
                     "all_starts": runs})

included = [z for z in profiles if z["status"] == "accepted" and z["in_evaluated_grid_set"]]
holes = [z["delta"] for z in profiles if z["status"] != "accepted"]
left_support_bounded = bool(included and included[0]["delta"] == grid[0] == box4[2][0])
answer = {
    "independence_contract": {
        "inputs": ["raw_primitives.json only"],
        "production_imports": [], "stored_terminals_or_objectives_used_as_inputs_or_seeds": False,
        "likelihood": "separate scalar-loop Bernoulli mixture implementation",
        "optimizer": "independent cosine-lattice starts; Powell then SLSQP; finite-difference KKT"
    },
    "unrestricted": unr, "unrestricted_all_starts": unruns, "profile_grid": profiles,
    "summary": {"holes": holes,
                "left_censored": bool(included and included[0]["delta"] == grid[0] and not left_support_bounded),
                "left_support_bounded": left_support_bounded,
                "left_endpoint_status": "closed economic/label-normalization boundary delta=0" if left_support_bounded else "interior or grid-censored",
                "right_censored": bool(included and included[-1]["delta"] == grid[-1]),
                "included_delta": [z["delta"] for z in included],
                "policy_image_selected_only": [min(z["policy_adoption"] for z in included),
                                                 max(z["policy_adoption"] for z in included)] if included else None},
    "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
}
(HERE / "independent_results.json").write_text(json.dumps(answer, indent=2), encoding="utf-8")
print(json.dumps({"objective": unr["objective"], "theta": unr["terminal"], "holes": holes,
                  "set": answer["summary"]["included_delta"], "policy_image": answer["summary"]["policy_image_selected_only"]}))
