# Independent audit: `junzi-economist-struct-x058`

## Verdict: PASS

The response is complete and numerically correct for the stated evaluated-grid claim. I do not penalize it for being JSON rather than Markdown. I independently reconstructed the binomial-mixture likelihood from `raw_primitives.json`, used starts not present in either production or `independent_verify.py`, solved the unrestricted problem and all 15 conditional problems, independently replayed the 81 production initial points, recomputed projected-KKT residuals, LR membership, grid holes, censoring, ranked supports, and the selected-only policy image, and reconciled the stored files and counts. The independent results support the response's provisional claim and branch decision.

## Independence and method

- The audit likelihood was constructed directly as a two-component mixture of `Binomial(6,p)` probabilities using `math.comb`, log-sum-exp evaluation, and independently coded analytic gradients.
- Fresh audit starts were deliberately different from both sets already in the directory: 10 unrestricted starts and 8 starts for each of 15 conditional problems. All 10 unrestricted candidates and all 120 conditional candidates passed solver-success plus projected-KKT acceptance.
- Production-start acceptance was checked by reading only each stored `start_id`, `profile_pi`, and `initial` point, then independently rerunning that optimization and recomputing its objective, gradient, and projected residual. Stored terminal values, objectives, and gradients were not inputs to those solves; they were read only afterward for reconciliation.
- `independent_verify.py` statically imports only `json`, `math`, `pathlib`, NumPy, and SciPy. It imports no production module or function. Its only input file is `raw_primitives.json`; it does not open `start_records.jsonl`, `profile_records.jsonl`, `response.json`, or any stored terminal/objective source. It writes `verification_report.json`. Its declared fresh starts are 8 unrestricted and 6 per grid point and differ from production starts.

## Sample, likelihood, and unrestricted optimum

- Intended sample: 160 units.
- Realized sample: `19+11+5+13+34+49+29 = 160`; exact match.
- Independent accepted unrestricted optimum:
  - NLL: `280.0706832754517`
  - coordinate A mass: `0.2026346532888571`
  - `p_a = 0.08491699951655964`
  - `p_b = 0.7818472120641605`
  - ranked supports: low `0.08491699951655964`, high `0.7818472120641605`
  - projected-KKT infinity norm: `1.0544155060188132e-07`
- Difference from `response.json`: NLL `5.68e-14`, mass `1.78e-10`, `p_a` `9.06e-11`, and `p_b` `6.18e-11`. These are immaterial optimizer-level differences.

## Independent conditional profile and LR set

The LR statistic below is `2*(conditional NLL - 280.0706832754517)`, using the independently accepted unrestricted optimum and cutoff `3.841458820694124`.

| pi | NLL | LR | ranked low | ranked high | KKT-inf | selected | policy probability |
|---:|---:|---:|---:|---:|---:|:---:|---:|
| 0.15 | 281.4689538488875 | 2.7965411468716 | 0.0766160968824 | 0.7780955083235 | 5.6805e-07 | yes | 0.7301073574305 |
| 0.20 | 280.0737298530927 | 0.0060931552820 | 0.0845125548696 | 0.7816748858190 | 1.0373e-07 | yes | 0.6980505741122 |
| 0.25 | 280.9570732680165 | 1.7727799851295 | 0.0920736576608 | 0.7847360697863 | 2.7512e-08 | yes | 0.6663629798539 |
| 0.30 | 283.5216412673111 | 6.9019159837187 | 0.0997415966494 | 0.7874926918845 | 2.0483e-08 | no | — |
| 0.35 | 287.4770460642785 | 14.8127255776536 | 0.1083593025176 | 0.7902053287711 | 1.2883e-06 | no | — |
| 0.40 | 292.6719822079928 | 25.2025978650821 | 0.1194569625533 | 0.7932745722461 | 7.4715e-08 | no | — |
| 0.45 | 299.0109109366957 | 37.8804553224879 | 0.1362646356349 | 0.7974895236751 | 3.1509e-07 | no | — |
| 0.50 | 306.3686568097427 | 52.5959470685820 | 0.1654232517554 | 0.8044682011014 | 8.0943e-09 | no | — |
| 0.55 | 299.0109109366956 | 37.8804553224878 | 0.1362646356349 | 0.7974895236751 | 3.1509e-07 | no | — |
| 0.60 | 292.6719822079928 | 25.2025978650821 | 0.1194569625578 | 0.7932745722650 | 1.2506e-12 | no | — |
| 0.65 | 287.4770460642785 | 14.8127255776536 | 0.1083593028304 | 0.7902053291271 | 9.8812e-09 | no | — |
| 0.70 | 283.5216412673111 | 6.9019159837187 | 0.0997415966572 | 0.7874926918864 | 1.0743e-08 | no | — |
| 0.75 | 280.9570732680164 | 1.7727799851294 | 0.0920736576611 | 0.7847360697769 | 1.0782e-08 | yes | 0.6663629798485 |
| 0.80 | 280.0737298530927 | 0.0060931552820 | 0.0845125548696 | 0.7816748858190 | 1.0373e-07 | yes | 0.6980505741122 |
| 0.85 | 281.4689538488876 | 2.7965411468717 | 0.0766160968824 | 0.7780955083235 | 5.6805e-07 | yes | 0.7301073574305 |

