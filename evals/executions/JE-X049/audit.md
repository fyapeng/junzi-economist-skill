# Independent audit of the blind structural-estimation transfer

## Overall judgment: MIXED

The transfer is substantially reproducible and most Monte Carlo, start-accounting, KKT, support, inference-eligibility, and model-comparison claims survive independent raw-artifact checks. However, the executed likelihood profile—the report's central diagnostic—is not a valid complete profile as reported. Numerical nonacceptance at two grid points was treated as if it were likelihood exclusion, the displayed interval bridges one of those missing points, and the reported policy image uses all accepted local solutions rather than the profiled optimum at each fixed value of `delta`. A separate constrained optimization recovers the missing points and changes the profile set from the reported `[0.15, 3.00]` to the full prespecified grid domain `[0.10, 3.00]`; it also changes the policy image from `[0.07215, 0.07610]` to approximately `[0.07260, 0.07610]` when one profiled optimum per `delta` is used.

The high-level economic conclusion remains defensible: finite-sample type separation is weak under the maintained two-logit specification, while the policy response is comparatively stable. The exact headline profile and policy-range claims do not pass.

## Audit scope and independent method

I read `REPORT.md`, `run_analysis.py`, `independent_verify.py`, the provenance and execution metadata, and every saved data table. I did not modify the production code, source skill repository, or any original output.

Checks were recomputed directly from `simulated_training.parquet`, `start_records.csv`, `replication_results.csv`, and `profile_delta.csv`. The independent calculations used separately written probability, likelihood, moment, gradient, grid, covariance, and constrained-optimization calculations and did not import the production module. For the two missing profile points, I minimized a separately coded Bernoulli negative log likelihood using objective-only SLSQP and Powell searches from multiple saved starts, then checked finite-difference gradients and bound signs.

## Findings by requested issue

### 1. Projected-gradient and KKT rules: PASS

For box-constrained minimization, the production rule has the correct sign: at a lower bound it removes a positive raw derivative, and at an upper bound it removes a negative raw derivative. Recomputing the active-bound labels and projected gradient from every saved final vector and raw gradient produced:

- maximum projected-gradient-vector discrepancy: `0`;
- active-bound mismatches: `0 / 384`;
- numerical-acceptance mismatches at tolerance `2e-5`: `0 / 384`.

All 48 selected fits pass the declared rule. This is evidence of numerical stationarity under the computational boxes, not identification.

One documentation detail is inaccurate in principle: `distance_from_best` in `run_analysis.py` is measured from the best **finite** start, while the report describes distance from the best **accepted** start. In these artifacts no rejected start has a lower objective than the best accepted start, so the saved distances are numerically unaffected.

### 2. Retention and accounting of all starts: PASS

There are exactly 48 fit groups, 8 records in every group, and 384 start records in total. Counts independently match the report:

| Estimator | Model | Starts | Software success | KKT accepted |
|---|---:|---:|---:|---:|
| MLE | mixture | 96 | 96 | 45 |
| MLE | single | 96 | 96 | 69 |
| SMM | mixture | 96 | 96 | 90 |
| SMM | single | 96 | 96 | 92 |

All 88 rejected starts remain in the file, and all carry the relative-objective-reduction convergence message described in the report. No evidence of deletion or favorable-start filtering was found.

### 3. Selected solution versus start convergence: PASS

Every selected objective equals the minimum objective among KKT-accepted starts in its fit group to saved precision; the maximum absolute discrepancy is `0`. Every selected objective is tied by between 2 and 8 saved starts, which is consistent with convergence to the same solution from multiple initial values. Every group has at least one accepted start (range 1 to 8).

Software success alone is demonstrably insufficient here: 384 starts report success but only 296 pass the predeclared projected-gradient tolerance. The report correctly keeps these concepts separate.

### 4. Boundary count and inference eligibility: MIXED

The eligibility rule in code is correctly applied: selected-run KKT acceptance, no saved active bound, and finite positive standard errors. Independent reconstruction gives exactly 28 eligible fits overall: 24 single-logit fits and 4 mixture fits. The mixture breakdown is `2/6`, `0/6`, `1/6`, and `1/6` for `(n=600 MLE, n=600 SMM, n=3000 MLE, n=3000 SMM)`.

Independent finite-difference Hessian/sandwich calculations reproduce the same eligibility decisions. The eligible mixture covariance calculations are positive, but poorly conditioned: condition numbers are approximately `8.26e3`, `1.54e4`, `2.47e4`, and `5.54e4`, which reinforces the weak-geometry interpretation.

The report's headline count “19 of 24 selected mixture fits lie on an optimizer bound” is arithmetically wrong. The saved results contain **20 of 24** boundary mixture fits: `4 + 6 + 5 + 5` across the four estimator/sample-size cells. The cell rates in the report's own table imply the correct count. The statement that only 4 mixture fits are inference eligible is correct.

Coverage fractions, including treating failed/boundary fits as noncoverage in the all-replication denominator, reproduce exactly. With six replications per cell, the report appropriately calls them diagnostics rather than calibrated coverage evidence.

### 5. Support distinctions: PASS

The geometric labels are correct:

- the holdout rectangle is strictly inside the training rectangle;
- baseline and post-policy rectangles are only partly supported;
- the stress grid is deliberate extrapolation.

On the saved deterministic `31 x 31` grids, the fraction of points inside the training rectangle is `1.0000` for holdout, `0.4589` for baseline policy, `0.4152` for post-policy, and `0.2123` for stress. The report does not improperly relabel the policy exercises as interpolation.

### 6. Likelihood profile and interpretation: FAIL

