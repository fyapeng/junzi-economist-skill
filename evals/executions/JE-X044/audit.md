# Independent audit

## Verdict: MIXED

The implemented finite-state dynamic replacement model is internally coherent and the main saved numerical results reproduce. Timing, controlled transitions, the cap-state treatment in the transition likelihood, Bellman/EV1 choice probabilities, the fixed-beta NFXP estimates, the two-step CCP equations, held-out metrics, sample and population profile values, stationary subsidy calculations, and the separation of private, fiscal, resource, and social-welfare objects all pass substantive recomputation.

The endpoint is not a full pass for four reasons. First, a 50-point population grid with local numerical minimization does not establish population point identification on the continuous parameter space; the report mostly acknowledges this, but still uses “point-separated” language that is stronger than its evidence. Second, five simulation seeds per sample size document favorable recovery in the tested draws but are too few to support a general estimator-recovery claim. Third, `PROVENANCE.md` says that `optimizer_starts.json` contains every NFXP start, but the 150 starts used for the sample beta profile are discarded and absent from that file. Fourth, `verify_analysis.py` is not an independent implementation: it imports `solve` and `trans` from `run_analysis.py` and mostly checks stored artifacts. These are evidence/provenance defects, not failures of the core economic calculations.

I did not modify any endpoint original. Independent calculations were run outside the endpoint in `C:\Users\ENAN\AppData\Local\Temp\x044-independent-audit-scratch\audit_recompute.py`; results are in `audit_recompute_output.json` there. The requested audit file is the only new endpoint artifact.

## Audit matrix

| Object | Status | Independent finding |
|---|---|---|
| Timing and controlled transitions | PASS | Choice precedes the independent Bernoulli deterioration draw. Keep gives `min(x+d,5)` and replacement gives `d`. Both transition matrices are row-stochastic. |
| Cap-state information for `p` | PASS | A keep at `x=5` is uninformative and is excluded; replacement observations and non-cap keeps reveal `d`. In the designated panel, 50 cap-keeps were excluded and the independent estimate is `p_hat=0.596795994993742`, matching the saved value. |
| Bellman system and EV1 probabilities | PASS, with normalization note | The log-sum Bellman equation and `logistic(v_R-v_K)` probabilities are correct. The truth residual independently reproduces as `8.79e-13`. Absolute private-value levels omit the Euler constant; see the qualification below. |
| NFXP likelihood and fixed-beta optimizer results | PASS | State-action counts are sufficient for the conditional action likelihood. Independent objective evaluation differs from the saved designated NLL by only `3.64e-12`. Two derivative-free starts converge to `(0.6514313, 3.1935910)` and the same NLL. |
| Optimizer accounting | MIXED | All 40 recovery-fit starts succeeded and the maximum within-sample objective spread is `4.51e-10`. But the beta-profile starts are not preserved, contradicting the artifact-map claim that every NFXP start is stored. |
| CCP estimator and linear equations | PASS | It is genuinely a two-step Hotz–Miller-style CCP inversion for this finite-state model. Jeffreys-smoothed empirical CCPs enter the inversion, and the signs in both the value equation and linear regression are correct. |
| Recovery summaries | PASS numerically; MIXED inferentially | All means and RMSEs reproduce exactly. RMSE falls from `N=400` to `N=2,000` in these five paired seeds. Five draws per cell are a demonstration, not a Monte Carlo basis for a general “supported recovery” claim or coverage assessment. |
| Held-out split and prediction | PASS | Training uses periods 0–19 and testing uses 20–24. The split is temporal and action prediction is conditional on the observed held-out states. The report correctly says this is same-machine conditional prediction, not external validation. |
| Gradient and residual claims | PASS | The largest saved central-difference gradient norm at `h=1e-5` is `8.849e-4`; the maximum `h=1e-4` versus `1e-5` component change is `1.35e-4`. Bellman and transition-score residual statements reproduce. |
| Sample beta profile | PASS | Re-evaluated profile NLLs match. The minimum is the imposed upper grid endpoint `beta=0.99`; at truth the relative NLL is `1.564878`, so the conventional LR statistic is about `3.1298`. |
| Population KL profile and identification language | MIXED | Selected KL values and compensating parameters reproduce, including the grid minimum at `0.90`. This establishes a unique minimum among tested grid points under the maintained restrictions, not injectivity or point identification on the continuous parameter space. |
| Observational similarity | PASS | Independent four-start calculations reproduce maximum CCP gaps of about `0.00109` at `beta=0.89/0.91` and `0.01030` at `0.99`, with very small KL losses. The report’s practical weak-information conclusion is warranted. |
| Subsidy transition and stationary calculations | PASS | Baseline and subsidy stationary residuals are `1.42e-16` and `2.22e-16`. The replacement-rate effect independently reproduces as `0.07121021864`. |
| Private value, fiscal transfer, and real resources | PASS, with normalization note | The private policy problem uses `RC-s`; fiscal outlay is `s` times the stationary replacement rate; the subsidy is excluded from real-resource cost. Saved flow and discounted resource-cost effects reproduce exactly. |
| Uncertainty and welfare distinctions | PASS | Intervals are explicitly conditional on fixed `beta` and `p_hat`; beta sensitivity is shown, and no social-welfare claim is made. The report correctly identifies omitted output/service value, externalities, financing distortions, incidence, and distributional weights. |
| Preserved failure | PASS | `failed_branch_parameter_name.txt` is nonempty and retains the original `RC` versus `rc` interface `TypeError`. |

