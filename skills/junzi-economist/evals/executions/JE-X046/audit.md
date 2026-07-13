# Independent audit

## Overall verdict: MIXED

The core DGP, normalization, label ordering, mixture probability, analytic derivatives, distinction between MLE and SMM, raw-run aggregates, local-rank calculation, prediction summaries, and welfare caveats are substantially correct. Five selected replications rerun from the declared seeds reproduce all stored numerical fields to at most `4.44e-16`, and independent aggregation of `raw_runs.csv` reproduces the reported tables up to CSV floating-point roundoff.

There are nevertheless material, reproducible defects. Most importantly, the reported “strict convergence” rates use the **unprojected** gradient for a box-constrained optimizer. This incorrectly labels almost every valid boundary optimum as a numerical failure. With the appropriate projected-gradient/KKT check at the same `1e-3` threshold, the rates are 100%, 97.5%, 100%, and 100%, rather than 22.5%, 62.5%, 80%, and 100% for MLE-500, MLE-2500, SMM-500, and SMM-2500. Exactly one selected solution (MLE, `n=2500`, seed `24006`) remains a genuine first-order failure. That run is nevertheless included in the reported Wald-coverage denominator. In addition, the artifact does not retain start-level outcomes despite claiming that all starts are retained, and the grid called policy support is not the actual counterfactual support.

## Scope and reproduction

I read only `response.md`, `run_study.py`, `verify.py`, `results.json`, `summary.csv`, `raw_runs.csv`, the two stored console outputs, and `PROVENANCE.md` in this endpoint. I did not inspect other endpoints or repository evaluations and did not alter an original artifact.

Independent checks used `C:\Users\ENAN\miniforge3\envs\codex\python.exe` with the endpoint's declared seeds and environment. I:

1. reimplemented the mixture probability and its derivative independently;
2. checked probability, likelihood, and SMM gradients by central differences at multiple step sizes;
3. recomputed the population derivative singular values with 1,000-node Gauss-Legendre quadrature rather than the endpoint's uniform grid;
4. recomputed all principal summaries directly from `raw_runs.csv`;
5. reran `one(seed,n)` for `(500,24001)`, `(500,24040)`, `(2500,24001)`, `(2500,24006)`, and `(2500,24040)` without writing outputs; and
6. reconstructed every sample and SMM pilot weight to evaluate raw and projected gradients at all 160 stored mixture estimates.

## Claim-by-claim findings

