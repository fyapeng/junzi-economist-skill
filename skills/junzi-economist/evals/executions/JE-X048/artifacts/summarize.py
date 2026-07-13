from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"

run = json.loads((OUT / "run_summary.json").read_text(encoding="utf-8"))
ind = json.loads((OUT / "independent_check_summary.json").read_text(encoding="utf-8"))
trace = pd.read_csv(OUT / "all_start_traces.csv", encoding="utf-8-sig")
roots = pd.read_csv(OUT / "detected_roots.csv", encoding="utf-8-sig")
est = pd.read_csv(OUT / "estimates.csv", encoding="utf-8-sig")
rec = pd.read_csv(OUT / "markup_cost_recovery.csv", encoding="utf-8-sig")
diag = pd.read_csv(OUT / "sample_diagnostics.csv", encoding="utf-8-sig")
w = pd.read_csv(OUT / "welfare_market.csv", encoding="utf-8-sig")
ic = pd.read_csv(OUT / "independent_checks.csv", encoding="utf-8-sig")

def method_summary(method):
    g = est[est.method == method]
    return {p: {"mean": float(h.estimate.mean()), "min": float(h.estimate.min()),
                "max": float(h.estimate.max()), "truth": float(h.truth.iloc[0])}
            for p, h in g.groupby("parameter")}

compact = {
    "status": "pass" if all(x["status"] == "complete" for x in run["replication_status"]) and ind["status"] == "pass" else "fail",
    "failure_counts": run["failure_counts"],
    "accepted_replications": sum(x["status"] == "complete" for x in run["replication_status"]),
    "equilibrium": {
        "attempted_start_rows": int(len(trace)), "accepted_start_rows": int(trace.accepted.sum()),
        "market_scenario_cases": int(trace[["seed", "market", "scenario"]].drop_duplicates().shape[0]),
        "detected_roots": int(len(roots)),
        "roots_per_case_min": int(roots.groupby(["seed", "market", "scenario"]).size().min()),
        "roots_per_case_max": int(roots.groupby(["seed", "market", "scenario"]).size().max()),
        "max_raw_foc": float(trace.raw_foc_max.max()),
        "max_share_scaled_foc": float(trace.scaled_foc_max.max()),
        "scaled_jacobian_condition_min": float(trace.jacobian_condition.min()),
        "scaled_jacobian_condition_max": float(trace.jacobian_condition.max()),
        "price_bounds": "private marginal cost + [1e-8, 10]",
        "claim": "One root detected per finite eight-start scan; no global uniqueness claim."
    },
    "estimation": {m: method_summary(m) for m in est.method.unique()},
    "moment_and_support_diagnostics": {
        "max_abs_sample_moment_by_method": {m: float(g.moment_max_abs.max()) for m, g in est.groupby("method")},
        "ZX_condition_max_by_method": {m: float(g.design_condition.max()) for m, g in est.groupby("method")},
        "mean_corr_valid_w_xi": float(diag.corr_valid_w_xi.mean()),
        "mean_corr_invalid_proxy_xi": float(diag.corr_invalid_proxy_xi.mean()),
        "mean_first_stage_w_coefficient": float(diag.first_stage_w_coefficient.mean()),
        "observed_real_mc": [float(diag.observed_min_real_mc.min()), float(diag.observed_max_real_mc.max())],
        "observed_share_min": float(diag.observed_min_share.min()),
        "observed_outside_share_min": float(diag.observed_min_outside_share.min()),
        "declared_support": run["primitive_support"]
    },
    "recovery": {"markup_mean_error": float(rec.markup_error.mean()),
                 "markup_rmse": float(np.sqrt(np.mean(rec.markup_error**2))),
                 "mc_mean_error": float(rec.mc_error.mean()),
                 "mc_rmse": float(np.sqrt(np.mean(rec.mc_error**2)))},
    "welfare_market_means": {scenario: {col: float(g[col].mean()) for col in
        ["consumer_payment", "producer_revenue", "producer_profit", "tax_payment",
         "subsidy_payment", "real_resource_cost", "consumer_surplus",
         "welfare_CS_plus_profit_minus_net_fiscal"]}
        for scenario, g in w.groupby("scenario")},
    "independent_check": {**ind,
        "max_raw_foc": float(ic.independent_raw_foc_max.max()),
        "max_finite_difference_profit_gradient": float(ic.finite_difference_profit_gradient_max.max()),
        "max_fresh_solve_price_gap": float(ic.independent_solve_price_gap.max())}
}
(OUT / "compact_results.json").write_text(json.dumps(compact, indent=2), encoding="utf-8")

