# Structural work participation with latent fixed-cost heterogeneity

## Research judgment

This experiment is a warning against promoting a latent-class interpretation from smooth participation data. The correctly specified two-type model is locally population-identified after normalization in this design, but only weakly: its population derivative matrix has condition number 938. A single logit approximates the true training probability with population RMSE 0.00037 and maximum error 0.00092. In 40 replications at each of `n=500` and `n=2,500`, both mixture estimators frequently choose the imposed cost-gap boundary, disagree across starts, and recover the mixture primitives poorly even as their participation predictions remain usable. This is weak separation/sample likelihood geometry, compounded in some runs by numerical stopping; it is not evidence that the true DGP is a single logit.

The practical endpoint is therefore: report the participation curve and supported-policy predictions, but treat the two masses, mixing probability, and out-of-support subsidy calculations as underidentified/unstable at these sample sizes. Do not claim recovered latent “types.”

## Model, normalization, and design

Type `t` works when `a0 + a1 w - k_t + epsilon_1 >= epsilon_0`. Type-I extreme-value shocks imply

`P(work|w) = pi Lambda(b+a1 w) + (1-pi) Lambda(b+a1 w-d)`,

where `b=a0-k1`, `d=k2-k1>0`, and `pi` is the low-cost mass. Because `a0` and both `k_t` enter only through differences, they are not separately identified. I normalize `k1=0`, impose the label ordering `d>0`, and estimate `(b,a1,d,pi)`. Bounds are `b in [-4,4]`, `a1 in [-1,4]`, `d in [.02,5]`, and `pi in [.02,.98]`.

The deliberately weak-separation DGP is `(b,a1,d,pi)=(-0.10,1.25,0.80,0.58)`. For every replication, training wages are iid `Uniform[-1,1]`. A fresh held-out choice sample is half `Uniform[-.75,.75]` interpolation and half `Uniform(1,1.5]` extrapolation. The noise-free validation grids separately cover training, extrapolation `(1,1.5]`, and policy support `[1.5,2.5]`.

Population identification must not be inferred from optimizer convergence. On a dense training grid, the four columns of the probability derivative are numerically full rank, with singular values `(0.2863, 0.1095, 0.001213, 0.000305)`. This is evidence of local population identification under the functional form and continuous support, not a proof of global injectivity. The two tiny singular values diagnose weak separation.

## Estimators and computation

The MLE maximizes the individual Bernoulli likelihood with an analytic gradient. The distinct SMM estimator minimizes seven residual moments

`g_j(theta) = n^{-1} sum_i L_j(w_i)[y_i-P(w_i;theta)]`, `j=0,...,6`,

where `L_j` are Legendre polynomials on `[-1,1]`. It is two-step: an identity-weight pilot is followed by the inverse sample covariance of the seven pilot moment contributions (with a `1e-6 I` ridge). Thus SMM is overidentified and not a relabeled likelihood estimator.

Each mixture estimator uses eight dispersed starts, analytic gradients, bound-constrained L-BFGS-B, and tight objective/gradient settings. All starts and boundary outcomes are retained. “Optimizer success” records the software flag; “strict convergence” additionally requires gradient norm below `1e-3`. The analytic likelihood gradient agrees with central differences to `6.46e-8`. A positive-definite observed-information Wald interval is computed only for interior MLE runs; no SMM coverage is reported because weak identification, frequent boundaries, and a small Monte Carlo make normal sandwich coverage misleading.

## Monte Carlo recovery and failures

All entries use 40 seeds per sample size. Bias/RMSE are relative to the normalized truth.

| n | estimator | b bias/RMSE | a1 bias/RMSE | d bias/RMSE | pi bias/RMSE |
|---:|:--|--:|--:|--:|--:|
| 500 | MLE | 2.035 / 2.437 | 0.991 / 1.146 | 3.988 / 4.005 | -0.142 / 0.269 |
| 500 | SMM | 1.595 / 2.059 | 1.070 / 1.255 | 3.526 / 3.825 | -0.054 / 0.255 |
| 2,500 | MLE | 1.632 / 2.130 | 0.565 / 0.697 | 3.283 / 3.390 | -0.115 / 0.290 |
| 2,500 | SMM | 1.458 / 1.989 | 0.589 / 0.729 | 3.122 / 3.342 | -0.094 / 0.287 |

| n | estimator | software success | strict convergence | at boundary | starts differ > .10 |
|---:|:--|--:|--:|--:|--:|
| 500 | MLE | 100% | 22.5% | 80.0% | 60.0% |
| 500 | SMM | 100% | 80.0% | 77.5% | 55.0% |
| 2,500 | MLE | 100% | 62.5% | 40.0% | 65.0% |
| 2,500 | SMM | 100% | 100% | 45.0% | 55.0% |

