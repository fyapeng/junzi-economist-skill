# Independent audit — `junzi-economist-struct-x051`

## Overall judgment: MIXED

The DGP, raw data, estimator objectives, saved starts, projected-gradient bookkeeping, conditional-profile optimization, policy arithmetic, counts, and stated verifier-coverage limits reproduce. The main inferential output does **not**: the likelihood-ratio statistics were normalized by the best point on the 9-point grid rather than by the unrestricted MSL optimum. This is a material defect because it changes the accepted evaluated grid set from the reported `{0.3, 0.4, 0.5}` to `{0.4, 0.5}` and therefore changes the reported policy-set image.

This audit was read-only with respect to the production scripts and existing artifacts. All likelihoods, the SMM criterion, policy shares, DGP arrays, acceptance flags, and selected rows were recomputed from `raw_simulation.npz` or regenerated from the declared seeds.

## Exact defects

### D1 — FAIL: wrong LR reference objective

`study.py` sets `prof_min` to the minimum objective among the nine conditional grid solutions and calculates

`LR_grid(sigma) = 2 * (conditional NLL(sigma) - prof_min)`.

A likelihood-ratio profile must instead use the unrestricted optimum:

`LR(sigma) = 2 * (conditional NLL(sigma) - unrestricted NLL)`.

The unrestricted normal-random-coefficient MSL NLL is **1739.851639113888** at estimated `sigma = 0.4306865`. The best 9-point conditional-grid NLL is **1739.9734280825735** at `sigma = 0.4`, which is worse by **0.12178896868545**. Consequently every saved LR statistic is understated by **0.24357793737090**.

The defect is outcome-relevant at `sigma = 0.3`:

| sigma | conditional NLL | saved LR | correct LR | saved decision | correct decision at 3.841459 |
|---:|---:|---:|---:|---|---|
| 0.3 | 1741.8548392168752 | 3.7628223 | **4.0064002** | inside | **outside** |
| 0.4 | 1739.9734280825735 | 0.0000000 | 0.2435779 | inside | inside |
| 0.5 | 1740.4985917793850 | 1.0503274 | 1.2939053 | inside | inside |

Thus the accepted **evaluated grid points** are `{0.4, 0.5}`, not `{0.3, 0.4, 0.5}`.

### D2 — FAIL: policy-set range inherits D1

The policy arithmetic in every selected profile row is exact, and it uses the selected conditional solution. However, the reported policy set includes `sigma = 0.3` only because of D1. Using the unrestricted LR denominator, the accepted evaluated points map to:

- `sigma = 0.4`: drive-share change **-0.0765727169**;
- `sigma = 0.5`: drive-share change **-0.0760460576**.

The corrected evaluated-grid image is therefore **[-0.0765727, -0.0760461]** (about -7.657 to -7.605 percentage points), rather than the reported **[-0.0771081, -0.0760461]**.

### D3 — MIXED: 9-point grid language is not fully bounded

It is correct to say that all nine declared grid indices were evaluated and that the accepted **grid points** can be listed. A 0.1-spaced grid does not establish a continuous confidence-set boundary, however. The response sometimes calls the discrete collection “the reported set” while elsewhere acknowledging that the grid is an approximation. It should consistently say “accepted evaluated grid points.” Continuous lower and upper endpoints require adaptive/finer profiling around cutoff crossings; the current run cannot report a continuous interval or its policy image.

After correcting D1, neither domain endpoint (`sigma = 0` or `0.8`) is accepted, so the saved left/right endpoint-censoring flags remain correct **for the evaluated grid/domain endpoints**. They do not substitute for locating the continuous cutoff crossings.

### D4 — MIXED: “predeclared before estimation” is asserted, not independently evidenced

The constants, bounds, grid, and acceptance tolerance appear near the start of `study.py`, and the DGP attributes are generated before shocks and choices. That makes the executed design internally reproducible. But `support.predeclared_before_estimation = true` is only a self-authored Boolean written after estimation; there is no immutable preregistration, prior hash/timestamp, or independent design record establishing temporal predeclaration. The defensible label is “declared in the executed script” unless outside evidence is supplied.

The attribute boxes are DGP/design supports, not realized empirical extrema. All realized values lie strictly within them; wording them as “training support” is acceptable only if “support” means the generating distribution's declared boxes, not the observed min/max.

## Audit results by requested item

### DGP and support labels — PASS, subject to D4

Fresh regeneration using simulation seed `51051` and integration seed `9117` exactly reproduced every saved cost, time, reliability, choice, and integration-draw array. Intended and realized samples are both 900, with 700 training and 200 validation people and four tasks per person.

The declared DGP boxes contain all realized attributes. For example, realized drive cost is `[4.0030949, 11.9969419]` within the declared `[4,12]`; corresponding checks pass for every alternative and attribute. Adding $3 gives the declared policy support `[7,15]`. In the validation sample, **37.625%** of post-policy drive costs exceed $12, and the entire positive-charge regime is unobserved, so the extrapolation warning is correct. The absence of congestion/equilibrium feedback is also correctly labeled.

### Estimator distinctness — PASS

The four estimators are genuinely distinct:

