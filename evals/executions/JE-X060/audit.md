# Independent audit of `junzi-economist-struct-x060`

## Verdict: MIXED

The numerical and economic content passes independent recomputation. The panel, every saved controlled-transition and CCP row, both estimators, all ten optimizer starts, the declared closed box and corners, the local-rank calculation, arbitrary-policy solutions, Bellman residuals, midpoint accounting, support labels, and monotonicity checks are correct to tight numerical tolerances. I found no hard-coded-regime bug and no shared arbitrary-policy solver bug.

The bundle is nevertheless **MIXED** because `verify.py` materially overstates its coverage. It does not recompute either estimator, objective optimum, optimizer result, or projected gradient; it trusts those saved fields. It also does not enforce row-key uniqueness/completeness, the exact saved-policy label set, several boundary labels, or verifier immutability/chronology. Thus the current artifacts are correct, but the bundled verifier alone would not establish all claims it says it covers.

Audit conditions: the target had no `.git` metadata. I did not run `production.py` or `verify.py`, did not overwrite any artifact, and did not modify production or verifier code. Recomputation used an external audit-only program and output outside the target. The only target file added is this report.

## 1. Panel and count reconstruction — PASS

The panel has exactly 15,000 rows, 500 agents, and 30 observations per agent. Agent IDs are exactly 0–499; periods are exactly 0–29 for every agent; each agent's policy is constant; the split is 250 agents at policy 0 and 250 at policy 1; within-agent `next_state[t] = state[t+1]` for every adjacent period. Observed support is policies `{0,1}`, states and next states `{0,1,2,3,4}`, and actions `{0,1}`.

Recomputed controlled-transition counts, with one 5×5 matrix per action:

```text
action 0
[[1131, 3470,    0,    0,   0],
 [   0,  875, 2685,    0,   0],
 [   0,    0,  355, 1181,   0],
 [   0,    0,    0,   96, 327],
 [   0,    0,    0,    0, 134]]
row totals = [4601, 3560, 1536, 423, 134]

action 1
[[ 447,  73, 0, 0, 0],
 [1189, 214, 0, 0, 0],
 [1278, 218, 0, 0, 0],
 [ 781, 123, 0, 0, 0],
 [ 367,  56, 0, 0, 0]]
row totals = [520, 1403, 1496, 904, 423]
```

The corresponding nonzero probabilities are:

```text
action 0: (0.24581612692892849, 0.7541838730710715)
          (0.24578651685393257, 0.7542134831460674)
          (0.23111979166666666, 0.7688802083333334)
          (0.22695035460992907, 0.7730496453900709)
          state 4 -> state 4 with probability 1
action 1: (0.8596153846153847, 0.14038461538461539)
          (0.8474697077690663, 0.1525302922309337)
          (0.8542780748663101, 0.14572192513368984)
          (0.8639380530973452, 0.13606194690265486)
          (0.8676122931442081, 0.13238770685579196)
```

All 50 rows in `transition_rows.csv` match their recomputed key, count, row total, and probability exactly within absolute tolerance `2e-15`; total count is 15,000 and there are no mismatches.

Recomputed choice counts `[continue, replace]` and Jeffreys-smoothed replacement CCPs:

| policy | state | counts | total | smoothed CCP |
|---:|---:|---:|---:|---:|
| 0 | 0 | [2197, 143] | 2340 | 0.06129859034600598 |
| 0 | 1 | [1873, 522] | 2395 | 0.21807178631051752 |
| 0 | 2 | [929, 687] | 1616 | 0.42517006802721086 |
| 0 | 3 | [275, 519] | 794 | 0.6534591194968553 |
| 0 | 4 | [97, 258] | 355 | 0.726123595505618 |
| 1 | 0 | [2404, 377] | 2781 | 0.1356937455068296 |
| 1 | 1 | [1687, 881] | 2568 | 0.34312962242117556 |
| 1 | 2 | [607, 809] | 1416 | 0.5712773465067043 |
| 1 | 3 | [148, 385] | 533 | 0.7219101123595506 |
| 1 | 4 | [37, 165] | 202 | 0.8152709359605911 |

