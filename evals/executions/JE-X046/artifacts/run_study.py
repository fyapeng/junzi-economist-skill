import json, platform, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize
from scipy.special import expit

OUT = Path(__file__).resolve().parent
TRUE = np.array([-0.10, 1.25, 0.80, 0.58])  # b, a1, d=k2-k1, pi(low-cost)
SIZES = [500, 2500]
SEEDS = list(range(24001, 24041))
BOUNDS = [(-4,4), (-1,4), (0.02,5), (0.02,0.98)]
TAU = 1.0

def p_mix(w, th):
    b,a,d,pi=th; z=b+a*w
    return pi*expit(z)+(1-pi)*expit(z-d)

def dp_mix(w, th):
    b,a,d,pi=th; z=b+a*w; q1=expit(z); q2=expit(z-d)
    s1=q1*(1-q1); s2=q2*(1-q2)
    return np.column_stack((pi*s1+(1-pi)*s2,
                            w*(pi*s1+(1-pi)*s2),
                            -(1-pi)*s2, q1-q2))

def nll_grad(th,w,y):
    p=np.clip(p_mix(w,th),1e-10,1-1e-10); dp=dp_mix(w,th)
    nll=-np.sum(y*np.log(p)+(1-y)*np.log1p(-p))
    g=-np.sum(((y-p)/(p*(1-p)))[:,None]*dp,axis=0)
    return nll,g

def legendre(w, degree=6):
    return np.polynomial.legendre.legvander(w, degree)

def smm_obj_grad(th,w,y,H,W):
    p=p_mix(w,th); dp=dp_mix(w,th)
    m=(H*(y-p)[:,None]).mean(axis=0)
    D=-(H[:,:,None]*dp[:,None,:]).mean(axis=0)
    return float(m@W@m), 2*D.T@W@m

def starts(rng):
    base=[TRUE, np.array([0,1,.2,.5]), np.array([-.5,1.8,1.8,.25]),
          np.array([.5,.5,3,.8])]
    return base+[np.array([rng.uniform(-1,1),rng.uniform(.1,2.5),
                           rng.uniform(.03,4),rng.uniform(.04,.96)]) for _ in range(4)]

def multistart(fun, sts):
    runs=[]
    for x in sts:
        r=minimize(lambda t: fun(t)[0], x, jac=lambda t: fun(t)[1],
                   method='L-BFGS-B', bounds=BOUNDS,
                   options={'ftol':1e-12,'gtol':1e-7,'maxiter':1500,'maxls':50})
        runs.append(r)
    good=[r for r in runs if np.all(np.isfinite(r.x)) and np.isfinite(r.fun)]
    best=min(good,key=lambda r:r.fun) if good else runs[0]
    spread=np.ptp(np.array([r.x for r in good]),axis=0) if good else np.full(4,np.nan)
    return best,runs,spread

def fit_logit(w,y):
    def f(t):
        p=expit(t[0]+t[1]*w); pc=np.clip(p,1e-10,1-1e-10)
        val=-np.sum(y*np.log(pc)+(1-y)*np.log1p(-pc))
        return val, -np.array([np.sum(y-p),np.sum((y-p)*w)])
    return minimize(lambda t:f(t)[0],[0,1],jac=lambda t:f(t)[1],method='BFGS',
                    options={'gtol':1e-7,'maxiter':1000})

def num_hessian_grad(th,w,y):
    H=np.zeros((4,4))
    for j in range(4):
        h=2e-4*max(1,abs(th[j])); xp=th.copy(); xm=th.copy()
        xp[j]+=h; xm[j]-=h
        H[:,j]=(nll_grad(xp,w,y)[1]-nll_grad(xm,w,y)[1])/(2*h)
    return (H+H.T)/2

def metrics_probs(th, blogit, grids):
    out={}
    for name,w in grids.items():
        pt=p_mix(w,TRUE); pm=p_mix(w,th); pl=expit(blogit[0]+blogit[1]*w)
        out[f'mix_rmse_{name}']=float(np.sqrt(np.mean((pm-pt)**2)))
        out[f'logit_rmse_{name}']=float(np.sqrt(np.mean((pl-pt)**2)))
    return out

