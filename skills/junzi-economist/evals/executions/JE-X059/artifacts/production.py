import csv, hashlib, json, math, platform
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"
OUT.mkdir(exist_ok=True)
SEED, N, T, DELTA = 20260713, 800, 8, 0.90
TRUE_THETA = np.array([-0.45, 1.15])
REGIMES = np.array([0.0, 0.4])
BOUNDS = [(-2.0, 1.0), (0.0, 2.5)]
STARTS = np.array([[-1.8,.15],[-1.2,2.2],[-.7,.7],[-.1,1.8],[.7,.25],[.8,2.3],[-.45,1.15]])
PG_SCALE = 1e-6
FD_STEP = 2e-5
EULER = 0.5772156649015329

# rows: current state, action; probability next state=1
P1_TRUE = np.array([[0.18, 0.08], [0.82, 0.35]])

def logsum(v):
    m = np.max(v, axis=1)
    return m + np.log(np.exp(v[:,0]-m) + np.exp(v[:,1]-m))

def solve_value(theta, subsidy, p1, tol=1e-13):
    V = np.zeros(2)
    for it in range(10000):
        u1 = theta[0] + theta[1]*np.arange(2) + subsidy
        ev0 = (1-p1[:,0])*V[0] + p1[:,0]*V[1]
        ev1 = (1-p1[:,1])*V[0] + p1[:,1]*V[1]
        W = np.column_stack((DELTA*ev0, u1 + DELTA*ev1))
        Vn = logsum(W)
        if np.max(np.abs(Vn-V)) < tol:
            return Vn, it+1, float(np.max(np.abs(Vn-V)))
        V = Vn
    raise RuntimeError("Bellman iteration failed")

def probs_nfxp(theta, subsidies, states, p1):
    ans = np.empty(len(states))
    for z in REGIMES:
        V,_,_ = solve_value(theta, z, p1)
        ev0 = (1-p1[:,0])*V[0] + p1[:,0]*V[1]
        ev1 = (1-p1[:,1])*V[0] + p1[:,1]*V[1]
        d = theta[0] + theta[1]*np.arange(2) + z + DELTA*(ev1-ev0)
        mask = subsidies == z
        ans[mask] = 1/(1+np.exp(-d[states[mask]]))
    return ans

def simulate():
    rng = np.random.default_rng(SEED)
    regimes = REGIMES[np.arange(N) % 2]
    states = rng.integers(0,2,size=N)
    rows=[]
    for t in range(T):
        pr = probs_nfxp(TRUE_THETA, regimes, states, P1_TRUE)
        a = (rng.random(N)<pr).astype(np.int8)
        nxt = (rng.random(N)<P1_TRUE[states,a]).astype(np.int8)
        rows.extend(zip(np.arange(N),np.full(N,t),states,a,nxt,regimes))
        states=nxt
    arr=np.asarray(rows,float)
    return {"id":arr[:,0].astype(np.int32),"t":arr[:,1].astype(np.int8),
            "state":arr[:,2].astype(np.int8),"action":arr[:,3].astype(np.int8),
            "next_state":arr[:,4].astype(np.int8),"subsidy":arr[:,5]}

def transition_mle(d):
    p=np.empty((2,2)); counts=[]
    for s in range(2):
      for a in range(2):
        m=(d['state']==s)&(d['action']==a); n=int(m.sum()); y=int(d['next_state'][m].sum())
        p[s,a]=y/n; counts.append({"state":s,"action":a,"n":n,"next_one":y,"p1":p[s,a]})
    return p,counts

def nll_nfxp(theta,d,p1):
    p=probs_nfxp(theta,d['subsidy'],d['state'],p1)
    p=np.clip(p,1e-12,1-1e-12)
    return float(-np.sum(d['action']*np.log(p)+(1-d['action'])*np.log(1-p)))

def empirical_ccp(d):
    p=np.empty((2,2)); counts=[]
    for r,z in enumerate(REGIMES):
      for s in range(2):
        m=(d['subsidy']==z)&(d['state']==s); n=int(m.sum()); y=int(d['action'][m].sum())
        # exact empirical cell frequency; data design guarantees interiors
        p[r,s]=y/n; counts.append({"regime":float(z),"state":s,"n":n,"ones":y,"ccp":p[r,s]})
    if np.any((p<=0)|(p>=1)): raise RuntimeError("CCP support cell at boundary")
    return p,counts