## Core derivations checked

Let `q(x)=Pr(replace|x)`, `P_K` be the keep transition, and `P_R` the replacement transition. With the normalized EV1 inclusive value,

`v_K=-theta*x+beta*P_K V`,

`v_R=-RC+beta*P_R V`,

`V=log(exp(v_K)+exp(v_R))`, and

`log(q/(1-q))=v_R-v_K`.

Because `1-q=exp(v_K-V)`, `V=v_K-log(1-q)`, hence

`(I-beta*P_K)V=-theta*x-log(1-q)`.

Writing

`V=A[-log(1-q)] + theta*A[-x]`, where `A=(I-beta*P_K)^(-1)`,

gives

`log(q/(1-q))-beta*(P_R-P_K)A[-log(1-q)]`

`= theta*{x+beta*(P_R-P_K)A[-x]}-RC`.

This is exactly the equation implemented in `fit_ccp`: the first regressor has a positive coefficient `theta` and the constant regressor is `-1` with coefficient `RC`. The independent structural identity error, using Bellman-implied CCPs, is `2.22e-15`; the design matrix has rank two. For the designated sample the independent WLS estimate is `(theta,RC)=(0.6843500964,3.2734673573)`, exactly matching the saved CCP estimate.

## Reproducible defects and required wording corrections

### 1. Population identification is not established

`run_analysis.py` evaluates only 50 beta values from `0.50` to `0.99`. At each value the original population profile uses one L-BFGS-B start at the truth. This can show a unique numerical minimum **among those evaluated points**. It cannot rule out an observationally equivalent parameterization between grid points, outside the grid, or at an unvisited optimizer basin.

Independent four-start optimization at selected beta values supports the saved numerical profile:

| beta | theta | RC | KL per choice | max CCP gap |
|---:|---:|---:|---:|---:|
| 0.89 | 0.65529718 | 3.19256249 | `4.0402e-7` | `0.00108533` |
| 0.90 | 0.65000000 | 3.20000000 | numerical zero | `1.01e-10` |
| 0.91 | 0.64470543 | 3.20749451 | `4.0942e-7` | `0.00109692` |
| 0.99 | 0.60245737 | 3.26956248 | `3.5004e-5` | `0.01030446` |

The defensible claim is: **“The true beta uniquely minimizes the stationary-state-weighted population KL criterion among the 50 tested beta grid points, after numerical profiling of theta and RC; nearby beta values remain observationally close. This is not a proof of local or global population identification.”** Replace “numerically point-separated in the population exercise” and the `supported`-sounding identification status with this grid-specific statement.

