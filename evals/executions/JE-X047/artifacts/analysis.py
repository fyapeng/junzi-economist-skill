import json, platform, sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, minimize_scalar, differential_evolution
from scipy.special import expit, logsumexp

OUT=Path(__file__).resolve().parent; SEED=47013; rng=np.random.default_rng(SEED)
X=np.arange(5); X2=X**2; TRUE=np.array([0.18,3.20,0.91]); SUB_OBS=np.array([0.0,0.75])
N,T=2400,40; BOUNDS=[(0.001,0.8),(0.1,8.0),(0.55,0.995)]
Pr=np.zeros((5,5))
for x in X:
    for d,p in [(0,.58),(1,.32),(2,.10)]: Pr[x,min(4,x+d)]+=p
Po=np.tile(np.array([.86,.14,0,0,0]),(5,1))

def bellman(par,sub,Pr_=Pr,Po_=Po,tol=1e-12):
    th,F,beta=par; V=np.zeros(5)
    for it in range(20000):
        vr=-th*X2+beta*Pr_.dot(V); vo=-F+sub+beta*Po_.dot(V)
        z=np.logaddexp(vr,vo) # EV1 shocks shifted by -Euler gamma: Emax level is logsumexp
        if np.max(np.abs(z-V))<tol: break
        V=z
    return V,expit(vo-vr),it+1,float(np.max(np.abs(z-V)))

def simulate(par,N=N,T=T,seed=SEED):
    rr=np.random.default_rng(seed); rows=[]
    for i in range(N):
        s=float(SUB_OBS[i%2]); x=int(rr.choice(5,p=np.array([.45,.25,.15,.10,.05])))
        _,p,_it,_res=bellman(par,s)
        for t in range(T):
            a=int(rr.random()<p[x]); pn=Po[x] if a else Pr[x]; xn=int(rr.choice(5,p=pn))
            rows.append((i,t,s,x,a,xn)); x=xn
    return np.asarray(rows,float)

data=simulate(TRUE); np.save(OUT/'panel.npy',data)

def estimate_transitions(d):
    cr=np.zeros((5,5)); co=np.zeros(5)
    for row in d:
        x,a,xn=int(row[3]),int(row[4]),int(row[5])
        if a: co[xn]+=1
        else: cr[x,xn]+=1
    # constrained support MLE; zero cells outside declared supports remain zero
    er=np.zeros_like(cr)
    for x in X:
        allowed=np.unique([x,min(4,x+1),min(4,x+2)])
        er[x,allowed]=cr[x,allowed]/cr[x,allowed].sum()
    eo=np.tile(co/co.sum(),(5,1))
    return er,eo,cr,co
Prh,Poh,cr,co=estimate_transitions(data)

def nll(par,beta_fixed=None,d=data):
    if beta_fixed is not None: par=np.array([par[0],par[1],beta_fixed])
    ll=0.0
    for s in SUB_OBS:
        _,p,_,_=bellman(par,float(s),Prh,Poh)
        ds=d[d[:,2]==s]; a=ds[:,4].astype(int); x=ds[:,3].astype(int); pp=np.clip(p[x],1e-12,1-1e-12)
        ll-=np.sum(a*np.log(pp)+(1-a)*np.log(1-pp))
    return float(ll)

def fdgrad(fun,z):
    z=np.asarray(z,float); g=np.empty(len(z))
    for j in range(len(z)):
        h=1e-5*max(1,abs(z[j])); zp=z.copy(); zm=z.copy(); zp[j]+=h; zm[j]-=h
        g[j]=(fun(zp)-fun(zm))/(2*h)
    return g

def projected(g,z,bounds):
    q=np.array(g,float); active=[]
    for j,(lo,hi) in enumerate(bounds):
        if z[j]<=lo+1e-7:
            active.append(f'{j}:lower'); q[j]=min(g[j],0.0)
        elif z[j]>=hi-1e-7:
            active.append(f'{j}:upper'); q[j]=max(g[j],0.0)
    return q,active

def multistart(fun,starts,bounds,label):
    rec=[]
    for st in starts:
        r=minimize(fun,st,method='L-BFGS-B',bounds=bounds,options={'ftol':1e-11,'gtol':1e-7,'maxiter':800})
        raw=fdgrad(fun,r.x); pg,act=projected(raw,r.x,bounds)
        rec.append({'label':label,'initial':list(map(float,st)),'final':r.x.tolist(),'objective':float(r.fun),
                    'raw_gradient':raw.tolist(),'projected_gradient':pg.tolist(),'projected_gradient_inf':float(np.max(np.abs(pg))),
                    'active_bounds':act,'success':bool(r.success),'status':int(r.status),'message':str(r.message),'nit':int(r.nit)})
    best=min(x['objective'] for x in rec)
    for x in rec: x['objective_distance']=x['objective']-best; x['kkt_accepted']=x['projected_gradient_inf']<1e-2
    eligible=[x for x in rec if x['kkt_accepted']]
    return rec,min(eligible if eligible else rec,key=lambda q:q['objective'])