Consequences:

- All 15 declared grid points were evaluated and accepted as conditional optima.
- Evaluated-grid membership is exactly `{0.15, 0.20, 0.25, 0.75, 0.80, 0.85}`: 6 selected points.
- The nine points `{0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70}` are resolved, accepted profile points whose LR statistics exceed the cutoff. They are holes in the selected evaluated-grid set, not unresolved computations or missing evaluations.
- Because the selected set includes both endpoints of the declared grid, lower and upper grid censoring are both true. The response correctly avoids claiming a continuous confidence set.
- Against `profile_records.jsonl`, the largest absolute differences from this independent profile are `5.68e-14` in NLL, `1.14e-13` in LR, `4.82e-09` in the low support, `9.08e-10` in the high support, and `7.82e-11` in selected policy probability.

## Projected-KKT audit of all 81 production starts

- Intended starts: `6 + 15*5 = 81`.
- Stored start rows: 81, with 81 unique IDs: 6 unrestricted and 75 conditional across exactly 15 grid values.
- Stored acceptance: all 81 have solver success and projected-KKT infinity norm at or below `1e-5`; the largest stored residual is `7.102368954292615e-06` at `g04s05`.
- Independent replay acceptance: all 81 pass, with zero acceptance mismatches. The largest independently replayed residual is `9.70495966612361e-06` at `g10s02`, still below `1e-5`.
- Independent replay versus stored results: maximum terminal-coordinate difference `4.7706877476239e-09`; maximum NLL difference `1.13686837721616e-13`. KKT residuals are solver-path sensitive near zero, but every stored and replayed result satisfies the executed threshold.

## Policy image, supports, and label branch

- The policy mapping was recomputed only for the six LR-selected points; all nine unselected records have null policy values. Thus mapped count is 6 and unselected mapped count is 0.
- Independent selected-only policy image values, in selected-pi order, are approximately `{0.7301073574305, 0.6980505741122, 0.6663629798539, 0.6663629798485, 0.6980505741122, 0.7301073574305}`. The image is `[0.6663629798485, 0.7301073574305]` on the evaluated selected points.
- `response.json` reports `[0.6663629798510762, 0.7301073575086675]`; endpoint discrepancies are at most `7.82e-11`.
- Coordinate pairs `pi` and `1-pi` have the same NLL and ranked supports up to numerical error, with A/B roles exchanged. For selected pairs, policy-probability discrepancies are at most `5.41e-12`. This confirms label switching and invariance of ranked supports and the mixture policy image.
- Therefore the branch decision—retain both coordinate branches while interpreting only ranked low/high supports—is justified. No coordinate-label identification or continuous-set claim is warranted. This is a `continue/retain` decision with explicit scope, not cosmetic rescue of a failed identification claim.

## File and count reconciliation

- `start_records.jsonl`: 81 rows, 81 unique IDs, 6 unrestricted plus 75 conditional.
- `profile_records.jsonl`: 16 rows, comprising 1 unrestricted and 15 conditional profiles.
- `verification_report.json`: reports 15 declared/evaluated/accepted conditional points, the same 6 selected points, the same 9 interior exclusions, both edge-censoring flags, and verdict `pass`.
- `response.json`: intended/realized sample `160/160`; intended/realized starts `81/81`; evaluated/accepted/selected profiles `15/15/6`; all reconcile with primitives and line-level artifacts.
- Provenance hashes reconcile exactly:
  - `raw_primitives.json`: `029f30b59dac8fa270c5e92a0254a60a95719914e30c7a87d627440c5f35989a`
  - `run_profile.py`: `b860b09c2599b893c34337533b0c77e255caa25e37d5132c7eb11d04e7518be8`
- Additional audited artifact hashes:
  - `independent_verify.py`: `5290f3b6e400dadd61752623324192724bc0b19cb6b9017c67f04012371b1f40`
  - `start_records.jsonl`: `f5135baeb774706e904738b92e5dbd6564501dcdd4374c56ff38f6b664084449`
  - `profile_records.jsonl`: `27e989ab0d63fb1938f77b345fdfe31443b59ddb38ae1a81ed03a3e1df24a56e`
  - `response.json`: `22d1b027fc3b80eefa3e6f8b80c34938f25f40f32bf6d838c240cccee97a99c6`
  - `verification_report.json`: `30801daaf21cd4aa63d43ca84ed8e4bca78a86943060d5abaf21f73af6a2997a`

## Final judgment

**PASS.** The numerical computation, evaluated-grid interpretation, selected-only policy mapping, ranked-support interpretation, label-switch branch decision, and file/count claims are supported. The appropriate claim status remains the response's `provisional_structural_grid_evidence`: this audit validates computation and the stated finite grid, not population identification, coordinate-label identification, external validation, or a continuous confidence set.
