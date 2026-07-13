# Independent audit — MIXED

## Bottom line

**Overall verdict: MIXED.** The row-level panel, controlled-transition estimates, independently solved NFXP, continuous local-rank calculation, exact restricted-domain construction, all 378 retained search rows, support labels, and stationary policy accounting pass independent recomputation. The package is not a full PASS because (i) `response.md` gives incorrect transition denominators and NFXP acceptance diagnostics, and (ii) the current CCP entries in `summary.json` and `ccp_starts.json` do not reproduce the CCP estimator in `run_model.py` and conflict with both an exact independent solution and `independent_verification.json`. The existing verifier is genuinely separate in important algorithms, but its saved result is stale relative to the current production artifacts and its executable coverage does not detect these cross-artifact failures.

This audit was read-only with respect to all pre-existing artifacts. It recomputed objects from `simulated_panel.csv` and mathematical primitives using a separately written value-iteration implementation, an exact affine least-squares solution for the CCP estimator, finite-difference Jacobians at several step sizes, and row-by-row checks of `alternative_search.csv`.

## 1. Timing, sample, and controlled transitions — MIXED (calculations pass; narrative counts fail)

- The panel has exactly 15,750 rows: 450 agents, 35 observations per agent, and 7,875 observations in each observed subsidy regime, 0 and 0.4. All agents have a recorded next state in every retained row.
- The implemented timing agrees with the stated model: state and subsidy are observed, action is chosen, and then the action-controlled transition generates `next_state`. Keep increments from states 0–3 with probability `p_m` and otherwise stays; keep at state 4 is absorbing. Replacement moves to 0 with probability `p_r` and to 1 otherwise.
- Independent counts from the row-level panel are:
  - all keep actions: 10,372;
  - eligible keep transitions with state below 4: **10,234**, including 7,391 increments, so `p_m = 7391/10234 = 0.7222005081102209`;
  - absorbing keep observations at state 4: 138;
  - replacement actions/transitions: **5,378**, including 4,619 resets to state 0, so `p_r = 4619/5378 = 0.8588694682037933`.
- These values agree with `summary.json`. They contradict the sentence in `response.md` reporting “12,164 eligible keep transitions and 3,315 replacement transitions.”

## 2. NFXP — PASS numerically, MIXED in reporting

- With the independently recomputed transition probabilities held fixed, six new value-iteration NFXP starts converged to the same optimum. The best independent run was approximately `(c,r) = (0.4291956905, 2.1474058910)` with choice NLL `9111.515741167237`. Other starts, including points near opposite box corners, agreed to about `2.3e-7` in parameters and `4.2e-10` in objective.
- The current `summary.json` estimate `(0.4291956636968231, 2.1474057945914597, 0.7222005081102209, 0.8588694682037933)` and NLL `9111.51574116724` therefore pass.
- All eight declared starts are retained, but only **six**, not eight, satisfy the declared `projected_grad_inf < 2e-3` rule. Their saved projected-gradient norms are
  `(0.0031212039, 0.0016951162, 0.0005071342, 0.0000626642, 0.0000376531, 0.0036025085, 0.0003234163, 0.0001692570)`.
  Starts 0 and 5 fail the stated threshold. `summary.json` correctly says 6/8; `response.md` incorrectly says all 8 were accepted.
- The current selected start is start 3 and its saved projected-gradient norm is `6.2664e-5`. The narrative's `1.1855e-4` is not the current selected diagnostic.
- The current summary's maximum Bellman residual is `9.1394e-13`, not “below `1.8e-15`” as stated in the narrative. This is still numerically small and does not alter the optimum.

## 3. Distinct CCP estimator — FAIL for artifact coherence; implemented method itself passes

- Source inspection confirms that `ccp_md_objective` is a genuinely distinct two-step estimator: it uses Jeffreys-smoothed empirical CCPs, evaluates the empirical policy through a linear system, and matches log odds. It does not call the Bellman solver.
- Because the CCP inversion residual is affine in `(c,r)`, I solved its weighted minimum-distance problem exactly rather than reusing its optimizer. The unique solution is
  `(c,r) = (0.4284716784041825, 2.1408941722066985)`, objective `0.001343923790108757`, with normal-equation infinity norm `7.32e-16`.
- This exact result agrees with the narrative and with the three independent CCP runs saved in `independent_verification.json` (about `(0.428471667, 2.140894146)`).
- It does **not** agree with the current `summary.json` and `ccp_starts.json`, which report approximately `(0.4289031261, 2.1415253388)` and objective `0.001356076921812042`. The largest parameter discrepancy from the independent verifier is about `6.31e-4`, far above that verifier's `2e-5` acceptance tolerance. The current summary also omits the `method` field that the current `run_model.py` writes.
- Thus the CCP economic method is distinct and reproducible, but the current saved production CCP result is not produced by the checked-in production formula. This is a material round-trip/provenance failure.