starts3=[[.08,2,.7],[.18,3.2,.91],[.4,5,.98],[.7,7,.6],[.25,1,.85],[.05,6,.95]]
fullrec,best=multistart(nll,starts3,BOUNDS,'full_nfxp')
fixedrec,fixedbest=multistart(lambda z:nll(z,TRUE[2]),[[.05,1],[.18,3.2],[.5,6],[.75,7.5]],BOUNDS[:2],'fixed_beta_nfxp')

# Distinct CCP estimator: cell frequencies -> Hotz-Miller log-odds and run-reference value equation; no Bellman solve.
def ccp_est(beta):
    A=[]; y=[]; w=[]; cells={}
    for s in SUB_OBS:
        ps=[]; ns=[]
        for x in X:
            q=data[(data[:,2]==s)&(data[:,3]==x),4]; n=len(q); p=(q.sum()+.5)/(n+1); ps.append(p); ns.append(n)
        ps=np.array(ps); V0=np.linalg.solve(np.eye(5)-beta*Prh,-np.log(1-ps))
        V1=np.linalg.solve(np.eye(5)-beta*Prh,-X2)
        # delta-s = -F + theta[x2 + beta(Po-Pr)V1] + beta(Po-Pr)V0
        delta=np.log(ps/(1-ps)); rhs=delta-s-beta*(Poh-Prh).dot(V0)
        reg=np.c_[X2+beta*(Poh-Prh).dot(V1),-np.ones(5)]
        A.append(reg); y.append(rhs); w.extend(ns); cells[str(s)]={'p_overhaul':ps.tolist(),'n':ns}
    A=np.vstack(A); y=np.hstack(y); W=np.sqrt(np.array(w))[:,None]
    coef=np.linalg.lstsq(W*A,W[:,0]*y,rcond=None)[0]
    return np.array([coef[0],coef[1],beta]),cells,float(np.sum((W[:,0]*(A@coef-y))**2))
ccp,cells,ccp_obj=ccp_est(TRUE[2])

# Continuous beta profile, with every inner start retained.
profile_trace=[]
def prof_obj(beta):
    rec,b=multistart(lambda z:nll(z,float(beta)),[[.08,2],[.18,3.2],[.5,6]],BOUNDS[:2],f'profile_beta={beta:.12g}')
    profile_trace.append({'beta':float(beta),'starts':rec,'best':b}); return b['objective']
pr=minimize_scalar(prof_obj,bounds=BOUNDS[2],method='bounded',options={'xatol':2e-6,'maxiter':80})
prof_beta=float(pr.x); prof_best=profile_trace[int(np.argmin([q['best']['objective'] for q in profile_trace]))]['best']

def logits(par):
    return np.hstack([np.log(np.clip(bellman(par,float(s))[1],1e-12,1)/np.clip(1-bellman(par,float(s))[1],1e-12,1)) for s in SUB_OBS])
base=logits(TRUE); J=np.empty((10,3))
for j,h in enumerate([1e-5,1e-5,1e-5]):
    up=TRUE.copy(); dn=TRUE.copy(); up[j]+=h; dn[j]-=h; J[:,j]=(logits(up)-logits(dn))/(2*h)
sv=np.linalg.svd(J,compute_uv=False); rank=int(np.linalg.matrix_rank(J,tol=1e-7))

# Search continuous box outside a radius around truth for closest CCP vector.
sc=np.array([.2,2,.1])
def alt_obj(z):
    dist=np.linalg.norm((np.asarray(z)-TRUE)/sc)
    pen=1e3*max(0,1-dist)**2
    return float(np.max(np.abs(expit(logits(z))-expit(base)))+pen)
de=differential_evolution(alt_obj,BOUNDS,seed=SEED,popsize=18,maxiter=220,tol=1e-9,polish=True)
alt=de.x; alt_gap=float(np.max(np.abs(expit(logits(alt))-expit(base))))

def stationary(P):
    A=np.vstack([P.T-np.eye(5),np.ones(5)]); b=np.r_[np.zeros(5),1.]; return np.linalg.lstsq(A,b,rcond=None)[0]
