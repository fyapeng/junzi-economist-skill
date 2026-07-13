# Replication response

## Research judgment

The bounded two-product, common-ownership Bertrand-logit simulation completed for all five predeclared seeds (120 markets and 240 product rows per seed). There were zero simulation, equilibrium, and estimation failures. The valid excluded cost shifter materially moves price and improves demand-slope recovery relative to OLS; the deliberately invalid proxy is biased in the expected direction. These are finite-sample recovery results conditional on the stated logit and ownership specification, not a population-identification proof.

## Design and timing

- Demand is `log(s_j/s_0) = 2 + 0.4 x_j - 1.2 p_j + xi_j`. A single multiproduct firm owns both products and sets prices simultaneously after observing costs and demand shocks.
- `w` is realized as a bounded cost shifter before pricing, enters marginal cost, is independent of the primitive demand shocks by construction, and is excluded from utility. The valid GMM instruments are `(1, x, w, w^2)`.
- The invalid proxy is `z_bad = w + 0.8 xi + 0.05 e`. It is recorded only after `xi` is realized and pricing occurs. Its direct `xi` component violates demand exclusion; it is used only for a labeled invalid-IV diagnostic.
- All primitives are drawn once from declared bounded supports. Analytical real marginal-cost support is `[1.03, 2.17]`; under the 0.20 subsidy, private marginal-cost support is `[0.83, 1.97]`. No redraw, clipping, conditional market survival, or observation dropping occurs.

## Equilibrium and numerical evidence

All 9,600 starts were retained and accepted across 1,200 baseline/subsidy market cases. The finite eight-start scan detected exactly one clustered root per case (1,200 roots total), but does not establish global uniqueness. Prices were bounded at private marginal cost plus `[1e-8, 10]`. Maximum raw and share-scaled FOC residuals were 1.465e-14 and 6.655e-14; scaled-Jacobian condition numbers ranged from 1 to 1. Observed shares were not degenerate: the minimum product share was 0.0864 and minimum outside share was 0.5933.

The separate implementation passed all 1,200 cases. Its maximum recomputed raw FOC was 1.316e-14, maximum finite-difference profit gradient was 1.110e-10, and maximum gap from a fresh root solve was 7.719e-09.

## Estimation and recovery

Across seeds, the mean price coefficient was -0.532 under OLS, -1.255 under 2SLS, and -1.256 under two-step GMM, against truth `-1.2`. The invalid proxy IV mean was -0.918. The valid shifter's mean first-stage price coefficient was 0.203; mean sample correlations with `xi` were -0.032 for valid `w` and 0.214 for invalid `z_bad`.

Using each seed's GMM demand slope and the observed ownership matrix, recovered markups have mean error -0.0450 and RMSE 0.1188; recovered marginal costs have the opposite mean error and the same RMSE. Full seed-level coefficients, moment norms, cross-moment conditioning, and product-level recoveries are saved in the output tables.

## Counterfactual accounting

Market-size-normalized means are kept as distinct objects:

| Scenario | Consumer payment | Producer profit | Subsidy | Tax | Real resource cost | Consumer surplus | CS + profit - net fiscal |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 0.9353 | 0.4106 | 0.0000 | 0.0000 | 0.5247 | 0.3333 | 0.7439 |
| Subsidy | 0.9882 | 0.4800 | 0.0729 | 0.0000 | 0.5811 | 0.3784 | 0.7855 |

The last column uses the explicit criterion `consumer surplus + producer profit - subsidy payment + tax payment`; payments and revenue remain transfers, while production cost is the real resource measure. The model omits marginal cost of public funds, distributional weights, labor or input-market effects, entry, and externalities, so the reported welfare change is criterion-specific rather than a general policy recommendation.

## Artifact map

- `replication.py`: complete production branch.
- `independent_check.py`: separate equation implementation, fresh solves, and finite-difference profit checks.
- `outputs/all_start_traces.csv`: every start and acceptance diagnostic.
- `outputs/detected_roots.csv`: all roots detected by the finite scan.
- `outputs/estimates.csv`, `outputs/markup_cost_recovery.csv`, `outputs/sample_diagnostics.csv`: estimation, moments, conditioning, support, and recovery.
- `outputs/welfare_market.csv`: disaggregated market-level accounting.
- `outputs/compact_results.json`: compact raw result.
- `outputs/run_summary.json`: predeclaration, versions, exact-count status, and separate failure counts.
- `provenance.md`: commit and read-scope provenance.
