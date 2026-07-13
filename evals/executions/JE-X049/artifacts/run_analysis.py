import json, platform, sys
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize
from scipy.special import expit
from scipy.stats import chi2, norm
from scipy.optimize._numdiff import approx_derivative

ROOT=Path(r"C:\Users\ENAN\AppData\Local\Temp\junzi-economist-struct-x049")
OUT=ROOT/"outputs"; OUT.mkdir(parents=True,exist_ok=True)
TRUE=np.array([1.15,.90,-.30,1.50,.58]) # b_s,a_q,k_low,delta,pi_low; k_high=k_low+delta
BOUNDS_MIX=[(.05,2.5),(.05,2.2),(-2.5,1.5),(.02,4.0),(.03,.97)]
BOUNDS_ONE=[(.05,2.5),(.05,2.2),(-2.5,2.5)]
SIZES=[600,3000]; SEEDS=[104,211,307,419,523,631]
NSTART=8; KKT_TOL=2e-5; FD_EPS=1e-5
TRAIN={"q":[.8,2.2],"s":[-.5,1.5]}
HOLD={"q":[.95,2.05],"s":[-.35,1.35]}
BASE={"q":[.5,2.5],"s":[-1.,2.]}; SHIFT=-.5
POST={"q":[BASE['q'][0]+SHIFT,BASE['q'][1]+SHIFT],"s":BASE['s']}
STRESS={"q":[-.5,3.0],"s":[-1.2,2.2]}

def prob(th,q,s,mix=True):
    if mix:
        b,a,k,d,pi=th; l1=expit(b*s-a*q-k); l2=expit(b*s-a*q-k-d)
        return pi*l1+(1-pi)*l2
    b,a,k=th; return expit(b*s-a*q-k)

def dp(th,q,s,mix=True):
    if mix:
        b,a,k,d,pi=th; l1=expit(b*s-a*q-k); l2=expit(b*s-a*q-k-d)
        h1=l1*(1-l1); h2=l2*(1-l2); h=pi*h1+(1-pi)*h2
        return np.column_stack([h*s,-h*q,-h,-(1-pi)*h2,l1-l2])
    p=prob(th,q,s,False); h=p*(1-p)
    return np.column_stack([h*s,-h*q,-h])

def zmat(q,s):
    qr=(q-1.5)/.7; sr=s-.5
    return np.column_stack([np.ones(len(q)),sr,qr,sr**2,qr**2,sr*qr,
                            (s>.5).astype(float),(q>1.5).astype(float),(s>q-1).astype(float)])

def objective_grad(th,q,s,y,est,mix):
    p=np.clip(prob(th,q,s,mix),1e-10,1-1e-10); D=dp(th,q,s,mix)
    if est=='mle':
        obj=-np.sum(y*np.log(p)+(1-y)*np.log(1-p))
        grad=D.T@((p-y)/(p*(1-p)))
    else:
        Z=zmat(q,s); g=np.mean(Z*(y-p)[:,None],axis=0); J=-(Z.T@D)/len(y)
        obj=len(y)*(g@g); grad=2*len(y)*(J.T@g)
    return float(obj),np.asarray(grad)

def projected_grad(x,g,bounds,tol=1e-8):
    pg=g.copy(); active=[]
    for j,(lo,hi) in enumerate(bounds):
        if x[j]<=lo+tol:
            active.append(f"{j}:lower")
            if g[j]>0: pg[j]=0
        if x[j]>=hi-tol:
            active.append(f"{j}:upper")
            if g[j]<0: pg[j]=0
    return pg,active

def fit(q,s,y,est,mix,rng,repkey):
    bounds=BOUNDS_MIX if mix else BOUNDS_ONE; starts=[]
    anchors=[TRUE.copy(),np.array([.8,.6,-.8,.5,.35]),np.array([1.5,1.2,.2,2.5,.75])] if mix else [np.array([1.,.8,.2]),np.array([.6,.5,-.8])]
    initials=[]
    for x in anchors: initials.append(np.clip(x,[b[0]+1e-4 for b in bounds],[b[1]-1e-4 for b in bounds]))
    while len(initials)<NSTART: initials.append(np.array([rng.uniform(lo+.01,hi-.01) for lo,hi in bounds]))
    for sid,x0 in enumerate(initials[:NSTART]):
        fun=lambda x: objective_grad(x,q,s,y,est,mix)
        try:
            r=minimize(lambda x:fun(x)[0],x0,jac=lambda x:fun(x)[1],method='L-BFGS-B',bounds=bounds,
                       options={'maxiter':1200,'ftol':1e-12,'gtol':1e-9,'maxls':50})
            obj,g=fun(r.x); pg,active=projected_grad(r.x,g,bounds)
            row={'rep':repkey,'estimator':est,'model':'mixture' if mix else 'single','start':sid,
                 'initial':json.dumps(x0.tolist()),'final':json.dumps(r.x.tolist()),'objective':obj,
                 'raw_grad_inf':float(np.max(np.abs(g))),'projected_grad_inf':float(np.max(np.abs(pg))),
                 'raw_gradient':json.dumps(g.tolist()),'projected_gradient':json.dumps(pg.tolist()),
                 'active_bounds':'|'.join(active),'software_success':bool(r.success),'status':int(r.status),'message':str(r.message)}
        except Exception as e:
            row={'rep':repkey,'estimator':est,'model':'mixture' if mix else 'single','start':sid,'initial':json.dumps(x0.tolist()),
                 'final':'','objective':np.inf,'raw_grad_inf':np.inf,'projected_grad_inf':np.inf,'raw_gradient':'','projected_gradient':'',
                 'active_bounds':'','software_success':False,'status':-999,'message':repr(e)}
        starts.append(row)
    finite=[r['objective'] for r in starts if np.isfinite(r['objective'])]; best=min(finite) if finite else np.inf
    for row in starts:
        row['distance_from_best']=row['objective']-best if np.isfinite(row['objective']) else np.inf
        row['numerical_accept']=bool(np.isfinite(row['objective']) and row['projected_grad_inf']<=KKT_TOL)
    eligible=[r for r in starts if r['numerical_accept']]
    selected=min(eligible,key=lambda r:r['objective']) if eligible else min(starts,key=lambda r:r['objective'])
    return starts,selected