- MSL integrates a normal person-specific time coefficient over 60 fixed antithetic draws in the repeated-choice panel likelihood.
- Homogeneous logit is the same likelihood with `sigma = 0` and five free parameters.
- The latent-class estimator is an exact two-point panel mixture with ordered support induced by midpoint plus positive gap; the fitted time coefficients are `-1.2629327` and `-0.4478315`, with weights `0.3937869` and `0.6062131`.
- SMM minimizes a separately defined diagonal-weighted criterion using 11 share and probability-weighted attribute moments. Its criterion, likelihood evaluations, and policy effect independently reproduce; fitted `sigma = 0.00000411`.

The reported fit comparisons reproduce: MSL improves training NLL over homogeneous logit by about 9.433; the two-point mixture is within about 0.154 NLL of MSL; SMM's selected moments lead to near-zero dispersion. These computational facts do not prove population identification or finite-sample performance, and the response appropriately declines those claims.

### Starts, selection, projected gradients, and KKT rules — PASS for this run

Complete recorded counts are:

| problem | starts |
|---|---:|
| normal RC MSL | 8 |
| homogeneous logit | 6 |
| two-point latent class | 8 |
| SMM | 8 |
| conditional profiles | 54 = 9 indices × 6 |

Every row contains its initial point, terminal point, objective/criterion, raw and projected gradients, active bounds, status/message, and distance from its problem's best objective. All terminal objectives and the SMM criterion reproduce exactly from raw data.

The saved projected-gradient transformation implements the correct minimization KKT sign rule at lower and upper bounds, and every stored projected gradient, active-bound list, and infinity norm exactly matches that rule. Independent finite-difference projected-gradient norms at all selected global/profile solutions range from about `1.6e-5` to `9.1e-5`, safely below the declared `0.002` tolerance.

The production functions select the minimum objective before checking acceptance for the three main estimators and SMM. This is a latent robustness weakness, because an unaccepted lowest row could be reported in another run. It does not alter this run: each selected main/SMM solution is accepted. The conditional-profile code correctly filters on solver success, finite objective, and projected-gradient tolerance before choosing the best accepted row.

### Every conditional profile index — PASS

Each of the nine indices has six starts and at least five accepted rows:

| sigma | accepted / 6 | selected is best accepted |
|---:|---:|---|
| 0.0 | 5 | yes |
| 0.1 | 6 | yes |
| 0.2 | 5 | yes |
| 0.3 | 6 | yes |
| 0.4 | 5 | yes |
| 0.5 | 6 | yes |
| 0.6 | 6 | yes |
| 0.7 | 6 | yes |
| 0.8 | 6 | yes |

There are nine resolved indices and zero holes. Every saved `accepted` flag and every selected-start record recomputes under the declared rule. Best-accepted selection occurs before the cutoff calculation. The later cutoff calculation is where D1 arises.

### Inference eligibility — MIXED

The numerical prerequisites for constructing a model-conditional profile are met: the unrestricted MSL solution and every conditional index have accepted solutions. The scope disclaimers about asymptotic cutoff approximation, population injectivity, finite-sample coverage, policy invariance, and equilibrium response are appropriate.

Nevertheless, the reported LR set is not inferentially valid as calculated because of D1. “Eligible” can describe the numerical inputs, but the saved LR decisions and policy-set image must be recomputed before the profile result is reported.

### Count reconciliation — PASS

All counts reconcile: 900 intended = 900 realized; 700 + 200 = 900; 22 likelihood-estimator starts = 8 + 6 + 8; 54 profile starts = 9 × 6; nine reported = nine resolved + zero holes. The stored three-member set count reconciles internally with the stored, but defective, LR rule. Under the correct LR denominator, the accepted evaluated-grid count is **two**.

### Verifier coverage — PASS as disclosed, insufficient to catch D1

`verify.py` accurately states its narrow coverage. It independently recomputes only the training likelihood at the selected grid-profile minimum and reconciles sample/profile counts, best accepted profile rows, and the saved set count. It explicitly lists SMM, latent-class/homogeneous likelihoods, KKT, policy arithmetic, cutoff validity, identification, coverage, and realism as uncovered.

Therefore `verification.json: all_pass = true` means all checks in that limited suite passed; it is not evidence that the whole analysis passed. In particular, the verifier compares rows using the already saved `inside_95` flags and never checks that LR values use the unrestricted MSL denominator, so it cannot detect D1.

### Branch decisions — PASS after correcting the profile set

“Continue and fork narrowly” is supported: panel MSL rejects `sigma = 0` even under the corrected LR calculation (`LR = 18.8653`), the latent-class fit shows that the normal mixing distribution is not uniquely selected by fit, and the SMM moments fail to reveal dispersion. Continuing MSL, retaining a mixture-distribution robustness branch, redesigning SMM moments, and pausing welfare/external-policy claims are appropriately calibrated decisions. The branch rationale survives D1, but any statement of the profile set and its policy image must use the corrected denominator and grid-qualified language.

## Required correction

Use the accepted unrestricted normal-RC MSL objective (`best_rc["objective"]`) as the LR reference, not the minimum of `profile_selected`. Recompute `lr_stat`, `inside_95`, `inside_count`, `set_sigma`, `set_policy_change`, the policy range, and the response text. Label the result as accepted evaluated grid points; if a continuous profile confidence interval is desired, add finer/adaptive conditional solves around both cutoff crossings.