All 10 rows in `ccp_rows.csv` match their key, both counts, row total, and smoothed CCP within `2e-15`; total count is 15,000 and there are no mismatches. Headline sample, transition, and CCP totals therefore reconcile exactly.

## 2. Estimators and every start — PASS

The audit NFXP path solved the Bellman equation by damped Newton iteration, derived the likelihood score by implicit differentiation of the Bellman fixed point, and optimized with SLSQP. It did not use production value iteration. At the saved accepted NFXP estimate:

```text
saved theta                  = [0.6141485388723869, 3.3091664821549203]
saved objective              = 0.5169302208662993
recomputed objective         = 0.5169302208662994
recomputed analytic gradient = [1.1781894287661923e-08, -4.431454912767231e-09]
```

For the CCP estimator, the empirical-policy forward mapping is affine in theta. I constructed its affine design from basis evaluations and solved the weighted least-squares normal equations directly, independently of the production optimizer:

```text
saved theta                  = [0.6165996876033254, 3.3364627193601204]
closed-form audit theta      = [0.6165996970175173, 3.336462740731985]
maximum parameter difference = 2.137186464e-08
saved objective              = 0.0036730123927171555
audit optimum objective      = 0.003673012392716997
audit optimum gradient       = [-2.1163626406917047e-16, -7.112366251504909e-16]
```

Every saved point is interior, so its projected gradient equals its raw gradient. The table gives the independently recomputed maximum projected gradient, the saved finite-difference value, the maximum coordinate distance between an independent SLSQP reoptimization and that row's saved solution, and recomputed acceptance under `optimizer_success && PG <= 2e-5`.

| estimator | start | audit PG max | saved PG max | audit-to-saved max distance | accepted |
|---|---:|---:|---:|---:|:---:|
| NFXP | 0 | 1.4895323096264165e-08 | 1.4821477379142395e-08 | 3.683496134776476e-07 | yes |
| NFXP | 1 | 1.1781894287661923e-08 | 1.1796119636957899e-08 | 1.3197713277790513e-07 | yes |
| NFXP | 2 | 2.619042969911195e-08 | 2.614575223062198e-08 | 5.404447656065514e-08 | yes |
| NFXP | 3 | 4.331215842034129e-08 | 4.335420911277233e-08 | 3.961169603439174e-08 | yes |
| NFXP | 4 | 5.701114149303174e-08 | 5.7037707891643486e-08 | 3.4256516201480736e-07 | yes |
| CCP | 0 | 4.0309506899038894e-08 | 4.030781784844105e-08 | 3.1836678626717685e-08 | yes |
| CCP | 1 | 4.239502931352446e-08 | 4.2397942796614524e-08 | 3.053120600782222e-08 | yes |
| CCP | 2 | 3.6901709937753324e-08 | 3.69091692982598e-08 | 2.137186649875389e-08 | yes |
| CCP | 3 | 4.0512816924104245e-08 | 4.051826149012611e-08 | 2.3977691387955247e-08 | yes |
| CCP | 4 | 3.8648517112355174e-08 | 3.864421803493478e-08 | 3.7920219853049275e-08 | yes |

All ten independent optimizations succeeded. The largest independently recomputed projected gradient is `5.701114149303174e-08`, only 0.00286 of the required tolerance. The largest saved-versus-audit projected-gradient difference is `7.38457171217701e-11`.

## 3. Declared closed domain, corners, and slacks — PASS

The declared domain is exactly the inclusive box `theta_x ∈ [0.15,1.50]`, `replacement_cost ∈ [1.00,6.00]`. The four estimator-parameter keys are unique and complete. Recomputed slacks and boundary labels are:

| estimator | parameter | estimate | lower slack | upper slack | lower boundary | upper boundary |
|---|---|---:|---:|---:|:---:|:---:|
| NFXP | theta_x | 0.6141485388723869 | 0.46414853887238683 | 0.8858514611276131 | no | no |
| NFXP | replacement_cost | 3.3091664821549203 | 2.3091664821549203 | 2.6908335178450797 | no | no |
| CCP | theta_x | 0.6165996876033254 | 0.4665996876033254 | 0.8834003123966746 | no | no |
| CCP | replacement_cost | 3.3364627193601204 | 2.3364627193601204 | 2.6635372806398796 | no | no |

Every saved slack has zero floating-point discrepancy from direct subtraction. The complete corner set and slacks is:

| corner `(theta_x, replacement_cost)` | tx lower | tx upper | rc lower | rc upper | boundary count |
|---|---:|---:|---:|---:|---:|
| (0.15, 1.00) | 0 | 1.35 | 0 | 5 | 2 |
| (0.15, 6.00) | 0 | 1.35 | 5 | 0 | 2 |
| (1.50, 1.00) | 1.35 | 0 | 0 | 5 | 2 |
| (1.50, 6.00) | 1.35 | 0 | 5 | 0 | 2 |

All four corners are present exactly once; every corner slack has zero discrepancy and every `boundary_count` equals 2.

## 4. Local rank — PASS, with correctly limited interpretation

Using analytic implicit derivatives of replacement probabilities rather than the saved finite-difference Jacobian, I obtain:

```text
audit singular values = [1.7322569726363501, 0.16432355671257604]
saved singular values = [1.7322569727240198, 0.16432355672775767]
absolute differences  = [8.766964931e-11, 1.518163928e-11]
rank at 1e-8           = 2
```

This supports only local rank at the saved NFXP estimate, conditional on the estimated controlled transitions and observed policy support `{0,1}`. The README, headline, and `local_rank.json` correctly avoid a global-identification claim.

## 5. Support labels and arbitrary-policy implementation — PASS

Support labels reconcile exactly:

- panel observed policies: `{0,1}`;
- headline observed regimes: `{0,1}`;
- local-rank observed support: `{0,1}`;
- saved policy-level labels: `{0,0.5,1}`;
- `0.5` is explicitly labeled model interpolation, not observed support.

Production utilities use the passed scalar directly (`production.py:48–54`), and the Bellman solver receives that scalar (`production.py:57`). Observed-regime loops are confined to estimation/data objects, while saved policy claims are deliberately `{0,1,0.5}` (`production.py:386–388`).

I also called the production solver at unsaved policies `0.25`, `0.75`, and `0.37`, and at finite policies outside the declared policy interval, `-0.2` and `1.4`. All calls succeeded. Against the separately coded damped-Newton audit path, the maximum value-vector error over `{−0.2,0,0.25,0.37,0.5,0.75,1,1.4}` was `8.954614827416663e-12`; the maximum CCP error was `1.2878587085651816e-14`. There is no hard-coded-regime failure.

The audit solver is a third implementation: hand-coded damped Newton steps and an eigenvector stationary distribution. Production uses value iteration and an augmented linear system; the verifier uses SciPy nonlinear root finding and an augmented linear system. Agreement across these paths rejects the suspected shared arbitrary-policy solver bug.

## 6. Arbitrary-policy solutions, residuals, and economic sanity — PASS

All vectors below are independently recomputed. `V` is the ex-ante value vector; `CCP` is the replacement-probability vector; `π` is the stationary state distribution.

### Policy 0

