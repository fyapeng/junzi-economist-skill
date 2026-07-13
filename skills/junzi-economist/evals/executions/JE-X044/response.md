# Finite-state machine replacement: estimation, identification, and subsidy experiment

## Research judgment

With the discount factor fixed at 0.9, the controlled-transition estimator, NFXP, and the two-step CCP estimator recover the data-generating model. Across five seeds, increasing the panel from 400 to 2,000 machines sharply reduces RMSE; NFXP is more precise than the CCP estimator, while both predict held-out actions almost equally well. The computational diagnostics are clean.

The discount factor is a different matter. Conditional on this tightly parameterized model, a population CCP/KL calculation has a unique numerical minimum at the true beta on the tested grid. Yet nearby discount factors are observationally very similar, and the designated finite-sample likelihood is maximized at the upper grid boundary, beta=0.99, not at 0.90. Thus the honest conclusion is: beta is numerically point-separated in the population exercise under the maintained functional form, but weakly informed by these observables in realistic samples. Optimizer convergence supplies no identification evidence.

A subsidy of 1 raises replacement in the designated sample by 7.12 percentage points. It raises the owner's model-implied inclusive value, but under the explicitly imposed narrow resource-cost accounting it also raises real resource cost. These are different objects; a social-welfare conclusion requires externalities, incidence, and the social value of machine condition, none of which the choice model identifies.

## Economic environment and timing

One forward-looking owner controls one machine. At the beginning of period t the owner observes state x_t in {0,...,5} and two iid type-I extreme-value action shocks. The owner chooses keep (a_t=0) or replace (a_t=1). Deterministic flow utility is

    u(0,x) = -theta*x,       u(1,x) = -RC.

After the action, an independent deterioration draw d_t is Bernoulli(p). If the owner keeps, x_{t+1}=min(x_t+d_t,5). If the owner replaces, x_{t+1}=d_t. The state transition is therefore action-controlled and observed after choice. Simulation uses theta=0.65, RC=3.2, p=0.6, beta=0.9. Each panel has T=25 transitions. Initial states are iid discrete uniform on {0,...,5}, independently of all shocks. Periods 0--19 are used for estimation and periods 20--24 for conditional held-out action prediction.

Let P_K(p) and P_R(p) be the two controlled transition matrices. Omitting the additive Euler constant, which cancels from choice probabilities, the Bellman system is

    v_K(x) = -theta*x + beta P_K(x)' V,
    v_R(x) = -RC      + beta P_R(x)' V,
    V(x)   = log(exp(v_K(x)) + exp(v_R(x))),
    Pr(replace|x) = logistic(v_R(x)-v_K(x)).

The derivation and computation are verified for this finite state/action system; the welfare interpretation remains conditional on the accounting assumptions below.

## Estimators

Transition MLE estimates p before estimating preferences. A keep observation at x<5 reveals d_t from whether the state stays or rises; a replacement observation reveals d_t from whether the new state is 0 or 1. Keeps at the cap x=5 carry no information about p and are correctly excluded. The Bernoulli transition score at the estimate is numerically zero.

NFXP solves the Bellman contraction at every candidate (theta,RC) and maximizes the conditional action likelihood, taking beta=0.9 and the estimated p as inputs. It uses four dispersed starts, bounds theta in [0.02,2] and RC in [0.2,8], and an L-BFGS-B optimizer.

The distinct two-step CCP estimator first estimates six state CCPs with Jeffreys smoothing. It then applies Hotz--Miller log-odds inversion. In particular,

    (I-beta P_K)V = -theta*x - log(P_keep),

so V is affine in theta, and the six replacement log-odds equations are linear in theta and RC. Weighted least squares, with state information weights n_x P_x(1-P_x), estimates the two parameters without repeatedly solving the Bellman equation.

## Recovery and held-out prediction

Each cell below contains five independently simulated panels. Sample size is the number of machines; training choices are 20 times that number.

| Machines | p mean (RMSE) | NFXP theta mean (RMSE) | NFXP RC mean (RMSE) | CCP theta mean (RMSE) | CCP RC mean (RMSE) |
|---:|---:|---:|---:|---:|---:|
| 400 | 0.5966 (0.0061) | 0.6594 (0.0331) | 3.2211 (0.1264) | 0.6995 (0.0582) | 3.3090 (0.1629) |
| 2,000 | 0.5991 (0.0029) | 0.6463 (0.0099) | 3.1801 (0.0450) | 0.6645 (0.0261) | 3.2229 (0.0685) |

Held-out future-action prediction is similar for the two methods:

| Machines | NFXP log loss | CCP log loss | NFXP Brier | CCP Brier |
|---:|---:|---:|---:|---:|
| 400 | 0.48040 | 0.48084 | 0.15786 | 0.15808 |
| 2,000 | 0.48650 | 0.48657 | 0.16030 | 0.16033 |

These are conditional predictions for later periods of the same machines, not external validation on a new institution or transition regime.

## Computation and failure record

- All 10 designated NFXP fits succeeded. All 40 optimizer starts succeeded and converged to likelihood values differing by at most 4.6e-10 within a sample.
- The largest Bellman fixed-point residual among saved estimates is 8.92e-13.
- The CCP log-odds equation weighted RMSE averages 0.0486 and has a maximum of 0.0918 across samples. It need not be zero because empirical CCP noise is projected onto two structural parameters.
- Central finite-difference gradients were compared at steps 1e-4, 1e-5, and 1e-6. The largest 1e-4 versus 1e-5 component difference was 1.35e-4; the largest gradient norm at step 1e-5 was 8.85e-4.
- The transition score residual is zero to floating-point accuracy by construction of its Bernoulli MLE.
- No statistical-estimation branch failed. An initial executable branch failed because the dictionary key `RC` did not match the solver argument `rc`; its traceback is retained in `failed_branch_parameter_name.txt`, and the interface was corrected without changing the model or standards.

