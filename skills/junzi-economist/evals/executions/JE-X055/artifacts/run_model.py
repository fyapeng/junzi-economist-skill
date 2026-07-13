import csv
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize, root


ROOT = Path(__file__).resolve().parent
SEED = 55055
BETA = 0.93
STATES = np.arange(5, dtype=float)
REGIMES = np.array([0.0, 0.4])
TRUE = np.array([0.42, 2.15, 0.72, 0.86])  # cost slope, replacement cost, P(increment|keep), P(reset|replace)
BOUNDS = np.array([[0.05, 1.50], [0.20, 5.00], [0.0, 1.0], [0.0, 1.0]])
ALT_DELTA = 0.15
FEAS_TOL = 1e-10
OPT_TOL = 1e-10


def trans_mats(pm, pr):
    pk = np.zeros((5, 5))
    for x in range(5):
        if x == 4:
            pk[x, x] = 1.0
        else:
            pk[x, x] = 1.0 - pm
            pk[x, x + 1] = pm
    rr = np.zeros((5, 5))
    rr[:, 0] = pr
    rr[:, 1] = 1.0 - pr
    return pk, rr


def solve_dp(theta, subsidy, tol=1e-12, maxit=10000):
    c, r, pm, pr = theta
    pk, rr = trans_mats(pm, pr)
    def residual(ev):
        v0 = -c * STATES + BETA * pk.dot(ev)
        v1 = -(r - subsidy) + BETA * rr.dot(ev)
        return ev - np.logaddexp(v0, v1)
    sol = root(residual, np.zeros(5), method='hybr', options={'xtol':tol, 'maxfev':300})
    ev = sol.x
    if (not sol.success) or np.max(np.abs(residual(ev))) > 2e-9:
        ev = np.zeros(5)
        for it in range(maxit):
            v0 = -c * STATES + BETA * pk.dot(ev)
            v1 = -(r - subsidy) + BETA * rr.dot(ev)
            new = np.logaddexp(v0, v1)
            if np.max(np.abs(new - ev)) < tol:
                ev = new
                break
            ev = new
        else:
            raise RuntimeError('Bellman iteration failed')
        nit = it + 1
    else:
        nit = int(sol.nfev)
    v0 = -c * STATES + BETA * pk.dot(ev)
    v1 = -(r - subsidy) + BETA * rr.dot(ev)
    p1 = 1.0 / (1.0 + np.exp(np.clip(v0 - v1, -700, 700)))
    resid = np.max(np.abs(ev - np.logaddexp(v0, v1)))
    return p1, ev, resid, nit


def simulate():
    rng = np.random.default_rng(SEED)
    rows = []
    n_agents, periods = 450, 35
    policy = {float(s): solve_dp(TRUE, float(s))[0] for s in REGIMES}
    for i in range(n_agents):
        regime = float(REGIMES[i % 2])
        x = int(rng.integers(0, 5))
        for t in range(periods):
            p = policy[regime]
            a = int(rng.random() < p[x])
            if a == 0:
                xp = x if x == 4 or rng.random() >= TRUE[2] else x + 1
            else:
                xp = 0 if rng.random() < TRUE[3] else 1
            rows.append((i, t, regime, x, a, xp))
            x = xp
    return np.asarray(rows, dtype=float)


def estimate_transitions(data):
    keep = data[:, 4] == 0
    repl = ~keep
    elig = keep & (data[:, 3] < 4)
    pm = np.mean(data[elig, 5] == data[elig, 3] + 1)
    pr = np.mean(data[repl, 5] == 0)
    return float(pm), float(pr), int(elig.sum()), int(repl.sum())


def choice_nll(pref, data, pm, pr):
    theta = np.array([pref[0], pref[1], pm, pr])
    total = 0.0
    for s in REGIMES:
        mask = data[:, 2] == s
        x = data[mask, 3].astype(int)
        a = data[mask, 4]
        p, _, _, _ = solve_dp(theta, s)
        pa = np.where(a == 1, p[x], 1 - p[x])
        total -= np.log(np.maximum(pa, 1e-14)).sum()
    return float(total)