```text
V   = [-7.357951395850331, -8.542057240702784, -9.246455942174363, -9.624133393528089, -9.812723189503265]
CCP = [0.06567883432329488, 0.21186281618967834, 0.43164060873981397, 0.6362333268385212, 0.7712948904615001]
π   = [0.31240918761116715, 0.3229472547901417, 0.22099753760969715, 0.1052664686687916, 0.03837955132020243]
rate=0.2809066852157689; deterioration=0.7580189395360988; replacement=0.9295669873292655
transfer=0; private=1.6875859268653643; social=1.6875859268653643
Bellman residual=1.7763568394002505e-15; stationarity residual=1.1102230246251565e-16
```

### Policy 0.25

```text
V   = [-6.712494207411419, -7.823929691939032, -8.475188581719582, -8.82223428665783, -8.996138143451606]
CCP = [0.07979115181924974, 0.2395348411426657, 0.462556228758121, 0.660816788705976, 0.7892284305398675]
π   = [0.32541967270331973, 0.3297870519294028, 0.2159778243988475, 0.09669159135397574, 0.03212385961445432]
rate=0.2941114777535769; deterioration=0.7248874510827585; replacement=0.9732638441991891
transfer=0.07352786943839422; private=1.6246234258435532; social=1.6981512952819475
Bellman residual=1.7763568394002505e-15; stationarity residual=1.6653345369377348e-16
```

### Policy 0.5 (saved midpoint)

```text
V   = [-6.029692058001336, -7.067666807743435, -7.666994800839445, -7.984645119486458, -8.144433087811096]
CCP = [0.09658407622199079, 0.2696277811811967, 0.4940963973909127, 0.6849905793235624, 0.8064367306765186]
π   = [0.33954712899965955, 0.33627431335542446, 0.2097656225362979, 0.08787693182110405, 0.026536003287514008]
rate=0.30870265933188107; deterioration=0.6912735378019136; replacement=1.0215484932131496
transfer=0.15435132966594053; private=1.5584707013491226; social=1.712822031015063
Bellman residual=1.7763568394002505e-15; stationarity residual=1.6653345369377348e-16
```

The saved midpoint vector errors are `8.125944361836446e-12` for value, `4.996003610813204e-16` for CCP, and `1.1102230246251565e-16` for the stationary distribution. The largest saved midpoint accounting-level error is `4.440892098500626e-16`.

Midpoint identities hold to rounding:

```text
replacement resource cost = replacement_cost × rate
                          = 3.3091664821549203 × 0.30870265933188107
                          = 1.0215484932131496
fiscal transfer           = policy × rate = 0.5 × 0.30870265933188107
                          = 0.15435132966594053
social resource cost      = deterioration + replacement
                          = 0.6912735378019136 + 1.0215484932131496
                          = 1.712822031015063
private flow cost         = social − transfer
                          = 1.712822031015063 − 0.15435132966594053
                          = 1.5584707013491226
```

### Policy 0.75

```text
V   = [-5.305547563767636, -6.2695718922941275, -6.8183686358293265, -7.107887979501597, -7.254131359232501]
CCP = [0.1164361189102529, 0.30212150183987724, 0.5261219828128881, 0.7087009488230609, 0.8229248427969682]
π   = [0.3549122034959032, 0.3422572852572724, 0.20230373636026122, 0.07892845832861409, 0.021598316557949068]
rate=0.3248747920355913; deterioration=0.6571655901459176; replacement=1.0750647727012288
transfer=0.24365609402669347; private=1.488574268820453; social=1.7322303628471465
Bellman residual=8.881784197001252e-16; stationarity residual=1.1102230246251565e-16
```

### Policy 1

```text
V   = [-4.535541782947614, -5.4254833026849365, -5.925334583984036, -6.188011077256417, -6.321282960150232]
CCP = [0.13972864432694562, 0.3369436678930865, 0.5584807685443438, 0.7318926214598502, 0.8386962199907942]
π   = [0.37163734143586924, 0.3475511382018472, 0.19355673895760236, 0.06996491055658469, 0.01728987084809658]
rate=0.34283900463812067; deterioration=0.6225739389961247; replacement=1.1345113429238243
transfer=0.34283900463812067; private=1.4142462772818283; social=1.757085281919949
Bellman residual=8.970602038971265e-14; stationarity residual=2.220446049250313e-16
```

