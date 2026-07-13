# Independent audit of `junzi-economist-struct-x061`

## Overall judgment: MIXED

The numerical artifact is **PASS**: an independent reconstruction from `raw_primitives.json` reproduces all substantive saved quantities, all ten optimizer terminals pass the declared projected-gradient rule, all nine restricted-grid rows and all five policy records check, the manifest hashes are exact, and the recorded chronology is ordered.

The verifier/coverage claim is **MIXED**, not a full PASS, for three narrow reasons. First, the verifier's “arbitrary off-regime policies” check evaluates only the three declared saved interior levels (0.25, 0.5, 0.75), not arbitrary unrecorded interior inputs. Second, it verifies the set of policy keys and the set of policy levels separately but never verifies the key-to-level mapping (`policy_025` ↔ 0.25, etc.). Third, `verifier_authored_after_production` is supported by filesystem modification times, not by an immutable authorship/provenance mechanism. These limitations do not overturn any saved numerical result.

## Audit basis and independence

I did not import `production.py` for the main reconstruction, did not use `verifier.py`, and did not overwrite any supplied artifact. I rebuilt transitions and CCPs from raw counts, derived the Hotz–Miller system as an affine two-equation system, solved its parameters analytically, derived the NFXP score and CCP gradient analytically, derived the choice-probability Jacobian by implicit differentiation, and solved each Bellman/accounting object at a tighter residual tolerance. I used the declared finite-difference rule separately to audit optimizer acceptance. Only after completing those checks did I call the production policy function read-only at two unrecorded levels to test for a shared hard-coded policy bug.

## The ten coverage-map objects

### 1. Row keys, uniqueness, and counts — PASS

All lists have the exact required cardinality and no duplicates:

- raw/production transitions: `s0_a0`, `s0_a1`, `s1_a0`, `s1_a1` (4 each);
- raw/production CCPs: `s0`, `s1` (2 each);
- NFXP and CCP starts: `start_00` through `start_04` (5 each);
- restricted rows: `grid_t0_00_t1_00` through `grid_t0_02_t1_02` (9);
- policies: `policy_000`, `policy_025`, `policy_050`, `policy_075`, `policy_100` (5).

### 2. Every transition and CCP cell — PASS

| Cell | Raw counts | Total | Recomputed probabilities |
|---|---:|---:|---:|
| `s0_a0` | (72, 18) | 90 | (0.8, 0.2) |
| `s0_a1` | (24, 36) | 60 | (0.4, 0.6) |
| `s1_a0` | (28, 42) | 70 | (0.4, 0.6) |
| `s1_a1` | (12, 68) | 80 | (0.15, 0.85) |
| `s0` CCP | (70, 30) | 100 | (0.7, 0.3) |
| `s1` CCP | (25, 75) | 100 | (0.25, 0.75) |

Every saved total and probability is exactly equal to these count ratios.

### 3. Both estimators, objectives, and parameters — PASS

The independently constructed Hotz–Miller log-odds-gap system is affine with determinant `1.08626198083067`, so it is nonsingular on the two-parameter system. Its exact numerical solution is

`theta = (-1.33182464494304, 2.12760769326375)`.

At this solution the two CCP gaps are `(5.55e-16, 1.55e-15)`, the CCP objective is `2.72e-28`, the NFXP probabilities are exactly `(0.3, 0.75)` for action 1, and the NFXP objective is `117.319944667370`. The saved estimates are:

| Estimator | Selected start | Saved parameters | Saved objective | Maximum parameter difference from analytic solution |
|---|---|---|---:|---:|
| NFXP | `start_03` | (-1.331824624909887, 2.1276076442512184) | 117.31994466737018 | 4.90e-8 |
| CCP/Hotz–Miller MD | `start_04` | (-1.3318246515905652, 2.1276076957237633) | 7.306073646640533e-15 | 6.65e-9 |

The tiny nonzero saved CCP objective is optimizer termination error, not a distinct optimum.

### 4. Projected gradients and acceptance for all ten starts — PASS

All terminals are interior, so their projected gradients equal their raw gradients. The table reports my fresh application of the declared step rule; the acceptance threshold is `2e-4`.

| Estimator/start | Recomputed projected gradient | Max abs | Accepted |
|---|---|---:|---|
| NFXP/`start_00` | (-1.81394e-8, -1.51720e-6) | 1.51720e-6 | yes |
| NFXP/`start_01` | (-2.54164e-6, 6.72602e-7) | 2.54164e-6 | yes |
| NFXP/`start_02` | (7.60786e-7, -4.61871e-7) | 7.60786e-7 | yes |
| NFXP/`start_03` | (-6.63154e-7, -8.33906e-7) | 8.33906e-7 | yes |
| NFXP/`start_04` | (-1.32257e-6, -2.17644e-6) | 2.17644e-6 | yes |
| CCP/`start_00` | (-2.8211880e-6, -1.6836284e-6) | 2.8211880e-6 | yes |
| CCP/`start_01` | (-2.8211884e-6, -1.6836344e-6) | 2.8211884e-6 | yes |
| CCP/`start_02` | (-2.8211883e-6, -1.6836346e-6) | 2.8211883e-6 | yes |
| CCP/`start_03` | (-2.8211887e-6, -1.6836311e-6) | 2.8211887e-6 | yes |
| CCP/`start_04` | (-2.8211869e-6, -1.6836327e-6) | 2.8211869e-6 | yes |

