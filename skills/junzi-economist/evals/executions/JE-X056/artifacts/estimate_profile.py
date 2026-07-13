import csv
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent
RAW = json.loads((ROOT / "raw_primitives.json").read_text(encoding="utf-8"))
obs = RAW["observations"]
x = np.array([o["x"] for o in obs], dtype=float)
y = np.array([o["y"] for o in obs], dtype=float)
policy_x = float(RAW["design"]["policy_x"])

BOUNDS = np.array([[-3.0, 2.0], [0.05, 2.5], [0.0, 5.0], [0.08, 0.92]])
N_STARTS = 26
KKT_TOL = 2e-5
OBJ_AGREE = 2e-5
LR_CUTOFF = 3.841458820694124
GRID = np.round(np.arange(0.0, 5.0001, 0.10), 10)


def sigmoid(z):
    return np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))


def nll_grad(theta):
    a, b, d, w = theta
    pl = sigmoid(a + b * x - d)
    ph = sigmoid(a + b * x + d)
    q = np.clip((1 - w) * pl + w * ph, 1e-12, 1 - 1e-12)
    nll = -np.sum(y * np.log(q) + (1 - y) * np.log1p(-q))
    score_q = (q - y) / (q * (1 - q))
    dl, dh = pl * (1 - pl), ph * (1 - ph)
    dq = np.vstack(((1 - w) * dl + w * dh,
                    x * ((1 - w) * dl + w * dh),
                    -(1 - w) * dl + w * dh,
                    ph - pl))
    return float(nll), dq @ score_q


def projected_residual(theta, grad, bounds):
    pg = np.asarray(grad, float).copy()
    scale = 1 + np.linalg.norm(grad, ord=np.inf)
    eps = 5e-8
    for j, (lo, hi) in enumerate(bounds):
        if theta[j] <= lo + eps and grad[j] > 0:
            pg[j] = 0
        elif theta[j] >= hi - eps and grad[j] < 0:
            pg[j] = 0
    return float(np.linalg.norm(pg, ord=np.inf) / scale), pg.tolist()


def starts(bounds, n, phase=0.0):
    lo, hi = bounds[:, 0], bounds[:, 1]
    golden = np.array([0.61803398875, 0.41421356237, 0.73205080757, 0.27182818285])[:len(lo)]
    ans = [(lo + hi) / 2]
    for k in range(1, n):
        frac = (phase + k * golden[:len(lo)]) % 1
        ans.append(lo + frac * (hi - lo))
    return ans


def solve_unrestricted():
    runs = []
    for i, s in enumerate(starts(BOUNDS, N_STARTS, 0.137)):
        r = minimize(lambda t: nll_grad(t), s, jac=True, method="L-BFGS-B", bounds=BOUNDS.tolist(),
                     options={"ftol": 1e-13, "gtol": 1e-9, "maxiter": 2500, "maxls": 40})
        obj, grad = nll_grad(r.x)
        kres, pg = projected_residual(r.x, grad, BOUNDS)
        runs.append({"start_id": i, "initial": s.tolist(), "terminal": r.x.tolist(), "objective": obj,
                     "raw_gradient": grad.tolist(), "projected_gradient": pg, "kkt_scaled_inf": kres,
                     "solver_success": bool(r.success), "status": int(r.status), "message": str(r.message),
                     "accepted": bool(np.isfinite(obj) and kres <= KKT_TOL)})
    good = [r for r in runs if r["accepted"]]
    if not good:
        raise RuntimeError("no accepted unrestricted optimum")
    selected = min(good, key=lambda r: r["objective"])
    for r in runs:
        r["objective_gap"] = r["objective"] - selected["objective"]
    near = [r for r in good if r["objective_gap"] <= OBJ_AGREE]
    return selected, runs, near


