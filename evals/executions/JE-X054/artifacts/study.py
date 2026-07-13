import csv
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import expit, logsumexp

ROOT = Path(__file__).resolve().parent
SEED = 731904
N, T = 900, 4
BOUNDS = [(-4, 2), (-2.5, 1.5), (-2, 1.5), (-2, 1.5), (-2, 2), (-3, 3)]
PGRID = np.round(np.arange(0.10, 0.901, 0.05), 2)
LR_CUTOFF = 3.841458820694124
PG_TOL = 2e-4


def unpack(z, fixed_pi=None):
    a1, ld, lb1, lb2, g = z[:5]
    a2 = a1 + np.exp(ld)
    b1, b2 = np.exp(lb1), np.exp(lb2)
    pi = expit(z[5]) if fixed_pi is None else float(fixed_pi)
    return a1, a2, b1, b2, g, pi


def class_ll(a, b, g, price, quality, y):
    v = a - b * price + g * quality
    return (y * v - np.logaddexp(0.0, v)).sum(axis=1), expit(v)


def criterion(z, price, quality, y, fixed_pi=None):
    a1, a2, b1, b2, g, pi = unpack(z, fixed_pi)
    l1, p1 = class_ll(a1, b1, g, price, quality, y)
    l2, p2 = class_ll(a2, b2, g, price, quality, y)
    comp = np.column_stack((np.log1p(-pi) + l1, np.log(pi) + l2))
    den = logsumexp(comp, axis=1)
    w2 = np.exp(comp[:, 1] - den)
    w1 = 1.0 - w2
    s1 = y - p1
    s2 = y - p2
    d = np.exp(z[1])
    grad = np.array([
        np.sum(w1[:, None] * s1) + np.sum(w2[:, None] * s2),
        d * np.sum(w2[:, None] * s2),
        np.sum(w1[:, None] * s1 * (-b1 * price)),
        np.sum(w2[:, None] * s2 * (-b2 * price)),
        np.sum(w1[:, None] * s1 * quality) + np.sum(w2[:, None] * s2 * quality),
    ])
    if fixed_pi is None:
        grad = np.r_[grad, np.sum(w2 - pi)]
    return -float(den.sum()), -grad


def projected_grad(x, grad, bounds):
    pg = np.asarray(grad, float).copy()
    for j, (lo, hi) in enumerate(bounds):
        if x[j] <= lo + 1e-8 and grad[j] > 0:
            pg[j] = 0.0
        if x[j] >= hi - 1e-8 and grad[j] < 0:
            pg[j] = 0.0
    return float(np.max(np.abs(pg))), pg


def fit_multistart(price, quality, y, starts, fixed_pi=None):
    bds = BOUNDS if fixed_pi is None else BOUNDS[:5]
    rows, accepted = [], []
    for sid, x0 in enumerate(starts):
        x0 = np.asarray(x0, float)[:len(bds)]
        res = minimize(lambda z: criterion(z, price, quality, y, fixed_pi), x0,
                       method="L-BFGS-B", jac=True, bounds=bds,
                       options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 2500, "maxls": 50})
        obj, grad = criterion(res.x, price, quality, y, fixed_pi)
        pgmax, pg = projected_grad(res.x, grad, bds)
        ok = bool(np.isfinite(obj) and pgmax <= PG_TOL)
        row = {"index": "unrestricted" if fixed_pi is None else fixed_pi,
               "start_id": sid, "initial": x0.tolist(), "terminal": res.x.tolist(),
               "objective": obj, "raw_gradient": grad.tolist(), "projected_gradient": pg.tolist(),
               "projected_gradient_max": pgmax, "optimizer_success": bool(res.success),
               "accepted": ok, "status": int(res.status), "message": str(res.message),
               "nit": int(res.nit)}
        rows.append(row)
        if ok:
            accepted.append((obj, res.x.copy(), sid, pgmax))
    if not accepted:
        return None, rows
    accepted.sort(key=lambda v: v[0])
    for row in rows:
        row["distance_from_best"] = float(row["objective"] - accepted[0][0])
    return accepted[0], rows


