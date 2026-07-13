# Compact dynamic discrete-choice result

## Economic object and status

The artifact models households choosing whether to maintain a deteriorating durable asset. The controlled state transition is estimated from the simulated panel rather than imposed in estimation. The sample has **4800 decision rows from 240 agents**; the overall maintenance rate is **0.4552** (regime 0: **0.3729**; regime 1: **0.5375**).

NFXP estimates `(state harm, maintenance cost, subsidy loading)` as **(0.758544, 1.227319, 0.887152)** from 8/8 successful starts. The genuinely distinct CCP-WMD estimator uses empirical CCP inversion and no nested Bellman likelihood; it estimates **(0.774794, 1.224178, 0.859037)** from 8/8 successful starts.

## Identification and restricted alternatives

The continuous claim is **local only**: the six observed-regime CCPs have a numerical Jacobian of rank 3 at the NFXP estimate, conditional on the estimated transitions, logit shocks, discount factor, and utility normalization. This is not a global population-identification claim.

The restricted alternative exercise exhausts all **4913** points of the declared closed 17-by-17-by-17 lattice, including **1538** boundary points. Exactly **4793** rows satisfy the hard L-infinity distance restriction `distance >= 0.35` at tolerance `1e-12`. The best accepted row has CCP SSE **0.0050775983** and slack **0.022681246**. This is exact for the evaluated lattice only and supplies no continuous global-separation theorem.

## Policy and welfare

Regimes 0 and 1 are observed supports. Regime 0.5 is explicitly labeled model-based interpolation, not observed support. `policy_results.csv` keeps private payoff, government transfer outlay, real maintenance resources, state harm, and social welfare separate. Social welfare equals private payoff minus transfers and also equals negative state harm minus real maintenance cost; the maximum saved accounting error is **5.551e-17**.

## Limits

Results are a deterministic simulated-data recovery exercise, conditional on the specified dynamic logit and estimated transition law. The local rank check, finite-lattice restricted search, and policy interpolation do not establish global population identification, external validity, or policy invariance outside the two observed regimes.
