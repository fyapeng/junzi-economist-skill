from __future__ import annotations

import csv, json, platform, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import logsumexp, expit

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 51051
N, T, J, NTRAIN = 900, 4, 3, 700
ALT = ["drive", "transit", "micromobility"]
TRUE = {"asc_drive": .55, "asc_transit": .25, "mu_time": -.80,
        "sigma_time": .35, "beta_cost": -.55, "beta_rel": -.40}
BOUNDS = [(-2,2), (-2,2), (-1.8,-.05), (.0,.8), (-1.5,-.05), (-1.5,.2)]
PROFILE_GRID = np.round(np.linspace(0, .8, 9), 2)
PROFILE_CUTOFF = 3.841459
ACCEPT_PG = 2e-3

rng = np.random.default_rng(SEED)
# Attributes are designed before shocks/choices. Units: $ cost, 10-minute time, 10-minute reliability SD.
cost = np.empty((N,T,J)); time = np.empty_like(cost); rel = np.empty_like(cost)
cost[:,:,0] = rng.uniform(4,12,(N,T)); cost[:,:,1] = rng.uniform(1.5,5,(N,T)); cost[:,:,2] = rng.uniform(.2,2,(N,T))
time[:,:,0] = rng.uniform(1.5,4.5,(N,T)); time[:,:,1] = rng.uniform(2.5,6.5,(N,T)); time[:,:,2] = rng.uniform(2,5.5,(N,T))
rel[:,:,0] = rng.uniform(.3,1.2,(N,T)); rel[:,:,1] = rng.uniform(.5,1.8,(N,T)); rel[:,:,2] = rng.uniform(.2,.8,(N,T))
z = rng.normal(size=N)
bt = TRUE["mu_time"] + TRUE["sigma_time"]*z
u = TRUE["beta_cost"]*cost + TRUE["beta_rel"]*rel + bt[:,None,None]*time
u[:,:,0] += TRUE["asc_drive"]; u[:,:,1] += TRUE["asc_transit"]
eps = rng.gumbel(size=(N,T,J)); choice = np.argmax(u+eps, axis=2)

# Fixed integration draws, generated independently of simulated agents and held fixed across all objectives.
drng = np.random.default_rng(9117)
half = drng.normal(size=30); draws = np.r_[half, -half]

def unpack(x):
    return dict(asc_drive=x[0], asc_transit=x[1], mu_time=x[2], sigma_time=x[3], beta_cost=x[4], beta_rel=x[5])

def rc_nll(x, idx):
    p=unpack(x); ii=np.asarray(idx)
    btime=p["mu_time"] + p["sigma_time"]*draws
    v=(p["beta_cost"]*cost[ii,None,:,:] + p["beta_rel"]*rel[ii,None,:,:]
       + btime[None,:,None,None]*time[ii,None,:,:])
    v[:,:,:,0]+=p["asc_drive"]; v[:,:,:,1]+=p["asc_transit"]
    lp=v-logsumexp(v,axis=3,keepdims=True)
    c=choice[ii]
    picked=np.take_along_axis(lp, c[:,None,:,None], axis=3).squeeze(3)
    person=logsumexp(picked.sum(axis=2),axis=1)-np.log(len(draws))
    return -float(person.sum())

def hom_nll(x, idx):
    full=np.r_[x[:3],0.,x[3:]]
    return rc_nll(full,idx)

def lc_nll(x, idx):
    # Nonparametric two-point mixing distribution; midpoint + positive gap prevents label switching.
    ad,at,mid,loggap,bc,br,logitpi=x; gap=np.exp(loggap)
    b=np.array([mid-gap/2,mid+gap/2]); ii=np.asarray(idx)
    v=bc*cost[ii,None,:,:]+br*rel[ii,None,:,:]+b[None,:,None,None]*time[ii,None,:,:]
    v[:,:,:,0]+=ad; v[:,:,:,1]+=at
    lp=v-logsumexp(v,axis=3,keepdims=True); c=choice[ii]
    picked=np.take_along_axis(lp,c[:,None,:,None],axis=3).squeeze(3).sum(axis=2)
    lw=np.log([expit(logitpi),expit(-logitpi)])
    return -float(logsumexp(picked+lw[None,:],axis=1).sum())

def projected_gradient(x,g,bounds):
    pg=np.array(g,float); active=[]
    for k,((lo,hi),xi,gi) in enumerate(zip(bounds,x,g)):
        if xi <= lo+1e-6 and gi>0: pg[k]=0; active.append(f"{k}:lower")
        elif xi >= hi-1e-6 and gi<0: pg[k]=0; active.append(f"{k}:upper")
    return pg,active