def em_fit(price, quality, y, x0, maxit=800, tol=1e-9):
    a1, a2, b1, b2, g, pi = unpack(np.asarray(x0))
    q = np.array([a1, a2, np.log(b1), np.log(b2), g], float)
    trace = []
    for it in range(maxit):
        l1, _ = class_ll(q[0], np.exp(q[2]), q[4], price, quality, y)
        l2, _ = class_ll(q[1], np.exp(q[3]), q[4], price, quality, y)
        cc = np.column_stack((np.log1p(-pi) + l1, np.log(pi) + l2))
        den = logsumexp(cc, axis=1)
        w2 = np.exp(cc[:, 1] - den)
        pi_new = np.clip(w2.mean(), expit(-3), expit(3))

        def qobj(v):
            ll1, p1 = class_ll(v[0], np.exp(v[2]), v[4], price, quality, y)
            ll2, p2 = class_ll(v[1], np.exp(v[3]), v[4], price, quality, y)
            val = -np.sum((1-w2)*ll1 + w2*ll2)
            s1, s2 = y-p1, y-p2
            gr = -np.array([
                np.sum((1-w2)[:, None]*s1), np.sum(w2[:, None]*s2),
                np.sum((1-w2)[:, None]*s1*(-np.exp(v[2])*price)),
                np.sum(w2[:, None]*s2*(-np.exp(v[3])*price)),
                np.sum((1-w2)[:, None]*s1*quality)+np.sum(w2[:, None]*s2*quality)])
            return val, gr
        rr = minimize(qobj, q, jac=True, method="L-BFGS-B",
                      bounds=[(-4, 5), (-4, 5), (-2, 1.5), (-2, 1.5), (-2, 2)],
                      options={"ftol": 1e-13, "gtol": 1e-9, "maxiter": 500})
        qnew = rr.x
        if qnew[0] > qnew[1]:
            qnew = qnew[[1, 0, 3, 2, 4]]
            pi_new = 1-pi_new
        if qnew[1]-qnew[0] < np.exp(-2.5):
            qnew[1] = qnew[0] + np.exp(-2.5)
        znew = np.array([qnew[0], np.log(qnew[1]-qnew[0]), qnew[2], qnew[3], qnew[4],
                         np.log(pi_new/(1-pi_new))])
        obj, gr = criterion(znew, price, quality, y)
        trace.append({"iteration": it+1, "objective": obj, "pi": pi_new})
        if it and abs(trace[-2]["objective"]-obj) < tol:
            q, pi = qnew, pi_new
            break
        q, pi = qnew, pi_new
    obj, gr = criterion(znew, price, quality, y)
    pgmax, pg = projected_grad(znew, gr, BOUNDS)
    return znew, obj, pgmax, trace


def homogeneous(price, quality, y):
    X = np.stack((np.ones_like(price), -price, quality), axis=2)
    def fun(v):
        eta = np.einsum("ntk,k->nt", X, v)
        pr = expit(eta)
        return -float(np.sum(y*eta-np.logaddexp(0, eta))), -np.einsum("ntk,nt->k", X, y-pr)
    res = minimize(fun, np.array([-0.5, 1.0, 0.5]), jac=True, method="L-BFGS-B",
                   options={"ftol": 1e-13, "gtol": 1e-8, "maxiter": 1000, "maxls": 50})
    obj, grad = fun(res.x)
    return res.x, obj, float(np.max(np.abs(grad))), res