These findings establish numerical reliability for the implemented problem; they do not establish population identification or external validity.

## Can beta be estimated here?

### Sample likelihood geometry

For the designated N=2,000, seed=1103 panel, theta and RC were re-estimated at each beta on a 50-point grid from 0.50 to 0.99. The profile minimum occurs at the upper endpoint, beta=0.99. Selected results are:

| beta | profiled theta | profiled RC | relative NLL |
|---:|---:|---:|---:|
| 0.50 | 0.8540 | 2.9158 | 36.619 |
| 0.70 | 0.7528 | 3.0436 | 14.465 |
| 0.80 | 0.7021 | 3.1156 | 6.598 |
| 0.90 | 0.6514 | 3.1936 | 1.565 |
| 0.95 | 0.6262 | 3.2350 | 0.312 |
| 0.99 | 0.6060 | 3.2694 | 0.000 |

The truth is not rejected by a conventional one-parameter likelihood-ratio comparison, but the profile does not close before the imposed upper bound. A standard interior Hessian-based standard error for beta would therefore be misleading. There is strong compensation: higher beta is paired with lower theta and higher RC.

### Population separation under maintained restrictions

To distinguish finite-sample curvature from population identification, exact CCPs at the true parameters were treated as the population observables. At each beta, theta and RC minimize stationary-state-weighted Bernoulli KL divergence from those CCPs, with p known at truth. The grid minimum is beta=0.90 with effectively zero KL. Nearby alternatives are not exactly equivalent numerically but are close:

| beta | theta | RC | KL per choice | maximum CCP difference |
|---:|---:|---:|---:|---:|
| 0.80 | 0.7031 | 3.1281 | 3.81e-5 | 0.01035 |
| 0.89 | 0.6553 | 3.1926 | 4.04e-7 | 0.00109 |
| 0.90 | 0.6500 | 3.2000 | approximately 0 | 3.3e-10 |
| 0.91 | 0.6447 | 3.2075 | 4.09e-7 | 0.00110 |
| 0.99 | 0.6025 | 3.2696 | 3.50e-5 | 0.01030 |

This is numerical evidence of point separation on the tested compact grid, conditional on EV1 shocks, the utility normalization, known transition form, state support, stationary KL weights, and the two-parameter flow-utility restriction. It is not an analytic injectivity proof. The observationally similar neighboring parameterizations explain why sample estimation of beta is unstable even though the population grid has a unique minimum. Additional exclusion restrictions or variation that changes continuation values without directly changing current utility would be the natural next discriminating evidence.

## Replacement subsidy

The counterfactual gives the owner a subsidy s=1 upon replacement, so private replacement cost becomes RC-s. It uses the designated N=2,000 estimate (theta=0.65143, RC=3.19359, p=0.59680) and beta=0.9.

| Object | No subsidy | Subsidy 1 | Change |
|---|---:|---:|---:|
| Stationary replacement rate | 0.28266 | 0.35387 | +0.07121 |
| Private inclusive value, uniform initial state | -9.7839 | -6.4494 | +3.3345 |
| Fiscal outlay per stationary period | 0 | 0.35387 | +0.35387 |
| Real resource cost per stationary period | 1.41609 | 1.51542 | +0.09932 |
| Discounted resource cost, uniform initial state | 14.5720 | 15.6736 | +1.1016 |

The private inclusive value includes the owner's extreme-value shocks and the transfer. The resource calculation instead treats theta*x while keeping and RC upon replacement as real costs and treats the subsidy as a transfer; it excludes the taste shocks. Under that narrow criterion the subsidy raises costs, because more frequent replacement costs outweigh lower deterioration costs. This is not a general social-welfare result. A complete welfare analysis would need the machine's output/service value, breakdown or safety externalities, tax-finance distortions, subsidy incidence, distributional weights, and any effects on other parties.

Conditional on beta=0.9 and p-hat, local Hessian draws give a 5--95% interval of [0.06947, 0.07311] for the replacement-rate effect, [3.310, 3.360] for the private-value effect, and [0.09726, 0.10156] for the per-period resource-cost effect. These intervals do not propagate discount-factor uncertainty. Reprofiling theta and RC shows that changing beta from 0.70 to 0.98 moves the rate effect from about 0.0818 to 0.0669 and the private-value effect from 1.27 to 15.85; the latter is highly beta-sensitive because it is an infinite-horizon discounted value. Moving p by plus or minus two transition standard errors changes the rate effect by less than 0.0003 in the displayed cases.

## Claim status and limits

- Parameter recovery at fixed beta: supported for the simulated designs tested.
- Numerical implementation: verified for the saved finite-state model and tolerances.
- Population identification of beta: provisional numerical point separation under strong maintained restrictions; no analytic global proof.
- Practical estimation of beta in the designated sample: weakly informed/boundary-profiled.
- Subsidy effects: model-implied and specification-conditional.
- Social welfare: underidentified without additional economic primitives and incidence assumptions.

All executable code, raw results, profiles, diagnostics, the preserved failed branch, and provenance are stored beside this report.
