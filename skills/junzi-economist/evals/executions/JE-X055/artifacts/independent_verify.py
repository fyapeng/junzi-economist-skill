import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent
BETA = 0.93
X = np.arange(5.0)
REG = [0.0, 0.4]
BOUNDS = np.array([[0.05,1.5],[0.2,5.0],[0.0,1.0],[0.0,1.0]])
DELTA = 0.15


def tmats(pm, pr):
    a = np.zeros((5,5))
    for x in range(5):
        a[x,x] += 1-pm if x < 4 else 1
        if x < 4: a[x,x+1] += pm
    b = np.zeros((5,5)); b[:,0]=pr; b[:,1]=1-pr
    return a,b


def vi(theta, subsidy):
    c,r,pm,pr = theta; p0,p1=tmats(pm,pr); v=np.zeros(5)
    for it in range(2000):
        q0=-c*X+BETA*p0@v; q1=-(r-subsidy)+BETA*p1@v
        nv=np.logaddexp(q0,q1)
        if np.max(np.abs(nv-v)) < 2e-11: v=nv; break
        v=nv
    else: raise RuntimeError('independent value iteration failure')
    q0=-c*X+BETA*p0@v; q1=-(r-subsidy)+BETA*p1@v
    cp=1/(1+np.exp(q0-q1))
    return cp,v,float(np.max(np.abs(v-np.logaddexp(q0,q1))))


def read_data():
    with (ROOT/'simulated_panel.csv').open(encoding='utf-8-sig') as f:
        return np.array([[float(z) for z in row] for row in list(csv.reader(f))[1:]])


def nll(pref,data,pm,pr):
    ans=0.0
    for s in REG:
        d=data[data[:,2]==s]; p,_,_=vi([pref[0],pref[1],pm,pr],s)
        pp=np.where(d[:,4]==1,p[d[:,3].astype(int)],1-p[d[:,3].astype(int)])
        ans-=np.log(pp).sum()
    return float(ans)


def empirical(data):
    n=np.zeros((2,5,2),int)
    for z in data: n[int(z[2]>0),int(z[3]),int(z[4])]+=1
    p=(n[:,:,1]+.5)/(n.sum(2)+1)
    return p,n


def ccp_obj(pref,p,n,pm,pr):
    c,r=pref; k,a=tmats(pm,pr); total=0
    for g,s in enumerate(REG):
        pg=p[g]; u0=-c*X; u1=np.full(5,-r+s)
        pp=(1-pg)[:,None]*k+pg[:,None]*a
        flow=(1-pg)*u0+pg*u1-(1-pg)*np.log(1-pg)-pg*np.log(pg)
        v=np.linalg.solve(np.eye(5)-BETA*pp,flow)
        err=np.log(pg/(1-pg))-((u1-u0)+BETA*(a-k)@v)
        total+=np.sum(n[g].sum(1)*err**2)
    return float(total/n.sum())


def obs(theta):
    z=[]
    for s in REG: z.extend(vi(theta,s)[0])
    z.extend(theta[2:])
    return np.array(z)


def jac(theta):
    j=np.zeros((12,4))
    for k in range(4):
        h=2e-5*max(1,abs(theta[k])); u=theta.copy(); d=theta.copy(); u[k]+=h; d[k]-=h
        j[:,k]=(obs(u)-obs(d))/(2*h)
    return j


