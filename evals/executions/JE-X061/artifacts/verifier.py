from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parent
RAW = json.loads((ROOT / "raw_primitives.json").read_text(encoding="utf-8"))
SAVED = json.loads((ROOT / "production_output.json").read_text(encoding="utf-8"))
BETA = float(RAW["beta"])
BOUNDS = [tuple(x) for x in RAW["parameter_bounds"]]
H = float(RAW["numerics"]["gradient_step"])
KKT_TOL = float(RAW["numerics"]["accept_projected_gradient_tol"])
BELL_TOL = float(RAW["numerics"]["bellman_tol"])
CHECKS = []


def now():
    return datetime.now(timezone.utc)


def stamp(x):
    return x.isoformat().replace("+00:00", "Z")


def parse(x):
    return datetime.fromisoformat(x.replace("Z", "+00:00"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8")


def close(a, b, atol=1e-8, rtol=1e-8):
    return bool(np.allclose(np.asarray(a, float), np.asarray(b, float), atol=atol, rtol=rtol))


def require(name, condition, detail):
    passed = bool(condition)
    CHECKS.append({"check": name, "passed": passed, "detail": detail})
    if not passed:
        raise AssertionError(f"{name}: {detail}")


# Independent reconstruction: no import from production.py.
def rebuild_arrays():
    P = np.full((2, 2, 2), np.nan)
    counts = {}
    for cell in RAW["transition_cells"]:
        c = np.array(cell["next_state_counts"], dtype=float)
        P[int(cell["state"]), int(cell["action"]), :] = c / c.sum()
        counts[cell["key"]] = (c.astype(int).tolist(), int(c.sum()))
    phat = np.full((2, 2), np.nan); choice_counts = {}
    for cell in RAW["choice_cells"]:
        c = np.array(cell["action_counts"], dtype=float)
        phat[int(cell["state"]), :] = c / c.sum()
        choice_counts[cell["key"]] = (c.astype(int).tolist(), int(c.sum()))
    return P, phat, counts, choice_counts


P, PHAT, TRANS_COUNTS, CHOICE_COUNTS = rebuild_arrays()


def flow(theta, z=0.0):
    ans = np.zeros((2, 2), dtype=float)
    ans[0, 1] = theta[0] - z
    ans[1, 1] = theta[0] + theta[1] - z
    return ans


def fixed_point(theta, z=0.0):
    u = flow(theta, z); v = np.array([0.17, -0.11])
    for _ in range(20000):
        q = np.empty((2, 2))
        for s in range(2):
            for a in range(2):
                q[s, a] = u[s, a] + BETA * sum(P[s, a, k] * v[k] for k in range(2))
        vn = np.logaddexp(q[:, 0], q[:, 1])
        if max(abs(vn-v)) < BELL_TOL / 10:
            v = vn; break
        v = vn
    q = np.empty((2, 2))
    for s in range(2):
        for a in range(2):
            q[s, a] = u[s, a] + BETA * sum(P[s, a, k] * v[k] for k in range(2))
    pr = np.empty((2, 2))
    for s in range(2):
        den = np.logaddexp(q[s, 0], q[s, 1])
        pr[s, :] = np.exp(q[s, :] - den)
    resid = max(abs(v - np.logaddexp(q[:, 0], q[:, 1])))
    return v, pr, float(resid)


def ll_loss(theta):
    pr = fixed_point(theta)[1]
    val = 0.0
    for cell in RAW["choice_cells"]:
        s = int(cell["state"])
        for a in range(2):
            val -= int(cell["action_counts"][a]) * math.log(pr[s, a])
    return float(val)


def ccp_loss(theta):
    u = flow(theta)
    trans = np.zeros((2, 2)); payoff = np.zeros(2)
    for s in range(2):
        entropy = 0.0
        for a in range(2):
            trans[s] += PHAT[s, a] * P[s, a]
            payoff[s] += PHAT[s, a] * u[s, a]
            entropy -= PHAT[s, a] * math.log(PHAT[s, a])
        payoff[s] += entropy
    v = np.linalg.solve(np.eye(2) - BETA * trans, payoff)
    gaps = []
    for s in range(2):
        q0 = u[s, 0] + BETA * np.dot(P[s, 0], v)
        q1 = u[s, 1] + BETA * np.dot(P[s, 1], v)
        gaps.append(q1 - q0 - math.log(PHAT[s, 1] / PHAT[s, 0]))
    weights = [sum(c["action_counts"]) for c in RAW["choice_cells"]]
    return float(sum(weights[s] * gaps[s] ** 2 for s in range(2)))


def grad(fun, x):
    x = np.array(x, dtype=float); ans = np.zeros(2)
    for j in range(2):
        step = H * max(1.0, abs(x[j])); left = x.copy(); right = x.copy()
        left[j] = max(BOUNDS[j][0], x[j]-step); right[j] = min(BOUNDS[j][1], x[j]+step)
        ans[j] = (fun(right)-fun(left))/(right[j]-left[j])
    return ans


def project(x, g):
    ans = np.array(g, dtype=float)
    for j, (lo, hi) in enumerate(BOUNDS):
        if x[j] <= lo+1e-8 and g[j] >= 0: ans[j] = 0.0
        if x[j] >= hi-1e-8 and g[j] <= 0: ans[j] = 0.0
    return ans


def rerun_estimator(saved, fun):
    recomputed = []
    for expected_start, row in zip(RAW["starts"], saved["starts"]):
        x0 = np.array(expected_start["initial"], float)
        fit = minimize(fun, x0, method="L-BFGS-B", bounds=BOUNDS,
                       options={"ftol": 1e-13, "gtol": 1e-10, "maxiter": 2000, "maxls": 50})
        xnew = np.array(fit.x); anew = float(fun(xnew))
        xsaved = np.array(row["terminal"], float); osaved = float(fun(xsaved))
        g = grad(fun, xsaved); pg = project(xsaved, g)
        accepted = bool(math.isfinite(osaved) and max(abs(pg)) <= KKT_TOL)
        require(f"{saved['name']}:{row['start_key']}:start_identity", row["start_key"] == expected_start["start_key"] and close(row["initial"], x0, 0, 0), row["start_key"])
        require(f"{saved['name']}:{row['start_key']}:independent_resolve", close(xsaved, xnew, 3e-5, 3e-5) and math.isclose(row["objective"], anew, abs_tol=2e-8, rel_tol=2e-8), {"saved": row["terminal"], "rerun": xnew.tolist()})
        require(f"{saved['name']}:{row['start_key']}:objective", math.isclose(row["objective"], osaved, abs_tol=1e-9, rel_tol=1e-9), {"saved": row["objective"], "recomputed": osaved})
        require(f"{saved['name']}:{row['start_key']}:raw_projected_gradients", close(row["raw_gradient"], g, 2e-7, 2e-5) and close(row["projected_gradient"], pg, 2e-7, 2e-5), {"raw": g.tolist(), "projected": pg.tolist()})
        require(f"{saved['name']}:{row['start_key']}:acceptance", row["accepted"] is accepted and accepted and math.isclose(row["projected_gradient_max_abs"], max(abs(pg)), abs_tol=2e-7, rel_tol=2e-5), {"accepted": accepted, "pgmax": float(max(abs(pg)))})
        recomputed.append((row["start_key"], xsaved, osaved))
    best = min(recomputed, key=lambda z: z[2])
    require(f"{saved['name']}:selected_solution", saved["selected_start_key"] == best[0] and close(saved["parameters"], best[1], 3e-5, 3e-5) and math.isclose(saved["objective"], best[2], abs_tol=2e-8, rel_tol=2e-8), best[0])
    return best


def independent_policy(theta, z):
    v, pr, residual = fixed_point(theta, z)
    mu = np.array(RAW["initial_state_distribution"], float)
    T = np.zeros((2, 2))
    for s in range(2):
        for a in range(2): T[s] += pr[s, a] * P[s, a]
    d = np.linalg.solve((np.eye(2)-BETA*T).T, mu)
    occ = d[:, None]*pr; activity = occ[:,1].sum()
    parts = {
        "discounted_activity": float(activity),
        "action_intercept_component": float(theta[0]*activity),
        "state1_action_return_component": float(theta[1]*occ[1,1]),
        "policy_cost_component": float(z*activity),
        "entropy_component": float(sum(d[s]*(-sum(pr[s,a]*math.log(pr[s,a]) for a in range(2))) for s in range(2))),
    }
    parts["total_model_value"] = parts["action_intercept_component"]+parts["state1_action_return_component"]-parts["policy_cost_component"]+parts["entropy_component"]
    parts["initial_value_from_bellman"] = float(mu@v)
    parts["identity_residual"] = parts["total_model_value"]-parts["initial_value_from_bellman"]
    return v, pr[:,1], residual, parts


def run():
    verification_started = now()
    # Unique and complete row identities across every row-oriented object.
    expected_sets = {
        "raw_transition": ({x["key"] for x in RAW["transition_cells"]}, {f"s{s}_a{a}" for s in range(2) for a in range(2)}),
        "raw_choice": ({x["key"] for x in RAW["choice_cells"]}, {f"s{s}" for s in range(2)}),
        "production_transition": ({x["key"] for x in SAVED["transition_estimates"]}, {f"s{s}_a{a}" for s in range(2) for a in range(2)}),
        "production_ccp": ({x["key"] for x in SAVED["observed_ccp_estimates"]}, {f"s{s}" for s in range(2)}),
        "restricted": ({x["row_key"] for x in SAVED["restricted_grid_rows"]}, {f"grid_t0_{i:02d}_t1_{j:02d}" for i in range(3) for j in range(3)}),
        "policies": ({x["policy_key"] for x in SAVED["policy_records"]}, {f"policy_{int(round(100*z)):03d}" for z in RAW["policy_levels"]}),
    }
    cardinalities = {"raw_transition": len(RAW["transition_cells"]), "raw_choice": len(RAW["choice_cells"]),
                     "production_transition": len(SAVED["transition_estimates"]), "production_ccp": len(SAVED["observed_ccp_estimates"]),
                     "restricted": len(SAVED["restricted_grid_rows"]), "policies": len(SAVED["policy_records"])}
    unique_complete = all(got == exp and len(got) == cardinalities[k] for k,(got,exp) in expected_sets.items())
    for est in SAVED["estimators"].values():
        keys = [x["start_key"] for x in est["starts"]]
        unique_complete = unique_complete and keys == [x["start_key"] for x in RAW["starts"]] and len(keys)==len(set(keys))
    require("row_key_uniqueness_and_completeness", unique_complete, {k: sorted(v[0]) for k,v in expected_sets.items()})

    trans_ok = True
    for row in SAVED["transition_estimates"]:
        counts, total = TRANS_COUNTS[row["key"]]; probs = np.array(counts)/total
        trans_ok &= row["count_total"] == total and close(row["probabilities"], probs, 0, 0)
    require("every_transition_cell_count_and_estimate", trans_ok and len(TRANS_COUNTS)==4, TRANS_COUNTS)
    ccp_ok = True
    for row in SAVED["observed_ccp_estimates"]:
        counts, total = CHOICE_COUNTS[row["key"]]; probs = np.array(counts)/total
        ccp_ok &= row["count_total"] == total and close(row["probabilities"], probs, 0, 0)
    require("every_CCP_cell_count_and_estimate", ccp_ok and len(CHOICE_COUNTS)==2, CHOICE_COUNTS)

    nbest = rerun_estimator(SAVED["estimators"]["nfxp"], ll_loss)
    cbest = rerun_estimator(SAVED["estimators"]["ccp"], ccp_loss)
    require("both_estimators_objectives_and_parameters", close(SAVED["estimators"]["nfxp"]["parameters"], nbest[1], 3e-5, 3e-5) and close(SAVED["estimators"]["ccp"]["parameters"], cbest[1], 3e-5, 3e-5), {"nfxp": nbest[1].tolist(), "ccp": cbest[1].tolist()})
    require("every_start_raw_and_projected_gradient_and_acceptance", all(x["accepted"] for est in SAVED["estimators"].values() for x in est["starts"]), "Detailed per-start recomputations appear above")

    theta = np.array(SAVED["estimators"]["nfxp"]["parameters"])
    J = np.zeros((2,2))
    for j in range(2):
        step=1e-5*max(1,abs(theta[j])); lo=theta.copy(); hi=theta.copy(); lo[j]-=step; hi[j]+=step
        J[:,j]=(fixed_point(hi)[1][:,1]-fixed_point(lo)[1][:,1])/(2*step)
    singular = np.linalg.svd(J, compute_uv=False); rank=int(sum(singular>float(SAVED["local_rank_diagnostic"]["rank_threshold"])))
    lr=SAVED["local_rank_diagnostic"]
    require("saved_local_rank_singular_values", close(lr["jacobian"],J,2e-8,2e-7) and close(lr["singular_values"],singular,2e-8,2e-7) and lr["local_numerical_rank"]==rank and lr["claim_scope"]=="local numerical rank only; no global or population identification claim", {"singular_values": singular.tolist(), "rank":rank})

    grid=RAW["restricted_grid"]; rows={x["row_key"]:x for x in SAVED["restricted_grid_rows"]}; grid_ok=True; feasible=[]
    for i,t0 in enumerate(grid["theta0_values"]):
        for j,t1 in enumerate(grid["theta1_values"]):
            key=f"grid_t0_{i:02d}_t1_{j:02d}"; r=rows[key]; slack=t1-t0-0.5; feas=slack>=-grid["feasibility_tol"]; obj=ll_loss([t0,t1])
            grid_ok &= r["domain_label"]==grid["domain_label"] and r["theta0"]==t0 and r["theta1"]==t1
            grid_ok &= r["theta0_lower_boundary"]==(i==0) and r["theta0_upper_boundary"]==(i==len(grid["theta0_values"])-1)
            grid_ok &= r["theta1_lower_boundary"]==(j==0) and r["theta1_upper_boundary"]==(j==len(grid["theta1_values"])-1)
            grid_ok &= r["restriction_slack"]==slack and r["feasible"] is feas and math.isclose(r["nfxp_objective"],obj,abs_tol=1e-9,rel_tol=1e-9)
            if feas: feasible.append((key,obj))
    require("every_restricted_row_key_domain_label_boundary_slack_feasibility_and_objective", grid_ok and SAVED["restricted_grid_selected_key"]==min(feasible,key=lambda x:x[1])[0], {"rows":len(rows),"selected":min(feasible,key=lambda x:x[1])[0]})

    saved_policies={r["level"]:r for r in SAVED["policy_records"]}; policy_ok=set(saved_policies)==set(RAW["policy_levels"])
    independent=[]
    for z in RAW["policy_levels"]:
        r=saved_policies[z]; v,p,resid,acct=independent_policy(theta,z); independent.append((z,p))
        expected_label="observed_regime" if z in RAW["observed_policy_levels"] else "interior_model_interpolation"
        policy_ok &= r["support_label"]==expected_label and r["is_midpoint"] is (z==0.5)
        policy_ok &= close(r["choice1_probabilities"],p,2e-9,2e-9) and close(r["value_vector"],v,2e-9,2e-9)
        policy_ok &= math.isclose(r["bellman_residual_max_abs"],resid,abs_tol=2e-11,rel_tol=2e-3)
        policy_ok &= all(math.isclose(r["accounting"][k],acct[k],abs_tol=3e-9,rel_tol=3e-9) for k in acct)
        policy_ok &= abs(acct["identity_residual"])<2e-9
    mono=all(independent[k+1][1][s]<=independent[k][1][s]+1e-12 for k in range(len(independent)-1) for s in range(2))
    policy_ok &= SAVED["policy_choice1_monotone_nonincreasing"] is mono and mono
    require("exact_saved_policy_set_support_labels_and_arbitrary_interior_policies", policy_ok, {"levels":RAW["policy_levels"],"observed":RAW["observed_policy_levels"]})
    require("off_regime_midpoint_levels_vectors_Bellman_residuals_monotonic_sanity_and_separate_accounting", policy_ok and all(saved_policies[z]["support_label"]=="interior_model_interpolation" for z in [0.25,0.5,0.75]), {"midpoint":saved_policies[0.5],"monotone":mono})

    expected_headlines={
        "nfxp_parameters":SAVED["estimators"]["nfxp"]["parameters"], "nfxp_objective":SAVED["estimators"]["nfxp"]["objective"],
        "ccp_parameters":SAVED["estimators"]["ccp"]["parameters"], "ccp_objective":SAVED["estimators"]["ccp"]["objective"],
        "transition_cell_count":len(TRANS_COUNTS), "choice_cell_count":len(CHOICE_COUNTS),
        "accepted_start_count_each":len(RAW["starts"]), "restricted_row_count":len(rows),
        "policy_record_count":len(saved_policies), "local_numerical_rank":rank, "monotonic_policy_sanity":mono}
    headline_ok=set(SAVED["headlines"])==set(expected_headlines)
    for k,v in expected_headlines.items():
        if isinstance(v,list): headline_ok &= close(SAVED["headlines"][k],v,0,0)
        elif isinstance(v,float): headline_ok &= math.isclose(SAVED["headlines"][k],v,abs_tol=0,rel_tol=0)
        else: headline_ok &= SAVED["headlines"][k]==v
    require("all_headline_values",headline_ok,expected_headlines)

    start=parse(SAVED["chronology"]["production_started_utc"]); finish=parse(SAVED["chronology"]["production_finished_utc"])
    prod_m=datetime.fromtimestamp((ROOT/"production.py").stat().st_mtime,timezone.utc)
    raw_m=datetime.fromtimestamp((ROOT/"raw_primitives.json").stat().st_mtime,timezone.utc)
    out_m=datetime.fromtimestamp((ROOT/"production_output.json").stat().st_mtime,timezone.utc)
    ver_m=datetime.fromtimestamp((ROOT/"verifier.py").stat().st_mtime,timezone.utc)
    chronology_ok=prod_m<=start<=raw_m<=finish<=out_m<=ver_m<=verification_started
    hashes_ok=SAVED["production_source_sha256"]==digest(ROOT/"production.py") and SAVED["raw_primitives_sha256"]==digest(ROOT/"raw_primitives.json")
    require("production_hashes_and_chronology",hashes_ok and chronology_ok,{"hashes_ok":hashes_ok,"source":stamp(prod_m),"start":stamp(start),"raw":stamp(raw_m),"finish":stamp(finish),"output":stamp(out_m),"verifier":stamp(ver_m),"verification_start":stamp(verification_started)})

    coverage=[
        "row-key uniqueness/completeness",
        "every transition and CCP cell/count",
        "both estimators/objectives/parameters",
        "raw and projected gradients plus acceptance for every start",
        "saved singular values and local-rank label only",
        "every restricted row/key/domain label/boundary/slack/feasible flag/objective",
        "exact saved policy set and support labels",
        "arbitrary off-regime policies including midpoint levels/vectors/Bellman residuals/monotonic sanity/separate accounting",
        "all headline values",
        "production hashes/chronology",
    ]
    finished=now()
    report={"schema":"dynamic-ddc-independent-verification-v1","verifier_source_sha256":digest(ROOT/"verifier.py"),
            "verification_started_utc":stamp(verification_started),"verification_finished_utc":stamp(finished),
            "passed":all(c["passed"] for c in CHECKS),"coverage_map":coverage,
            "coverage_limit":"Only the checks listed in coverage_map are claimed; no global identification, continuous-grid, external-validity, or welfare claim is verified.",
            "checks":CHECKS}
    save(ROOT/"verification.json",report)
    manifest_files=["README.md","production.py","raw_primitives.json","production_output.json","verifier.py","verification.json"]
    manifest={"schema":"dynamic-ddc-final-manifest-v1","created_utc":stamp(now()),
              "verifier_authored_after_production":ver_m>=out_m,
              "verifier_self_sha256":digest(ROOT/"verifier.py"),
              "files":{name:{"sha256":digest(ROOT/name),"bytes":(ROOT/name).stat().st_size} for name in manifest_files}}
    save(ROOT/"final_manifest.json",manifest)
    print(json.dumps({"passed":report["passed"],"checks":len(CHECKS),"manifest_files":len(manifest_files)},sort_keys=True))


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        failure={"schema":"dynamic-ddc-independent-verification-v1","passed":False,"error":repr(exc),"checks":CHECKS}
        save(ROOT/"verification.json",failure)
        print(repr(exc),file=sys.stderr)
        sys.exit(1)
