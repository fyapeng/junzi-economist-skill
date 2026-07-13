# Preventive-maintenance model: result and identification judgment

## Economic environment and normalization

An asset has condition `x=0,...,4`. Each period its owner observes `x` and a policy subsidy `s`, then chooses run (`a=0`) or overhaul (`a=1`). Deterministic flow utility is `-theta*x^2` under run and `-F+s` under overhaul. Run produces controlled deterioration; overhaul resets the asset. The subsidy is a transfer, not a reduction in overhaul's real resource cost. The state and subsidy are observed by the econometrician; EV1 action shocks are private.

The declared truth is `(theta,F,beta)=(0.18,3.20,0.91)`. Run moves by 0, 1, or 2 condition units with probabilities `(0.58,0.32,0.10)`, capped at 4; overhaul resets to 0 or 1 with probabilities `(0.86,0.14)`. I simulated 2,400 assets for 40 periods (96,000 choices), split equally between observed subsidy regimes `s=0` and `s=0.75`, with seed 47013. This provides actual policy interpolation support between the two regimes; policies outside `[0,0.75]` remain extrapolations.

EV1 shocks are standard type-I extreme-value draws shifted by minus Euler's constant. Each shock therefore has mean zero and the inclusive-value equation is `V(x)=logsumexp(v_run(x),v_overhaul(x))`. An alternative common-location normalization shifts absolute value levels but leaves CCPs and policy value differences invariant.

## Estimation

Controlled transitions were estimated first by conditional frequency MLE on their declared supports; the common overhaul-reset distribution was pooled across states. These estimates were then held fixed in utility estimation.

At the true fixed `beta=0.91`, NFXP gives `(theta,F)=(0.17796,3.19372)`. A genuinely distinct CCP estimator—smoothed cell CCPs, Hotz–Miller log-odds inversion, a run-reference linear value equation, and weighted least squares, without a Bellman solve inside estimation—gives `(0.17671,3.18713)`. Their agreement is useful recovery evidence, not proof that either estimator is generally well behaved.

Joint NFXP gives `(theta,F,beta)=(0.17668,3.19988,0.91604)`. Continuous bounded profiling of beta, not a finite grid, yields `beta=0.9160408`; the selected inner solution has projected-gradient infinity norm `0.00202`. The selected full and fixed-beta solutions have projected-gradient norms `0.00795` and `0.00192`, respectively, below the declared `0.01` numerical acceptance threshold. No selected solution is on an active bound. Every start records its initial and final point, objective, raw and projected gradients, active bounds, solver status/message, and distance from the best objective in `full_start_traces.json`. Some individual starts fail the KKT acceptance rule and are retained rather than silently discarded.

Sixteen independently simulated smaller panels (`N=450,T=25`) at fixed true beta produced mean estimates `(theta,F)=(0.17865,3.19558)`, with ranges `(0.16776,0.19214)` and `(3.07274,3.29233)`; all selected replications pass the numerical acceptance rule. This is only a finite recovery demonstration. It is not general estimator-performance, coverage, or failure-rate support.

## What is and is not identified

The population mapping used for the local argument is the vector of ten CCP logits (five states in each of two observed subsidy regimes) as a function of `(theta,F,beta)`, holding the controlled transitions and the EV1/utility restrictions fixed. Its numerical derivative at truth has singular values `(30.0978,2.9978,1.0121)` and column rank 3. By the local rank/inverse-function argument, the three parameters are locally identified under the maintained stationarity, subsidy exogeneity, transition, EV1, and parametric utility restrictions. This is a local population statement, not a conclusion from a sample Hessian.

There is no finite-grid identification claim. A unique point on any reported grid would establish separation only on that grid; here beta was refined continuously instead.

There is also no proof of global injectivity. A continuous differential-evolution search over the declared box, constrained to remain a scaled distance of at least one from truth, finds `(0.19637,3.02895,0.81070)`, whose maximum absolute population CCP difference from truth is about `0.01149`. Thus the computation supplies bounded search evidence against exact observational equivalence in the searched region, while also documenting a practically close alternative. It does not exclude a closer alternative elsewhere or prove global identification.

## Subsidy counterfactual and welfare incidence

The table uses the jointly estimated model and stationary state distribution. “Private value difference” is the change in stationary-initial inclusive lifetime value. Transfers are reported per period. Real resources include deterioration cost when running and the full overhaul cost `F`; social flow welfare is minus these resources, excludes EV shocks, has no external benefit from better condition, and treats transfers as cancelling between owner and government.

| support | subsidy | overhaul rate | private value change | transfer flow | resource-cost flow | social-flow change |
|---|---:|---:|---:|---:|---:|---:|
| observed | 0.00 | 0.2077 | 0.0000 | 0.0000 | 0.8492 | 0.0000 |
| observed | 0.75 | 0.2442 | 2.0939 | 0.1831 | 0.9261 | -0.0769 |
| interpolation | 0.25 | 0.2181 | 0.6637 | 0.0545 | 0.8691 | -0.0200 |
| interpolation | 0.50 | 0.2302 | 1.3599 | 0.1151 | 0.8944 | -0.0453 |
| extrapolation | 1.25 | 0.2798 | 3.7017 | 0.3497 | 1.0137 | -0.1645 |
| extrapolation | 2.00 | 0.3583 | 6.5934 | 0.7165 | 1.2271 | -0.3780 |

The subsidy raises private value and overhaul frequency, but it lowers this narrowly defined social welfare because it induces more costly overhauls and the model contains no reliability, safety, output, or external benefit from improved condition. That welfare conclusion is therefore criterion- and specification-specific; adding a real benefit of maintenance could reverse it.

## Verification and artifact map

The separate verifier does not import the production solver. It independently reconstructs transitions, iterates a separately coded log-sum-exp Bellman equation, recomputes CCPs and residuals, and independently finite-differences the population CCP mapping. Bellman residuals are below `2e-13`; rank is 3; singular values agree with production within `1.9e-10`; status is `PASS`.

- `analysis.py`: executable production simulation, estimation, profiling, alternative search, recovery exercise, and counterfactual.
- `panel.npy`: raw simulated panel.
- `results.json`: machine-readable estimates and results.
- `full_start_traces.json`: complete start-level recovery and beta-profile diagnostics.
- `run_output.txt`: raw production output.
- `verify.py`, `verification.json`, `verification_output.txt`: independent implementation and raw verification results.
- `PROVENANCE.md`: exact commit, permitted files read, commands, environment, and seed.

Strongest honest endpoint: the exercise verifies local population identification and good simulated recovery near the truth under tight parametric restrictions; it does not establish global identification or broad estimator performance. The most discriminating next step would be to enlarge observed policy variation or add excluded transition shifters, then test whether the close low-beta alternative remains observationally close out of sample.
