# Independent audit: junzi-economist-struct-x057

## Overall judgment: MIXED

The saved production results are internally consistent and independently reproducible to numerical precision. The data construction, controlled-transition estimates, NFXP and genuinely distinct CCP-WMD estimates, local-rank calculation, complete restricted lattice, policy support labels, welfare accounting, and cross-artifact headline values all pass.

The overall result is **MIXED**, rather than unqualified PASS, for two reasons. First, the supplied verifier is temporally and code-path independent but is not substantively complete: it does not re-solve either estimator, recompute local rank, recompute any restricted-search objective, or reconstruct stationary policy outcomes. Second, all estimator starts satisfy the production rule `success == True` and reproduce under a fresh run, but seven of eight saved NFXP runs (including the selected run) stopped on relative objective reduction rather than the requested projected-gradient tolerance. The selected saved NFXP projected-gradient infinity norm is `9.0949469720e-05`; an independent central difference gives approximately `1.43e-05` at steps `1e-5` to `1e-6`, still above `gtol=1e-8`. This is a numerical-convergence qualification, not a material discrepancy in the estimates or objective.

The audit was read-only with respect to all production and verification artifacts. This report is the only file added to the audited directory and is not one of the 12 provenance-tracked production artifacts.

## 1. Production finalization, hashes, and timestamps — PASS

- `provenance.json` declares exactly 12 production artifacts, and all 12 current files match their recorded SHA-256 hashes, byte sizes, and UTC modification timestamps.
- The latest production-artifact timestamp is `2026-07-13T07:57:59.512297+00:00`, exactly the declared `production_completed_at_utc`.
- The verifier source timestamp is later: `verifier.py` was modified at `2026-07-13T07:58:16.092070+00:00`.
- The verifier started at `2026-07-13T07:58:22.709746+00:00`, 23.197449 seconds after declared production completion. `verification_report.json` was written at `2026-07-13T07:58:22.743346+00:00`.
- Therefore production was finalized before verifier construction/execution, and no provenance-tracked production artifact is newer than verifier start.

Hash results for the current 12 files:

| Artifact | SHA-256 match | mtime match | byte-size match |
|---|---:|---:|---:|
| `production.py` | yes | yes | yes |
| `model_data.csv` | yes | yes | yes |
| `transition_estimates.csv` | yes | yes | yes |
| `choice_cells.csv` | yes | yes | yes |
| `nfxp_starts.csv` | yes | yes | yes |
| `ccp_starts.csv` | yes | yes | yes |
| `local_rank.json` | yes | yes | yes |
| `restricted_search.csv` | yes | yes | yes |
| `policy_results.csv` | yes | yes | yes |
| `summary.json` | yes | yes | yes |
| `response.md` | yes | yes | yes |
| `production_stdout.txt` | yes | yes | yes |

## 2. Sample and controlled transitions — PASS

- Independently read `4,800` decision rows for `240` agents.
- Every agent has exactly `20` periods, covering periods `0` through `19`; there are no duplicate agent-period rows.
- There are no invalid action/state/next-state values and no broken within-agent identity `next_state[t] == state[t+1]`.
- Each agent remains in one regime. Each regime contains `2,400` rows.
- Recomputed maintenance rate is `0.4552083333333333`; regime rates are `0.3729166666666667` and `0.5375`.
- The controlled transition table has all `2 × 3 × 3 = 18` rows and six nonempty action-state cells. Cell totals are `(a,x)=(0,0):1730`, `(0,1):685`, `(0,2):200`, `(1,0):1105`, `(1,1):752`, `(1,2):328`; minimum is `200`.
- Recomputed counts differ from saved counts by exactly `0`. Maximum probability difference is `9.02e-17`; maximum transition-row sum error is `1.11e-16`.
- The six empirical choice cells also reproduce: count and action-sum differences are `0`, maximum Jeffreys-CCP difference is `5.55e-17`, and maximum log-odds difference is `1.11e-16`.

## 3. NFXP estimation and starts — MIXED (estimate PASS; stopping qualification)

