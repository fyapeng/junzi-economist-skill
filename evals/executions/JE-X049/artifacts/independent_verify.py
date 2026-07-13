import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import expit

ROOT=Path(r"C:\Users\ENAN\AppData\Local\Temp\junzi-economist-struct-x049\outputs")
rep=pd.read_csv(ROOT/'replication_results.csv',encoding='utf-8-sig')
starts=pd.read_csv(ROOT/'start_records.csv',encoding='utf-8-sig')
dat=pd.read_parquet(ROOT/'simulated_training.parquet')

def p_alt(t,q,s,mix):
    if mix:
        b,a,k,d,w=t
        return w/(1+np.exp(-(b*s-a*q-k)))+(1-w)/(1+np.exp(-(b*s-a*q-k-d)))
    b,a,k=t; return 1/(1+np.exp(-(b*s-a*q-k)))

checks=[]
for _,r in rep.iterrows():
    d=dat[dat.rep==r.rep]; t=np.array(json.loads(r.theta)); mix=r.model=='mixture'
    p=np.clip(p_alt(t,d.q.to_numpy(),d.s.to_numpy(),mix),1e-12,1-1e-12)
    if r.estimator=='mle': obj=-np.sum(d.y*np.log(p)+(1-d.y)*np.log(1-p))
    else:
        q=d.q.to_numpy(); s=d.s.to_numpy(); qr=(q-1.5)/.7; sr=s-.5
        Z=np.column_stack([np.ones(len(q)),sr,qr,sr**2,qr**2,sr*qr,s>.5,q>1.5,s>q-1])
        g=np.mean(Z*(d.y.to_numpy()-p)[:,None],axis=0); obj=len(q)*(g@g)
    accepted=starts[(starts.rep==r.rep)&(starts.estimator==r.estimator)&(starts.model==r.model)&(starts.numerical_accept)]
    minobj=accepted.objective.min()
    checks.append({'rep':r.rep,'estimator':r.estimator,'model':r.model,'objective_recomputed':obj,
                   'objective_saved':r.objective,'objective_abs_diff':abs(obj-r.objective),
                   'selected_minus_min_accepted':r.objective-minobj})
ck=pd.DataFrame(checks); ck.to_csv(ROOT/'independent_objective_checks.csv',index=False,encoding='utf-8-sig')

# Independent central-difference raw gradients for one interior single-logit and one boundary mixture fit.
grad=[]
for selector in [((rep.model=='single')&(rep.estimator=='mle')),((rep.model=='mixture')&(rep.estimator=='mle'))]:
    r=rep[selector].iloc[0]; d=dat[dat.rep==r.rep]; t=np.array(json.loads(r.theta)); mix=r.model=='mixture'
    def nll(x):
        p=np.clip(p_alt(x,d.q.to_numpy(),d.s.to_numpy(),mix),1e-12,1-1e-12)
        return -np.sum(d.y*np.log(p)+(1-d.y)*np.log(1-p))
    h=1e-6; gd=[]
    for j in range(len(t)):
        xp=t.copy(); xm=t.copy(); xp[j]+=h; xm[j]-=h; gd.append((nll(xp)-nll(xm))/(2*h))
    sr=starts[(starts.rep==r.rep)&(starts.estimator=='mle')&(starts.model==r.model)&(np.isclose(starts.objective,r.objective))].iloc[0]
    grad.append({'rep':r.rep,'model':r.model,'finite_difference_gradient':gd,
                 'saved_raw_gradient':json.loads(sr.raw_gradient),'max_abs_difference':float(np.max(np.abs(np.array(gd)-np.array(json.loads(sr.raw_gradient)))))})

prof=pd.read_csv(ROOT/'profile_delta.csv',encoding='utf-8-sig'); inset=prof[prof.in_95_set]
result={'implementation':'independent probability/objective formulas; central differences do not import production functions',
        'max_objective_abs_difference':float(ck.objective_abs_diff.max()),
        'max_selected_minus_min_accepted':float(ck.selected_minus_min_accepted.abs().max()),
        'gradient_checks':grad,
        'profile_set':{'delta_min':float(inset.delta.min()),'delta_max':float(inset.delta.max()),
                       'policy_effect_min':float(inset.policy_effect.min()),'policy_effect_max':float(inset.policy_effect.max())},
        'passed':bool(ck.objective_abs_diff.max()<1e-7 and ck.selected_minus_min_accepted.abs().max()<1e-7 and max(x['max_abs_difference'] for x in grad)<1e-4)}
(ROOT/'independent_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