def probs_ccp(theta, subsidies, states, p1, ccp):
    ans=np.empty(len(states)); S=np.arange(2)
    for r,z in enumerate(REGIMES):
        q=ccp[r]
        Pmix=(1-q)[:,None]*np.column_stack((1-p1[:,0],p1[:,0])) + q[:,None]*np.column_stack((1-p1[:,1],p1[:,1]))
        flow=q*(theta[0]+theta[1]*S+z) + EULER-(1-q)*np.log(1-q)-q*np.log(q)
        V=np.linalg.solve(np.eye(2)-DELTA*Pmix,flow)
        ev0=(1-p1[:,0])*V[0]+p1[:,0]*V[1]
        ev1=(1-p1[:,1])*V[0]+p1[:,1]*V[1]
        diff=theta[0]+theta[1]*S+z+DELTA*(ev1-ev0)
        mask=subsidies==z; ans[mask]=1/(1+np.exp(-diff[states[mask]]))
    return ans

def nll_ccp(theta,d,p1,ccp):
    p=np.clip(probs_ccp(theta,d['subsidy'],d['state'],p1,ccp),1e-12,1-1e-12)
    return float(-np.sum(d['action']*np.log(p)+(1-d['action'])*np.log(1-p)))

def central_grad(fun,x):
    g=np.empty_like(x,dtype=float)
    for j in range(len(x)):
        h=FD_STEP*max(1.,abs(x[j])); xp=x.copy(); xm=x.copy(); xp[j]+=h; xm[j]-=h
        # one-sided only if a central step would leave the declared box
        if xp[j]>BOUNDS[j][1]: xp[j]=x[j]; g[j]=(fun(xp)-fun(xm))/(xp[j]-xm[j])
        elif xm[j]<BOUNDS[j][0]: xm[j]=x[j]; g[j]=(fun(xp)-fun(xm))/(xp[j]-xm[j])
        else: g[j]=(fun(xp)-fun(xm))/(2*h)
    return g

def projected_grad(x,g):
    pg=g.copy()
    for j,(lo,hi) in enumerate(BOUNDS):
        if x[j] <= lo+1e-10: pg[j]=min(g[j],0.0)
        elif x[j] >= hi-1e-10: pg[j]=max(g[j],0.0)
    return pg

def fit_all(name,fun):
    rows=[]
    for k,start in enumerate(STARTS):
        res=minimize(fun,start,method='L-BFGS-B',bounds=BOUNDS,options={'ftol':1e-13,'gtol':1e-10,'maxiter':2000})
        x=np.asarray(res.x); obj=float(fun(x)); g=central_grad(fun,x); pg=projected_grad(x,g)
        tol=PG_SCALE*(1+abs(obj)); accepted=bool(np.max(np.abs(pg))<=tol)
        rows.append({'estimator':name,'start_id':k,'start':start.tolist(),'terminal':x.tolist(),
          'objective':obj,'raw_gradient':g.tolist(),'projected_gradient':pg.tolist(),
          'pg_norm_inf':float(np.max(np.abs(pg))),'declared_pg_tolerance':tol,'accepted':accepted,
          'solver_success_record_only':bool(res.success),'solver_status_record_only':int(res.status),
          'solver_message_record_only':str(res.message),'iterations_record_only':int(res.nit)})
    eligible=[r for r in rows if r['accepted']]
    if not eligible: raise RuntimeError(name+' has no independently KKT-eligible start')
    best=min(eligible,key=lambda r:r['objective'])
    for r in rows:r['distance_from_selected_objective']=r['objective']-best['objective']
    return rows,best

def cell_probs(theta,p1,method,ccp=None, regimes=REGIMES):
    vals=[]
    for z in regimes:
      st=np.array([0,1]); zs=np.full(2,z)
      pp=probs_nfxp(theta,zs,st,p1) if method=='nfxp' else probs_ccp(theta,zs,st,p1,ccp)
      vals.extend(pp.tolist())
    return np.array(vals)

def local_rank(theta,p1):
    h=1e-5; J=np.empty((4,2))
    for j in range(2):
      xp=theta.copy();xm=theta.copy();xp[j]+=h;xm[j]-=h
      J[:,j]=(cell_probs(xp,p1,'nfxp')-cell_probs(xm,p1,'nfxp'))/(2*h)
    sv=np.linalg.svd(J,compute_uv=False)
    return {'population_mapping':'four exact model CCPs at states x observed regimes','jacobian':J.tolist(),
      'singular_values':sv.tolist(),'numerical_rank_tolerance':1e-8,'rank':int(np.sum(sv>1e-8)),
      'scope':'local population-rank evidence under fixed estimated controlled transitions; not global identification'}

