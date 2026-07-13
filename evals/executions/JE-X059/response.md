# Minimal dynamic discrete-choice demonstration

Run `production.py` once, then run `verify.py` last. The production model is a two-state, two-action infinite-horizon dynamic logit. The simulated population and sample size are fixed before drawing. Policy regimes 0 and 0.4 are observed; 0.2 is explicitly model interpolation.

NFXP solves Bellman optimality inside the likelihood. The distinct two-step CCP estimator first estimates four empirical CCP cells and then uses a fixed-policy linear evaluation system inside its pseudo-likelihood. Controlled transitions are estimated from state-action-next-state counts.

Optimization messages are diagnostic only. Every start is retained, and eligibility is determined solely by a separately evaluated box-projected-gradient rule, `||g_P||_inf <= 1e-6*(1+|objective|)`. The finite restricted exercise is exactly the full 9-by-9 closed Cartesian grid, including boundaries; infeasible rows are retained with exact restriction slacks and null objectives.

`verify.py` is separately coded, imports no production functions, and must be run after all production artifacts. It reconstructs all decisive objects from `raw_primitives.npz` and checks hashes and counts.
