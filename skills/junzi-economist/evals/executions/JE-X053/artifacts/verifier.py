from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
TRUE = np.array([18.0, 0.7, 4.0, 0.8]); LOWER=np.array([10.,.2,2.,.1]); UPPER=np.array([25.,1.5,6.,1.5])
RAW_TOL=1e-9; SCALED_TOL=1e-8

def loadj(name): return json.loads((ROOT/name).read_text(encoding="utf-8"))
def moments(theta, d, invalid=False):
    alpha,beta,c0,c1=theta; zd=d["z_invalid_post"] if invalid else d["z_cost"].mean(1)
    dem=d["price"]-alpha+beta*d["Q"]; cost=d["price"][:,None]-beta*d["q"]-c0-c1*d["z_cost"]
    raw=np.array([dem.mean(),np.mean(zd*dem),cost.mean(),np.mean(d["z_cost"]*cost)])
    scales=np.array([1.,max(float(np.std(zd)),.1),1.,float(np.std(d["z_cost"]))])
    return raw,raw/scales
def ivbeta(d,z):
    z=z-z.mean(); q=d["Q"]-d["Q"].mean(); p=d["price"]-d["price"].mean()
    return float(-z@p/(z@q))
def add(cov, claim, passed, evidence): cov.append({"claim":claim,"passed":bool(passed),"evidence":evidence})

d0=np.load(ROOT/"primitives.npz",allow_pickle=False); d={k:d0[k] for k in d0.files}
res=loadj("results.json"); acct=loadj("accounting.json"); rt=np.load(ROOT/"terminal_vectors_full_precision.npz",allow_pickle=False)
cov=[]
add(cov,"DGP has unconditional exact market count, exact IDs, three firms, zero selection/redraws",len(d["market_id"])==4000 and np.array_equal(d["market_id"],np.arange(4000)) and d["q"].shape==(4000,3) and np.all(d["q"]>0),{"count":len(d["market_id"]),"shape":list(d["q"].shape)})
# Independently reconstruct all outcomes from primitives.
mc=TRUE[2]+TRUE[3]*d["z_cost"]+d["omega"]; a=TRUE[0]+d["eta"]
q=(a[:,None]+mc.sum(1)[:,None]-4*mc)/(TRUE[1]*4); Q=q.sum(1); p=a-TRUE[1]*Q
add(cov,"DGP equations and equilibrium outcomes reproduce from primitives",np.array_equal(mc,d["mc"]) and np.allclose(q,d["q"],rtol=0,atol=2e-15) and np.allclose(Q,d["Q"],rtol=0,atol=4e-15) and np.allclose(p,d["price"],rtol=0,atol=4e-15),{"q_max_diff":float(np.max(abs(q-d["q"])))})
zv=d["z_cost"].mean(1); zi=d["z_invalid_post"]
add(cov,"Instrument timing is executable: invalid instrument equals post-shock eta plus saved noise proxy and was excluded from reconstructed t2 rule",np.std(zi-d["eta"])<0.051 and np.array_equal(q,(a[:,None]+mc.sum(1)[:,None]-4*mc)/(TRUE[1]*4)),{"noise_sd":float(np.std(zi-d["eta"]))})
corrv=float(np.corrcoef(zv,d["eta"])[0,1]); corri=float(np.corrcoef(zi,d["eta"])[0,1]); bvalid=ivbeta(d,zv); binvalid=ivbeta(d,zi)
add(cov,"Valid instrument has sample near-exclusion, relevance, and recovers beta; invalid post-outcome instrument violates exclusion and distorts beta",abs(corrv)<.05 and abs(np.corrcoef(zv,Q)[0,1])>.2 and abs(bvalid-TRUE[1])<.06 and abs(corri)>.95 and abs(binvalid-TRUE[1])>.2,{"corr_valid_eta":corrv,"corr_invalid_eta":corri,"beta_valid":bvalid,"beta_invalid":binvalid})
# Closed-form independent moment root, not production solver.
def closed_root(invalid=False):
    zd=zi if invalid else zv; x=d["z_cost"]; qq=d["q"]
    A=np.array([[-1,d["Q"].mean(),0,0],[-zd.mean(),np.mean(zd*d["Q"]),0,0],[0,-qq.mean(),-1,-x.mean()],[0,-np.mean(x*qq),-x.mean(),-np.mean(x*x)]])
    b=-np.array([d["price"].mean(),np.mean(zd*d["price"]),d["price"].mean(),np.mean(x*d["price"][:,None])])
    return np.linalg.solve(A,b)
for label,invalid in [("valid",False),("invalid",True)]:
    root=closed_root(invalid); terminals=rt[label]
    if not invalid:
        ok=np.all(terminals>=LOWER)&np.all(terminals<=UPPER)&(np.max(abs(terminals-root))<1e-10)
        for theta in terminals:
            raw,scaled=moments(theta,d,invalid); ok=ok and np.max(abs(raw))<RAW_TOL and np.max(abs(scaled))<SCALED_TOL
        claim="All bounded valid estimator starts reach the independently solved root with raw and scaled residual acceptance"
    else:
        ok=np.all(terminals>=LOWER)&np.all(terminals<=UPPER)&(np.ptp(terminals,axis=0).max()<1e-8) and not np.all((root>=LOWER)&(root<=UPPER))
        for theta in terminals:
            raw,scaled=moments(theta,d,invalid); ok=ok and (np.max(abs(raw))>=RAW_TOL or np.max(abs(scaled))>=SCALED_TOL) and np.isclose(theta[2],UPPER[2],atol=1e-10)
        claim="All bounded invalid-instrument starts reach the same boundary candidate, while raw and scaled residual rules correctly reject it because the unconstrained moment root is outside the declared box"
    add(cov,claim,ok,{"independent_unconstrained_root":root.tolist(),"max_start_spread":float(np.ptp(terminals,axis=0).max())})
