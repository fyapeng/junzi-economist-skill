import json, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize, differential_evolution
from scipy.special import logsumexp

OUT=Path(__file__).resolve().parent/'artifacts'; OUT.mkdir(exist_ok=True)
SEED=52077; rng=np.random.default_rng(SEED)
S=[(i,r) for i in range(3) for r in range(2)]; K=len(S); A=3
idx={x:j for j,x in enumerate(S)}; rebates=np.array([0.0,0.8])
true_th=np.array([1.15,1.35,2.10,0.91]) # insulation benefit, generator cost, retrofit cost, beta

def Pmats(q):
    # q[a,r]=Pr(next reliability=1); retrofit raises insulation with 0.82 probability.
    P=np.zeros((2,A,K,K))
    for g in range(2):
      for j,(ins,r) in enumerate(S):
       for a in range(A):
        for rn in range(2):
         pr=(q[a,r] if rn else 1-q[a,r])
         if a==2 and ins<2:
          P[g,a,j,idx[(ins+1,rn)]]+=.82*pr; P[g,a,j,idx[(ins,rn)]]+=.18*pr
         else: P[g,a,j,idx[(ins,rn)]]+=pr
    return P

qtrue=np.array([[.30,.78],[.43,.86],[.55,.91]])
def flow(th,g):
    b,cg,cr,_=th; u=np.zeros((K,A))
    for j,(ins,r) in enumerate(S):
      u[j,0]=b*ins + .65*r
      u[j,1]=b*ins + .95 - cg + .25*r
      u[j,2]=b*ins + .65*r - cr + rebates[g]
    return u

def solve(th,P,tol=1e-11):
    beta=th[3]; Vs=[]; CCP=[]; resid=[]; iters=[]
    for g in range(2):
      V=np.zeros(K)
      for it in range(100):
       v=flow(th,g)+beta*np.column_stack([P[g,a]@V for a in range(A)])
       lse=logsumexp(v,axis=1); p=np.exp(v-lse[:,None]); F=V-(np.euler_gamma+lse)
       if np.max(abs(F))<tol: break
       J=np.eye(K)-beta*sum(p[:,a,None]*P[g,a] for a in range(A))
       V=V-np.linalg.solve(J,F)
      v=flow(th,g)+beta*np.column_stack([P[g,a]@V for a in range(A)])
      Vs.append(V); CCP.append(np.exp(v-logsumexp(v,axis=1)[:,None])); resid.append(float(np.max(abs(V-(np.euler_gamma+logsumexp(v,axis=1)))))); iters.append(it+1)
    return np.array(Vs),np.array(CCP),{'residuals':resid,'iterations':iters}

Ptrue=Pmats(qtrue); _,cp0,_=solve(true_th,Ptrue)
# fixed intended population; no redraw or outcome-conditioned survival
N,T=1200,14; rows=[]
for n in range(N):
 g=n%2; s=int(rng.integers(K))
 for t in range(T):
  a=int(rng.choice(A,p=cp0[g,s])); sn=int(rng.choice(K,p=Ptrue[g,a,s])); rows.append((n,t,g,s,a,sn)); s=sn
d=np.array(rows,int)

# controlled reliability transitions and retrofit success estimated from all realized transitions
qhat=np.zeros((A,2)); counts=[]
for a in range(A):
 for r in range(2):
  m=(d[:,4]==a)&(np.array([S[x][1] for x in d[:,3]])==r); y=np.array([S[x][1] for x in d[m,5]])
  qhat[a,r]=(y.sum()+.5)/(len(y)+1); counts.append({'a':a,'r':r,'n':int(len(y)),'success':int(y.sum()),'qhat':float(qhat[a,r])})
P=Pmats(qhat)

trace=[]
choice_counts=np.zeros((2,K,A),dtype=int)
for g,s,a in d[:,[2,3,4]]: choice_counts[g,s,a]+=1
def unpack(z,restricted=False):
 b=np.exp(z[0]); cg=np.exp(z[1]); cr=np.exp(z[2]);
 beta=.55+((.23 if restricted else .44)/(1+np.exp(-z[3])))
 return np.array([b,cg,cr,beta])
def nllz(z,restricted=False,tag=''):
 th=unpack(z,restricted); _,cp,diag=solve(th,P,tol=1e-9)
 val=-np.sum(choice_counts*np.log(cp+1e-300))
 return val

starts=rng.normal(size=(6,4)); starts[:,:3]+=np.log([1.0,1.2,1.8]); starts[:,3]+=1.0
local=[]
for k,z0 in enumerate(starts):
 r=minimize(nllz,z0,args=(False,'nfxp'),method='L-BFGS-B',options={'maxiter':400,'ftol':1e-11})
 local.append({'start_id':k,'initial_z':z0.tolist(),'terminal_z':r.x.tolist(),'theta':unpack(r.x).tolist(),'objective':float(r.fun),'success':bool(r.success),'nit':int(r.nit),'message':str(r.message)})
best=min(local,key=lambda x:x['objective']); zbest=np.array(best['terminal_z']); thhat=unpack(zbest); Vhat,cphat,fpdiag=solve(thhat,P)

