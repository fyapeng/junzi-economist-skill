"""Independent primitive reimplementation: no import from analysis.py."""
import json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent; R=json.loads((P/'results.json').read_text(encoding='utf-8'))
x=np.arange(5); pr=np.array(R['transition_estimates']['run']); po=np.array(R['transition_estimates']['overhaul'])
def independent_policy(q,s):
    th,F,b=q; v=np.zeros(5)
    for n in range(50000):
        ar=-th*x*x+b*(pr@v); ao=-F+s+b*(po@v)
        m=np.maximum(ar,ao); nv=m+np.log(np.exp(ar-m)+np.exp(ao-m))
        if np.linalg.norm(nv-v,np.inf)<2e-13: break
        v=nv
    odds=np.exp(np.clip(ao-ar,-700,700)); p=odds/(1+odds)
    residual=np.linalg.norm(v-(np.maximum(ar,ao)+np.log(np.exp(ar-np.maximum(ar,ao))+np.exp(ao-np.maximum(ar,ao)))),np.inf)
    return v,p,residual,n
q=np.array(R['full_nfxp_best']['final']); checks=[]
for s in [0,.75,.25,.5,1.25,2.0]:
    v,p,e,n=independent_policy(q,s); assert e<1e-10 and np.all((p>0)&(p<1))
    checks.append({'subsidy':s,'residual':float(e),'iterations':n+1,'p':p.tolist(),'V':v.tolist()})
# independently recompute population-rank derivative from true primitives and central differences
true=np.array(R['design']['true'])
pr_saved,po_saved=pr.copy(),po.copy()
pr=np.zeros((5,5))
for state in range(5):
    for d,w in [(0,.58),(1,.32),(2,.10)]: pr[state,min(4,state+d)]+=w
po=np.tile(np.array([.86,.14,0,0,0]),(5,1))
def primitive_logits(q):
    out=[]
    for s in [0,.75]:
        _,pp,_,_=independent_policy(q,s); out.extend(np.log(pp/(1-pp)))
    return np.array(out)
J=np.empty((10,3))
for j in range(3):
    a=true.copy(); b=true.copy(); a[j]+=1e-5; b[j]-=1e-5; J[:,j]=(primitive_logits(a)-primitive_logits(b))/(2e-5)
sv=np.linalg.svd(J,compute_uv=False); rank=np.linalg.matrix_rank(J,tol=1e-7); assert rank==3
pr,po=pr_saved,po_saved
out={'independent_bellman_checks':checks,'independent_rank':int(rank),'independent_singular_values':sv.tolist(),
     'max_sv_difference_vs_production':float(np.max(np.abs(sv-np.array(R['population_local_identification']['singular_values'])))),'status':'PASS'}
(P/'verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
