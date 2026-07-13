"""Independent last-stage verifier: no imports from production.py and no trust in saved diagnostics."""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np

R=Path(__file__).resolve().parent; O=R/'artifacts'; DELTA=.90; REG=np.array([0.,.4]); B=[(-2.,1.),(0.,2.5)]; H=2e-5; E=.5772156649015329
def loadj(n): return json.loads((O/n).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lse(w):
 m=w.max(1);return m+np.log(np.exp(w[:,0]-m)+np.exp(w[:,1]-m))
def value(x,z,P):
 v=np.zeros(2)
 for _ in range(20000):
  u=x[0]+x[1]*np.arange(2)+z;e0=(1-P[:,0])*v[0]+P[:,0]*v[1];e1=(1-P[:,1])*v[0]+P[:,1]*v[1];vn=lse(np.c_[DELTA*e0,u+DELTA*e1])
  if abs(vn-v).max()<1e-13:return vn
  v=vn
 raise AssertionError('value')
def pn(x,zs,s,P):
 out=np.empty(len(s))
 for z in REG:
  v=value(x,z,P);d=x[0]+x[1]*np.arange(2)+z+DELTA*((1-P[:,1])*v[0]+P[:,1]*v[1]-(1-P[:,0])*v[0]-P[:,0]*v[1]);m=zs==z;out[m]=1/(1+np.exp(-d[s[m]]))
 return out
def pc(x,zs,s,P,Q):
 out=np.empty(len(s))
 for k,z in enumerate(REG):
  q=Q[k];Pm=(1-q)[:,None]*np.c_[1-P[:,0],P[:,0]]+q[:,None]*np.c_[1-P[:,1],P[:,1]]
  f=q*(x[0]+x[1]*np.arange(2)+z)+E-(1-q)*np.log(1-q)-q*np.log(q);v=np.linalg.solve(np.eye(2)-DELTA*Pm,f)
  d=x[0]+x[1]*np.arange(2)+z+DELTA*((1-P[:,1])*v[0]+P[:,1]*v[1]-(1-P[:,0])*v[0]-P[:,0]*v[1]);m=zs==z;out[m]=1/(1+np.exp(-d[s[m]]))
 return out
def obj(x,a,z,s,P,Q,kind):
 p=pn(x,z,s,P) if kind=='NFXP' else pc(x,z,s,P,Q);p=np.clip(p,1e-12,1-1e-12);return float(-sum(a*np.log(p)+(1-a)*np.log(1-p)))
def grad(f,x):
 g=np.empty(2)
 for j in range(2):
  h=H*max(1,abs(x[j]));xp=x.copy();xm=x.copy();xp[j]+=h;xm[j]-=h
  if xp[j]>B[j][1]:xp[j]=x[j];g[j]=(f(xp)-f(xm))/(xp[j]-xm[j])
  elif xm[j]<B[j][0]:xm[j]=x[j];g[j]=(f(xp)-f(xm))/(xp[j]-xm[j])
  else:g[j]=(f(xp)-f(xm))/(2*h)
 return g
def pg(x,g):
 y=g.copy()
 for j,(lo,hi) in enumerate(B):
  if x[j]<=lo+1e-10:y[j]=min(g[j],0)
  elif x[j]>=hi-1e-10:y[j]=max(g[j],0)
 return y
def close(a,b,t=2e-8):return np.max(np.abs(np.asarray(a)-np.asarray(b)))<=t
def main():
 failures=[]; raw=np.load(O/'raw_primitives.npz'); s=raw['state'];a=raw['action'];ns=raw['next_state'];z=raw['subsidy']
 P=np.empty((2,2)); tc=[]
 for i in range(2):
  for j in range(2):
   m=(s==i)&(a==j);P[i,j]=ns[m].mean();tc.append((i,j,int(m.sum()),int(ns[m].sum())))
 Q=np.empty((2,2));cc=[]
 for k,zz in enumerate(REG):
  for i in range(2):m=(z==zz)&(s==i);Q[k,i]=a[m].mean();cc.append((zz,i,int(m.sum()),int(a[m].sum())))
 sm=loadj('summary.json'); st=loadj('starts.json'); grid=loadj('restricted_grid.json')
 if not close(P,sm['transition_estimates']):failures.append('transitions')
 if not close(Q,sm['empirical_ccp']):failures.append('ccp')
 start_checks=[]
 for row in st:
  x=np.array(row['terminal']);f=lambda y:obj(y,a,z,s,P,Q,row['estimator']);o=f(x);g=grad(f,x);q=pg(x,g);tol=1e-6*(1+abs(o));acc=bool(abs(q).max()<=tol)
  # Independent Python summation order changes central differences by about 1e-5;
  # this audit tolerance is far below the predeclared objective-scaled KKT cutoff (~4e-3).
  ok=abs(o-row['objective'])<2e-8 and close(g,row['raw_gradient'],2e-5) and close(q,row['projected_gradient'],2e-5) and acc==row['accepted']
  if not ok:failures.append('start_'+str(row['estimator'])+'_'+str(row['start_id']))
  start_checks.append({'estimator':row['estimator'],'start_id':row['start_id'],'objective':o,'central_gradient':g.tolist(),'projected_gradient':q.tolist(),'tolerance':tol,'accepted':acc})
 selected={}
 for kind in ['NFXP','CCP_two_step']:
  elig=[x for x in start_checks if x['estimator']==kind and x['accepted']];best=min(elig,key=lambda r:r['objective']); saved=sm['selected'][kind]
  selected[kind]=best
  sx=np.array(saved['terminal']); sf=lambda y:obj(y,a,z,s,P,Q,kind); so=sf(sx); sg=grad(sf,sx); sp=pg(sx,sg)
  # Starts whose independently recomputed objectives differ by <=2e-7 are numerical ties.
  if abs(so-saved['objective'])>2e-8 or abs(sp).max()>1e-6*(1+abs(so)) or best['objective'] < so-2e-7:failures.append('selected_'+kind)
 # exact complete restricted grid, independently regenerate order and every objective/slack/status
 A=np.linspace(-1.5,.5,9);D=np.linspace(.25,2.25,9); rr=grid['rows'];expected=[]
 for i,x0 in enumerate(A):
  for j,x1 in enumerate(D):
   sl=.5-(x0+x1);feas=sl>=0;expected.append((i,j,x0,x1,sl,feas,obj(np.array([x0,x1]),a,z,s,P,Q,'NFXP') if feas else None))
 if len(rr)!=81:failures.append('restricted_count')
 for got,ex in zip(rr,expected):
  i,j,x0,x1,sl,feas,o=ex
  if (got['i'],got['j'])!=(i,j) or abs(got['restriction_slack']-sl)>1e-14 or got['feasible']!=feas or got['lower_or_upper_boundary']!=(i in(0,8) or j in(0,8)) or got['restriction_boundary']!=(sl==0) or (feas and abs(got['objective']-o)>2e-8) or ((not feas) and got['objective'] is not None):failures.append('restricted_row_'+str(i)+'_'+str(j))
 gm=grid['metadata'];counts={'feasible':sum(x[5] for x in expected),'infeasible':sum(not x[5] for x in expected),'boundary':sum(x[4]==0 for x in expected)}
 if counts!={'feasible':gm['feasible_count'],'infeasible':gm['infeasible_count'],'boundary':gm['restriction_boundary_count']}:failures.append('restricted_metadata')
 # population rank mapping at selected NFXP theta
 xn=np.array(sm['selected']['NFXP']['terminal']);J=np.empty((4,2));hh=1e-5
 def cells(x):return np.r_[pn(x,np.zeros(2),np.array([0,1]),P),pn(x,np.full(2,.4),np.array([0,1]),P)]
 for j in range(2):xp=xn.copy();xm=xn.copy();xp[j]+=hh;xm[j]-=hh;J[:,j]=(cells(xp)-cells(xm))/(2*hh)
 sv=np.linalg.svd(J,compute_uv=False);rank=int(sum(sv>1e-8))
 if not close(J,sm['local_population_rank']['jacobian'],2e-7) or rank!=sm['local_population_rank']['rank']:failures.append('rank')
 # support, policies, and accounting from primitives/model
 pol=[]
 for zz,label,support in [(0.,'observed_baseline','observed'),(.2,'midpoint_counterfactual','model_interpolation'),(.4,'observed_high','observed')]:
  v=value(xn,zz,P);pr=pn(xn,np.full(2,zz),np.array([0,1]),P);M=np.array([(1-pr[i])*np.array([1-P[i,0],P[i,0]])+pr[i]*np.array([1-P[i,1],P[i,1]]) for i in range(2)]);p1=M[0,1]/(M[0,1]+M[1,0]);up=float(np.array([1-p1,p1])@pr)
  pol.append({'subsidy':zz,'label':label,'support':support,'stationary_state1':p1,'stationary_action1':up,'government_transfer_per_period':zz*up,'real_resource_cost_per_period':.3*up,'social_resource_accounting_excludes_transfer':.3*up,'private_value_state0':v[0]})
 for x,y in zip(pol,sm['policy_accounting']):
  for k in x:
   if isinstance(x[k],str): ok=x[k]==y[k]
   else: ok=abs(x[k]-y[k])<2e-8
   if not ok:failures.append('policy_'+str(x['subsidy'])+'_'+k)
 man=loadj('manifest.json');hashes={}
 for f,rec in man['production_files'].items():hashes[f]=sha(O/f); failures += ([] if hashes[f]==rec['sha256'] and (O/f).stat().st_size==rec['bytes'] else ['hash_'+f])
 actual_counts={'raw_rows':len(s),'starts_total':len(st),'restricted_rows':len(rr),'policy_rows':len(pol)}
 if actual_counts!=man['counts']:failures.append('manifest_counts')
 out={'passed':not failures,'failures':failures,'coverage':['raw controlled transitions and cell counts','empirical CCP and support','objectives plus independently central/projected gradients for every optimizer start','gradient-only acceptance and selected estimates','every row, boundary, slack, feasibility flag, objective, and count in the closed restricted grid','local population Jacobian, singular values, and rank','observed-policy labels versus midpoint model interpolation','transfer and real-resource accounting separately','cross-file SHA-256, byte sizes, and row counts'],'recomputed':{'transition':P.tolist(),'ccp':Q.tolist(),'starts':start_checks,'selected':selected,'restricted_counts':counts,'local_rank':{'jacobian':J.tolist(),'singular_values':sv.tolist(),'rank':rank},'policy_accounting':pol,'hashes':hashes,'counts':actual_counts}}
 (O/'verification.json').write_text(json.dumps(out,indent=2,sort_keys=True,default=lambda x:x.item() if isinstance(x,np.generic) else x.tolist()),encoding='utf-8')
 print(json.dumps({'passed':out['passed'],'failures':failures,'counts':actual_counts},indent=2));return 0 if out['passed'] else 1
if __name__=='__main__':sys.exit(main())