def one(seed,n):
    rng=np.random.default_rng(seed+100000*n)
    w=rng.uniform(-1,1,n); y=rng.binomial(1,p_mix(w,TRUE))
    sts=starts(rng)
    mle, mruns, mspread=multistart(lambda t:nll_grad(t,w,y),sts)
    # SMM: seven Legendre residual moments; two-step heteroskedasticity-robust weight.
    H=legendre(w,6)
    pilot,_runs,_=multistart(lambda t:smm_obj_grad(t,w,y,H,np.eye(7)),sts)
    e=y-p_mix(w,pilot.x); G=H*e[:,None]
    S=(G-G.mean(0)).T@(G-G.mean(0))/n + 1e-6*np.eye(7)
    W=np.linalg.inv(S)
    smm,sruns,sspread=multistart(lambda t:smm_obj_grad(t,w,y,H,W),sts)
    lr=fit_logit(w,y)
    grids={'train':np.linspace(-1,1,301),'interp':np.linspace(-.75,.75,201),
           'extra':np.linspace(1,1.5,151),'policy':np.linspace(1.5,2.5,201)}
    row={'seed':seed,'n':n}
    for nm,r,runs,spread in [('mle',mle,mruns,mspread),('smm',smm,sruns,sspread)]:
        row[f'{nm}_success']=bool(r.success)
        row[f'{nm}_strict_convergence']=bool(r.success and np.linalg.norm(r.jac)<1e-3)
        row[f'{nm}_objective']=float(r.fun); row[f'{nm}_gradnorm']=float(np.linalg.norm(r.jac))
        row[f'{nm}_starts_success']=int(sum(x.success for x in runs))
        row[f'{nm}_near_boundary']=bool(np.any(np.array(r.x)-np.array([x[0] for x in BOUNDS])<.005) or np.any(np.array([x[1] for x in BOUNDS])-np.array(r.x)<.005))
        row[f'{nm}_start_maxspread']=float(np.max(spread))
        for k,v in zip(['b','a1','d','pi'],r.x): row[f'{nm}_{k}']=float(v)
    row['logit_success']=bool(lr.success); row['logit_b']=float(lr.x[0]); row['logit_a1']=float(lr.x[1])
    row.update(metrics_probs(mle.x,lr.x,grids))
    smet=metrics_probs(smm.x,lr.x,grids)
    for k,v in smet.items():
        if k.startswith('mix_'): row['smm_'+k[4:]]=v
    # Untargeted calibration: four equal-width bins (not SMM's global polynomial summary).
    bins=np.minimum(((w+1)*2).astype(int),3)
    row['mix_bin_mae']=float(np.mean([abs(y[bins==j].mean()-p_mix(w[bins==j],mle.x).mean()) for j in range(4)]))
    row['logit_bin_mae']=float(np.mean([abs(y[bins==j].mean()-expit(lr.x[0]+lr.x[1]*w[bins==j]).mean()) for j in range(4)]))
    row['smm_bin_mae']=float(np.mean([abs(y[bins==j].mean()-p_mix(w[bins==j],smm.x).mean()) for j in range(4)]))
    ms=(H*(y-p_mix(w,smm.x))[:,None]).mean(0)
    row['smm_targeted_weighted_norm']=float(np.sqrt(ms@W@ms))
    # Fresh held-out choices: half interpolation, half extrapolation.
    whold=np.r_[rng.uniform(-.75,.75,n//2),rng.uniform(1,1.5,n-n//2)]
    yhold=rng.binomial(1,p_mix(whold,TRUE))
    for tag,pred in [('mix',p_mix(whold,mle.x)),('smm',p_mix(whold,smm.x)),('logit',expit(lr.x[0]+lr.x[1]*whold))]:
        row[f'{tag}_heldout_brier']=float(np.mean((yhold-pred)**2))
    # Out-of-support wage-index subsidy: baseline heldout w~U(1,1.5), policy shifts index by tau.
    wh=np.linspace(1,1.5,501)
    for tag,th in [('true',TRUE),('mix',mle.x),('smm',smm.x)]:
        base=p_mix(wh,th); cf=p_mix(wh+TAU,th)
        row[f'{tag}_cf_participation']=float(cf.mean()); row[f'{tag}_cf_change']=float((cf-base).mean())
        row[f'{tag}_transfer_per_person']=float(TAU*cf.mean())
    pl0=expit(lr.x[0]+lr.x[1]*wh); plc=expit(lr.x[0]+lr.x[1]*(wh+TAU))
    row['logit_cf_participation']=float(plc.mean()); row['logit_cf_change']=float((plc-pl0).mean())
    row['logit_transfer_per_person']=float(TAU*plc.mean())
    # Wald coverage only when interior and observed information is positive definite.
    row['mle_hess_pd']=False
    for j,k in enumerate(['b','a1','d','pi']): row[f'mle_cover_{k}']=np.nan
    try:
        Hess=num_hessian_grad(mle.x,w,y); eig=np.linalg.eigvalsh(Hess)
        if eig.min()>1e-7 and not row['mle_near_boundary']:
            V=np.linalg.inv(Hess); row['mle_hess_pd']=True
            se=np.sqrt(np.diag(V))
            for j,k in enumerate(['b','a1','d','pi']): row[f'mle_cover_{k}']=bool(abs(mle.x[j]-TRUE[j])<=1.96*se[j])
    except Exception: pass
    return row

def summarize(df):
    rows=[]
    for n,g in df.groupby('n'):
        r={'n':int(n),'reps':len(g)}
        for est in ['mle','smm']:
            r[f'{est}_success_rate']=g[f'{est}_success'].mean()
            r[f'{est}_strict_convergence_rate']=g[f'{est}_strict_convergence'].mean()
            r[f'{est}_boundary_rate']=g[f'{est}_near_boundary'].mean()
            r[f'{est}_median_gradnorm']=g[f'{est}_gradnorm'].median()
            r[f'{est}_start_disagreement_rate']=(g[f'{est}_start_maxspread']>.10).mean()
            for j,k in enumerate(['b','a1','d','pi']):
                e=g[f'{est}_{k}']-TRUE[j]; r[f'{est}_{k}_bias']=e.mean(); r[f'{est}_{k}_rmse']=np.sqrt(np.mean(e**2))
        r['mle_wald_eligible_rate']=g.mle_hess_pd.mean()
        for k in ['b','a1','d','pi']: r[f'mle_{k}_coverage_conditional']=g[f'mle_cover_{k}'].mean()
        for k in ['mix_rmse_train','smm_rmse_train','logit_rmse_train','mix_rmse_extra','smm_rmse_extra','logit_rmse_extra','mix_rmse_policy','smm_rmse_policy','logit_rmse_policy','mix_bin_mae','smm_bin_mae','logit_bin_mae','smm_targeted_weighted_norm','mix_heldout_brier','smm_heldout_brier','logit_heldout_brier']:
            r[k+'_mean']=g[k].mean()
        for est in ['true','mix','smm','logit']:
            for k in ['cf_participation','cf_change','transfer_per_person']:
                r[f'{est}_{k}_mean']=g[f'{est}_{k}'].mean()
                if est!='true': r[f'{est}_{k}_sd']=g[f'{est}_{k}'].std()
        rows.append(r)
    return pd.DataFrame(rows)

def main():
    t=time.time(); rows=[]
    for n in SIZES:
        for seed in SEEDS: rows.append(one(seed,n))
    raw=pd.DataFrame(rows); summ=summarize(raw)
    raw.to_csv(OUT/'raw_runs.csv',index=False,encoding='utf-8-sig')
    summ.to_csv(OUT/'summary.csv',index=False,encoding='utf-8-sig')
    meta={'true':dict(zip(['b','a1','d','pi'],TRUE.tolist())),'sizes':SIZES,'seeds':SEEDS,
          'training_design':'w iid Uniform[-1,1]','heldout':'interpolation grid [-.75,.75]; extrapolation grid (1,1.5]',
          'policy':'heldout w Uniform[1,1.5], subsidy shifts wage index by tau=1; transfers=tau times participation',
          'seconds':time.time()-t,'python':sys.version,'platform':platform.platform(),
          'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__}
    (OUT/'results.json').write_text(json.dumps({'meta':meta,'summary':summ.to_dict('records')},indent=2),encoding='utf-8')
    print(summ.to_string(index=False)); print(json.dumps(meta,indent=2))

if __name__=='__main__': main()