### 2. Recovery evidence is too small for a general support label

The recovery table is arithmetically correct, and all ten runs are retained. However, each sample-size cell contains only five seeds. There are no sampling distributions, coverage rates, failure-rate precision, or additional sample sizes. “Recovers the DGP in these ten simulated panels, with lower RMSE in the five larger panels” is supported. “Parameter recovery at fixed beta: supported for the simulated designs tested” is too broad unless explicitly limited to this small demonstration; a credible estimator-performance claim needs substantially more replications and coverage/failure reporting.

### 3. Optimizer-start provenance is incomplete

`optimizer_starts.json` contains 10 recovery cells times 4 starts = 40 starts, all successful. But `run_analysis.py` lines 248–253 runs three starts at each of 50 beta values and saves only the selected point, discarding the 150 start-level records. The population profile likewise saves only one optimizer result per beta. Therefore `PROVENANCE.md` must not describe `optimizer_starts.json` as containing “every NFXP start.” It contains every **fixed-beta recovery-fit** start only. This omission matters most for the boundary sample profile and the identification discussion.

### 4. Verification is fresh but not independent

`verify_analysis.py` imports `TRUE`, `solve`, and `trans` from `run_analysis.py`; it then reads the saved recovery, profile, and counterfactual files. It freshly resolves the truth Bellman problem, but it does not independently implement the transition or Bellman logic and does not reconstruct estimation, held-out metrics, profiles, or counterfactuals from the deterministic simulated panels. Accordingly, `PROVENANCE.md` should call it a fresh invariant/schema check, not “independent artifact and invariant checks rerun from primitives.”

### 5. Private inclusive-value levels require an explicit EV1 normalization label

The Bellman solver intentionally omits the Euler constant. Under the conventional uncentered standard type-I EV1 normalization, the expected-max value level would be higher by `EulerGamma/(1-beta)=5.7721566490` at `beta=0.9`. This constant does not affect CCPs, policies, or the subsidy private-value **difference**, because it cancels across the two policies. Thus the reported effect `3.3344679254` is correct, but the level entries `-9.7839` and `-6.4494` should be labeled “Euler-constant-normalized inclusive value” rather than implying an unqualified expected utility level that fully includes the shocks.

## Independently reproduced numerical checkpoints

- Designated `p_hat`: `0.596795994993742`.
- Truth Bellman residual: `8.79296635503124e-13`.
- Designated NFXP NLL: matches saved value within `3.64e-12`.
- Designated central-difference gradient at `h=1e-5`: `(8.8494e-4, 6.2391e-5)`.
- Recovery optimizer records: 40/40 successes; maximum within-cell NLL spread `4.51e-10`.
- Sample profile: minimum `beta=0.99`; truth relative NLL `1.5648780496`.
- Subsidy replacement-rate effect: `0.07121021864`.
- Subsidy normalized private-value effect: `3.33446792541`.
- Subsidy stationary fiscal outlay: `0.35386803705`.
- Subsidy stationary real-resource-cost effect: `0.09932394079`.
- Subsidy discounted resource-cost effect from a uniform initial state: `1.10159563464`.

## Final claim statuses

- Economic timing, state/action structure, and controlled transitions: **verified-piecewise for the finite state space**.
- Fixed-beta implementation and saved numerical results: **verified for the designated code, seeds, bounds, and tolerances**.
- Hotz–Miller-style CCP linearization: **verified algebraically and numerically**.
- Fixed-beta estimator recovery: **exploratory/small Monte Carlo demonstration**, not broadly supported estimator performance.
- Population identification of beta: **not established**; the artifact provides grid-specific numerical separation under strong maintained restrictions.
- Practical beta information in the designated sample: **weak/boundary-profiled**, supported by the saved and independent calculations.
- Subsidy effects: **model-implied and specification-conditional**; the numerical accounting is verified.
- Social welfare: **underidentified**, correctly left unresolved.