def projected_grad(fun, x, bounds, h=1e-5):
    g = np.zeros_like(x)
    for j in range(len(x)):
        step = h * max(1.0, abs(x[j]))
        lo, hi = bounds[j]
        if x[j] - step >= lo and x[j] + step <= hi:
            xp, xm = x.copy(), x.copy(); xp[j] += step; xm[j] -= step
            g[j] = (fun(xp) - fun(xm)) / (2 * step)
        elif x[j] + step <= hi:
            xp = x.copy(); xp[j] += step
            g[j] = (fun(xp) - fun(x)) / step
        else:
            xm = x.copy(); xm[j] -= step
            g[j] = (fun(x) - fun(xm)) / step
    pg = g.copy()
    for j, (lo, hi) in enumerate(bounds):
        if x[j] <= lo + FEAS_TOL and g[j] > 0: pg[j] = 0
        if x[j] >= hi - FEAS_TOL and g[j] < 0: pg[j] = 0
    return g, pg


def empirical_ccp(data):
    counts = np.zeros((2, 5, 2), dtype=int)
    for row in data:
        g = int(row[2] > 0)
        counts[g, int(row[3]), int(row[4])] += 1
    # Jeffreys smoothing is declared and retained; all cells have support.
    p = (counts[:, :, 1] + 0.5) / (counts.sum(axis=2) + 1.0)
    return p, counts


def ccp_md_objective(pref, p_emp, counts, pm, pr):
    c, r = pref
    pk, rr = trans_mats(pm, pr)
    val = 0.0
    for g, s in enumerate(REGIMES):
        p = p_emp[g]
        u0 = -c * STATES
        u1 = -(r - s) * np.ones(5)
        pp = (1-p)[:,None] * pk + p[:,None] * rr
        flow = (1-p)*u0 + p*u1 - (1-p)*np.log(1-p) - p*np.log(p)
        ev = np.linalg.solve(np.eye(5)-BETA*pp, flow)
        implied_log_odds = (u1-u0) + BETA*(rr-pk).dot(ev)
        w = counts[g].sum(axis=1)
        val += np.sum(w * (np.log(p / (1-p)) - implied_log_odds) ** 2)
    return float(val / counts.sum())


def observable_map(theta):
    vals = []
    for s in REGIMES:
        p, _, _, _ = solve_dp(theta, s)
        vals.extend(p.tolist())
    vals.extend(theta[2:].tolist())
    return np.asarray(vals)


def jacobian(theta):
    base = observable_map(theta)
    J = np.zeros((base.size, 4))
    for j in range(4):
        h = 2e-5 * max(1.0, abs(theta[j]))
        up, dn = theta.copy(), theta.copy()
        up[j] += h; dn[j] -= h
        J[:, j] = (observable_map(up) - observable_map(dn)) / (2 * h)
    return J


def alt_distance(theta, target):
    d = observable_map(theta) - observable_map(target)
    return float(d @ d)


