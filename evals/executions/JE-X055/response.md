# Dynamic replacement model: exact closed-domain transfer

## Research judgment

The compact experiment successfully recovers a dynamic replacement model with estimated action-controlled transitions using both NFXP and a genuinely distinct two-step CCP inversion. The continuous population-observable Jacobian has full local rank at the NFXP estimate, but this is **local evidence only** under the maintained logit model, fixed discount factor, observed policy support, and normalizations. The restricted search found no closer observational alternative outside an L-infinity radius of 0.15 than a squared observable distance of `0.000984932245666759`; this is an auditable numerical falsification exercise, not proof of global identification.

## Economic environment and data

- One agent observes condition state `x in {0,1,2,3,4}` and subsidy `s`, then chooses keep (`a=0`) or replace (`a=1`). IID type-I extreme-value shocks are integrated out; the Euler-constant level is omitted.
- Deterministic utility is `u(keep)=-c*x` and `u(replace)=-r+s`; `beta=0.93` is fixed.
- Keep moves from `x<4` to `x+1` with probability `p_m` and otherwise stays; state 4 is absorbing under keep. Replacement moves to 0 with probability `p_r` and to 1 otherwise.
- The fixed simulated population has 450 agents, 35 periods, 15,750 retained observations, seed 55055, and no outcome-, shock-, or solver-based selection.
- Subsidies `s=0` and `s=0.4` are observed regimes. `s=0.2` is explicitly only model interpolation.

## Estimation

True parameters `(c,r,p_m,p_r)` were `(0.42, 2.15, 0.72, 0.86)`.

| Method | c | r | p_m | p_r |
|---|---:|---:|---:|---:|
| NFXP | 0.429196 | 2.147406 | 0.722201 | 0.858869 |
| CCP inversion MD | 0.428472 | 2.140894 | 0.722201 | 0.858869 |

Transitions are estimated directly from controlled-transition counts: 12,164 eligible keep transitions and 3,315 replacement transitions. NFXP nests a Bellman solve inside the choice likelihood. The CCP estimator instead applies Jeffreys-smoothed empirical CCPs, values the empirical CCP policy by a linear system, and minimizes log-odds inversion residuals; it never calls the Bellman solver.

All eight declared NFXP starts and all eight CCP starts were retained and accepted. The selected NFXP choice negative log likelihood is `9111.515741167252`; its projected-gradient infinity norm is `1.1855e-4` under the declared `2e-3` acceptance threshold. The selected CCP objective is `0.001343923790109`; its projected-gradient norm is `4.30e-8`. The maximum reported Bellman residual is below `1.8e-15`.

## Domain, local rank, and restricted alternative search

The full declared economic domain is the closed box

`c in [0.05,1.50], r in [0.20,5.00], p_m in [0,1], p_r in [0,1]`,

implemented directly in economic coordinates, with every boundary included. The NFXP estimate's nearest-boundary slacks are `(0.379196, 1.947406, 0.277799, 0.141131)`.

The population mapping consists of ten model CCPs across the two observed subsidy regimes plus the two controlled-transition probabilities. Its `12 x 4` continuous Jacobian has singular values `(2.126572, 1.014702, 0.992319, 0.212754)` at the NFXP estimate. At rank tolerance `1e-7`, numerical rank is four. This supports only a continuous **local population-rank** statement; it does not establish global injectivity, finite-sample coverage, or policy invariance.

The alternative restriction is the full closed set

`theta in closed box` and `max_j |theta_j-theta_hat_j| >= 0.15`.

It is represented exactly as the union of all nonempty lower and upper closed slabs. Seven slabs are nonempty; the eighth possible slab, `p_r >= p_r_hat+0.15`, is empty because its lower endpoint exceeds 1. Direct bounds therefore cover all feasible boundaries without a transformed-coordinate truncation. The production search retained 378 rows: 27 starts in each of two independent seeded reruns for each nonempty slab. All 378 met success, projected-gradient (`2e-6`), box, and restriction acceptance rules.

The best candidate is `(0.452756, 2.297406, 0.725540, 0.863055)`. It lies exactly on the nonlocal boundary through `r=r_hat+0.15`: reported restriction slack is `-8.33e-17`, accepted under feasibility tolerance `1e-10`; nearest box-boundary slack is `0.136945`. Its projected-gradient norm is `1.19e-8`. A separate value-iteration implementation independently reran every slab from three new starts and reproduced the best objective to less than `1e-15`.

## Policy accounting

These are stationary discounted deterministic-flow quantities; integrated taste-shock surplus is deliberately excluded from the welfare criterion. Subsidies are transfers, not resources, and fiscal financing distortions are omitted.

| subsidy | support | replacement rate | private payoff | fiscal transfer | real resource cost | social welfare |
|---:|---|---:|---:|---:|---:|---:|
| 0.0 | observed | 0.318879 | -13.265471 | 0.000000 | 13.265471 | -13.265471 |
| 0.2 | model interpolation | 0.336108 | -12.544330 | 0.960310 | 13.504639 | -13.504639 |
| 0.4 | observed | 0.354977 | -11.771564 | 2.028442 | 13.800005 | -13.800005 |

Private payoff includes the subsidy received. Social welfare cancels the transfer exactly: `private payoff - fiscal transfer = -real resource cost`. Thus the model predicts that the subsidy improves the agent's deterministic private payoff while raising replacement and real resource use; under this deliberately narrow welfare criterion, social welfare falls. This is a model-conditional accounting result, not a general policy recommendation.

## Verification coverage and limits

The independent verifier passed all ten executable checks. It separately recomputed controlled transitions; reoptimized NFXP with value iteration and four new starts; reoptimized CCP inversion; reconstructed the Jacobian and SVD; audited all nonempty slabs and both saved seeds; recomputed the selected alternative and feasibility slacks; reran every slab independently; and checked the policy-support labels and transfer-resource-welfare identity.

It does **not** verify global identification, estimator sampling distributions, confidence coverage, external validity, unobserved-regime extrapolation, or welfare criteria that include taste-shock surplus, financing costs, externalities, or distributional weights. Derivation status is `local-only` for identification and `verified-piecewise/computational` for the closed-domain search and accounting identities.

## Artifacts

- `summary.json`: headline model, estimates, diagnostics, support labels, and accounting.
- `nfxp_starts.json`, `ccp_starts.json`: every estimator start and terminal diagnostic.
- `alternative_search.csv`: complete 378-row restricted search history.
- `independent_verification.json`: pass/fail record, fresh reruns, and claim-by-claim coverage map.
- `compact_arrays.npz`: empirical choice counts/CCPs, Jacobian, and singular values.
- `simulated_panel.csv`: fixed row-level simulated sample, UTF-8 with BOM.
- `run_model.py`, `independent_verify.py`: production and separate verifier implementations.