- Saved estimate: `(state_harm, maintenance_cost, subsidy_loading) = (0.7585435394988677, 1.2273187538521104, 0.8871519453404465)`.
- Saved objective: `3152.106538715204`.
- There are exactly eight retained starts with IDs `0` through `7`; all have `success=True`, `status=0`, finite objectives, and exactly one selected row (`start_id=7`). The selected row is the minimum saved objective under the production selection rule.
- Independently evaluating the NFXP likelihood at every saved terminal vector gives a maximum objective discrepancy of `4.55e-13`.
- Fresh independent optimization from all eight initial values again gives `8/8` successful status-0 runs. Its numerically best start is ID `1`, with theta `(0.7585435412526786, 1.2273187406352823, 0.8871520024797017)` and objective `3152.1065387152044`. Relative to the saved selected result, the maximum parameter difference is `5.71e-08` and the objective difference is `4.55e-13`.
- The saved eight-start objective spread is only `7.28e-12`, so selection of ID `7` versus fresh ID `1` is floating-point tie behavior, not evidence of a different optimum.
- Qualification: only saved start ID `2` reports projected-gradient stopping. The other seven, including selected ID `7`, report relative-function-reduction stopping. Saved projected-gradient infinity norms range up to `9.09e-05`, above the configured `gtol=1e-8`. Independent central differences at the selected estimate give an infinity norm around `1.4e-05`. The estimates are stable, but “successful” should be read as SciPy status success, not universal satisfaction of `gtol`.

## 4. Distinct CCP-WMD estimation and starts — PASS with minor stopping note

- Saved estimate: `(0.7747940698319838, 1.224177940665068, 0.8590366888952735)`.
- Saved objective: `0.0020964860522356`.
- There are exactly eight retained starts with IDs `0` through `7`; all have `success=True`, `status=0`, finite objectives, and exactly one selected row (`start_id=7`).
- Independently evaluating the CCP-WMD criterion at all saved terminals gives a maximum discrepancy of `9.80e-17`.
- Fresh independent optimization gives `8/8` successful status-0 starts and selects ID `7`: theta `(0.7747940702309893, 1.2241779410703482, 0.8590366888072061)`, objective `0.0020964860522356583`. Maximum theta difference from the saved selected result is `4.05e-10`; objective difference is `5.85e-17`.
- The estimator is computationally distinct from NFXP. It uses the six empirical Jeffreys CCPs, solves `(I - beta P0)V = u0 - log(P0)`, constructs action-value log-odds, and minimizes a count-weighted log-odds criterion. Its objective makes no nested Bellman solve. Its estimates differ from NFXP by approximately `(0.01625053, -0.00314081, -0.02811526)`.
- Minor note: selected CCP-WMD start ID `7` stopped on relative objective reduction and has saved projected-gradient infinity norm `1.314e-08`, marginally above `gtol=1e-8`; the independent central-difference norm is `1.109e-08`.

## 5. Local rank and claim scope — PASS

- At the saved NFXP estimate, an independent central-difference Jacobian with step `1e-5` differs from the saved Jacobian by at most `1.67e-11`.
- Recomputed singular values are `(0.8110518060454581, 0.3013183372523157, 0.1581138325851432)`, differing from the saved values by at most `1.38e-11`; rank is `3` at tolerance `1e-6`.
- Step checks at `1e-4` and `1e-6` also return rank `3`, with smallest singular values `0.1581138325733940` and `0.1581138325460816`.
- The stored claim is correctly limited to continuous local rank at the NFXP estimate, conditional on estimated transitions and normalization. `global_identification_claim` is `false`; `response.md` explicitly disclaims a global population-identification result.

## 6. Full closed-domain restricted lattice — PASS

- The saved search contains exactly `4,913 = 17^3` rows and consecutive row IDs `0` through `4912`.
- Each parameter has exactly 17 unique nodes. The full declared closed domain is present: state harm `[0.1, 2.0]`, maintenance cost `[0.2, 3.0]`, and subsidy loading `[0.0, 2.0]`. Comparison with independently generated Cartesian nodes differs by at most `2.22e-16` from CSV decimal representation.
- Every row has restriction delta `0.35` and acceptance tolerance `1e-12`.
- Independently recomputed L-infinity distances differ by at most `2.78e-16`; slacks differ by at most `2.88e-16`.
- There are zero acceptance mismatches, zero slab-membership mismatches, and zero boundary-flag mismatches.
- Accepted count is exactly `4,793`. Boundary count is exactly `1,538 = 17^3 - 15^3`.
- The smallest accepted slack is `0.01284805465955352`; the largest rejected slack is `-0.02268124614788947`. Thus no lattice point is numerically ambiguous at the `1e-12` tolerance.
- All `4,913` CCP-SSE objectives were independently recomputed. Maximum saved-versus-audit discrepancy is `2.00e-15`.
- Best accepted row is ID `2168`, theta `(0.93125, 1.6, 1.125)`, objective `0.005077598256793347`, and slack `0.02268124614788969`. These reconcile with `summary.json` and `response.md` at saved/displayed precision.
- The interpretation is properly restricted to the evaluated closed lattice and does not assert continuous global separation or global identification.

