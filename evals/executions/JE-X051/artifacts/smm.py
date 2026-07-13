from pathlib import Path
import csv,json,sys
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

R=Path(__file__).resolve().parent; A=R/"artifacts"
d=np.load(A/"raw_simulation.npz"); s=json.loads((A/"summary.json").read_text(encoding="utf-8"))
cost,time,rel,choice,draws=[d[k] for k in ["cost","time","reliability","choice","draws"]]
train=d["train"];valid=d["valid"]
bounds=[(-2,2),(-2,2),(-1.8,-.05),(0,.8),(-1.5,-.05),(-1.5,.2)]

def contributions_from_choices(idx):
    c=choice[idx]; one=np.eye(3)[c]
    return np.concatenate([one[:,:,:2],one*cost[idx],one*time[idx],one*rel[idx]],axis=2).reshape(-1,11)

obs_contrib=contributions_from_choices(train); obs=obs_contrib.mean(axis=0)
scale=np.maximum(obs_contrib.std(axis=0,ddof=1),.08)

def probs(x,idx,charge=0):
    cc=cost[idx].copy();cc[:,:,0]+=charge
    bt=x[2]+x[3]*draws
    v=x[4]*cc[:,None,:,:]+x[5]*rel[idx,None,:,:]+bt[None,:,None,None]*time[idx,None,:,:]
    v[:,:,:,0]+=x[0];v[:,:,:,1]+=x[1]
    return np.exp(v-logsumexp(v,axis=3,keepdims=True)).mean(axis=1)

def pred_mom(x,idx):
    p=probs(x,idx)
    return np.concatenate([p[:,:,:2],p*cost[idx],p*time[idx],p*rel[idx]],axis=2).reshape(-1,11).mean(axis=0)

def criterion(x):
    gap=(pred_mom(x,train)-obs)/scale
    return float(len(train)*4*np.mean(gap*gap))

def pg(x,g):
    out=np.array(g);active=[]
    for k,((lo,hi),xx,gg) in enumerate(zip(bounds,x,g)):
        if xx<=lo+1e-6 and gg>0:out[k]=0;active.append(f"{k}:lower")
        elif xx>=hi-1e-6 and gg<0:out[k]=0;active.append(f"{k}:upper")
    return out,active

rng=np.random.default_rng(7651); starts=[s["models"][0]["parameters"]]
for k in range(7): starts.append([rng.uniform(-.2,1),rng.uniform(-.2,.8),rng.uniform(-1.2,-.35),rng.uniform(.03,.75),rng.uniform(-.9,-.25),rng.uniform(-.8,-.1)])
rows=[]
for k,x0 in enumerate(starts):
    q=minimize(criterion,x0,method="L-BFGS-B",bounds=bounds,options={"maxiter":900,"ftol":1e-13,"gtol":1e-8,"maxls":50})
    g=np.asarray(q.jac);pgrad,active=pg(q.x,g)
    rows.append({"estimator":"diagonal_weighted_smm","start":k,"initial":list(map(float,x0)),"terminal":q.x.tolist(),"criterion":float(q.fun),
     "raw_gradient":g.tolist(),"projected_gradient":pgrad.tolist(),"projected_gradient_inf":float(np.max(np.abs(pgrad))),"active_bounds":active,
     "solver_success":bool(q.success),"status":int(q.status),"message":str(q.message)})
best=min(rows,key=lambda x:x["criterion"])
for x in rows:x["distance_from_best_objective"]=x["criterion"]-best["criterion"]

def nll(x,idx):
    bt=x[2]+x[3]*draws;v=x[4]*cost[idx,None,:,:]+x[5]*rel[idx,None,:,:]+bt[None,:,None,None]*time[idx,None,:,:]
    v[:,:,:,0]+=x[0];v[:,:,:,1]+=x[1];lp=v-logsumexp(v,axis=3,keepdims=True)
    picked=np.take_along_axis(lp,choice[idx,None,:,None],axis=3).squeeze(3).sum(axis=2)
    return -float((logsumexp(picked,axis=1)-np.log(len(draws))).sum())

pp=best["terminal"];p0=probs(pp,valid,0)[:,:,0].mean();p3=probs(pp,valid,3)[:,:,0].mean()
out={"model":"normal_random_coefficient_diagonal_weighted_smm","parameters":pp,"criterion":best["criterion"],
 "train_nll_evaluation":nll(pp,train),"validation_nll_evaluation":nll(pp,valid),"projected_gradient_inf":best["projected_gradient_inf"],
 "numerically_accepted":bool(best["solver_success"] and best["projected_gradient_inf"]<=.002),
 "moments":{"count":11,"definition":"drive/transit shares plus probability-weighted cost, time, and reliability for all three alternatives","weighting":"diagonal inverse contribution standard deviations; criterion is 2,800 times mean squared standardized gap"},
 "policy":{"baseline_drive_share":float(p0),"post_drive_share":float(p3),"change":float(p3-p0)}}
fields=list(rows[0])
with (A/"smm_all_starts.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for x in rows:w.writerow({k:json.dumps(v) if isinstance(v,list) else v for k,v in x.items()})
(A/"smm_summary.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
sys.exit(0 if out["numerically_accepted"] else 4)