def hessian(fun,x):
    return approx_derivative(lambda z: fun(z)[1],x,method='3-point',rel_step=FD_EPS)

def inference(th,q,s,y,est,mix,accepted,active):
    p=len(th); out={'inference_eligible':False,'se':[np.nan]*p,'cover':[False]*p,'geometry':'rejected'}
    if not accepted: return out
    if active: out['geometry']='boundary'; return out
    try:
        if est=='mle': V=np.linalg.inv(hessian(lambda x:objective_grad(x,q,s,y,est,mix),th))
        else:
            D=dp(th,q,s,mix); Z=zmat(q,s); J=-(Z.T@D)/len(y); u=Z*(y-prob(th,q,s,mix))[:,None]
            Om=(u.T@u)/len(y); A=np.linalg.inv(J.T@J); V=A@(J.T@Om@J)@A/len(y)
        se=np.sqrt(np.diag(V)); ok=np.all(np.isfinite(se)) and np.all(se>0)
        out['inference_eligible']=bool(ok); out['se']=se.tolist(); out['geometry']='interior' if ok else 'singular'
        if mix and ok: out['cover']=(np.abs(th-TRUE)<=1.96*se).tolist()
    except Exception as e: out['geometry']='hessian_failure:'+type(e).__name__
    return out

def grid(rect,nq=31,ns=31):
    q=np.linspace(*rect['q'],nq); s=np.linspace(*rect['s'],ns); Q,S=np.meshgrid(q,s); return Q.ravel(),S.ravel()

def profile_delta(q,s,y,best):
    econ=np.linspace(.10,3.00,59); rows=[]; bounds=[BOUNDS_MIX[i] for i in [0,1,2,4]]
    base=np.delete(best,3)
    for d in econ:
        def fg(x):
            th=np.insert(x,3,d); o,g=objective_grad(th,q,s,y,'mle',True); return o,np.delete(g,3)
        local=[]
        initials=[base,np.array([.7,.5,-.8,.3]),np.array([1.6,1.3,.2,.8])]
        for sid,x0 in enumerate(initials):
            r=minimize(lambda x:fg(x)[0],np.clip(x0,[b[0]+1e-4 for b in bounds],[b[1]-1e-4 for b in bounds]),
                       jac=lambda x:fg(x)[1],method='L-BFGS-B',bounds=bounds,options={'maxiter':1000,'ftol':1e-12,'gtol':1e-9})
            o,g=fg(r.x); pg,act=projected_grad(r.x,g,bounds); th=np.insert(r.x,3,d)
            qb,sb=grid(BASE); pp=np.mean(prob(th,qb+SHIFT,sb,True)-prob(th,qb,sb,True))
            local.append({'delta':d,'start':sid,'objective':o,'theta':json.dumps(th.tolist()),'software_success':r.success,
                          'projected_grad_inf':np.max(np.abs(pg)),'active_bounds':'|'.join(act),'policy_effect':pp,'message':str(r.message)})
        rows.extend(local)
    df=pd.DataFrame(rows); good=df.projected_grad_inf<=KKT_TOL; m=df.loc[good,'objective'].min(); df['lr']=2*(df.objective-m); df['in_95_set']=good&(df.lr<=chi2.ppf(.95,1)); return df