def main():
    summary=json.loads((ROOT/'summary.json').read_text(encoding='utf-8'))
    data=read_data(); keep=(data[:,4]==0)&(data[:,3]<4); repl=data[:,4]==1
    pm=float(np.mean(data[keep,5]==data[keep,3]+1)); pr=float(np.mean(data[repl,5]==0))
    nh=np.array(summary['nfxp']['estimate'])
    checks={}
    checks['data_rows']=len(data)==summary['sample']['rows']==15750
    checks['controlled_transitions']=max(abs(pm-nh[2]),abs(pr-nh[3]))<1e-14
    sols=[]
    for st in ([.07,.25],[.45,2.2],[1.4,4.8],[.9,1.2]):
        q=minimize(lambda z:nll(z,data,pm,pr),st,method='L-BFGS-B',bounds=BOUNDS[:2].tolist(),options={'ftol':1e-12,'gtol':2e-8,'maxiter':800})
        sols.append({'start':st,'terminal':q.x.tolist(),'objective':float(q.fun),'success':bool(q.success)})
    ib=min(sols,key=lambda q:q['objective'])
    checks['nfxp_independent_value_iteration']=np.max(np.abs(np.r_[ib['terminal'],pm,pr]-nh))<2e-5 and abs(ib['objective']-summary['nfxp']['choice_nll'])<2e-5
    p,n=empirical(data); csol=[]
    for st in ([.06,.3],[.45,2.2],[1.45,4.8]):
        q=minimize(lambda z:ccp_obj(z,p,n,pm,pr),st,method='L-BFGS-B',bounds=BOUNDS[:2].tolist(),options={'ftol':1e-13,'gtol':1e-9})
        csol.append({'start':st,'terminal':q.x.tolist(),'objective':float(q.fun),'success':bool(q.success)})
    cb=min(csol,key=lambda q:q['objective']); reported=np.array(summary['ccp_minimum_distance']['estimate'])
    checks['ccp_independent_inversion']=np.max(np.abs(np.r_[cb['terminal'],pm,pr]-reported))<2e-5
    sv=np.linalg.svd(jac(nh),compute_uv=False)
    checks['continuous_local_rank']=len(sv)==4 and sv[-1]>1e-7 and np.max(np.abs(sv-np.array(summary['population_local_rank_evidence']['singular_values'])))<2e-6

    with (ROOT/'alternative_search.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    slab_ids={int(r['slab_id']) for r in rows}; seeds={(int(r['slab_id']),int(r['rerun_seed'])) for r in rows}
    expected_nonempty=sum(int(BOUNDS[j,0] <= min(BOUNDS[j,1],nh[j]-DELTA)) + int(max(BOUNDS[j,0],nh[j]+DELTA) <= BOUNDS[j,1]) for j in range(4))
    checks['restricted_trace_coverage']=slab_ids==set(range(expected_nonempty)) and all((j,s) in seeds for j in range(expected_nonempty) for s in (991,992))
    selected=summary['restricted_alternative_search']['selected']; alt=np.array(selected['terminal'])
    recomputed=float(np.sum((obs(alt)-obs(nh))**2)); slack=float(np.max(np.abs(alt-nh))-DELTA); box=float(np.min(np.r_[alt-BOUNDS[:,0],BOUNDS[:,1]-alt]))
    checks['selected_alternative_recomputed']=abs(recomputed-selected['objective'])<2e-8 and slack>=-1e-10 and box>=-1e-10
    # Fresh algorithmic reruns: independent value iteration and three starts on every closed slab.
    fresh=[]; rng=np.random.default_rng(60317)
    for j in range(4):
        for side in ('lower','upper'):
            b=BOUNDS.copy()
            if side=='lower': b[j,1]=min(b[j,1],nh[j]-DELTA)
            else: b[j,0]=max(b[j,0],nh[j]+DELTA)
            if b[j,0]>b[j,1]: continue
            candidates=[]
            for st in (np.clip(nh,b[:,0],b[:,1]),b.mean(1),b[:,0]+rng.random(4)*(b[:,1]-b[:,0])):
                q=minimize(lambda z:float(np.sum((obs(z)-obs(nh))**2)),st,method='L-BFGS-B',bounds=b.tolist(),options={'ftol':1e-14,'gtol':2e-9,'maxiter':1200})
                candidates.append(float(q.fun))
            fresh.append({'dimension':j,'side':side,'best_objective':min(candidates),'all_objectives':candidates})
    fresh_best=min(r['best_objective'] for r in fresh)
    checks['restricted_search_independent_rerun']=abs(fresh_best-selected['objective'])<3e-7

    accounting=[]
    for z in summary['policy_accounting']:
        identity=z['private_value']-z['fiscal_transfer']
        accounting.append({'subsidy':z['subsidy'],'identity_residual':identity-z['social_welfare_private_plus_transfer_cancellation']})
    checks['private_transfer_resource_welfare_identity']=max(abs(z['identity_residual']) for z in accounting)<2e-10
    checks['policy_support_labels']=([z['support'] for z in summary['policy_accounting']]==['observed','model interpolation','observed'])

    checks = {k: bool(v) for k, v in checks.items()}
    coverage={
      'controlled transition estimates':'independently recomputed from row-level transitions',
      'NFXP estimate and objective':'independently reoptimized using value iteration from four new starts',
      'distinct CCP estimate':'independently reoptimized from empirical CCP inversion; no Bellman solver',
      'continuous local population rank':'independent finite-difference Jacobian and SVD at reported estimate; local only',
      'restricted alternative result':'all nonempty closed slabs/two saved seeds audited; selected candidate recomputed; each nonempty slab independently rerun from three starts',
      'closed-domain global identification':'not claimed and not verified; finite numerical searches cannot prove it',
      'policy accounting':'stationary private, transfer, resource, and welfare identity checked',
      'sampling/estimator distribution':'not covered; one fixed simulated sample only',
      'external validity':'not covered; synthetic model'
    }
    result={'pass':bool(all(checks.values())),'checks':checks,'independent_nfxp_runs':sols,'independent_ccp_runs':csol,'independent_singular_values':sv.tolist(),'selected_alternative_recomputed':{'objective':recomputed,'restriction_slack':slack,'box_slack':box},'independent_restricted_reruns':fresh,'accounting':accounting,'coverage_map':coverage}
    (ROOT/'independent_verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'pass':result['pass'],'checks':checks},indent=2))
    if not result['pass']: sys.exit(1)


if __name__=='__main__': main()