def policy_effect(z, price, quality, fixed_pi=None, subsidy=0.45):
    a1, a2, b1, b2, g, pi = unpack(z, fixed_pi)
    base = (1-pi)*expit(a1-b1*price+g*quality) + pi*expit(a2-b2*price+g*quality)
    post = (1-pi)*expit(a1-b1*(price-subsidy)+g*quality) + pi*expit(a2-b2*(price-subsidy)+g*quality)
    return float(np.mean(post-base))


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def main():
    rng = np.random.default_rng(SEED)
    price = np.clip(rng.normal(2.0, 0.65, (N,T)), 0.35, 3.8)
    quality = rng.normal(0, 1, (N,T))
    true = {"a1": -0.8, "a2": 1.05, "b1": 0.72, "b2": 1.48, "gamma": 0.62, "pi": 0.37}
    latent = rng.binomial(1, true["pi"], N)
    a = np.where(latent[:,None] == 1, true["a2"], true["a1"])
    b = np.where(latent[:,None] == 1, true["b2"], true["b1"])
    prob = expit(a-b*price+true["gamma"]*quality)
    y = rng.binomial(1, prob)
    np.savez_compressed(ROOT/"simulated_data.npz", price=price, quality=quality, y=y,
                        seed=np.array(SEED), true=np.array(list(true.values())))

    starts = [
        [-1.2, np.log(1.0), np.log(.6), np.log(1.3), .4, -0.7],
        [-.6, np.log(1.5), np.log(1.0), np.log(.7), .8, -1.1],
        [-1.8, np.log(2.2), np.log(.4), np.log(1.8), .1, 0.2],
        [-.2, np.log(.5), np.log(1.7), np.log(.5), 1.0, -1.8],
        [-2.3, np.log(2.8), np.log(.3), np.log(2.1), -.2, .7],
        [-1.0, np.log(1.8), np.log(.8), np.log(1.6), .6, -0.3],
    ]
    unrestricted, start_rows = fit_multistart(price, quality, y, starts)
    if unrestricted is None:
        raise RuntimeError("No accepted unrestricted optimum")
    uobj, uz, usid, upg = unrestricted
    emz, emobj, empg, emtrace = em_fit(price, quality, y, starts[0])
    hz, hobj, hgrad, hres = homogeneous(price, quality, y)

    profile_rows, all_rows, holes = [], list(start_rows), []
    warm = uz[:5]
    for pidx, pv in enumerate(PGRID):
        pst = [warm, uz[:5]] + [np.asarray(s)[:5] for s in starts[:4]]
        best, rows = fit_multistart(price, quality, y, pst, fixed_pi=pv)
        all_rows.extend(rows)
        if best is None:
            holes.append(float(pv)); continue
        obj, z5, sid, pg = best
        warm = z5
        lr = 2*(obj-uobj)
        profile_rows.append({"pi_index": float(pv), "selected_start": int(sid),
                             "objective": float(obj), "lr_from_unrestricted": float(lr),
                             "in_grid_set": bool(lr <= LR_CUTOFF), "projected_gradient_max": float(pg),
                             "policy_adoption_effect": policy_effect(z5, price, quality, pv) if lr <= LR_CUTOFF else "",
                             "terminal": json.dumps(z5.tolist())})
    if holes:
        raise RuntimeError(f"Profile holes: {holes}")
    inset = [r for r in profile_rows if r["in_grid_set"]]
    vals = [r["pi_index"] for r in inset]
    left_censored = bool(vals and vals[0] == float(PGRID[0]))
    right_censored = bool(vals and vals[-1] == float(PGRID[-1]))
    a1,a2,b1,b2,g,upi = unpack(uz)
    summary = {
        "design": {"N":N,"T":T,"seed":SEED,"true":true,"policy_subsidy":0.45,
                   "baseline_price_support":[float(price.min()),float(price.max())],
                   "post_policy_price_support":[float((price-.45).min()),float((price-.45).max())],
                   "post_policy_share_below_observed_min":float(np.mean(price-.45 < price.min()))},
        "unrestricted": {"objective":uobj,"parameters":{"a1":a1,"a2":a2,"b1":b1,"b2":b2,"gamma":g,"pi":upi},
                           "selected_start":usid,"projected_gradient_max":upg,"policy_effect":policy_effect(uz,price,quality)},
        "em": {"objective":emobj,"parameters":unpack(emz),"projected_gradient_max":empg,"iterations":len(emtrace)},
        "homogeneous": {"objective":hobj,"parameters":hz.tolist(),"gradient_max":hgrad,"optimizer_success":bool(hres.success)},
        "comparison": {"lr_heterogeneity_vs_homogeneous":2*(hobj-uobj),"aic_mixture":2*6+2*uobj,"aic_homogeneous":2*3+2*hobj},
        "profile": {"grid":PGRID.tolist(),"cutoff":LR_CUTOFF,"holes":holes,"accepted_indices":len(profile_rows),
                    "in_set_count":len(inset),"in_set_values":vals,"left_endpoint_censored":left_censored,
                    "right_endpoint_censored":right_censored,"policy_effect_range_on_selected_in_set_solutions":
                    [min(r["policy_adoption_effect"] for r in inset),max(r["policy_adoption_effect"] for r in inset)]},
    }
    write_csv(ROOT/"starts_and_diagnostics.csv", all_rows)
    write_csv(ROOT/"profile.csv", profile_rows)
    write_csv(ROOT/"em_trace.csv", emtrace)
    (ROOT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    provenance={"instruction_source":{"repository":"C:/Users/ENAN/junzi-economist-skill","commit":"f120979",
                "files":["skills/junzi-economist/SKILL.md","skills/junzi-economist/references/EMPIRICAL_AND_STRUCTURAL_METHODS.md",
                         "skills/junzi-economist/references/THEORY_MODELING.md","skills/junzi-economist/references/SOFTWARE_AND_COMPUTATION.md"]},
                "python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"scipy":scipy.__version__,
                "script":"study.py","seed":SEED,"acceptance":{"projected_gradient_max":PG_TOL,"finite_objective":True},
                "profile_rule":"best accepted conditional objective per index; LR reference is accepted unrestricted optimum of same likelihood"}
    (ROOT/"provenance.json").write_text(json.dumps(provenance,indent=2),encoding="utf-8")


if __name__ == "__main__":
    main()