def optimize_all(name,fun,bounds,starts,idx):
    rows=[]
    for s,x0 in enumerate(starts):
        r=minimize(fun,np.array(x0),args=(idx,),method="L-BFGS-B",bounds=bounds,
                   options={"maxiter":700,"ftol":1e-11,"gtol":1e-7,"maxls":40})
        g=np.asarray(r.jac,float); pg,active=projected_gradient(r.x,g,bounds)
        rows.append({"estimator":name,"start":s,"initial":list(map(float,x0)),
          "terminal":r.x.tolist(),"objective":float(r.fun),"raw_gradient":g.tolist(),
          "projected_gradient":pg.tolist(),"projected_gradient_inf":float(np.max(np.abs(pg))),
          "active_bounds":active,"solver_success":bool(r.success),"status":int(r.status),
          "message":str(r.message)})
    best=min(rows,key=lambda q:q["objective"])
    for q in rows: q["distance_from_best_objective"]=q["objective"]-best["objective"]
    return rows,best

train=np.arange(NTRAIN); valid=np.arange(NTRAIN,N)
starts_rc=[]
for k in range(8):
    starts_rc.append([rng.uniform(-.2,1),rng.uniform(-.2,.8),rng.uniform(-1.2,-.35),rng.uniform(.05,.7),rng.uniform(-.9,-.25),rng.uniform(-.8,-.1)])
rows_rc,best_rc=optimize_all("normal_random_coefficient_msl",rc_nll,BOUNDS,starts_rc,train)
hb=[BOUNDS[i] for i in [0,1,2,4,5]]
starts_h=[np.delete(np.array(x),3).tolist() for x in starts_rc[:6]]
rows_h,best_h=optimize_all("homogeneous_logit",hom_nll,hb,starts_h,train)
lcb=[(-2,2),(-2,2),(-1.8,-.05),(-3,.7),(-1.5,-.05),(-1.5,.2),(-3,3)]
starts_l=[]
for k in range(8): starts_l.append([rng.uniform(-.2,1),rng.uniform(-.2,.8),rng.uniform(-1.2,-.4),rng.uniform(-1.5,-.1),rng.uniform(-.9,-.25),rng.uniform(-.8,-.1),rng.uniform(-1,1)])
rows_l,best_l=optimize_all("two_point_latent_class_mle",lc_nll,lcb,starts_l,train)

def policy_effect_rc(x,idx):
    p=unpack(x); ii=np.asarray(idx); bt=p["mu_time"]+p["sigma_time"]*draws
    def share(charge):
        cc=cost[ii].copy(); cc[:,:,0]+=charge
        v=p["beta_cost"]*cc[:,None,:,:]+p["beta_rel"]*rel[ii,None,:,:]+bt[None,:,None,None]*time[ii,None,:,:]
        v[:,:,:,0]+=p["asc_drive"];v[:,:,:,1]+=p["asc_transit"]
        pr=np.exp(v-logsumexp(v,axis=3,keepdims=True))
        return float(pr[:,:,:,0].mean())
    a,b=share(0),share(3); return {"baseline_drive_share":a,"post_drive_share":b,"change":b-a}

def valid_nll(model,x):
    return rc_nll(x,valid) if model=="rc" else hom_nll(x,valid) if model=="hom" else lc_nll(x,valid)

# Conditional profile: all starts retained, and only the best accepted optimum at each sigma maps to policy.
profile_rows=[]; profile_selected=[]
base=np.array(best_rc["terminal"])
for sig in PROFILE_GRID:
    fixed_bounds=[BOUNDS[i] for i in [0,1,2,4,5]]
    def ffix(y,idx): return rc_nll(np.r_[y[:3],sig,y[3:]],idx)
    pstarts=[]
    pstarts.append(np.delete(base,3).tolist())
    for k in range(5):
        jitter=np.array([.25,.25,.18,.15,.15])*rng.normal(size=5)
        y=np.clip(np.delete(base,3)+jitter,[b[0] for b in fixed_bounds],[b[1] for b in fixed_bounds])
        pstarts.append(y.tolist())
    rr,bb=optimize_all(f"profile_sigma_{sig:.2f}",ffix,fixed_bounds,pstarts,train)
    for q in rr:
        q["sigma_index"]=float(sig)
        q["accepted"]=bool(q["solver_success"] and q["projected_gradient_inf"]<=ACCEPT_PG and np.isfinite(q["objective"]))
        profile_rows.append(q)
    accepted=[q for q in rr if q["accepted"]]
    if accepted:
        sel=min(accepted,key=lambda q:q["objective"]); full=np.r_[sel["terminal"][:3],sig,sel["terminal"][3:]]
        profile_selected.append({"sigma":float(sig),"resolved":True,"selected_start":sel["start"],"objective":sel["objective"],
          "parameters":full.tolist(),"projected_gradient_inf":sel["projected_gradient_inf"],"policy":policy_effect_rc(full,valid)})
    else: profile_selected.append({"sigma":float(sig),"resolved":False,"hole_reason":"no accepted conditional optimum"})

