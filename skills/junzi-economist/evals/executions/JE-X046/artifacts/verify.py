import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from run_study import TRUE, nll_grad, p_mix, dp_mix

out=Path(__file__).resolve().parent
rng=np.random.default_rng(99117); w=rng.uniform(-1,1,1200); y=rng.binomial(1,p_mix(w,TRUE))
analytic=nll_grad(TRUE,w,y)[1]
numeric=np.empty(4); h=1e-6
for j in range(4):
    xp=TRUE.copy(); xm=TRUE.copy(); xp[j]+=h; xm[j]-=h
    numeric[j]=(nll_grad(xp,w,y)[0]-nll_grad(xm,w,y)[0])/(2*h)

grid=np.linspace(-1,1,4001); J=dp_mix(grid,TRUE)
sv=np.linalg.svd(J/np.sqrt(len(grid)),compute_uv=False)
pt=p_mix(grid,TRUE)
def obj(t): return np.mean((expit(t[0]+t[1]*grid)-pt)**2)
poplog=minimize(obj,[0,1],method='BFGS',options={'gtol':1e-12})
pl=expit(poplog.x[0]+poplog.x[1]*grid)
report={'gradient_max_abs_error':float(np.max(np.abs(analytic-numeric))),
        'population_jacobian_singular_values':sv.tolist(),
        'population_jacobian_condition':float(sv[0]/sv[-1]),
        'best_single_logit':poplog.x.tolist(),
        'training_population_rmse':float(np.sqrt(np.mean((pl-pt)**2))),
        'training_population_max_abs_gap':float(np.max(np.abs(pl-pt))),
        'note':'Full column rank on this dense design is numerical evidence of local population identification, not a global injectivity proof.'}
(out/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
