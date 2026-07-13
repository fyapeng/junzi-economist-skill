# Independent audit

## Overall judgment: FAIL

The estimation, raw-data summaries, local-rank calculation, complete restricted grid, support labels, declared gradient-only acceptance rule, and production-artifact hashes reproduce independently. The package nevertheless fails as a whole because the saved `subsidy = 0.2` policy row is numerically invalid: the policy probability function evaluates only the observed regimes `0.0` and `0.4`, so its output is uninitialized when called at `0.2`. `verify.py` duplicates the same bug and therefore reports a false pass. The corrected midpoint stationary action probability is `0.4577303417`, not `0.02489279535`; this propagates to transfers and resource costs.

Audit date: 2026-07-13 (Asia/Shanghai). I did not run `production.py` or `verify.py`, did not overwrite any artifact, and used fresh calculations from `artifacts/raw_primitives.npz`. Independent derivative checks use the declared step `2e-5*max(1,abs(parameter))` and the declared scaled threshold `1e-6*(1+abs(objective))`.

## 1. Raw primitives, transitions, and empirical CCPs — PASS

- Raw structure: 6,400 rows; 800 unique IDs (`0`–`799`); periods `0`–`7`, exactly 800 rows per period; 3,200 rows at each observed subsidy `0.0` and `0.4`; no state, action, or next-state value outside `{0,1}`.
- Controlled transition cells `(state, action): n, next_state=1, p1`:
  - `(0,0): 2692, 464, 0.1723625557206538`
  - `(0,1): 1903, 149, 0.07829742511823437`
  - `(1,0): 703, 593, 0.8435277382645804`
  - `(1,1): 1102, 383, 0.34754990925589835`
- Empirical CCP cells `(subsidy, state): n, action=1, CCP`:
  - `(0.0,0): 2292, 858, 0.3743455497382199`
  - `(0.0,1): 908, 529, 0.5825991189427313`
  - `(0.4,0): 2303, 1045, 0.4537559704732957`
  - `(0.4,1): 897, 573, 0.6387959866220736`

All estimates and all eight saved count records match exactly. Every CCP cell is interior.

## 2. NFXP and distinct two-step CCP estimates — PASS

Fresh likelihood code confirms that NFXP solves Bellman optimality at every likelihood evaluation, whereas `CCP_two_step` fixes the four empirical CCPs and solves a policy-evaluation linear system. They are genuinely distinct criteria.

Selected saved estimates reproduce:

| Estimator | theta0 | theta1 | Negative log likelihood |
|---|---:|---:|---:|
| NFXP | -0.4631694048 | 1.1845521914 | 4306.789798621620 |
| CCP two-step | -0.4631737043 | 1.1832084743 | 4306.790771405549 |

Independent derivative-free re-optimization also reaches the same optima. Powell gives `(-0.4631693562, 1.1845519909)` with objective `4306.789798621619` for NFXP and `(-0.4631736769, 1.1832085094)` with objective `4306.790771405548` for CCP; Nelder–Mead agrees to the displayed objective precision.

## 3. All 14 starts and declared projected-gradient rule — PASS

All terminal points are interior, so raw and box-projected gradients coincide. Fresh objectives and gradients match the saved values (maximum discrepancy at the reported precision is zero). `tol` is the declared objective-scaled cutoff; every start is eligible without consulting solver success, status, message, `ftol`, or iteration count.