# Distinct two-step CCP minimum distance: empirical CCP inversion, then value equation under action 0.
cnt=np.ones((2,K,A))*.5
for g,s,a in d[:,[2,3,4]]: cnt[g,s,a]+=1
ecp=cnt/cnt.sum(axis=2,keepdims=True)
def ccp_obj(z):
 th=unpack(z); beta=th[3]; rr=[]
 for g in range(2):
  u=flow(th,g); EV=np.linalg.solve(np.eye(K)-beta*P[g,0],u[:,0]-np.log(ecp[g,:,0])+np.euler_gamma)
  for a in (1,2): rr.extend((np.log(ecp[g,:,a]/ecp[g,:,0])-(u[:,a]-u[:,0]+beta*(P[g,a]-P[g,0])@EV)).tolist())
 return np.mean(np.square(rr))
ccpr=minimize(ccp_obj,zbest,method='BFGS',options={'maxiter':1000,'gtol':1e-8})

# Continuous local population rank: Jacobian of exact population CCP log-odds and controlled transition probabilities.
def popmap(th):
 _,c,_=solve(th,Ptrue); return np.r_[np.log(c[:,:,1]/c[:,:,0]).ravel(),np.log(c[:,:,2]/c[:,:,0]).ravel(),qtrue.ravel()]
h=1e-5; J=np.column_stack([(popmap(true_th+np.eye(4)[j]*h)-popmap(true_th-np.eye(4)[j]*h))/(2*h) for j in range(4)])
sv=np.linalg.svd(J,compute_uv=False); rank=int((sv>sv[0]*1e-7).sum())

# Restricted alternative: beta <= .78 by construction. Save full DE initial population + generation-best trace.
de_init=rng.uniform([-1,-1,-1,-5],[1.5,1.5,1.5,5],size=(32,4)); de_trace=[]
def cb(x,convergence):
 de_trace.append({'generation':len(de_trace),'z':x.tolist(),'theta':unpack(x,True).tolist(),'objective':float(nllz(x,True)),'convergence':float(convergence)})
de=differential_evolution(lambda z:nllz(z,True),[(-2,2),(-2,2),(-2,2),(-8,8)],init=de_init,popsize=8,maxiter=30,tol=1e-7,polish=False,seed=SEED+1,callback=cb,workers=1)
polish=[]
for k,z0 in enumerate([de.x,*de_init[np.argsort([nllz(z,True) for z in de_init])[:7]]]):
 r=minimize(lambda z:nllz(z,True),z0,method='L-BFGS-B',bounds=[(-2,2)]*3+[(-8,8)],options={'maxiter':500,'ftol':1e-12})
 polish.append({'start_id':k,'initial_z':np.asarray(z0).tolist(),'terminal_z':r.x.tolist(),'theta':unpack(r.x,True).tolist(),'objective':float(r.fun),'success':bool(r.success),'nit':int(r.nit)})
alt=min(polish,key=lambda x:x['objective']); alt_th=np.array(alt['theta']); slack=.78-alt_th[3]; feas=slack>=-1e-12

# Counterfactual: unobserved rebate 0.4 is interpolation; benefit paid only for retrofit.
def cf(th,reb):
 old=rebates.copy(); rebates[0]=rebates[1]=reb
 V,c,_=solve(th,P); rebates[:]=old
 dist=np.ones(K)/K
 for _ in range(300): dist=sum(np.diag(dist@P[0,a])@np.ones((K,K))*0 for a in []) if False else sum((dist*c[0,:,a])@P[0,a] for a in range(A))
 u=flow(th,0); # resource utility excludes policy transfer/rebate; reset baseline regime flow then adjust action-2 private payoff
 private=float(np.sum(dist[:,None]*c[0]*(u+np.array([0,0,reb])))); transfers=float(reb*np.sum(dist*c[0,:,2])); resources=float(np.sum(dist*c[0,:,1])*cg_resource + np.sum(dist*c[0,:,2])*1.1)
 welfare=private-transfers-resources
 return {'rebate':reb,'private_flow_payoff':private,'government_transfers':transfers,'real_resource_cost':resources,'social_welfare_flow':welfare,'retrofit_share':float(np.sum(dist*c[0,:,2]))}
cg_resource=.55
cfs=[cf(thhat,x) for x in (0,.4,.8)]

summary={'seed':SEED,'sample':{'N':N,'T':T,'rows':len(d),'regimes_observed':[0,.8]},'transition_estimates':counts,'true_theta':true_th.tolist(),'nfxp_theta':thhat.tolist(),'nfxp_objective':best['objective'],'fixed_point':fpdiag,'ccp_theta':unpack(ccpr.x).tolist(),'ccp_objective':float(ccpr.fun),'population_local_rank':{'rank':rank,'columns':4,'singular_values':sv.tolist(),'claim':'continuous local population rank under maintained state/action support and normalization; no global identification claim'},'restricted_alternative':{'restriction':'beta <= 0.78 via beta=0.55+0.23*logistic(z)','theta':alt_th.tolist(),'objective':alt['objective'],'objective_gap':alt['objective']-best['objective'],'realized_slack':float(slack),'acceptance_tolerance':1e-12,'feasible':bool(feas)},'policy_support':{'observed':[0,.8],'model_based_interpolation':[.4],'extrapolation':[]},'counterfactuals':cfs,'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(OUT/'local_starts.json').write_text(json.dumps(local,indent=2),encoding='utf-8')
(OUT/'restricted_search.json').write_text(json.dumps({'initial_population':[{'z':z.tolist(),'objective':float(nllz(z,True))} for z in de_init],'generation_trace':de_trace,'polish_starts':polish},indent=2),encoding='utf-8')
np.savez_compressed(OUT/'simulation.npz',data=d,qhat=qhat,empirical_ccp=ecp,jacobian=J)
print(json.dumps(summary,indent=2))