Economic sanity is coherent over policies `[0,.25,.5,.75,1]`:

- replacement CCP strictly increases with state at every policy and strictly increases with subsidy at every state;
- replacement-rate increments are `[0.013204792537807986, 0.014591181578304191, 0.016172132703710207, 0.017964212602529395]`;
- private-flow-cost increments are `[-0.06296250102181111, -0.06615272449443066, -0.0698964325286695, -0.0743279915386248]`;
- social-resource-cost increments are positive, `[0.010565368416583176, 0.014670735733115503, 0.01940833183208346, 0.02485491907280246]`, because the subsidy induces more replacement and changes the stationary state distribution; this is economically plausible and makes clear that the fiscal subsidy is a transfer, not a resource saving;
- every stationary distribution is nonnegative, sums to one, and has direct stationarity residual at most `2.220446049250313e-16`.

## 7. Production hashes and chronology — PASS for declared production freeze; limited provenance

All 12 records in `production_hashes.json` match both current byte length and SHA-256 exactly. The declared manifest covers `production.py`, `README.md`, and all production outputs other than the manifest itself. Exact hashes:

| file | bytes | SHA-256 |
|---|---:|---|
| production.py | 18515 | ebedb41da435761fbebfacde41a1e4820bec962c5b3ad2f62ea0603bd1970bc0 |
| README.md | 1736 | 9f698090fe59887c4c4a3635d20cfe7dab83d9625c29e25fe299816bb02a27d9 |
| artifacts/panel.csv | 261748 | df769a2566714f1ab08f4759a1eb3038254b6a9a192086fac2d30526733856f2 |
| artifacts/transition_rows.csv | 1250 | acfa1ce59d3abb80caa94c599f42166c6d6eb73e9a2b0b6c2d14a4f637b25edb |
| artifacts/ccp_rows.csv | 468 | ecbc2ec1f3970c03d29ca440045df1917cea71513e62114e194d096c1eb5839b |
| artifacts/optimizer_starts.csv | 3032 | 2de900355b2293edf30064b77cb3a019cab07922bc15992593906c9bacfd9f21 |
| artifacts/domain_rows.csv | 508 | d076d8dc9d8f962d611a674fa171f8ab9a1f74b0a7eff0770bf8c998364e98a4 |
| artifacts/closed_domain_corners.csv | 256 | 6dd2d93f4afc88b8c77958385d243d7bac35fde0217316c6c046307b53abbc2c |
| artifacts/estimates.json | 281 | a112dcd43e0a44a8973b19f6dedf75055cbfe2729a394897482bf8ecfa03039a |
| artifacts/local_rank.json | 1052 | 95c575665d78fee0c0713db8764b5c196f45bc0c367de51c37295956b8c71ac6 |
| artifacts/policy_levels.json | 2738 | 105959c0b16ee867fd68f6c1ab09776f186d1c9700307e292272febed01219f1 |
| artifacts/headline.json | 999 | 3dae601f0c0e07c4a8e3b7401a2b79f955077144deaee2832f10359b6bccacee |

Filesystem chronology in Asia/Shanghai is coherent with production freeze followed by verification:

```text
16:19:54  production.py, README.md
16:20:11  panel.csv, transition_rows.csv, ccp_rows.csv
16:20:17  optimizer/domain/corners/estimates/local_rank/policy_levels/headline
16:20:38  production_hashes.json
16:22:19  verify.py
16:22:24  verification.json
```

Current hashes of the unhashed verifier-side files are:

```text
production_hashes.json  df218d77525380b7de280b7aeb30109ce5eee78470cf7c5486f1a849b6826edc
verify.py               065953fa417c041e98cc9e2ebb23bd1237eed57423229d412877755d89d6f6b9
verification.json       af82ce3c7f2799239d0fb98771b2dbc440791f53009b36c5bb70be6b954cec18
```

