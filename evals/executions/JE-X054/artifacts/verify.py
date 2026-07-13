import csv, json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

R=Path(__file__).resolve().parent
data=np.load(R/"simulated_data.npz")
p,q,y=data["price"],data["quality"],data["y"]
S=json.loads((R/"summary.json").read_text(encoding="utf-8"))
with (R/"profile.csv").open(encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))

def nll(v, pi):
    a1,ld,lb1,lb2,g=v; a2=a1+np.exp(ld); b1=np.exp(lb1); b2=np.exp(lb2)
    u1=a1-b1*p+g*q; u2=a2-b2*p+g*q
    l1=np.sum(y*u1-np.logaddexp(0,u1),axis=1)
    l2=np.sum(y*u2-np.logaddexp(0,u2),axis=1)
    return -float(np.sum(np.logaddexp(np.log1p(-pi)+l1,np.log(pi)+l2)))

uz=S["unrestricted"]["parameters"]
uvec=np.array([uz["a1"],np.log(uz["a2"]-uz["a1"]),np.log(uz["b1"]),np.log(uz["b2"]),uz["gamma"]])
uobj=float(S["unrestricted"]["objective"])
cut=float(S["profile"]["cutoff"])
recomputed=[]
for row in rows:
    pi=float(row["pi_index"]); saved=np.array(json.loads(row["terminal"]))
    sols=[]
    for x0 in [saved,uvec,np.array([-1,np.log(1.5),np.log(.7),np.log(1.5),.5])]:
        rr=minimize(lambda z:nll(z,pi),x0,method="Powell",
                    bounds=[(-4,2),(-2.5,1.5),(-2,1.5),(-2,1.5),(-2,2)],
                    options={"xtol":1e-10,"ftol":1e-12,"maxiter":12000})
        sols.append((rr.fun,rr.x,rr.success))
    best=min(sols,key=lambda t:t[0]); lr=2*(best[0]-uobj)
    recomputed.append({"pi":pi,"objective":float(best[0]),"lr":float(lr),"in_set":bool(lr<=cut),
                       "objective_difference_from_reported":float(best[0]-float(row["objective"]))})
vals=[r["pi"] for r in recomputed if r["in_set"]]
maxdiff=max(abs(r["objective_difference_from_reported"]) for r in recomputed)
checks={
 "coverage_map":"independent derivative-free recomputation covers selected conditional objectives, LR reference arithmetic, evaluated-grid membership/count, holes, and endpoint censoring; it does not independently validate simulation generation, EM, or policy mapping",
 "all_indices_recomputed":len(recomputed)==len(S["profile"]["grid"]),
 "max_objective_difference":float(maxdiff),
 "objective_agreement":bool(maxdiff<2e-5),
 "in_set_values":vals,
 "in_set_count":len(vals),
 "count_agreement":len(vals)==S["profile"]["in_set_count"],
 "values_agreement":vals==S["profile"]["in_set_values"],
 "holes_recomputed":sorted(set(S["profile"]["grid"])-set(r["pi"] for r in recomputed)),
 "left_endpoint_censored":bool(vals and vals[0]==S["profile"]["grid"][0]),
 "right_endpoint_censored":bool(vals and vals[-1]==S["profile"]["grid"][-1]),
 "details":recomputed}
(R/"verification.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
if not all([checks["all_indices_recomputed"],checks["objective_agreement"],checks["count_agreement"],checks["values_agreement"]]):
    raise SystemExit(2)