def main():
    allstarts=[]; reps=[]; datasets=[]
    for n in SIZES:
      for seed in SEEDS:
        rng=np.random.default_rng(seed+10000*n); q=rng.uniform(*TRAIN['q'],n); s=rng.uniform(*TRAIN['s'],n)
        p=prob(TRUE,q,s,True); y=rng.binomial(1,p); repkey=f"n{n}_s{seed}"
        datasets.append(pd.DataFrame({'rep':repkey,'q':q,'s':s,'y':y,'p_true':p}))
        for est in ['mle','smm']:
          for mix in [True,False]:
            starts,sel=fit(q,s,y,est,mix,np.random.default_rng(seed+n+(0 if est=='mle' else 100)+(0 if mix else 200)),repkey)
            allstarts.extend(starts); th=np.array(json.loads(sel['final'])) if sel['final'] else np.full(5 if mix else 3,np.nan)
            inf=inference(th,q,s,y,est,mix,sel['numerical_accept'],sel['active_bounds'])
            qh,sh=grid(HOLD); qb,sb=grid(BASE); qs,ss=grid(STRESS)
            true_hold=prob(TRUE,qh,sh,True); pred_hold=prob(th,qh,sh,mix)
            true_base=prob(TRUE,qb,sb,True); pred_base=prob(th,qb,sb,mix)
            true_post=prob(TRUE,qb+SHIFT,sb,True); pred_post=prob(th,qb+SHIFT,sb,mix)
            true_stress=prob(TRUE,qs,ss,True); pred_stress=prob(th,qs,ss,mix)
            reps.append({'rep':repkey,'n':n,'seed':seed,'estimator':est,'model':'mixture' if mix else 'single',
              'theta':json.dumps(th.tolist()),'objective':sel['objective'],'software_success':sel['software_success'],
              'numerical_accept':sel['numerical_accept'],'active_bounds':sel['active_bounds'],'geometry':inf['geometry'],
              'inference_eligible':inf['inference_eligible'],'se':json.dumps(inf['se']),'cover':json.dumps(inf['cover']),
              'holdout_rmse':np.sqrt(np.mean((pred_hold-true_hold)**2)),'baseline_rmse':np.sqrt(np.mean((pred_base-true_base)**2)),
              'post_policy_rmse':np.sqrt(np.mean((pred_post-true_post)**2)),'stress_rmse':np.sqrt(np.mean((pred_stress-true_stress)**2)),
              'policy_effect_hat':np.mean(pred_post-pred_base),'policy_effect_true':np.mean(true_post-true_base)})
    starts=pd.DataFrame(allstarts); rep=pd.DataFrame(reps); data=pd.concat(datasets,ignore_index=True)
    starts.to_csv(OUT/'start_records.csv',index=False,encoding='utf-8-sig'); rep.to_csv(OUT/'replication_results.csv',index=False,encoding='utf-8-sig')
    data.to_parquet(OUT/'simulated_training.parquet',index=False)
    target=rep[(rep['n']==600)&(rep.seed==104)&(rep.estimator=='mle')&(rep.model=='mixture')].iloc[0]
    dd=data[data.rep==target.rep]; prof=profile_delta(dd.q.to_numpy(),dd.s.to_numpy(),dd.y.to_numpy(),np.array(json.loads(target.theta)))
    prof.to_csv(OUT/'profile_delta.csv',index=False,encoding='utf-8-sig')
    summary=[]
    for keys,g in rep.groupby(['n','estimator','model']):
        mix=g.model.iloc[0]=='mixture'; row={'n':keys[0],'estimator':keys[1],'model':keys[2],'replications':len(g),
          'software_success_rate':g.software_success.mean(),'numerical_accept_rate':g.numerical_accept.mean(),
          'boundary_rate':g.active_bounds.ne('').mean(),'inference_eligible_rate':g.inference_eligible.mean(),
          'holdout_rmse_mean':g.holdout_rmse.mean(),'baseline_rmse_mean':g.baseline_rmse.mean(),'post_policy_rmse_mean':g.post_policy_rmse.mean(),
          'stress_rmse_mean':g.stress_rmse.mean(),'policy_bias_mean':(g.policy_effect_hat-g.policy_effect_true).mean()}
        if mix:
            cov=np.array([json.loads(x) for x in g.cover]); elig=g.inference_eligible.to_numpy()
            for j,name in enumerate(['b_s','a_q','k_low','delta','pi_low']):
                row['coverage_all_'+name]=cov[:,j].mean(); row['coverage_conditional_'+name]=cov[elig,j].mean() if elig.any() else np.nan
        summary.append(row)
    pd.DataFrame(summary).to_csv(OUT/'monte_carlo_summary.csv',index=False,encoding='utf-8-sig')
    meta={'true_parameters':dict(zip(['b_s','a_q','k_low','delta','pi_low'],TRUE)),'k_high':TRUE[2]+TRUE[3],
      'normalization':'EV1 scale normalized to 1; low-cost type first; delta=k_high-k_low>0; pi is low-cost mass',
      'supports':{'training':TRAIN,'interpolation_holdout':HOLD,'baseline_policy_population':BASE,'price_shift':SHIFT,'post_policy':POST,'stress':STRESS},
      'optimizer_boxes':{'mixture':BOUNDS_MIX,'single':BOUNDS_ONE},'profile_economic_delta_bounds':[.10,3.00],
      'sample_sizes':SIZES,'seeds':SEEDS,'starts_per_fit':NSTART,'kkt_tolerance':KKT_TOL,
      'versions':{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'platform':platform.platform()},
      'skill_repo':'C:/Users/ENAN/junzi-economist-skill','skill_commit':'e25b4d0'}
    (OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps({'replications':len(rep),'starts':len(starts),'accepted':int(starts.numerical_accept.sum()),'profile_rows':len(prof)},indent=2))
if __name__=='__main__': main()
