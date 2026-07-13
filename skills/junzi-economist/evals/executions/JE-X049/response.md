# Two-type retrofit adoption: structural recovery and policy validation

## Research judgment

The declared design predicts average adoption responses to a 0.5 reduction in the price index much more reliably than it separates the two latent fixed-cost types. Across 12 samples, every selected mixture MLE and SMM solution passes the predeclared projected-gradient/KKT rule, but 19 of 24 selected mixture fits lie on an optimizer bound and only 4 are eligible for interior Wald inference. An executed likelihood profile for the separation parameter in one prespecified small-sample replication gives a 95% LR set of **[0.15, 3.00]**, reaching the economically justified upper profiling bound, while the corresponding policy-effect set is only **[0.07215, 0.07610]** around the true **0.07504**.

This is weak finite-sample separation under the maintained two-logit specification, not evidence of partial identification. The LR set is a likelihood confidence set and is censored by the stated economic profiling domain; the policy range is its image under the maintained model. No observational-equivalence proof or population identified-set calculation was performed.

## Economic environment and normalization

Household `i` observes `(q_i,s_i)` and adopts when latent net utility

`b_s s_i - a_q q_i - k_t + epsilon_i`

exceeds the normalized outside option. `epsilon` follows the type-I EV normalization, so its scale is one. Type is latent and independent of the randomized design variables. The low-cost type is labeled first, `k_high = k_low + delta`, `delta > 0`, and `pi_low` is its mass. Truth is `(b_s,a_q,k_low,delta,pi_low)=(1.15,0.90,-0.30,1.50,0.58)`, hence `k_high=1.20`. The mixture adoption probability is the type-mass-weighted average of the two logits.

The structural parameters are behaviorally policy-invariant only under the maintained independence, EV1, two-mass, and linear-index assumptions. The simulation establishes recovery behavior for this declared DGP; it is not evidence about real retrofit households or welfare. No welfare calculation is made because retrofit resource costs, fiscal incidence, externalities, and distributional weights were not specified.

## Declared designs and support

| Object | q support | s support | Interpretation |
|---|---:|---:|---|
| Training | [0.8, 2.2] | [-0.5, 1.5] | Random uniform rectangle used for estimation |
| Interpolation holdout | [0.95, 2.05] | [-0.35, 1.35] | Strictly inside training support |
| Baseline policy population | [0.5, 2.5] | [-1.0, 2.0] | Partly outside training support |
| Post-policy population | [0.0, 2.0] | [-1.0, 2.0] | Same households after `q' = q - 0.5`; partly outside training support |
| Stress grid | [-0.5, 3.0] | [-1.2, 2.2] | Deliberate extrapolation, not policy support |

Thus the interpolation result is supported by the training rectangle. Baseline-policy and post-policy results combine supported and extrapolated cells and must not be relabeled interpolation. Stress-grid results are reported only as a robustness diagnostic.

## Estimators and numerical rules

The mixture MLE targets the Bernoulli likelihood. The overidentified SMM uses nine declared moments—constant, centered `s` and `q`, their squares and interaction, and three threshold indicators—for five mixture parameters, with identity weighting. The misspecified single logit has one fixed-cost intercept and is estimated by the same MLE and SMM criteria.

Each of 48 estimator/model/replication combinations has eight starts. Optimizer boxes are `b_s in [0.05,2.5]`, `a_q in [0.05,2.2]`, `k_low in [-2.5,1.5]`, `delta in [0.02,4]`, `pi_low in [0.03,0.97]`; these are computational boxes, not economic identification bounds. A start is numerically accepted only if its projected-gradient infinity norm is at most `2e-5`. Every record contains its initial and final vector, objective, full raw and projected gradients, their norms, active bounds, software status/message, and objective distance from the accepted best.

All 384 starts returned software success. Only 296 passed KKT: mixture MLE 45/96, single MLE 69/96, mixture SMM 90/96, and single SMM 92/96. All 88 rejected starts had a relative-objective-reduction convergence message, illustrating why software success was not treated as numerical acceptance. No run was deleted.

## Monte Carlo results

Each cell contains six seeds. RMSEs compare predicted probabilities with the known DGP on deterministic grids.

| n | estimator | model | selected KKT | boundary | inference eligible | interpolation RMSE | baseline RMSE | post-policy RMSE | stress RMSE | policy bias |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 600 | MLE | mixture | 1.00 | 0.67 | 0.33 | .0264 | .0422 | .0516 | .0545 | -.0052 |
| 600 | MLE | single | 1.00 | 0.00 | 1.00 | .0262 | .0351 | .0416 | .0446 | -.0089 |
| 600 | SMM | mixture | 1.00 | 1.00 | 0.00 | .0258 | .0444 | .0547 | .0572 | -.0055 |
| 600 | SMM | single | 1.00 | 0.00 | 1.00 | .0257 | .0358 | .0446 | .0470 | -.0073 |
| 3000 | MLE | mixture | 1.00 | 0.83 | 0.17 | .0192 | .0322 | .0386 | .0433 | -.0027 |
| 3000 | MLE | single | 1.00 | 0.00 | 1.00 | .0174 | .0251 | .0304 | .0342 | -.0046 |
| 3000 | SMM | mixture | 1.00 | 0.83 | 0.17 | .0203 | .0318 | .0382 | .0425 | -.0030 |
| 3000 | SMM | single | 1.00 | 0.00 | 1.00 | .0185 | .0264 | .0319 | .0356 | -.0059 |