The maximum discrepancy between these finite-difference projected gradients and the saved projected gradients is `4.27e-9` (NFXP) and `1.10e-13` (CCP). Independent analytic gradients agree at the same numerical scale.

### 5. Singular values and local rank — PASS

Implicit differentiation at the analytic solution gives singular values

`(0.402393871136282, 0.106292785659058)`.

The saved finite-difference values are `(0.402393874487768, 0.106292786721413)`, with maximum difference `3.35e-9`. Both exceed the declared `1e-6` threshold, so local numerical rank is 2. This supports only the artifact's stated local numerical-rank claim.

### 6. Every restricted-grid row — PASS

Boundary code is `(theta0 lower, theta0 upper, theta1 lower, theta1 upper)`.

| Key | (theta0, theta1) | Domain | Boundary | Slack | Feasible | Recomputed NFXP objective |
|---|---:|---|---:|---:|---|---:|
| `grid_t0_00_t1_00` | (-1, 0) | `closed_finite_theta_grid_v1` | 1010 | 0.5 | yes | 167.65233750364456 |
| `grid_t0_00_t1_01` | (-1, 1) | same | 1000 | 1.5 | yes | 127.73229360455761 |
| `grid_t0_00_t1_02` | (-1, 2) | same | 1001 | 2.5 | yes | 119.12724918388486 |
| `grid_t0_01_t1_00` | (0, 0) | same | 0010 | -0.5 | no | 138.62943611198910 |
| `grid_t0_01_t1_01` | (0, 1) | same | 0000 | 0.5 | yes | 132.25712633796869 |
| `grid_t0_01_t1_02` | (0, 2) | same | 0001 | 1.5 | yes | 157.15959159248660 |
| `grid_t0_02_t1_00` | (1, 0) | same | 0110 | -1.5 | no | 157.65233750364453 |
| `grid_t0_02_t1_01` | (1, 1) | same | 0100 | -0.5 | no | 183.28546712896650 |
| `grid_t0_02_t1_02` | (1, 2) | same | 0101 | 0.5 | yes | 228.17712225819100 |

Every saved key, coordinate, domain, boundary flag, slack, feasibility flag, and objective matches. The feasible-grid minimizer is `grid_t0_00_t1_02`, as saved.

### 7–8. Exact policy set, labels, arbitrary levels, Bellman residuals, monotonicity, and accounting — PASS numerically; verifier wording MIXED

The exact saved level set is `{0, 0.25, 0.5, 0.75, 1}`. Levels 0 and 1 are labeled `observed_regime`; 0.25, 0.5, and 0.75 are labeled `interior_model_interpolation`; only 0.5 has `is_midpoint=true`. All key-to-level pairs in the actual artifact are correct.

| Key | Choice-1 probabilities by state | Value vector | Saved Bellman residual | Accounting identity residual |
|---|---|---|---:|---:|
| `policy_000` | (0.3000000012, 0.7499999929) | (2.9946916544, 4.5088378118) | 6.9562e-12 | 3.4782e-11 |
| `policy_025` | (0.2394725912, 0.6925760199) | (2.4343442418, 3.7663799978) | 7.1028e-12 | 3.5513e-11 |
| `policy_050` | (0.1878904368, 0.6285060914) | (1.9607210233, 3.1108721909) | 7.1660e-12 | 3.5829e-11 |
| `policy_075` | (0.1455935727, 0.5599430446) | (1.5673330035, 2.5430724568) | 7.1587e-12 | 3.5793e-11 |
| `policy_100` | (0.1119363470, 0.4896834039) | (1.2453382414, 2.0600619356) | 7.0961e-12 | 3.5481e-11 |

At the saved theta, a tighter independent solve matches saved probabilities to `1.11e-16`, values to `3.58e-11`, and every accounting component to `3.58e-11`. The saved accounting separately contains discounted activity, action-intercept return, state-1 action return, policy cost, logit entropy, total model value, and initial Bellman value. Its signs and identity are correct.

The five-point monotonicity flag is true. A stronger audit over 101 evenly spaced levels from 0 to 1 is also monotone nonincreasing in both states.

To test for a common hard-coded policy bug, I evaluated two levels absent from all saved artifacts:

| Unrecorded level | Independently recomputed choice-1 probabilities | Production-function maximum probability difference | Production label |
|---:|---|---:|---|
| 0.137 | (0.26578846596, 0.71945062860) | 5.55e-17 | `interior_model_interpolation` |
| 0.6180339887498949 | (0.16678468684, 0.59653374323) | 1.11e-16 | `interior_model_interpolation` |