The saved profile contains 177 rows (`59 delta` values times 3 starts), all with software success, but only 145 KKT-accepted rows. At `delta=0.10` and `delta=1.75`, **none** of the three production starts meets the `2e-5` tolerance. Consequently, only 57 of 59 fixed-`delta` grid points have an accepted profiled solution.

This invalidates the displayed interval `[0.15, 3.00]` as a likelihood exclusion statement:

- At `delta=0.10`, the best saved production run has projected-gradient norm about `1.74e-4`, so the point was numerically unresolved, not rejected by the LR statistic.
- A separate constrained solve finds a KKT solution at `delta=0.10` with `pi_low=0.03`, negative log likelihood `342.3914519134`, and the correct outward bound sign. Relative to the profile minimum `342.2520519906` at `delta=3.00`, its LR statistic is about `0.27880`, far below the 95% cutoff `3.84146`.
- A separate solve at `delta=1.75` gives negative log likelihood `342.3638943568` with maximum absolute finite-difference gradient about `1.7e-6`, filling the interior numerical hole.

Thus the supported grid-based LR set is the full prespecified economic profile domain **`[0.10, 3.00]`**, with both endpoints censored by the chosen domain. The data do not exclude the near-homogeneous boundary of the declared profile.

There is a second construction error. `profile_delta.csv` marks every accepted start within the LR cutoff as in-set, and `independent_verify.py` takes the minimum and maximum policy effects over all such rows. A likelihood profile should first retain the best accepted objective at each fixed `delta`, then map that profiled solution. The reported lower policy endpoint `0.072148` comes from a worse local solution at `delta=3.00`, `pi_low=0.97`, with objective `342.402967`, not from the profiled optimum at that `delta` (objective `342.252052`). Using one profiled optimum per `delta`, plus the independently recovered `delta=0.10` optimum, gives an approximate policy image **`[0.07260, 0.07610]`**. It still contains the true grid effect (about `0.07504`) and remains narrow.

The qualitative interpretation survives after correction: the likelihood is flat across the entire economically declared separation domain while the policy effect varies little. The report correctly avoids calling this partial identification or a population identified set. But the numerical profile must be repaired before its endpoints are reported as an LR confidence set.

### 7. Policy range and direct raw-data metrics: MIXED

Independent raw-grid calculations reproduce every saved holdout RMSE, baseline RMSE, post-policy RMSE, stress RMSE, estimated policy effect, and true policy effect to a maximum absolute discrepancy below `1e-16`. The maintained-model policy response is indeed stable relative to the primitive parameter estimates.

The specific saved profile-based range fails for the reason above. The corrected profiled range remains substantively narrow, so the economic conclusion is more robust than the reported endpoint calculation.

### 8. Comparison with the single logit: PASS, with scope restriction

The single logit has lower **mean probability RMSE** in all four estimator/sample-size comparisons for holdout, baseline, post-policy, and stress grids. The independently computed single-minus-mixture mean RMSE differences are negative in every comparison (for example, post-policy differences range from about `-0.00629` to `-0.01008`). This supports the report's narrow provisional simplification claim for probability prediction.

It does not establish absence of heterogeneity, and the report correctly says so. It also should not be generalized to the policy-effect estimand: the mixture's mean policy-effect bias is closer to zero than the single logit's in all four cells. The recommendation is valid only when the target is grid-level probability prediction, as the branch section states.

### 9. Branch decisions and abandonment claims: PASS, with qualification

The decisions are broadly proportional to the evidence:

- provisional simplification to a single logit is tied to its observed probability-RMSE advantage;
- continuing the mixture only with new discriminating variation is consistent with the persistence of boundary/ridge behavior when moving from `n=600` to `n=3000` on the same support;
- abandoning routine interior Wald reporting under the current design is supported by 20/24 boundary mixture fits, only 4/24 eligible fits, and severe covariance conditioning;
- the report explicitly does **not** abandon the mixture as globally unidentified and correctly distinguishes finite-sample geometry from population identification.

The phrase “abandon interior Wald inference” is best read as abandoning it as the default reporting strategy for this design, not as claiming no interior replication can ever admit a Wald calculation. Four do. The profile repair is necessary before profile-based reporting is offered as the replacement.

### 10. Provenance: PASS for consistency; causality not independently provable

The provenance file matches the code's truth, supports, boxes, seeds, tolerances, versions, and profile domain. The source repository currently resolves to the recorded commit `e25b4d0cd1a3812911be2094197c5b61110189aa`. Its working tree contains the disclosed modification to `skills/junzi-economist/evals/cases.yaml`.

The artifacts are outside the source repository, and nothing in the transfer conflicts with the claim that the task did not modify the repository. An after-the-fact audit cannot independently prove which process caused a preexisting dirty-tree change; the execution summary appropriately discloses that limitation rather than asserting a clean tree.

## Required corrections before a full PASS

1. Re-execute every fixed-`delta` profile point until an accepted conditional KKT solution is obtained, explicitly preserving unresolved points rather than treating them as excluded.
2. Construct the LR statistic from the best accepted objective at each fixed `delta` and map only that profiled solution into the policy effect.
3. Report the corrected grid-based LR set as `[0.10, 3.00]`, censored at both economic profile bounds, unless a wider justified profile is executed.
4. Replace the saved policy image with approximately `[0.07260, 0.07610]` after confirming all repaired grid points.
5. Correct the selected-mixture boundary count from 19 to 20.
6. Clarify that `distance_from_best` is coded relative to the best finite start, or change the calculation in a future rerun to the best accepted start.

No original failures or output records were overwritten in this audit.