## 4. Continuous local-rank evidence — PASS

- The observable map is continuous in economic coordinates and contains ten model CCPs (five states in each observed regime) plus the two controlled-transition probabilities, giving a `12 x 4` Jacobian.
- Independent central finite differences produce the following singular values as the base step shrinks:
  - `1e-3`: `(2.1265733772, 1.0147022137, 0.9923192794, 0.2127537649)`;
  - `2e-4`: `(2.1265720681, 1.0147022116, 0.9923192663, 0.2127536962)`;
  - `2e-5`: `(2.1265720141, 1.0147022115, 0.9923192657, 0.2127536934)`;
  - `2e-6`: `(2.1265720135, 1.0147022115, 0.9923192657, 0.2127536934)`.
- The smallest singular value is stable near `0.212754`, comfortably above the declared `1e-7` tolerance, so numerical local rank is four.
- The claim is correctly limited to local population-rank evidence conditional on fixed beta, maintained logit structure, observed regimes, and normalizations. A full-rank Jacobian does not establish global injectivity or estimator coverage, and the narrative does not promote it to either claim.

## 5. Closed restricted domain and empty-slab logic — PASS

- The declared domain is the closed box `[0.05,1.50] x [0.20,5.00] x [0,1] x [0,1]`; all of its boundaries are included directly, including transition-probability boundaries 0 and 1.
- For `delta = 0.15`, the restriction `max_j |theta_j-theta_hat_j| >= delta` is exactly the union, over coordinates, of the lower closed slabs `theta_j <= theta_hat_j-delta` and upper closed slabs `theta_j >= theta_hat_j+delta`, intersected with the declared box. This is an equality of sets, not an approximation.
- At the current NFXP estimate, seven intersections are nonempty. Their restricted coordinate intervals are:
  - `c` lower `[0.05, 0.2791956636968231]`, upper `[0.5791956636968231, 1.50]`;
  - `r` lower `[0.20, 1.9974057945914598]`, upper `[2.2974057945914597, 5.00]`;
  - `p_m` lower `[0, 0.5722005081102208]`, upper `[0.8722005081102209, 1]`;
  - `p_r` lower `[0, 0.7088694682037933]`.
- The `p_r` upper slab is empty because its putative lower endpoint is `1.0088694682037933 > 1`. Skipping only this empty intersection is exact.
- I also solved the model at all 16 corners of the declared box for both observed regimes. The maximum independent Bellman residual was `9.28e-14`; choice probabilities remained finite (overall range about `2.21e-11` to `0.998837`). Thus the mapping is defined at the relevant declared boundaries.
- The box excludes `c=0` and `r=0` by declaration. Consequently, every nonlocal-search statement is restricted to this box; it is not a statement over all economically imaginable nonnegative costs.

## 6. All retained restricted-search rows and best candidate — PASS

- `alternative_search.csv` contains exactly 378 unique `(slab_id, rerun_seed, start_id)` rows: 7 nonempty slabs x 2 seeds x 27 starts. Every slab-seed cell contains exactly 27 rows; no terminal point lies outside its saved slab bounds.
- I independently recomputed the observable-distance objective and projected-gradient acceptance for every row using value iteration. All 378 rows satisfy success, projected-gradient `< 2e-6`, box feasibility, and restriction feasibility. The maximum absolute difference between a saved objective and the independent row-level recomputation is `2.29e-16`.
- The current best retained candidate is slab 3 (`r` upper), seed 991, start 17:
  `theta = (0.4527563710796874, 2.2974057945914597, 0.7255399911945896, 0.8630549722455670)`,
  objective `0.0009849321516048203`, projected-gradient infinity norm `1.14055e-8`, nearest box-boundary slack `0.136945027754433`, and restriction slack `-8.32667e-17`.
- The small negative restriction slack is floating-point error and is admissible under the declared feasibility tolerance `1e-10`. The candidate lies on `r = r_hat + 0.15`.
- The exact number in `response.md` (`0.000984932245666759`) belongs to an earlier target estimate and differs from the current artifact by about `9.41e-11`; the qualitative and rounded conclusion is unchanged.
- This finite multistart search is strong numerical falsification evidence on the declared restricted box, not proof that no closer point exists and not proof of global identification. The narrative states this limitation correctly.

## 7. Round trips and artifact counts — MIXED