Thus no shared hard-coded policy-level bug is present. The MIXED qualification concerns only the verifier's wording: its own loop covers the declared five-level set, not arbitrary unrecorded interior inputs, and it does not assert `policy_key == f(level)`.

### 9. All headline values — PASS

The independently supported headlines are: NFXP parameters/objective `(-1.331824624909887, 2.1276076442512184)` / `117.31994466737018`; CCP parameters/objective `(-1.3318246515905652, 2.1276076957237633)` / `7.306073646640533e-15`; transition cells 4; CCP cells 2; accepted starts per estimator 5; restricted rows 9; policy records 5; local numerical rank 2; monotonic policy sanity `true`. The saved headline object contains exactly these keys and values.

### 10. Production hashes and chronology — PASS with provenance caveat

The output-embedded hashes exactly match current bytes:

- `production.py`: `1ac0324705ab1cb3ca683744c442e968bbf20297c5b469ab3be1d94a3c7f95f3`;
- `raw_primitives.json`: `7075def180ad063f0aeed7c8a5f9015b2b2d2ab3af420df7317ab650db5a1741`.

The timestamp order is:

`production.py` mtime 08:33:56.805209Z ≤ production start 08:34:01.291728Z ≤ raw mtime 08:34:01.292732Z ≤ production finish 08:34:01.496254Z ≤ output mtime 08:34:01.505030Z ≤ verifier mtime 08:37:09.852474Z ≤ verification start 08:37:13.956130Z ≤ verification finish 08:37:14.118139Z ≤ manifest creation 08:37:14.119141Z ≤ manifest mtime 08:37:14.132139Z`.

This establishes internally consistent filesystem chronology. It cannot prove who authored the verifier or rule out timestamp manipulation, so the manifest's `verifier_authored_after_production=true` should be read as an mtime-based assertion.

## Manifest and verifier self-hash — PASS

All six manifest entries match both SHA-256 and byte count:

| File | Bytes | SHA-256 |
|---|---:|---|
| `README.md` | 1652 | `660447bcfb5cf132a086eb1590127f38754b46fe380338682f56bb3583457180` |
| `production.py` | 11996 | `1ac0324705ab1cb3ca683744c442e968bbf20297c5b469ab3be1d94a3c7f95f3` |
| `production_output.json` | 12786 | `19cd386df72d3627ea0d2d6efae393300bcccfa6c7cd98939347822d7c5dbd28` |
| `raw_primitives.json` | 1330 | `7075def180ad063f0aeed7c8a5f9015b2b2d2ab3af420df7317ab650db5a1741` |
| `verification.json` | 12741 | `81d4b19eca41b4bfcc8115adca960aa1522fca1a37281f15f9a6598b35f70d7c` |
| `verifier.py` | 18294 | `02b480988daeade7e6b8b35e83a7aa08a860d1f26a49949795c0acf7497390f6` |

The recomputed verifier hash equals both `verification.json.verifier_source_sha256` and `final_manifest.json.verifier_self_sha256`.

## Verifier independence, exactness, and claim scope

Positive evidence for independence: `verifier.py` does not import production code; it reconstructs arrays, utilities, the Bellman fixed point, likelihood, CCP evaluation, occupancy accounting, gradients, grid rows, and hashes in separate code. It also starts value iteration from a different vector and uses a transposed linear solve for discounted occupancy.

Limits: it uses the same SciPy optimizer and options, the same finite-difference convention, and the saved NFXP theta as the input to its rank and policy checks. The analytic inversion, analytic derivatives, tighter Bellman solve, dense policy path, and unrecorded-level tests above remove the material common-mode concern for this artifact.

The coverage map is accurate for the saved finite objects except for the two policy exactness overstatements already identified. It also intentionally does not claim to check solver status/message fields, distance-from-best fields, top-level schemas, continuous-grid identification, external validity, or welfare. Those omissions are consistent with its stated coverage limit.

No global identification claim was found. `production_output.json` explicitly says “local numerical rank only; no global or population identification claim”; `verification.json` excludes global identification, continuous-grid, external-validity, and welfare claims; and `README.md` labels the restricted domain as a closed finite 3×3 grid and the interior policies as model-based interpolation.

## Final disposition

- **Numerical/model artifact:** PASS.
- **Hashes and recorded chronology:** PASS, with the stated provenance limitation.
- **Verifier independence:** PASS for code-level reimplementation; strengthened by this analytic audit.
- **Verifier coverage-map exactness:** MIXED because “arbitrary” is broader than the executed finite-level check and policy keys are not tied to levels in the acceptance rule.
- **Overall:** MIXED. No substantive result needs retraction; the appropriate repair is to narrow the coverage wording or add unrecorded-level and key-to-level assertions.