| Area | Verdict | Audit finding |
|---|---|---|
| Normalization and labels | PASS | Only `a0-k1` and `k2-k1` enter. Setting `k1=0`, defining `d=k2-k1>0`, and assigning `pi` to the low-cost/high-participation component is coherent and removes the label switch within the stated parameterization. |
| Mixture probability and derivatives | PASS | `p=pi*Lambda(b+a1*w)+(1-pi)*Lambda(b+a1*w-d)` and all four columns in `dp_mix` have the correct signs and labels. Independent maximum probability-derivative error was `1.17e-11` at step `1e-5`; likelihood and SMM objective gradient errors were `2.11e-9` and `4.32e-13`. |
| MLE versus SMM | PASS | The estimators are genuinely distinct. MLE uses individual Bernoulli scores; SMM uses seven Legendre residual moments and a pilot-estimated covariance weight. No replication gives parameter vectors equal within `1e-6`. Mean absolute MLE-SMM differences at `n=2500` are `(0.233, 0.0507, 0.270, 0.0298)` for `(b,a1,d,pi)`. |
| Population rank versus global identification | PASS, with caution | Quadrature gives singular values `(0.286315, 0.109504, 0.00121243, 0.000305034)` and condition number `938.63`, reproducing the endpoint. Full derivative rank is legitimate numerical evidence for regular local identification under the normalized functional form. The response correctly refuses to infer global injectivity. The numerical condition number is parameter-scale dependent, so `938` alone should not be treated as an invariant measure of economic weakness; the near-single-logit approximation and Monte Carlo geometry supply the stronger evidence. |
| Single-logit population approximation | PASS | Independent quadrature gives best logit `(-0.420146, 1.207543)`, RMSE `0.00036869`, and maximum node gap `0.00092335`, matching the stored verification. This supports weak separation, not correctness of the single-logit DGP. |
| Raw summaries and reproducibility | PASS | Bias, RMSE, boundary rates, reported raw-gradient rates, prediction metrics, Brier scores, coverage conditional on the stored eligibility flag, and counterfactual means/SDs all recompute from `raw_runs.csv`. The five fresh replication reruns match numerical fields within `4.44e-16` and all flags exactly. |
| Start retention and disagreement | FAIL | `multistart` holds eight optimizer results only in memory. `raw_runs.csv` retains only the selected result, a count of software-successful starts, and maximum parameter spread. It does not retain start parameters, objectives, gradients, messages, or boundary flags. Thus “All starts and boundary outcomes are retained” and the provenance's implication of retained raw start runs are false. Moreover, `start_maxspread` is over all finite starts without restricting to objective-equivalent solutions, so the reported disagreement rate does not establish that the alternatives lie on an observationally equivalent ridge. All eight starts did receive a software-success flag in every replication, but that is not start-level retention or objective-equivalence evidence. |
| Boundary accounting | PASS | The reported any-parameter boundary rates recompute. The more specific statement that the cost-gap ceiling is frequent is also defensible: `d` is within `.005` of 5 in 67.5%/27.5% of MLE runs and 62.5%/27.5% of SMM runs at `n=500/2500`. |
| Strict convergence and numerical failure | FAIL | Lines 102-103 use `norm(r.jac)`, the ordinary gradient. At an optimum on a bound, a nonzero outward raw gradient is normally required by KKT and is not failure. Reconstructing every objective and zeroing KKT-satisfied active-bound components changes rates to MLE 100% (`n=500`) and 97.5% (`n=2500`), SMM 100% at both sizes. Maximum projected norm is `1.33e-5`, `1.47`, `1.06e-7`, and `9.95e-4`, respectively. The response's low “strict convergence” percentages therefore do not measure numerical stopping and materially overstate computational failure. |
| The remaining genuine failure | FAIL in accounting | MLE seed `24006`, `n=2500`, is interior and has raw/projected gradient `(-0.0900, 0.2223, 0.0461, -1.4496)`, norm `1.46999`, despite `success=True`. This is a real first-order stopping failure. It should be counted separately and excluded from inferential summaries unless repaired. |
| Wald coverage | MIXED | The response correctly says coverage is conditional on favorable interior/positive-definite geometry and explicitly warns it is not unconditional nominal coverage. However, eligibility is coded only as interior plus Hessian PD, not convergence. Seed `24006` is included and covers `(b,a1,d)` but not `pi`. Excluding it leaves 23 eligible runs at `n=2500`, with conditional coverage `(0.652, 0.913, 0.565, 0.652)`, rather than `(0.667, 0.917, 0.583, 0.625)`. If ineligible runs are treated as inferential failures, the stored `n=2500` success-and-cover shares are only `(0.400, 0.550, 0.350, 0.375)`. |
| Training/interpolation/extrapolation prediction | PASS, with reporting limits | Reported grid RMSE and pooled held-out Brier means recompute. Unreported interpolation-grid means also favor the logit: at `n=500`, `(MLE,SMM,logit)=(.02596,.02741,.01956)`; at `n=2500`, `(.01355,.01349,.01057)`. The held-out Brier score pools interpolation and extrapolation halves, so it is not a separate held-out assessment of each region. “Essentially indistinguishable” is a practical judgment: at `n=2500` the paired mean Brier advantages of logit are `.000733` over MLE and `.000757` over SMM, with across-replication paired SEs `.000234` and `.000239`. |
| Policy/extrapolation support | FAIL in labeling | Training support is `[-1,1]`; subsidy baselines use `[1,1.5]`; post-policy wages are `[2,2.5]`. The code's grid labeled `policy` is `[1.5,2.5]`, which contains the post-policy support but also an irrelevant gap and omits the baseline support. It is therefore not “policy support” as claimed. The table's policy RMSE is a stress-grid metric, not RMSE on the counterfactual support or its baseline/post union. The separately computed participation and change numbers use the correct baseline and post-policy grids. |
| Misspecification, weak separation, and numerical failure | MIXED | The response correctly states that the mixture is the DGP, the logit is a close misspecified approximation, and poor primitive recovery is evidence of weak finite-sample separation rather than proof of a homogeneous-cost DGP. But its convergence table conflates KKT-valid boundary optima with numerical failures, and the closing phrase “underidentified in practice” blurs population identification, weak finite-sample geometry, estimator instability, and unsupported extrapolation. Better labels are: locally population-identified numerically; globally unproven; weakly separated at these designs; one demonstrated numerical stopping failure; extrapolation specification-dependent. |
| Subsidy accounting and welfare | PASS | The transfer identity `tau*post-policy participation` is internally correct for a fixed `tau` payment conditional on work. The response appropriately warns that `w` is only an index, currency interpretation requires a mapping, transfers are not resource gains, and social welfare needs fiscal costs, outside-option/nonmarket time, employer effects, externalities, incidence, and distributional weights. “Subsidy” should remain illustrative because no institutional payment mapping is supplied. |
| Simplify decision | PASS as a conditional prediction rule | For the simulated sample sizes, the simpler logit has lower average true-probability RMSE in every reported region and slightly lower held-out Brier loss. Using it for interpolation/short-horizon prediction while denying a homogeneous-type interpretation follows from the evidence. This conclusion is about predictive loss under this DGP and design, not universal model selection. |
| Partially identify decision | MIXED | No profile likelihood, SMM criterion region, weak-ID-robust confidence set, global observational-equivalence analysis, or economically credible bound on `d` or `pi` was actually computed. The proposal is a sensible next branch, but “profile a criterion region” is not automatically population partial identification. It should be described as a proposed sensitivity/set-inference exercise until the set and its coverage or identifying interpretation are established. |
| Abandon/continue decision | MIXED | The current evidence supports withholding latent-type interpretation at `n<=2500` and demanding discriminating data before structural promotion. It does not itself establish the stated reopening/abandonment conditions involving plausible profiles or external type-linked outcomes, because neither was run. Those bullets are defensible prospective decision rules, not completed empirical findings. The participation-curve result survives either branch. |