Limitation: timestamps are mutable filesystem metadata, there is no Git history, and neither `verify.py` nor verifier output is included in the production manifest. The chronology is consistent, not cryptographic proof of authorship or historical ordering.

## 8. Verifier independence and coverage — MIXED

### What is genuinely independent and well covered

- `verify.py` does not import `production.py`.
- Its arbitrary-policy solver uses SciPy nonlinear root finding with an analytic Jacobian (`verify.py:102–143`), while production uses value iteration. It directly recomputes Bellman residuals and stationary distributions for `[0,.25,.5,.75,1]`.
- It reconstructs counts from the panel, recomputes controlled-transition probabilities and Jeffreys CCPs, compares saved policy vectors/levels, recomputes local singular values with a different finite-difference step, and checks core headline totals.
- The saved `verification.json` reports all checks passed, and this audit independently confirms the values it reports.

### Material gaps

1. **No estimator verification.** `verify.py` never defines or evaluates the NFXP likelihood or CCP criterion and never re-estimates either model. It simply loads the saved NFXP estimate for policy and rank checks. Therefore it does not validate `estimates.json` as an optimum or validate the CCP estimate at all.

2. **Saved optimizer evidence is trusted, not recomputed.** At `verify.py:253–256`, acceptance is calculated solely from the saved strings `optimizer_success`, `projected_gradient_max`, and `accepted`. No objective, gradient, projected gradient, returned estimate, start coordinate, optimizer status, or objective gap is independently computed. The coverage claim “all-start projected-gradient acceptance” is therefore too strong.

3. **Row completeness is inferred only from length.** For transitions and CCPs, the verifier iterates the saved rows and checks each row it sees, then requires lengths 50 and 10. It does not enforce unique keys or equality to the full expected key set. A duplicated correct row plus an omitted row could pass. The same issue affects the four domain keys; `len(domain)==4` does not establish the four unique estimator-parameter combinations.

4. **Incomplete domain-field coverage.** It recomputes numerical slacks, but does not validate `at_lower_boundary`, `at_upper_boundary`, or corner `boundary_count`; it also does not explicitly enforce unique corner rows beyond set equality plus length.

5. **Saved policy support is not enforced.** `compare_policy_levels` loops over whatever policies are present in `policy_levels.json` (`verify.py:162`) and only requires that a midpoint row exists later. It does not require the exact saved set `{0,0.5,1}` or link its actual length to `headline.saved_policy_level_rows`. A substituted three-row set such as `{0.25,0.5,0.75}` could satisfy the current comparison logic.

6. **Hash scope and chronology are narrower than stated.** `verify_hashes` checks only manifest entries (`verify.py:35–44`). The manifest excludes `verify.py`, `production_hashes.json`, and `verification.json`, and the verifier performs no chronology check. “Production file immutability” is fair for the 12 declared production files, but not for the verifier or complete bundle.

7. **Several headline/support claims are not reconciled.** The verifier checks selected totals and the literal identification-scope string, but does not reconcile agent count, periods, state count, beta, observed regime labels, interpolation label, solver contract, or saved singular values in the headline against their underlying objects.

These are verifier-design defects, not detected defects in the present numerical artifacts. The independent calculations above supply the missing evidence for this snapshot, but `verify.py` should be strengthened before the bundle itself earns an overall `PASS`.

## Final research judgment

The current snapshot's structural estimates and policy accounting are numerically credible conditional on the stated five-state dynamic-logit specification, estimated controlled transitions, inclusive parameter box, and interpolation interpretation. The local-rank result is well supported but is not global identification. Policy `0.5` is model interpolation; the exercise does not establish out-of-support causal validity, sampling uncertainty, or welfare optimality. The audit status remains **MIXED solely because verifier coverage and provenance are incomplete, not because any recomputed model result failed**.
