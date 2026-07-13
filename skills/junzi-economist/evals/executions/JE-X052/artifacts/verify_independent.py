import json, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent; A=ROOT/'artifacts'; s=json.loads((A/'summary.json').read_text(encoding='utf-8')); z=np.load(A/'simulation.npz')
checks=[]
def ck(name,ok,coverage,detail): checks.append({'name':name,'pass':bool(ok),'coverage':coverage,'detail':detail})
d=z['data']; q=z['qhat']
# independently recompute transition ratios from row data
S=[(i,r) for i in range(3) for r in range(2)]
qr=np.zeros((3,2))
for a in range(3):
 for r in range(2):
  m=(d[:,4]==a)&(np.array([S[x][1] for x in d[:,3]])==r); y=np.array([S[x][1] for x in d[m,5]])
  qr[a,r]=(y.sum()+.5)/(len(y)+1)
ck('controlled_transitions',np.max(abs(qr-q))<1e-14,'saved transition estimates only; not preference estimation',{'max_abs_diff':float(np.max(abs(qr-q)))})
sv=np.linalg.svd(z['jacobian'],compute_uv=False); rk=int((sv>sv[0]*1e-7).sum())
ck('local_rank_arithmetic',rk==s['population_local_rank']['rank'],'rank calculation for saved population Jacobian; not proof of global identification',{'rank':rk,'sv':sv.tolist()})
alt=s['restricted_alternative']; slack=.78-alt['theta'][3]
ck('hard_constraint',slack>=-alt['acceptance_tolerance'] and abs(slack-alt['realized_slack'])<1e-13,'selected restricted candidate feasibility and reported slack only; not global optimality',{'recomputed_slack':slack,'tol':alt['acceptance_tolerance']})
cf=s['counterfactuals']; identities=[abs(x['social_welfare_flow']-(x['private_flow_payoff']-x['government_transfers']-x['real_resource_cost'])) for x in cf]
ck('welfare_accounting',max(identities)<1e-12,'accounting identity in saved counterfactual rows; not normative completeness or external validity',{'max_identity_error':max(identities)})
search=json.loads((A/'restricted_search.json').read_text(encoding='utf-8'))
ck('search_metadata',len(search['initial_population'])==32 and len(search['generation_trace'])>0 and len(search['polish_starts'])==8,'presence/count of retained restricted-search starts and traces; not optimizer correctness',{'initial':len(search['initial_population']),'generations':len(search['generation_trace']),'polish':len(search['polish_starts'])})
report={'verifier':'independent arithmetic/schema recomputation; does not import production solver','coverage_map':checks,'all_checked_objects_pass':all(x['pass'] for x in checks),'blanket_pipeline_pass_claimed':False}
(A/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2)); sys.exit(0 if report['all_checked_objects_pass'] else 2)