def write_csv(path, header, rows):
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def main():
    data = simulate()
    write_csv(ROOT / 'simulated_panel.csv', ['agent','period','subsidy','state','action','next_state'], data.astype(object))
    pm, pr, nk, nr = estimate_transitions(data)

    starts = np.array([[0.08,0.3],[0.2,1.0],[0.4,2.0],[0.8,3.0],[1.45,4.8],[1.2,1.0],[0.1,4.5],[0.7,2.3]])
    nfxp_trace = []
    f = lambda z: choice_nll(z, data, pm, pr)
    for k, st in enumerate(starts):
        res = minimize(f, st, method='L-BFGS-B', bounds=BOUNDS[:2].tolist(), options={'ftol':OPT_TOL,'gtol':1e-8,'maxiter':1000,'maxls':50})
        raw, proj = projected_grad(f, res.x, BOUNDS[:2])
        nfxp_trace.append({'start_id':k,'start':st.tolist(),'terminal':res.x.tolist(),'objective':float(res.fun),'success':bool(res.success),'message':str(res.message),'nit':int(res.nit),'raw_grad':raw.tolist(),'projected_grad':proj.tolist(),'projected_grad_inf':float(np.max(np.abs(proj)))})
    accepted = [r for r in nfxp_trace if r['success'] and r['projected_grad_inf'] < 2e-3]
    best = min(accepted, key=lambda r:r['objective'])
    for r in nfxp_trace: r['objective_gap'] = r['objective'] - best['objective']
    theta_hat = np.array(best['terminal'] + [pm, pr])

    p_emp, counts = empirical_ccp(data)
    ccp_trace = []
    fccp = lambda z: ccp_md_objective(z, p_emp, counts, pm, pr)
    for k, st in enumerate(starts):
        res = minimize(fccp, st, method='L-BFGS-B', bounds=BOUNDS[:2].tolist(), options={'ftol':OPT_TOL,'gtol':1e-9,'maxiter':1000})
        raw, proj = projected_grad(fccp, res.x, BOUNDS[:2])
        ccp_trace.append({'start_id':k,'start':st.tolist(),'terminal':res.x.tolist(),'objective':float(res.fun),'success':bool(res.success),'message':str(res.message),'nit':int(res.nit),'raw_grad':raw.tolist(),'projected_grad':proj.tolist(),'projected_grad_inf':float(np.max(np.abs(proj)))})
    ccp_ok = [r for r in ccp_trace if r['success'] and r['projected_grad_inf'] < 2e-3]
    ccp_best = min(ccp_ok, key=lambda r:r['objective'])
    for r in ccp_trace: r['objective_gap'] = r['objective'] - ccp_best['objective']

    J = jacobian(theta_hat)
    sing = np.linalg.svd(J, compute_uv=False)

    # Exact coverage of the closed restricted set: union over 8 closed slabs,
    # theta_j <= hat_j-delta or theta_j >= hat_j+delta, intersected with BOUNDS.
    alt_trace = []
    alt_starts = [TRUE, np.mean(BOUNDS,axis=1), BOUNDS[:,0], BOUNDS[:,1], theta_hat]
    rng = np.random.default_rng(7811)
    alt_starts += [BOUNDS[:,0] + rng.random(4)*(BOUNDS[:,1]-BOUNDS[:,0]) for _ in range(16)]
    slab_id = 0
    for j in range(4):
        for side in ('lower','upper'):
            b = BOUNDS.copy()
            if side == 'lower': b[j,1] = min(b[j,1], theta_hat[j]-ALT_DELTA)
            else: b[j,0] = max(b[j,0], theta_hat[j]+ALT_DELTA)
            if b[j,0] > b[j,1]:
                continue
            for rerun_seed in [991, 992]:
                local_rng = np.random.default_rng(rerun_seed + slab_id)
                run_starts = alt_starts + [b[:,0] + local_rng.random(4)*(b[:,1]-b[:,0]) for _ in range(6)]
                for k, st0 in enumerate(run_starts):
                    st = np.clip(st0, b[:,0], b[:,1])
                    res = minimize(lambda z: alt_distance(z,theta_hat), st, method='L-BFGS-B', bounds=b.tolist(), options={'ftol':1e-15,'gtol':1e-11,'maxiter':2000,'maxls':50})
                    raw, proj = projected_grad(lambda z: alt_distance(z,theta_hat), res.x, b)
                    restriction = np.max(np.abs(res.x-theta_hat)) - ALT_DELTA
                    alt_trace.append({'slab_id':slab_id,'dimension':j,'side':side,'rerun_seed':rerun_seed,'start_id':k,'slab_bounds':b.tolist(),'start':st.tolist(),'terminal':res.x.tolist(),'objective':float(res.fun),'success':bool(res.success),'message':str(res.message),'nit':int(res.nit),'raw_grad':raw.tolist(),'projected_grad_inf':float(np.max(np.abs(proj))),'restriction_slack':float(restriction),'box_slack':float(np.min(np.r_[res.x-BOUNDS[:,0],BOUNDS[:,1]-res.x]))})
            slab_id += 1
    alt_ok = [r for r in alt_trace if r['success'] and r['projected_grad_inf'] < 2e-6 and r['restriction_slack'] >= -FEAS_TOL and r['box_slack'] >= -FEAS_TOL]
    alt_best = min(alt_ok, key=lambda r:r['objective'])

    policies = []
    # 0 and .4 are observed regimes; .2 is model interpolation only.
    for s, support in [(0.0,'observed'),(0.2,'model interpolation'),(0.4,'observed')]:
        p, ev, br, it = solve_dp(theta_hat,s)
        pk, rr = trans_mats(pm,pr)
        P = (1-p)[:,None]*pk + p[:,None]*rr
        A = np.vstack([P.T-np.eye(5), np.ones(5)])
        bvec = np.r_[np.zeros(5),1.0]
        dist = np.linalg.lstsq(A,bvec,rcond=None)[0]
        repl_rate = float(dist@p)
        private_flow = float(dist @ ((1-p)*(-theta_hat[0]*STATES) + p*(-theta_hat[1]+s)))
        transfers = float(s*repl_rate)
        resource_flow = float(dist @ ((1-p)*(theta_hat[0]*STATES) + p*theta_hat[1]))
        social_welfare = -resource_flow/(1-BETA)
        private_value = private_flow/(1-BETA)
        fiscal_outlay = transfers/(1-BETA)
        policies.append({'subsidy':s,'support':support,'replacement_rate':repl_rate,'private_value':private_value,'fiscal_transfer':fiscal_outlay,'real_resource_cost':resource_flow/(1-BETA),'social_welfare_private_plus_transfer_cancellation':social_welfare,'bellman_residual':br,'stationary_residual':float(np.max(np.abs(dist@P-dist))),'iterations':it})

    summary = {
      'model':{'states':[0,1,2,3,4],'actions':{'0':'keep','1':'replace'},'timing':'observe state and subsidy; choose; controlled transition; iid type-I EV shocks integrated out','discount_factor_fixed':BETA,'utility':{'keep':'-cost_slope*state','replace':'-replacement_cost+subsidy'},'observed_policy_regimes':REGIMES.tolist(),'interpolation_policy':[0.2],'shock_normalization':'Euler constant omitted from integrated value; policy differences unaffected'},
      'sample':{'seed':SEED,'agents':450,'periods':35,'rows':int(data.shape[0]),'selection':'none; all simulated histories retained'},
      'true_parameters':TRUE.tolist(),
      'declared_closed_domain':{'names':['cost_slope','replacement_cost','p_increment_keep','p_reset_replace'],'bounds':BOUNDS.tolist(),'boundaries_included':True,'discount_factor':BETA},
      'transition_estimates':{'p_increment_keep':pm,'p_reset_replace':pr,'eligible_keep_transitions':nk,'replacement_transitions':nr},
      'nfxp':{'estimate':theta_hat.tolist(),'choice_nll':best['objective'],'selected_start_id':best['start_id'],'accepted_starts':len(accepted),'total_starts':len(nfxp_trace),'max_bellman_residual':max(solve_dp(theta_hat,s)[2] for s in REGIMES),'domain_slack':np.minimum(theta_hat-BOUNDS[:,0],BOUNDS[:,1]-theta_hat).tolist()},
      'ccp_minimum_distance':{'estimate':ccp_best['terminal']+[pm,pr],'objective':ccp_best['objective'],'selected_start_id':ccp_best['start_id'],'accepted_starts':len(ccp_ok),'total_starts':len(ccp_trace),'method':'two-step CCP inversion: empirical CCP policy valuation and log-odds minimum distance; no Bellman solve inside estimator','smoothing':'Jeffreys 0.5 pseudo-count in each binary choice cell'},
      'population_local_rank_evidence':{'mapping':'10 model CCPs across two observed regimes plus two controlled-transition probabilities','jacobian_shape':list(J.shape),'singular_values':sing.tolist(),'rank_tolerance':1e-7,'numerical_rank':int(np.sum(sing>1e-7)),'claim':'continuous local population-rank evidence at the NFXP estimate under fixed beta and maintained model; not global identification'},
      'restricted_alternative_search':{'restriction':f'closed box and max_j |theta_j-theta_hat_j| >= {ALT_DELTA}','coverage':'exact finite union of all nonempty lower/upper closed slabs for each parameter; direct bounded coordinates include economic boundaries','feasibility_tolerance':FEAS_TOL,'optimizer_projected_gradient_acceptance':2e-6,'evaluations':len(alt_trace),'accepted':len(alt_ok),'selected':alt_best,'interpretation':'auditable continuous-domain search; failure to find a closer alternative is not a proof of global identification'},
      'policy_accounting':policies,
      'software':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()}
    }
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    (ROOT/'nfxp_starts.json').write_text(json.dumps(nfxp_trace,indent=2),encoding='utf-8')
    (ROOT/'ccp_starts.json').write_text(json.dumps(ccp_trace,indent=2),encoding='utf-8')
    write_csv(ROOT/'alternative_search.csv', list(alt_trace[0].keys()), [[json.dumps(r[k]) if isinstance(r[k],list) else r[k] for k in alt_trace[0].keys()] for r in alt_trace])
    np.savez_compressed(ROOT/'compact_arrays.npz', counts=counts, empirical_ccp=p_emp, jacobian=J, singular_values=sing)
    print(json.dumps({'nfxp':theta_hat.tolist(),'ccp':ccp_best['terminal']+[pm,pr],'singular_values':sing.tolist(),'alt_objective':alt_best['objective'],'alt_slack':alt_best['restriction_slack'],'rows':len(data)},indent=2))


if __name__ == '__main__':
    main()