def solve_conditional(delta):
    cb = np.delete(BOUNDS, 2, axis=0)

    def fg(v):
        t = np.array([v[0], v[1], delta, v[2]])
        f, g = nll_grad(t)
        return f, g[[0, 1, 3]]

    runs = []
    candidate_starts = starts(cb, 25, phase=0.391 + 0.071 * delta)
    candidate_starts += [np.array([-0.3, 1.1, 0.08]), np.array([-0.3, 1.1, 0.92]),
                         np.array([1.5, 0.9, 0.08]), np.array([-1.5, 1.8, 0.50])]
    for i, s in enumerate(candidate_starts):
        r = minimize(fg, s, jac=True, method="L-BFGS-B", bounds=cb.tolist(),
                     options={"ftol": 1e-13, "gtol": 1e-9, "maxiter": 2000, "maxls": 40})
        obj, grad = fg(r.x)
        kres, pg = projected_residual(r.x, grad, cb)
        theta = [float(r.x[0]), float(r.x[1]), float(delta), float(r.x[2])]
        runs.append({"start_id": i, "initial": s.tolist(), "terminal": theta, "objective": obj,
                     "raw_gradient_free": grad.tolist(), "projected_gradient_free": pg,
                     "kkt_scaled_inf": kres, "solver_success": bool(r.success), "status": int(r.status),
                     "message": str(r.message), "accepted": bool(np.isfinite(obj) and kres <= KKT_TOL)})
    good = [r for r in runs if r["accepted"]]
    if not good:
        return None, runs
    selected = min(good, key=lambda r: r["objective"])
    for r in runs:
        r["objective_gap"] = r["objective"] - selected["objective"]
    return selected, runs


u, uruns, unear = solve_unrestricted()
profile = []
all_runs = {}
for d in GRID:
    sel, runs = solve_conditional(float(d))
    all_runs[f"{d:.2f}"] = runs
    if sel is None:
        profile.append({"delta": float(d), "status": "hole_unresolved", "objective": None, "lr": None,
                        "in_evaluated_grid_set": None, "policy_adoption": None})
        continue
    a, b, dd, w = sel["terminal"]
    pol = (1 - w) * sigmoid(a + b * policy_x - dd) + w * sigmoid(a + b * policy_x + dd)
    lr = 2 * (sel["objective"] - u["objective"])
    profile.append({"delta": float(d), "status": "accepted", "objective": sel["objective"],
                    "lr": float(max(lr, 0.0)), "in_evaluated_grid_set": bool(lr <= LR_CUTOFF),
                    "policy_adoption": float(pol), "selected_terminal": sel["terminal"],
                    "selected_start_id": sel["start_id"], "kkt_scaled_inf": sel["kkt_scaled_inf"]})

included = [p for p in profile if p["status"] == "accepted" and p["in_evaluated_grid_set"]]
holes = [p["delta"] for p in profile if p["status"] != "accepted"]
left_support_bounded = bool(included and min(p["delta"] for p in included) == float(GRID.min()) == BOUNDS[2, 0])
left_censored = bool(included and min(p["delta"] for p in included) == float(GRID.min()) and not left_support_bounded)
right_censored = bool(included and max(p["delta"] for p in included) == float(GRID.max()))
result = {
    "model": "two-latent-intercept-type logit adoption model",
    "parameter_order": ["alpha", "beta", "delta", "pi_high"],
    "bounds": BOUNDS.tolist(), "likelihood": "individual Bernoulli likelihood after integrating latent type",
    "unrestricted_selected": u, "unrestricted_all_starts": uruns,
    "unrestricted_near_best_count": len(unear), "profile_grid": profile,
    "conditional_all_starts": all_runs,
    "inference": {"reference": "accepted unrestricted optimum of the identical likelihood",
                  "lr_cutoff": LR_CUTOFF, "object_name": "95% chi-square(1) evaluated-grid LR set",
                  "holes": holes, "left_censored": left_censored, "left_support_bounded": left_support_bounded,
                  "left_endpoint_status": "closed economic/label-normalization boundary delta=0" if left_support_bounded else "interior or grid-censored",
                  "right_censored": right_censored,
                  "included_delta": [p["delta"] for p in included],
                  "policy_image_selected_only": [min(p["policy_adoption"] for p in included),
                                                   max(p["policy_adoption"] for p in included)] if included else None},
    "support": {"training_x": sorted(set(x.tolist())), "profile_delta_evaluated": [float(GRID.min()), float(GRID.max())],
                "policy_x": policy_x, "policy_support_status": "model-based extrapolation above observed maximum x=1.6"},
    "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
}
(ROOT / "production_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
with (ROOT / "profile_selected.csv").open("w", newline="", encoding="utf-8-sig") as f:
    fields = ["delta", "status", "objective", "lr", "in_evaluated_grid_set", "policy_adoption", "kkt_scaled_inf"]
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader(); w.writerows(profile)
print(json.dumps({"unrestricted_objective": u["objective"], "theta": u["terminal"],
                  "grid_n": len(profile), "holes": holes, "censoring": [left_censored, right_censored],
                  "set": result["inference"]["included_delta"], "policy_image": result["inference"]["policy_image_selected_only"]}))
