# Compact latent-heterogeneity structural choice study

## Research judgment

The simulated panel supports a computationally admissible two-type mixture fit, but it does **not** deliver clean latent-parameter recovery. The accepted unrestricted optimum is well solved under the declared box, yet the low-type price coefficient sits at its lower bound. The profile for the high-type share is broad and left-endpoint-censored. The honest endpoint is therefore a bounded, specification-conditional demonstration: the model-implied adoption response to a 0.45 price subsidy is stable across the selected evaluated-grid solutions, while latent composition and one price coefficient remain weakly pinned down in this sample.

Claim status: **exploratory / model-implied**, not evidence of population identification, general estimator performance, a causal effect in observed data, or social welfare.

## Economic object and model

There are 900 simulated people, each making four binary plan-adoption choices. A persistent latent type governs the intercept and price sensitivity; observed price and service quality vary over occasions. Conditional on type `k`,

`Pr(y_it=1|k) = logit^{-1}(a_k - b_k price_it + gamma quality_it)`,

with `b_k>0`, `a_2>a_1`, and high-type probability `pi`. Conditional choices are independent over occasions given type. Prices and qualities are generated independently of type and utility shocks. The structural counterfactual lowers every observed price by 0.45 and holds preferences, quality, and the latent-type distribution fixed.

The intended simulated population and sample size were fixed before the draw (`N=900`, `T=4`, seed `731904`); there was no redraw or outcome-based sample selection. True parameters were `(a1,a2,b1,b2,gamma,pi)=(-0.8,1.05,0.72,1.48,0.62,0.37)`.

## Estimation comparison

| Estimator/model | Negative log likelihood | Numerical assessment | Main result |
|---|---:|---|---|
| Direct mixture MLE, six starts | 1316.92307824 | Accepted; selected start 3; max projected gradient `1.14e-5` | `a1=-2.021`, `a2=1.323`, `b1=0.1353` (lower bound), `b2=1.623`, `gamma=0.538`, `pi=0.4800` |
| EM mixture | 1316.92307842 | Iteration cap 800; max projected gradient `1.06e-3`, above the `2e-4` acceptance rule | Nearly identical objective, but not admitted as the reported optimum |
| Homogeneous logit | 1320.35167070 | Optimizer success; max gradient `2.08e-7` | Simpler three-parameter benchmark |

The mixture improves twice the log-likelihood difference by `6.857` and has AIC `2645.846` versus `2646.703` for the homogeneous logit. This is only a descriptive specification comparison: finite-mixture homogeneity tests have nonstandard geometry, so no chi-square p-value is asserted. The boundary estimate and poor recovery of the true low-type coefficient defeat any stronger recovery claim.

## Profile and evaluated-grid set

The index is `pi`. I evaluated `0.10, 0.15, ..., 0.90`. At every one of the 17 indices, six conditional starts were run and at least one conditional solution satisfied the predeclared finite-objective and projected-gradient rule (`max <= 2e-4`). The reported profile keeps only the best accepted conditional objective at each index.

LR distances use the accepted continuous unrestricted optimum of the **same mixture likelihood**, `1316.92307824` at `pi=0.480037`, rather than the best evaluated grid point. Using the conventional one-parameter cutoff `3.841459`, the **evaluated-grid set** is

`{0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80}`.

- Accepted reported indices: 17 of 17.
- Profile holes: 0.
- In-set count: 15.
- Left endpoint: censored, because `0.10` is in the set and is the lowest evaluated index.
- Right endpoint: not censored; `0.85` and `0.90` are rejected on this grid.

This is not a continuous confidence interval. No interpolation, between-grid exclusion, or coverage claim is made. The set is also conditional on the declared structural parameter box; that box is not an identification set.

## Policy mapping and support

Only the selected best accepted solutions that are inside the evaluated-grid set were mapped into policy effects. All out-of-set rows retain a blank policy field. Across those 15 selected solutions, the mean adoption increase from the 0.45 price subsidy ranges from `0.05063` to `0.05383` (5.06–5.38 percentage points); the unrestricted optimum gives `0.05266`.

This narrow image is specification-conditional, not welfare. It omits fiscal cost, producer incidence, quality responses, congestion, distributional weights, and equilibrium adjustment. Baseline simulated prices span `[0.35, 3.80]`; post-policy prices span `[-0.10, 3.35]`, and 3.28% fall below the observed baseline minimum. Thus the policy image includes limited lower-tail functional-form extrapolation and should not be presented as wholly supported by observed-price variation.

## Independent verification

A separate derivative-free bounded implementation recomputed all 17 conditional optima from the saved primitives, rebuilt every LR distance against the unrestricted likelihood, and independently reconstructed membership, counts, holes, and endpoint flags. The maximum conditional-objective difference from the production profile was `2.73e-11`; objective agreement, set values, and count all passed. Its explicit coverage map does not extend to simulation generation, EM, or the policy mapping.

## Branch decision

Retain this branch as a successful numerical/profile demonstration, but do not promote it as latent-type recovery. The next discriminating work would (i) extend the profile below `pi=0.10` to resolve left censoring, (ii) examine whether a substantively justified wider domain for `b1` changes the profile and policy image, and (iii) run repeated seeds and larger samples before making estimator-performance claims. A denser grid alone cannot repair the coefficient-bound problem.

## Artifacts

- `study.py`: production simulation, direct MLE, EM, homogeneous benchmark, profile, and policy mapping.
- `verify.py`: separate derivative-free profile/set recomputation.
- `simulated_data.npz`: compact immutable simulated primitives.
- `starts_and_diagnostics.csv`: every initial point, terminal vector, objective, raw/projected gradients, status, message, and distance from the best accepted solution.
- `profile.csv`: selected best accepted conditional solution at each index, LR distance, membership, and in-set-only policy mapping.
- `em_trace.csv`: EM objective and mixing-share trace.
- `summary.json`: machine-readable headline results.
- `verification.json`: independent recomputation and coverage map.
- `provenance.json`: exact instruction commit/files, environment, seed, tolerances, and profile rule.