def policy_account(par,s):
    V,p,_,_=bellman(par,s,Prh,Poh); P=(1-p)[:,None]*Prh+p[:,None]*Poh; mu=stationary(P)
    flow_private=np.sum(mu*((1-p)*(-par[0]*X2)+p*(-par[1]+s)))
    transfer=np.sum(mu*p*s); resources=np.sum(mu*((1-p)*par[0]*X2+p*par[1])); social=-resources
    return {'subsidy':s,'overhaul_rate':float(mu@p),'private_inclusive_value_initial_stationary':float(mu@V),
            'private_deterministic_flow':float(flow_private),'government_transfer_flow':float(transfer),
            'real_resource_cost_flow':float(resources),'social_welfare_flow_excluding_EV_shocks':float(social)}
cf=[]
for kind,ss in [('observed',[0,.75]),('interpolation',[.25,.5]),('extrapolation',[1.25,2.0])]:
    for s in ss:
        z=policy_account(np.array(best['final']),s); z['support']=kind; cf.append(z)
basecf=next(z for z in cf if z['subsidy']==0)
for z in cf:
    z['private_value_difference_vs_s0']=z['private_inclusive_value_initial_stationary']-basecf['private_inclusive_value_initial_stationary']
    z['social_welfare_difference_vs_s0']=z['social_welfare_flow_excluding_EV_shocks']-basecf['social_welfare_flow_excluding_EV_shocks']

# Repeated-sample recovery demonstration only.
reps=[]
for k in range(16):
    dd=simulate(TRUE,N=450,T=25,seed=SEED+100+k)
    rec,b=multistart(lambda z:nll(z,TRUE[2],dd),[[.1,2],[.3,4.5]],BOUNDS[:2],f'recovery_{k}')
    reps.append({'rep':k,'estimate':b['final'],'accepted':b['kkt_accepted'],'objective':b['objective'],'starts':rec})

alltr={'full':fullrec,'fixed_beta':fixedrec,'profile':profile_trace,'recovery':reps}
(OUT/'full_start_traces.json').write_text(json.dumps(alltr,indent=2),encoding='utf-8')
res={'design':{'true':TRUE.tolist(),'N':N,'T':T,'seed':SEED,'observed_subsidies':SUB_OBS.tolist(),'EV1_normalization':'iid type-I extreme-value shocks shifted by minus Euler constant, so each shock has mean zero and E[max_a(v_a+eps_a)]=logsumexp(v); only value levels depend on this additive normalization'},
     'transition_estimates':{'run':Prh.tolist(),'overhaul':Poh.tolist(),'run_counts':cr.tolist(),'overhaul_counts':co.tolist()},
     'full_nfxp_best':best,'fixed_beta_nfxp_best':fixedbest,'ccp_fixed_beta':{'estimate':ccp.tolist(),'objective':ccp_obj,'cells':cells},
     'continuous_profile':{'beta':prof_beta,'objective':float(pr.fun),'success':bool(pr.success),'message':str(pr.message),'selected_inner':prof_best,'evaluations':len(profile_trace)},
     'population_local_identification':{'mapping':'10 population CCP logits (5 states x 2 observed subsidy regimes) as function of theta,F,beta at truth','jacobian':J.tolist(),'singular_values':sv.tolist(),'rank':rank,'claim':'full column rank implies local identification under maintained transition, EV1, stationarity, subsidy exogeneity, and parametric utility restrictions; it is not a global result'},
     'continuous_alternative_search':{'candidate':alt.tolist(),'max_abs_ccp_gap':alt_gap,'scaled_distance_from_truth':float(np.linalg.norm((alt-TRUE)/sc)),'optimizer_objective':float(de.fun),'success':bool(de.success),'claim':'bounded numerical search evidence, not proof of global injectivity'},
     'counterfactuals':cf,'recovery_demonstration':{'replications':len(reps),'N':450,'T':25,'fixed_beta':TRUE[2],'results':reps,'mean_estimate':np.mean([q['estimate'] for q in reps],axis=0).tolist(),'label':'finite repeated-sample recovery demonstration; not general estimator-performance or coverage support'},
     'versions':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform()}}
(OUT/'results.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps({'true':TRUE.tolist(),'full':best['final'],'fixed':fixedbest['final'],'ccp':ccp.tolist(),'profile_beta':prof_beta,'rank':rank,'sv':sv.tolist(),'alt':alt.tolist(),'alt_gap':alt_gap},indent=2))