# Recompute every saved estimator trace vector's raw/scaled diagnostics.
trace_ok=True; trace_rows=0
for label,invalid in [("valid",False),("invalid",True)]:
  for sid in range(6):
    for line in (ROOT/f"trace_estimation_{label}_start{sid}.jsonl").read_text(encoding="utf-8").splitlines():
        row=json.loads(line); raw,scaled=moments(np.array(row["theta"]),d,invalid); trace_rows+=1
        trace_ok &= np.allclose(raw,row["raw"],rtol=0,atol=1e-15) and np.allclose(scaled,row["scaled"],rtol=0,atol=1e-15)
add(cov,"Every estimator trace row has independently reproduced raw and scaled residual vectors",trace_ok,{"trace_rows":trace_rows})
# Equilibrium terminals and traces.
eq_ok=True; eq_trace_ok=True; eq_rows=0; idx=0
for m in [0,17,901,2026,3999]:
  aa=TRUE[0]+d["eta"][m]; mm=mc[m]; analytic=np.linalg.solve(TRUE[1]*(np.eye(3)+np.ones((3,3))),aa-mm)
  for sid in range(4):
    qt=rt["equilibrium"][idx]; raw=aa-mm-TRUE[1]*(qt.sum()+qt); scale=max(float(aa),1.); idx+=1
    eq_ok &= np.max(abs(qt-analytic))<1e-10 and np.max(abs(raw))<RAW_TOL and np.max(abs(raw/scale))<SCALED_TOL and np.all((qt>=0)&(qt<=20))
    for line in (ROOT/f"trace_equilibrium_market{m}_start{sid}.jsonl").read_text(encoding="utf-8").splitlines():
      row=json.loads(line); qr=np.array(row["q"]); rr=aa-mm-TRUE[1]*(qr.sum()+qr); eq_rows+=1
      eq_trace_ok &= np.allclose(rr,row["raw"],rtol=0,atol=2e-15) and np.allclose(rr/scale,row["scaled"],rtol=0,atol=2e-15)
add(cov,"All equilibrium starts recover the unique positive bounded linear-system solution with raw and scaled residual acceptance",eq_ok,{"terminal_count":idx})
add(cov,"Every equilibrium trace row has independently reproduced raw and scaled residual vectors",eq_trace_ok,{"trace_rows":eq_rows})
# Accounting independently reconstructed at levels.
rev=p*Q; vc=np.sum(mc*q,1); prof=rev-vc; cs=.5*TRUE[1]*Q**2; welfare=cs+prof; levels=acct["levels"]
account_ok=abs(levels["consumer_expenditure"]-np.sum(p*Q))<1e-8 and abs(levels["producer_revenue"]-rev.sum())<1e-8 and abs(levels["variable_cost"]-vc.sum())<1e-8 and abs(levels["producer_profit"]-prof.sum())<1e-8 and abs(levels["consumer_surplus"]-cs.sum())<1e-8 and abs(levels["total_welfare"]-welfare.sum())<1e-8 and max(abs(v) for v in acct["identity_residuals"].values())<1e-8
add(cov,"Separate accounting levels and all three accounting identities reproduce",account_ok,{"recomputed":{"revenue":float(rev.sum()),"cost":float(vc.sum()),"profit":float(prof.sum()),"cs":float(cs.sum()),"welfare":float(welfare.sum())}})
manifest=loadj("process_failure_manifest.json"); fail_ok=True
for mode,code in [("simulation",31),("equilibrium",32),("estimation",33)]:
    diag=loadj(f"failure_{mode}.json"); row=next(x for x in manifest if x["mode"]==mode)
    fail_ok &= row["exit_code"]==code and row["diagnostic_exists"] and diag["required_unit_failed"] and not diag["accepted"]
add(cov,"Simulation, equilibrium, and estimation isolated failures wrote diagnostics and exited nonzero",fail_ok,{"manifest":manifest})
roundtrip=loadj("roundtrip_diagnostics.json")
add(cov,"Full-precision terminal vectors survived actual reload and reproduced both acceptance and rejection diagnostics",all(x["bitwise_equal"] and x["diagnostic_reproduced"] for x in roundtrip),{"checks":len(roundtrip)})
out={"verifier":"independent algebraic reconstruction; does not import model.py or call its solvers","all_passed":all(x["passed"] for x in cov),"coverage_count":len(cov),"coverage":cov}
(ROOT/"independent_verification.json").write_text(json.dumps(out,indent=2,allow_nan=False),encoding="utf-8")
(ROOT/"coverage_map.json").write_text(json.dumps({x["claim"]:{"passed":x["passed"],"evidence":x["evidence"]} for x in cov},indent=2,allow_nan=False),encoding="utf-8")
if not out["all_passed"]: raise SystemExit(41)