| Estimator | Start | theta0 | theta1 | Objective | gradient = projected gradient | inf-norm | tol | Accepted |
|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| NFXP | 0 | -0.4631694048 | 1.1845521914 | 4306.789798621620 | (-8.003553e-06, 1.733300e-05) | 1.733300e-05 | 4.307790e-03 | yes |
| NFXP | 1 | -0.4631693417 | 1.1845519292 | 4306.789798621621 | (4.602043e-05, -1.339805e-05) | 4.602043e-05 | 4.307790e-03 | yes |
| NFXP | 2 | -0.4631694204 | 1.1845521751 | 4306.789798621621 | (-3.137757e-05, 1.305254e-05) | 3.137757e-05 | 4.307790e-03 | yes |
| NFXP | 3 | -0.4631694059 | 1.1845523186 | 4306.789798621625 | (5.934453e-06, 3.581769e-05) | 3.581769e-05 | 4.307790e-03 | yes |
| NFXP | 4 | -0.4631694560 | 1.1845520972 | 4306.789798621623 | (-8.931238e-05, -2.648897e-06) | 8.931238e-05 | 4.307790e-03 | yes |
| NFXP | 5 | -0.4631694495 | 1.1845522137 | 4306.789798621623 | (-6.625669e-05, 1.520236e-05) | 6.625669e-05 | 4.307790e-03 | yes |
| NFXP | 6 | -0.4631693406 | 1.1845523803 | 4306.789798621630 | (1.024091e-04, 5.280518e-05) | 1.024091e-04 | 4.307790e-03 | yes |
| CCP two-step | 0 | -0.4631737043 | 1.1832084743 | 4306.790771405549 | (-2.628440e-05, -1.925514e-05) | 2.628440e-05 | 4.307791e-03 | yes |
| CCP two-step | 1 | -0.4631737263 | 1.1832085625 | 4306.790771405549 | (-4.565663e-05, -9.031850e-06) | 4.565663e-05 | 4.307791e-03 | yes |
| CCP two-step | 2 | -0.4631737397 | 1.1832085328 | 4306.790771405551 | (-6.743903e-05, -1.496981e-05) | 6.743903e-05 | 4.307791e-03 | yes |
| CCP two-step | 3 | -0.4631737419 | 1.1832090704 | 4306.790771405563 | (-5.252332e-06, 6.331901e-05) | 6.331901e-05 | 4.307791e-03 | yes |
| CCP two-step | 4 | -0.4631736576 | 1.1832089443 | 4306.790771405560 | (9.436008e-05, 5.509427e-05) | 9.436008e-05 | 4.307791e-03 | yes |
| CCP two-step | 5 | -0.4631736260 | 1.1832084234 | 4306.790771405552 | (7.421477e-05, -1.721817e-05) | 7.421477e-05 | 4.307791e-03 | yes |
| CCP two-step | 6 | -0.4631736845 | 1.1832082408 | 4306.790771405557 | (-2.764864e-05, -5.098193e-05) | 5.098193e-05 | 4.307791e-03 | yes |

Start 0 has the minimum eligible objective for each estimator (other starts are numerical ties at approximately `1e-11` or less). Source inspection confirms selection is `min(eligible, objective)` and `eligible` is formed only from the projected-gradient rule. Optimizer `success`, message, and `ftol` are record-only. Thus the claims do not rely on solver success or `ftol`.

## 4. Local-rank claim — PASS

At the selected NFXP estimate and fixed estimated controlled transitions, the independently recomputed Jacobian of the four model CCPs ordered `(z=0,s=0)`, `(z=0,s=1)`, `(z=.4,s=0)`, `(z=.4,s=1)` is

```text
[[ 0.225780697690747, -0.018104096974336],
 [ 0.209068642970101,  0.144320028805378],
 [ 0.242266018490866, -0.021166057970201],
 [ 0.197020426401240,  0.124982260879536]]
```

Its singular values are `(0.452337331969927, 0.157518340996695)`, so rank is 2 at the declared `1e-8` numerical tolerance. The wording is properly limited to local population-mapping rank conditional on fixed estimated transitions. `summary.json` explicitly says “not global identification” and describes the result as a simulated-data demonstration; there is no global-identification overclaim.

## 5. Full 9-by-9 closed restricted grid — PASS

I regenerated all 81 ordered Cartesian rows from the declared grids and independently evaluated every feasible NFXP objective from the raw primitives.

- Exact row mismatches: `0/81`.
- Feasible: 36, each with a non-null recomputed objective.
- Infeasible: 45, each retained with a null objective.
- Exact restriction boundary `theta0 + theta1 = 0.50`: 8 rows.
- Outer lower/upper grid boundary: 32 rows.
- Saved slack, feasibility flag, restriction-boundary flag, outer-boundary flag, coordinates, ordering, and objective/null logic all match for every row.
- The minimum feasible grid row is `(theta0,theta1)=(-0.5,1.0)`, objective `4311.171524562472`, slack `0`, so it is correctly marked as a restriction-boundary row.

Metadata counts and both saved grid vectors are exact.

## 6. Policy support labels and accounting — FAIL (labels PASS; midpoint numbers FAIL)

The labels are correct: `0.0` and `0.4` occur in the raw data and are marked `observed`; `0.2` does not occur, lies between the observed regimes, and is marked `model_interpolation`. Transfer is appropriately separated from the stated real resource cost, and the accounting identities are arithmetically correct for the two observed regimes.

However, the midpoint row is invalid. `production.py`'s NFXP probability routine loops over the fixed `REGIMES = [0.0, 0.4]`. `policy_and_accounting` passes a requested regime array containing `0.2` through `cell_probs`, but the underlying routine still loops only over fixed `REGIMES`; no mask is ever true and the returned array is uninitialized. The saved midpoint Bellman value happens to be valid because value iteration receives `0.2` directly, but its probabilities, stationary distribution, uptake, transfer, and costs are not.

