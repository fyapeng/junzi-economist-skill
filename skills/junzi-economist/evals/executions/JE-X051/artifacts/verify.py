from pathlib import Path
import csv,json,sys
import numpy as np
from scipy.special import logsumexp

R=Path(__file__).resolve().parent; A=R/"artifacts"
s=json.loads((A/"summary.json").read_text(encoding="utf-8")); d=np.load(A/"raw_simulation.npz")
profile=list(csv.DictReader((A/"profile_selected.csv").open(encoding="utf-8-sig")))
starts=list(csv.DictReader((A/"profile_all_starts.csv").open(encoding="utf-8-sig")))

def independent_nll(par):
    # Fresh loop-based likelihood recomputation, deliberately not importing production code.
    cost,time,rel,choice,draws=[d[k] for k in ["cost","time","reliability","choice","draws"]]
    total=0.
    for i in d["train"]:
        draw_ll=[]
        for z in draws:
            ll=0.; bt=par[2]+par[3]*z
            for t in range(choice.shape[1]):
                v=par[4]*cost[i,t]+par[5]*rel[i,t]+bt*time[i,t]
                v=v.copy();v[0]+=par[0];v[1]+=par[1]
                ll += v[choice[i,t]]-logsumexp(v)
            draw_ll.append(ll)
        total += logsumexp(draw_ll)-np.log(len(draws))
    return -total

checks=[]
def ck(name,ok,detail): checks.append({"check":name,"pass":bool(ok),"detail":detail})
ck("sample_count",s["sample"]["intended"]==s["sample"]["realized"]==d["choice"].shape[0],str(d["choice"].shape))
resolved=[r for r in profile if r["resolved"]=="True"]
ck("profile_count_reconciliation",len(profile)==s["profile"]["reported_indices"] and len(resolved)==s["profile"]["resolved_indices"],f"rows={len(profile)}, resolved={len(resolved)}")
for r in resolved:
    sig=float(r["sigma"]); accepted=[x for x in starts if float(x["sigma_index"])==sig and x["accepted"]=="True"]
    best=min(float(x["objective"]) for x in accepted)
    ck(f"best_accepted_sigma_{sig:.2f}",abs(float(r["objective"])-best)<1e-7,f"selected={r['objective']}, best={best}")
sel=min(resolved,key=lambda r:float(r["objective"])); par=json.loads(sel["parameters"])
fresh=independent_nll(par)
ck("independent_likelihood_at_profile_min",abs(fresh-float(sel["objective"]))<1e-7,f"fresh={fresh}, saved={sel['objective']}")
inside=[r for r in resolved if r["inside_95"]=="True"]
ck("set_count_reconciliation",len(inside)==s["profile"]["inside_count"],f"inside={len(inside)}")
coverage={
 "independently_recomputed":["training simulated likelihood at selected profile minimum from raw attributes, choices, and draws"],
 "row_level_reconciled":["intended/realized sample counts","profile reported/resolved/hole counts","best accepted start at every resolved index","profile-set count"],
 "not_covered":["optimizer search completeness between starts","SMM moments, criterion, and optimization","latent-class likelihood implementation","homogeneous likelihood implementation","gradients/KKT values","policy mapping arithmetic","asymptotic profile cutoff validity","population identification","finite-sample coverage","economic realism"]}
out={"all_pass":all(x["pass"] for x in checks),"checks":checks,"coverage_map":coverage}
(A/"verification.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
sys.exit(0 if out["all_pass"] else 3)