The software flags alone are plainly uninformative. MLE boundary incidence falls with sample size, and RMSE falls for `b`, `a1`, and `d`, which is consistent with weak rather than absent population identification. But 2,500 observations remain insufficient for a stable latent-class decomposition. Start disagreement can remain high because nearly observationally equivalent parameter combinations lie along a flat ridge; it does not by itself mean the best objective was not found.

Only 20% (`n=500`) and 60% (`n=2,500`) of MLE runs were interior with positive-definite observed information. Conditional 95% Wald coverage at `n=2,500` was `(b,a1,d,pi)=(.667,.917,.583,.625)`. These conditional figures are not nominal unconditional coverage: excluding boundary/non-PD cases selects the favorable geometry. At `n=500`, only eight runs were eligible, so the superficially high conditional rates are not defensible evidence.

## Fit and held-out predictions

Mean probability RMSE against the true curve:

| n | model | training `[-1,1]` | extrapolation `(1,1.5]` | policy `[1.5,2.5]` |
|---:|:--|--:|--:|--:|
| 500 | MLE mixture | .0306 | .0641 | .0723 |
| 500 | SMM mixture | .0330 | .0677 | .0716 |
| 500 | single logit | .0208 | .0250 | .0215 |
| 2,500 | MLE mixture | .0155 | .0340 | .0482 |
| 2,500 | SMM mixture | .0156 | .0347 | .0491 |
| 2,500 | single logit | .0117 | .0176 | .0149 |

The correctly specified model loses in finite-sample prediction because its weakly identified flexibility creates variance. This does not make the single logit structurally correct. For an untargeted check, four-bin training calibration MAE at `n=2,500` is .00676 (MLE mixture), .00685 (SMM), and .00957 (logit); hence the mixtures can track realized bins while estimating the wrong decomposition. SMM's targeted weighted moment norm falls from .0907 to .0336 as `n` grows. On fresh held-out binary outcomes, mean Brier scores at `n=2,500` are .20813, .20816, and .20740, respectively—essentially indistinguishable, with the logit slightly better. Targeted fit, untargeted fit, and structural recovery therefore tell different stories.

## Subsidy accounting, not welfare

For an illustrative wage-index subsidy, baseline `w` is uniform on `(1,1.5]`, the policy shifts the index by `tau=1`, and the transfer account is `tau` times post-policy participation per person. The true post-policy participation is .9088 and the true change is .1621.

| n | model | post-policy participation, mean (SD) | participation change, mean | transfer/person, mean |
|---:|:--|--:|--:|--:|
| 500 | MLE mixture | .9279 (.0685) | .1573 | .9279 |
| 500 | SMM mixture | .9348 (.0650) | .1547 | .9348 |
| 500 | single logit | .9158 (.0251) | .1555 | .9158 |
| 2,500 | MLE mixture | .9227 (.0523) | .1572 | .9227 |
| 2,500 | SMM mixture | .9231 (.0534) | .1570 | .9231 |
| 2,500 | single logit | .9115 (.0155) | .1582 | .9115 |

The mixture counterfactual is visibly more seed-sensitive, even though mean effects happen to be close here. This policy support lies entirely outside training support, so the result is conditional on the logit-mixture functional form. The transfer figures are accounting quantities only. Because `w` is an index, interpreting them as currency additionally requires a wage-index-to-payment mapping. None is “social welfare”: that would require fiscal resource or marginal public-funds costs, the value of the outside option and nonmarket time, effects on workers and employers, other externalities, and explicit distributional weights.

## Decision rule

- **Simplify to a single logit** when the target is interpolation or short-horizon prediction and held-out performance is no worse; label it a reduced behavioral approximation, not proof of homogeneous costs.
- **Partially identify** mixture-sensitive counterfactuals by profiling likelihood/SMM regions and reporting the range of policy predictions when substantively credible bounds on `d` and `pi` exist. Do not use the optimizer box as an economic bound.
- **Continue the mixture claim** only with discriminating information: repeated choices, direct cost proxies, excluded shifters that rotate type-specific participation, wider supported wage variation, or a much larger sample. Confirm stability across bounds and profiles.
- **Abandon the latent-type interpretation** if plausible bounds/profiles still include near-single-logit decompositions, type parameters remain boundary-driven, or external type-linked outcomes do not validate the inferred groups. Preserve the participation curve result even when the type story is abandoned.

Status: the participation DGP and computation are verified for this simulation; local population rank is numerically supported; finite-sample mixture-parameter recovery and Wald inference are unfavorable; the latent-type and out-of-support structural claims are underidentified in practice.