Correct fresh midpoint calculations are:

| Quantity at subsidy 0.2 | Saved | Correct |
|---|---:|---:|
| action probability, state 0 | not saved | 0.4129925070 |
| action probability, state 1 | not saved | 0.6118443065 |
| stationary state-1 probability | 0.2431823623 | 0.2249807884 |
| stationary action-1 probability | 0.02489279535 | 0.4577303417 |
| government transfer per period | 0.00497855907 | 0.09154606833 |
| real resource cost per period | 0.00746783860 | 0.1373191025 |
| social resource accounting excluding transfer | 0.00746783860 | 0.1373191025 |
| private value, state 0 | 6.9477057614 | 6.9477057614 |

For comparison, the independently recomputed observed-regime uptake values exactly match the saved `0.4154058558` at subsidy 0 and `0.5013845548` at subsidy 0.4. Only the midpoint probability-dependent fields fail.

## 7. Manifest, hashes, and cross-artifact consistency — PASS

Fresh SHA-256 and byte-size checks match the manifest for all four declared production files:

- `raw_primitives.npz`: `186df73c84ebc6d332f5b1f003aab50e4202487135b7c5fd6036c6f95c8de823`, 5,853 bytes.
- `starts.json`: `cf8c044ec623c808124d7519e1e8535a80ef3f8631d2798ec9a56e4bf5f6dc90`, 11,145 bytes.
- `restricted_grid.json`: `069669cf5257cfea7fd5bf0c53c08ed86dae9acf1e77490e63bd2cd024e2cad9`, 21,640 bytes.
- `summary.json`: `22a37a822f2601cc59a81fa065ca4a4173d57f2f897acab99bf74c64e386c362`, 7,380 bytes.

Manifest counts are exact: raw rows 6,400; starts 14; restricted rows 81; policy rows 3. Summary transition/CCP records match raw counts, selected rows match `starts.json`, and restricted metadata matches `restricted_grid.json`. Hash consistency proves artifact immutability relative to the manifest, not substantive correctness; consequently it does not rescue the incorrect midpoint row.

## 8. `verify.py` independence, coverage, and chronology — MIXED / substantively FAIL

PASS aspects:

- It imports no function or module from `production.py`; its imports are standard-library modules and NumPy only.
- It reloads raw primitives and freshly computes likelihoods, gradients, grid objectives, rank objects, policy rows, hashes, sizes, and top-level row counts.
- File chronology is consistent with “run verification last”: latest production artifact `manifest.json` at `16:09:09.725691`, `verify.py` at `16:10:05.399299`, and `verification.json` at `16:10:15.147030` on 2026-07-13. The existing verification output reports `passed: true` and no failures.

FAIL aspects:

- The verifier's probability routine repeats the fixed loop over `REG = [0.0, 0.4]` and is called at `0.2`, reproducing the production uninitialized-array bug. It therefore is separately written but not substantively independent for the decisive midpoint policy calculation.
- It computes raw transition count tuples `tc` and CCP count tuples `cc` but never compares either tuple list with `summary.json`. Its coverage claim “raw controlled transitions and cell counts” is therefore overstated: it compares only `P` and `Q` rates. Manifest top-level row counts do not fill this gap.
- It recomputes local-rank singular values but compares only the Jacobian and integer rank, not the saved singular values, despite claiming coverage of “Jacobian, singular values, and rank.”
- Its policy comparison omits `bellman_residual`, although the saved policy rows report that field.

Accordingly, source-level import independence and run-last chronology pass, but decisive verification coverage fails. The existing `verification.json` pass is not reliable evidence for the midpoint counterfactual.

## Final disposition

| Area | Result |
|---|---|
| Raw counts, transitions, CCPs | PASS |
| NFXP and distinct CCP estimates | PASS |
| 14-start objectives/gradients/acceptance/selection | PASS |
| Local-rank claim and identification wording | PASS |
| All 81 restricted-grid rows and metadata | PASS |
| Support labels | PASS |
| Policy accounting | FAIL (midpoint probability-dependent fields) |
| Manifest/hash/cross-artifact consistency | PASS |
| `verify.py` import independence | PASS |
| `verify.py` substantive coverage | FAIL |
| Run-last chronology | PASS |

The minimum repair is to make the NFXP probability evaluator solve and return probabilities for the regimes actually requested (including `0.2`), independently implement that logic in `verify.py`, compare saved transition/CCP count records and singular values explicitly, include Bellman residual checks, regenerate production artifacts and manifest, and then run the repaired verifier last.
