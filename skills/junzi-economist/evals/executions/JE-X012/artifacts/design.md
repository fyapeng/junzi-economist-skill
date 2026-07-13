# Predeclared repeated-sample and identification protocol

## Economic and statistical target

The environment is the five-state, two-action dynamic equipment-replacement model used in JE-X011. The estimands are the operating-cost slope `theta=0.7` and replacement cost `RC=2.2`, conditional on discount factor 0.9, known transition matrices, stationary behavior, and unit-scale iid type-I extreme-value choice shocks.

Repeated-sample recovery evaluates the NFXP estimator under the correctly specified data-generating process. It is not treated as proof of population identification. Population identification is examined separately through the mapping from `(theta, RC)` to the five state-conditional replacement probabilities.

## Monte Carlo protocol

- Panel lengths: 30 periods; every physician starts in state zero.
- Sample sizes: 100 and 400 physicians.
- Replications: 60 independently seeded panels at each size, 120 panels total.
- Seeds: `2026071300 + 10000 * size_index + replication`, where `size_index` is 0 for 100 physicians and 1 for 400 physicians and replication runs from 0 to 59.
- NFXP Bellman tolerance: `1e-10`.
- Bounds: `theta in [1e-6,5]`, `RC in [1e-6,8]`.
- Optimizer: L-BFGS-B with two dispersed starts, `(0.30,1.00)` and `(1.50,4.50)`. The best successful likelihood is retained; all start-level outcomes are saved.
- A replication is an optimizer failure only if neither start reports success with finite objective and parameters. Hessian failure is recorded separately.
- Finite-difference observed Hessian step: `2e-4 * max(1,abs(parameter))` with nested central gradients.
- Wald interval: estimate plus or minus 1.96 Hessian standard errors.
- Boundary hit: estimate within `1e-4` of an estimation bound.
- Report bias, RMSE, empirical SD, mean valid Hessian SE, 95% Wald coverage, optimizer failure, Hessian failure, boundary hits, and worst absolute-error replication for each parameter. Failed replications remain in `replications.jsonl`.

## Population mapping protocol

- Compute the five replacement CCPs and a central finite-difference `5 x 2` Jacobian at truth using steps `1e-5 * max(1,abs(parameter))`; report its rank and singular values.
- Nearby grid: theta within plus/minus 0.25 and RC within plus/minus 0.50, 51 points per dimension. Exclude an Euclidean parameter ball of radius 0.02 around truth and locate the closest CCP vector.
- Broad grid: theta from 0.05 to 2.00 (60 points) and RC from 0.20 to 6.00 (80 points). Exclude a radius-0.05 parameter ball and locate the closest CCP vector.
- In addition, minimize squared CCP distance to the truth from 12 dispersed starts over the estimation bounds. Record every solution. A returned truth from all starts is evidence against discovered observational equivalence, not a proof of global injectivity.

## Interpretation boundary

Full column rank of the Jacobian supports local regular identification of the two parameters from the five CCPs under the fixed model and normalizations. Finite grids and multi-start inverse searches can discover counterexamples but cannot prove global injectivity over a continuum. Monte Carlo bias and coverage describe this estimator and these sample sizes under correct specification; they do not validate the shock distribution, transitions, discount factor, or external counterfactuals.