def policy_and_accounting(theta,p1):
    rows=[]
    for z,label,support in [(0.,'observed_baseline','observed'),(.2,'midpoint_counterfactual','model_interpolation'),(.4,'observed_high','observed')]:
      V,_,res=solve_value(theta,z,p1); pr=cell_probs(theta,p1,'nfxp',regimes=np.array([z]))
      Ppol=np.empty((2,2))
      for s in range(2): Ppol[s]=(1-pr[s])*np.array([1-p1[s,0],p1[s,0]])+pr[s]*np.array([1-p1[s,1],p1[s,1]])
      pi1=Ppol[0,1]/(Ppol[0,1]+Ppol[1,0]); stat=np.array([1-pi1,pi1]); uptake=float(stat@pr)
      transfer=float(z*uptake); resource_cost=float(0.30*uptake); net_resource=float(resource_cost)
      rows.append({'subsidy':z,'label':label,'support':support,'stationary_state1':float(pi1),'stationary_action1':uptake,
        'government_transfer_per_period':transfer,'real_resource_cost_per_period':resource_cost,
        'social_resource_accounting_excludes_transfer':net_resource,'private_value_state0':float(V[0]),'bellman_residual':res})
    return rows

def restricted_grid(d,p1):
    # Exact finite closed evaluated domain A x B, including all boundaries. Hard restriction a+b<=0.50.
    A=np.linspace(-1.5,.5,9); B=np.linspace(.25,2.25,9); rows=[]
    for i,a in enumerate(A):
      for j,b in enumerate(B):
        slack=.50-(a+b); feasible=slack>=0.0
        rows.append({'i':i,'j':j,'theta0':float(a),'theta1':float(b),'lower_or_upper_boundary':bool(i in (0,8) or j in (0,8)),
          'restriction_slack':float(slack),'restriction_boundary':bool(slack==0.0),'feasible':bool(feasible),
          'objective':nll_nfxp(np.array([a,b]),d,p1) if feasible else None})
    return rows,{'theta0_grid':A.tolist(),'theta1_grid':B.tolist(),'cartesian_rows_expected':81,'cartesian_rows_saved':len(rows),
      'closed_domain':True,'all_boundaries_included':True,'hard_restriction':'theta0 + theta1 <= 0.50',
      'feasible_count':sum(r['feasible'] for r in rows),'infeasible_count':sum(not r['feasible'] for r in rows),
      'restriction_boundary_count':sum(r['restriction_boundary'] for r in rows)}

def dump_json(path,obj): path.write_text(json.dumps(obj,indent=2,sort_keys=True),encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    d=simulate(); np.savez_compressed(OUT/'raw_primitives.npz',**d)
    p1,tr=transition_mle(d); ccp,cc=empirical_ccp(d)
    nrows,nbest=fit_all('NFXP',lambda x:nll_nfxp(x,d,p1))
    crows,cbest=fit_all('CCP_two_step',lambda x:nll_ccp(x,d,p1,ccp))
    starts=nrows+crows; dump_json(OUT/'starts.json',starts)
    grid,gmeta=restricted_grid(d,p1); dump_json(OUT/'restricted_grid.json',{'metadata':gmeta,'rows':grid})
    rank=local_rank(np.array(nbest['terminal']),p1); pol=policy_and_accounting(np.array(nbest['terminal']),p1)
    summary={'specification':{'states':[0,1],'actions':[0,1],'discount':DELTA,'utility_action1':'theta0 + theta1*state + subsidy','utility_action0':0,
      'shock':'iid type-I extreme value, scale normalized to one','observed_regimes':REGIMES.tolist(),'counterfactual_regime':.2,'sample_predeclared':{'agents':N,'periods':T,'rows':N*T},
      'true_theta_simulation_only':TRUE_THETA.tolist(),'transition_truth_simulation_only':P1_TRUE.tolist()},
      'acceptance_rule':{'only_rule':'independently recomputed projected-gradient infinity norm <= 1e-6*(1+abs(objective))','fd_step':'2e-5*max(1,abs(parameter))','solver_success_message_ftol':'recorded but never used for acceptance or selection'},
      'transition_estimates':p1.tolist(),'transition_counts':tr,'empirical_ccp':ccp.tolist(),'empirical_ccp_counts':cc,
      'selected':{'NFXP':nbest,'CCP_two_step':cbest},'local_population_rank':rank,'policy_accounting':pol,
      'restricted_domain':gmeta,'estimator_distinction':'NFXP solves the Bellman fixed point at every likelihood evaluation; CCP_two_step fixes empirical conditional choice probabilities and uses a policy-evaluation linear system, with no Bellman optimality solve in its criterion.',
      'claim_status':'model-implied, locally rank-supported, simulated-data demonstration; no global or external identification claim'}
    dump_json(OUT/'summary.json',summary)
    files=['raw_primitives.npz','starts.json','restricted_grid.json','summary.json']
    manifest={'production_files':{f:{'sha256':sha(OUT/f),'bytes':(OUT/f).stat().st_size} for f in files},
      'counts':{'raw_rows':len(d['state']),'starts_total':len(starts),'restricted_rows':len(grid),'policy_rows':len(pol)}}
    dump_json(OUT/'manifest.json',manifest)
    print(json.dumps({'NFXP':nbest['terminal'],'CCP':cbest['terminal'],'accepted_starts':sum(r['accepted'] for r in starts)},indent=2))

if __name__=='__main__': main()