## 7. Policy support and accounting — PASS

- Regimes are exactly `0.0`, `0.5`, and `1.0`; labels are exactly `observed`, `model_interpolation`, and `observed`.
- Independently re-solving the Bellman policy and stationary distribution reproduces all saved numerical fields other than the iteration counter to a maximum difference of `8.00e-13`. The audit used a tighter Bellman tolerance, explaining 21–22 additional iterations.
- Maximum independently checked stationary-distribution sum error is `4.44e-16`; maximum stationary-law residual is `4.44e-16`.
- From the saved decimal fields, maximum error in `social_welfare = private_payoff - transfer_outlay` is `1.11e-16`; maximum error in `social_welfare = -state_harm - resource_cost` is `5.55e-17`.
- The saved accounting-error columns have maximum magnitude `5.551115123125783e-17`, exactly the quantity summarized and displayed in the response (to scientific-notation precision).
- Transfers are therefore kept separate from real resource costs and cancel from social welfare as claimed.

## 8. Cross-artifact reconciliation — PASS

- `summary.json` reproduces the saved row-level files: sample `4,800/240/20`, transition `18/6/min 200`, NFXP and CCP start counts `8/8`, selected start ID `7` for each saved table, local rank `3`, search `4,913/4,793/1,538`, best row `2168`, and policy rows `3` with support counts `2/1`.
- `response.md` agrees with `summary.json` at its declared rounding: action rates `0.4552/0.3729/0.5375`; NFXP `(0.758544, 1.227319, 0.887152)`; CCP-WMD `(0.774794, 1.224178, 0.859037)`; search objective `0.0050775983`; slack `0.022681246`; and accounting error `5.551e-17`.
- `production_stdout.txt` agrees: `rows=4800`, `nfxp_starts=8`, `ccp_starts=8`, `restricted_rows=4913`, `accepted=4793`, and `max_accounting_error=5.5511151231257827e-17`.
- `verification_stdout.txt` agrees with `verification_report.json`: `verification_passed=true`, `checks=36/36`, and `production_hashes=12`.

## 9. Supplied-verifier independence — MIXED

Positive evidence:

- `verifier.py` is a separate script written after production completion and executed later.
- It does not import `production.py` or call production functions.
- It independently rebuilds transition counts/probabilities from `model_data.csv`, checks provenance hashes and mtimes, checks saved start-table selection/count consistency, recomputes acceptance from saved distances/slacks, checks saved policy accounting identities/support labels, and checks selected response phrases/counts.
- Its reported 36 checks are all true, and the audit confirms those flags are consistent with the current files.

Limits preventing a full-independence PASS:

- Estimator verification trusts saved terminal parameters, objectives, gradients, and success flags; it does not reconstruct either objective or rerun any start.
- Local rank is not read or recomputed by the verifier.
- Restricted-search distance is not reconstructed from lattice coordinates and the NFXP estimate; the verifier starts from the saved `linf_distance`. It also does not regenerate the Cartesian lattice or recompute any of the 4,913 CCP-SSE objectives.
- Policy verification checks algebraic identities among saved columns but does not solve the Bellman equation, form the induced transition matrix, recover stationary distributions, or recompute policy outcomes.
- Response checks are substring-presence checks, not complete numerical reconciliation.

Accordingly, the supplied verifier is independent in chronology and implementation location, but only partially independent in evidentiary content. The additional computations in this audit close those numerical gaps and support the saved results, while the verifier itself remains **MIXED** on independence.

## Final disposition

- Production artifacts and economic/numerical claims within their stated local/lattice/interpolation scope: **PASS**.
- Estimator-start retention and reproducibility: **PASS**, with an NFXP convergence-tolerance qualification.
- Provenance and production-before-verifier chronology: **PASS**.
- Supplied verifier as a complete independent recomputation: **MIXED**.
- Overall audit: **MIXED**.