resolved=[q for q in profile_selected if q["resolved"]]
if len(resolved)!=len(PROFILE_GRID):
    # Required units failed: artifacts are still written below and process exits nonzero.
    required_failure=True
else: required_failure=False
prof_min=min(q["objective"] for q in resolved)
for q in profile_selected:
    if q["resolved"]:
        q["lr_stat"]=2*(q["objective"]-prof_min); q["inside_95"]=(q["lr_stat"]<=PROFILE_CUTOFF)
inside=[q for q in profile_selected if q.get("inside_95")]

support={
 "predeclared_before_estimation":True,
 "training_support":{"people":"simulated agents 0-699, four repeated trips","policy_charge":0,
  "attributes":{"cost_dollars":"drive [4,12], transit [1.5,5], micromobility [0.2,2]","time_10min":"drive [1.5,4.5], transit [2.5,6.5], micromobility [2,5.5]","reliability_10min_sd":"drive [.3,1.2], transit [.5,1.8], micromobility [.2,.8]"}},
 "interpolation_support":"new people drawn from same population with attributes inside the training boxes and zero charge",
 "validation_support":"agents 700-899, same predeclared attribute boxes and zero charge",
 "baseline_policy_support":"zero congestion charge only; this regime is observed",
 "post_policy_support":"$3 added to drive cost; implied drive cost [7,15]",
 "extrapolation_support":"the charge regime is unobserved; drive costs (12,15] are outside observed attribute support; no equilibrium congestion feedback modeled",
 "profile_domain":"sigma_time in [0,0.8], where one unit is utility SD per 10 minutes; upper bound permits substantial heterogeneity while limiting economically implausible mass with positive time utility",
}

models=[]
for key,b,kpar in [("normal_random_coefficient_msl",best_rc,6),("homogeneous_logit",best_h,5),("two_point_latent_class_mle",best_l,7)]:
    typ="rc" if key.startswith("normal") else "hom" if key.startswith("hom") else "lc"
    models.append({"model":key,"train_nll":b["objective"],"validation_nll":valid_nll(typ,b["terminal"]),"parameters":b["terminal"],"aic":2*b["objective"]+2*kpar,
      "numerically_accepted":bool(b["solver_success"] and b["projected_gradient_inf"]<=ACCEPT_PG),"projected_gradient_inf":b["projected_gradient_inf"]})

def write_csv(path,rows):
    fields=list(rows[0].keys())
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:
            w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})

write_csv(OUT/"all_starts.csv",rows_rc+rows_h+rows_l)
write_csv(OUT/"profile_all_starts.csv",profile_rows)
write_csv(OUT/"profile_selected.csv",profile_selected)
np.savez_compressed(OUT/"raw_simulation.npz",cost=cost,time=time,reliability=rel,choice=choice,draws=draws,train=train,valid=valid)
summary={"study":"latent value-of-time heterogeneity in repeated urban mode choice","seed":SEED,"true_parameters":TRUE,"sample":{"intended":N,"realized":N,"train":len(train),"validation":len(valid),"tasks_per_person":T},
 "support":support,"models":models,"profile":{"grid":PROFILE_GRID.tolist(),"cutoff":PROFILE_CUTOFF,"acceptance_projected_gradient_inf":ACCEPT_PG,
 "reported_indices":len(PROFILE_GRID),"resolved_indices":len(resolved),"holes":len(PROFILE_GRID)-len(resolved),"inside_count":len(inside),
 "set_sigma":[q["sigma"] for q in inside],"set_policy_change":[q["policy"]["change"] for q in inside],
 "left_endpoint_censored":bool(inside and inside[0]["sigma"]==PROFILE_GRID[0]),"right_endpoint_censored":bool(inside and inside[-1]["sigma"]==PROFILE_GRID[-1])},
 "inference_eligibility":{"eligible":not required_failure and all(m["numerically_accepted"] for m in models),
 "scope":"model-conditional one-parameter LR profile only; grid and asymptotic cutoff are approximations",
 "not_established":["population injectivity","finite-sample coverage","policy invariance outside observed charge regime","equilibrium congestion response"]},
 "software":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"platform":platform.platform()}}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
(OUT/"provenance.json").write_text(json.dumps({"created_by":"study.py","exact_skill_commit":"77aa2f1","seed":SEED,"integration_seed":9117,
 "command":"C:/Users/ENAN/miniforge3/envs/codex/python.exe study.py","permitted_sources":["skills/junzi-economist/SKILL.md","references/EMPIRICAL_AND_STRUCTURAL_METHODS.md","references/THEORY_MODELING.md","references/SOFTWARE_AND_COMPUTATION.md"]},indent=2),encoding="utf-8")
if required_failure: sys.exit(2)