## Reproducible defects

### 1. Correct the bound-constrained first-order test

For minimization with lower bounds `lo` and upper bounds `hi`, reconstruct each objective gradient `g` at stored `x`, then use:

```python
pg = g.copy()
pg[(x <= lo + 1e-5) & (g > 0)] = 0.0
pg[(x >= hi - 1e-5) & (g < 0)] = 0.0
strict_kkt = np.linalg.norm(pg) < 1e-3
```

This reproduces stored raw gradient norms to at most `6.90e-13` for MLE and `3.97e-16` for SMM, but changes the strict rates as reported above. An equivalent implementation may use the optimizer's projected-gradient infinity norm and document its active-bound tolerance.

### 2. Exclude the nonstationary run from Wald coverage

Filter `raw_runs.csv` to `n==2500` and `seed==24006`. It has `mle_success=True`, `mle_near_boundary=False`, and `mle_hess_pd=True`, so it enters coverage, while direct reconstruction gives projected gradient norm `1.46999`. Coverage eligibility must include a valid KKT/convergence check.

### 3. Retain actual start records

The only start fields in `raw_runs.csv` are `{est}_starts_success` and `{est}_start_maxspread`. A reproducible start audit needs one row per `(n, seed, estimator, stage, start_id)` containing initial values, final parameters, objective, raw/projected gradient, active bounds, status/message, iterations/evaluations, and distance from the best objective. Until such a file exists, claims about objective-equivalent ridges across starts remain unverified.

### 4. Relabel or recompute policy-grid RMSE

The current `policy=np.linspace(1.5,2.5,201)` is not the realized counterfactual support. Report separate baseline RMSE on `[1,1.5]` and post-policy RMSE on `[2,2.5]`, or label `[1.5,2.5]` explicitly as a stress grid. Counterfactual participation/change calculations themselves need no correction.

## Research judgment

The strongest defensible endpoint is narrower than the response's computational narrative but close to its economic conclusion: the normalized mixture is correctly implemented and numerically locally full rank, yet it is weakly separated from a single logit on the training support and its primitive estimates are highly unstable at `n=500` and `n=2500`. The single logit is preferable for prediction in this experiment, without licensing homogeneous-cost interpretation. Latent-type and out-of-support claims should remain provisional. Numerical failure is not widespread; it is demonstrated for one selected MLE run. Before any Wald or profile-based structural inference, repair that run, store all start-level diagnostics, use KKT-valid convergence, distinguish supported from stress-grid prediction, and then construct an actual weak-ID/set-inference exercise with economically justified bounds.