The single logit has slightly better held-out and policy-grid probability RMSE in these 12 samples even though it is structurally misspecified. That result supports simplification for this narrow prediction exercise, not a claim that household heterogeneity is absent.

Mixture parameter means do not improve toward truth over these two sample sizes. For MLE, mean `(b_s,a_q,k_low,delta,pi_low)` is `(1.7767,1.1447,-1.8122,3.7456,.3593)` at `n=600` and `(1.6983,1.1290,-2.0304,3.7214,.3143)` at `n=3000`. SMM is similar. These are boundary/ridge symptoms in the executed finite designs, not proof of population nonidentification.

## Inference and coverage

Inference eligibility requires selected-run KKT acceptance, no active optimizer bound, and a finite positive interior covariance calculation. Mixture MLE eligibility is 2/6 at `n=600` and 1/6 at `n=3000`; mixture SMM eligibility is 0/6 and 1/6. Single-logit eligibility is 6/6 in every cell, but coverage of the true mixture primitives is inapplicable to that misspecified parameterization.

For mixture MLE, all-replication 95% Wald coverage is 2/6 for each primitive at `n=600`. Conditional on the two eligible replications it is 2/2. At `n=3000`, all-replication coverage is 1/6 for `b_s,a_q,k_low,delta` and 0/6 for `pi_low`; conditional coverage in the sole eligible replication is respectively 1/1 and 0/1. SMM has zero all-replication coverage at `n=600` because no replication is eligible; conditional coverage is undefined. At `n=3000`, SMM matches the MLE pattern in its sole eligible replication. Failed or boundary runs count as noncoverage in the all-replication denominator; they are not silently omitted.

With only six replications per cell, these fractions are recovery diagnostics, not calibrated general coverage claims.

## Executed likelihood profile

The profile uses mixture MLE for the prespecified `n=600`, seed 104 sample. It fixes `delta` on `[0.10,3.00]` in steps of .05 and optimizes the remaining four parameters from three starts at every point. These profile bounds are economically motivated as a range from near-homogeneous to a three-EV1-scale fixed-cost gap and are distinct from the optimizer box `[0.02,4.00]`. The 95% set uses `2(ell_max-ell(delta)) <= chi2_1(.95)` and only KKT-accepted profile points.

The set is `[0.15,3.00]`; its upper endpoint equals the economic profiling bound, so values above 3 were not excluded by this exercise. The likelihood minimum on the profile occurs at 3.00. Mapping accepted LR-set points through the declared policy gives adoption increases `[0.07215,0.07610]`, containing the true `0.07504`. This contrast is the central finding: type decomposition is weakly resolved, while the policy-relevant mixture probability is stable over the likelihood set.

## Independent verification

A separate script reimplemented probabilities and both objectives from saved primitives rather than importing production functions. Across all 48 selected fits, the maximum absolute discrepancy from saved objectives is `2.27e-13`, and every saved selection equals the minimum KKT-accepted objective. Independent central-difference gradients agree with analytic raw gradients within `5.10e-5`; the large raw boundary derivative in the checked mixture run is correctly removed by the projected/KKT rule. Verification passed.

## Branch decision

* **Simplify provisionally** to the single logit when the target is average adoption prediction over the declared interpolation and policy rectangles: it has lower mean held-out RMSE in every estimator/sample-size comparison here.
* **Continue the mixture only with new discriminating variation** if latent type shares or type-specific fixed costs are the target—for example, wider independent variation in savings and prices, repeated household choices, or observed proxies for retrofit constraints. Merely raising `n` from 600 to 3000 in the same rectangle did not resolve the geometry.
* **Abandon interior Wald inference for the mixture under the current design.** Use profile-based reporting for the policy object and preserve boundary solutions. Do not abandon the maintained mixture model as globally unidentified: the executed evidence does not establish that claim.

## Artifact and provenance index

* `run_analysis.py`: executable production simulation, estimators, KKT logic, inference, grids, and profile.
* `independent_verify.py`: separate recomputation and derivative checks.
* `outputs/simulated_training.parquet`: all simulated training observations and true probabilities.
* `outputs/start_records.csv`: complete 384-start raw record, including rejected starts.
* `outputs/replication_results.csv`: selected run, geometry, inference, coverage, fit, and policy output for 48 fits.
* `outputs/monte_carlo_summary.csv`: cell summaries.
* `outputs/profile_delta.csv`: all 177 profile-start records and LR membership.
* `outputs/independent_objective_checks.csv` and `outputs/independent_verification.json`: fresh checks.
* `outputs/provenance.json`: truth, supports, seeds, tolerances, software versions, normalization, and skill commit.

The source skill repository was read only through committed content at commit `e25b4d0`; this work did not modify it. The analysis used the dedicated `codex` Python environment.