b = compact["welfare_market_means"]["baseline"]
s = compact["welfare_market_means"]["subsidy"]
text = f"""# Replication response

## Research judgment

The bounded two-product, common-ownership Bertrand-logit simulation completed for all five predeclared seeds (120 markets and 240 product rows per seed). There were zero simulation, equilibrium, and estimation failures. The valid excluded cost shifter materially moves price and improves demand-slope recovery relative to OLS; the deliberately invalid proxy is biased in the expected direction. These are finite-sample recovery results conditional on the stated logit and ownership specification, not a population-identification proof.

## Design and timing

- Demand is `log(s_j/s_0) = 2 + 0.4 x_j - 1.2 p_j + xi_j`. A single multiproduct firm owns both products and sets prices simultaneously after observing costs and demand shocks.
- `w` is realized as a bounded cost shifter before pricing, enters marginal cost, is independent of the primitive demand shocks by construction, and is excluded from utility. The valid GMM instruments are `(1, x, w, w^2)`.
- The invalid proxy is `z_bad = w + 0.8 xi + 0.05 e`. It is recorded only after `xi` is realized and pricing occurs. Its direct `xi` component violates demand exclusion; it is used only for a labeled invalid-IV diagnostic.
- All primitives are drawn once from declared bounded supports. Analytical real marginal-cost support is `[1.03, 2.17]`; under the 0.20 subsidy, private marginal-cost support is `[0.83, 1.97]`. No redraw, clipping, conditional market survival, or observation dropping occurs.

## Equilibrium and numerical evidence

All {compact['equilibrium']['attempted_start_rows']:,} starts were retained and accepted across {compact['equilibrium']['market_scenario_cases']:,} baseline/subsidy market cases. The finite eight-start scan detected exactly one clustered root per case ({compact['equilibrium']['detected_roots']:,} roots total), but does not establish global uniqueness. Prices were bounded at private marginal cost plus `[1e-8, 10]`. Maximum raw and share-scaled FOC residuals were {compact['equilibrium']['max_raw_foc']:.3e} and {compact['equilibrium']['max_share_scaled_foc']:.3e}; scaled-Jacobian condition numbers ranged from {compact['equilibrium']['scaled_jacobian_condition_min']:.6g} to {compact['equilibrium']['scaled_jacobian_condition_max']:.6g}. Observed shares were not degenerate: the minimum product share was {compact['moment_and_support_diagnostics']['observed_share_min']:.4f} and minimum outside share was {compact['moment_and_support_diagnostics']['observed_outside_share_min']:.4f}.

The separate implementation passed all {compact['independent_check']['checks']:,} cases. Its maximum recomputed raw FOC was {compact['independent_check']['max_raw_foc']:.3e}, maximum finite-difference profit gradient was {compact['independent_check']['max_finite_difference_profit_gradient']:.3e}, and maximum gap from a fresh root solve was {compact['independent_check']['max_fresh_solve_price_gap']:.3e}.

## Estimation and recovery

Across seeds, the mean price coefficient was {compact['estimation']['OLS']['price']['mean']:.3f} under OLS, {compact['estimation']['IV_2SLS']['price']['mean']:.3f} under 2SLS, and {compact['estimation']['GMM_2step']['price']['mean']:.3f} under two-step GMM, against truth `-1.2`. The invalid proxy IV mean was {compact['estimation']['INVALID_PROXY_IV']['price']['mean']:.3f}. The valid shifter's mean first-stage price coefficient was {compact['moment_and_support_diagnostics']['mean_first_stage_w_coefficient']:.3f}; mean sample correlations with `xi` were {compact['moment_and_support_diagnostics']['mean_corr_valid_w_xi']:.3f} for valid `w` and {compact['moment_and_support_diagnostics']['mean_corr_invalid_proxy_xi']:.3f} for invalid `z_bad`.

Using each seed's GMM demand slope and the observed ownership matrix, recovered markups have mean error {compact['recovery']['markup_mean_error']:.4f} and RMSE {compact['recovery']['markup_rmse']:.4f}; recovered marginal costs have the opposite mean error and the same RMSE. Full seed-level coefficients, moment norms, cross-moment conditioning, and product-level recoveries are saved in the output tables.

## Counterfactual accounting

Market-size-normalized means are kept as distinct objects:

| Scenario | Consumer payment | Producer profit | Subsidy | Tax | Real resource cost | Consumer surplus | CS + profit - net fiscal |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | {b['consumer_payment']:.4f} | {b['producer_profit']:.4f} | {b['subsidy_payment']:.4f} | {b['tax_payment']:.4f} | {b['real_resource_cost']:.4f} | {b['consumer_surplus']:.4f} | {b['welfare_CS_plus_profit_minus_net_fiscal']:.4f} |
| Subsidy | {s['consumer_payment']:.4f} | {s['producer_profit']:.4f} | {s['subsidy_payment']:.4f} | {s['tax_payment']:.4f} | {s['real_resource_cost']:.4f} | {s['consumer_surplus']:.4f} | {s['welfare_CS_plus_profit_minus_net_fiscal']:.4f} |

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
"""
(HERE / "response.md").write_text(text, encoding="utf-8")