- Panel rows round-trip: CSV 15,750 = NPZ empirical-count total 15,750 = summary 15,750.
- The NPZ count array has shape `2 x 5 x 2`; empirical CCPs have shape `2 x 5`; the Jacobian has shape `12 x 4`; and four singular values are retained.
- Starts round-trip: 8 NFXP and 8 CCP rows. Correct acceptance counts are 6 NFXP and 8 CCP. Search rows round-trip: CSV 378 = summary evaluations 378 = summary accepted 378.
- `verify_artifacts.py` currently exits successfully, but its hashes are generated from the files being checked and are not compared with a previously fixed manifest. A successful invocation therefore establishes current readability and a few internal counts, not immutability or provenance.
- File modification times show `summary.json`, `nfxp_starts.json`, `ccp_starts.json`, `compact_arrays.npz`, and `alternative_search.csv` were regenerated at 15:46:19, after `independent_verification.json` at 15:43:15, `response.md` at 15:44:34, and `provenance.json` at 15:45:05. The claimed final independent-verifier round trip is therefore not temporally true for the current production artifacts.

## 8. Policy accounting and support — PASS

Independent stationary-distribution calculations at the current NFXP estimate give:

| subsidy | support | replacement rate | private value | transfer | real resource cost | social welfare |
|---:|---|---:|---:|---:|---:|---:|
| 0.0 | observed | 0.3188788644 | -13.2654720339 | 0 | 13.2654720339 | -13.2654720339 |
| 0.2 | model interpolation | 0.3361083370 | -12.5443302082 | 0.9603095343 | 13.5046397424 | -13.5046397424 |
| 0.4 | observed | 0.3549772666 | -11.7715643992 | 2.0284415233 | 13.8000059224 | -13.8000059224 |

For every row, `private value - fiscal transfer = social welfare = -real resource cost` to machine precision. Stationary residuals are below `4.5e-16` in the independent calculation. The support labels are correct: 0 and 0.4 are observed, while 0.2 is model interpolation only. The welfare interpretation is appropriately narrow: deterministic flows only, subsidy treated as a transfer, and no taste-shock surplus, financing distortion, externality, or distributional weight.

## 9. Verifier independence and coverage — MIXED

- Positive: `independent_verify.py` does not import `run_model.py`; it independently implements transition matrices, value iteration, likelihood, CCP inversion, the finite-difference Jacobian, stationary accounting, and fresh restricted searches. This is meaningful algorithmic independence from the production Bellman root solver.
- Current failure: its saved CCP runs conflict with the current CCP summary/start artifacts, and rerunning its stated CCP acceptance logic against the current summary would fail (`~6.31e-4` maximum parameter discrepancy versus a `2e-5` tolerance). The saved top-level `pass: true` is stale.
- Coverage gap: `restricted_trace_coverage` checks only that slab IDs form `0,...,6` and that each slab ID has both seeds. It does not verify 27 rows per slab-seed, unique start IDs, dimension/side labels, saved slab bounds, all row objectives, all projected gradients, or all row feasibility conditions.
- Coverage gap: the fresh restricted reruns are saved for every slab, but the executable pass condition compares only the single global-best fresh objective with the selected production objective. A bad nonwinning slab could escape detection.
- Coverage gap: `verify_artifacts.py` checks existence, two row counts, an NPZ-to-summary singular-value round trip, the saved verifier's boolean, and presence of a “local evidence only” phrase. It does not cross-check transition denominators in the narrative, NFXP accepted-start claims, CCP outputs across code/summary/verifier, Bellman-residual claims, per-slab search rows, policy values, timestamps, or provenance ordering.
- Therefore the verifier has good independent computational ingredients but incomplete acceptance coverage and does not justify the package-wide “all ten checks passed” claim for the artifacts as they currently stand.

## Claim calibration

- **Supported:** controlled-transition estimates; NFXP optimum for the fixed sample; distinct CCP formula and its exact solution (but not the current CCP summary artifact); stable full local rank of the continuous observable Jacobian; exact seven-slab representation of the restricted closed set; row-by-row validity of the current 378-row trace; stationary transfer/resource accounting; policy-support labels.
- **Not supported as a clean artifact claim:** current CCP summary/start outputs, “all eight NFXP starts accepted,” the narrative transition denominators, the narrative's exact current Bellman/search diagnostics, and a final verifier pass over the current artifact generation.
- **Correctly not claimed:** global identification, finite-sample estimator coverage, external validity, policy invariance, or welfare conclusions beyond the declared deterministic-flow accounting.

## Required corrections for a PASS

1. Regenerate `summary.json` and `ccp_starts.json` from the checked-in `run_model.py` CCP objective (or document and commit the alternative CCP formula that produced the current values).
2. After production artifacts are frozen, rerun the independent verifier and make it read-only or write to a fresh verification target; record hashes in a fixed manifest.
3. Correct `response.md` to 10,234 eligible keep transitions, 5,378 replacements, 6/8 accepted NFXP starts, and the diagnostics from the final frozen run.
4. Strengthen verifier acceptance to validate every retained search row and every slab separately, and cross-check the CCP result across source, summary, starts, and independent solution.
