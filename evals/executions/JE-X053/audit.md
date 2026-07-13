# Independent audit — JE structural transfer X053

## Overall judgment: PASS

I independently recomputed the 12 decisive headline/coverage claims from the saved primitives and full-precision terminal vectors, without importing `model.py`, calling its production solvers, or trusting the stored coverage booleans. All 12 claims pass. I also reran the three forced failures from a copied script in an isolated temporary directory; the source artifacts were not overwritten. The only file added to the artifact directory by this audit is this report.

Audit environment: `C:\Users\ENAN\miniforge3\envs\codex\python.exe`; artifact directory `C:\Users\ENAN\AppData\Local\Temp\junzi-economist-struct-x053`; source repository `C:\Users\ENAN\junzi-economist-skill`.

## Claim-by-claim results

1. **PASS — unconditional exact counts and no selection.** An independent replay of NumPy RNG seed `20260713` reproduced every saved primitive and outcome array with maximum absolute difference exactly `0.0`. There are exactly 4,000 distinct market IDs `0,...,3999`, three firms per market, 12,000 firm-market quantities, and all quantities are positive. `planned_market_id` equals `market_id` exactly. The executable DGP contains no redraw, survivor filter, solver-conditioned retention, or outcome-based drop.

2. **PASS — DGP equations and outcomes.** From the replayed primitives I recomputed `mc = 4 + 0.8*z_cost + omega`, the closed-form three-firm Cournot quantities, total quantity, and price. Every saved array (`mc`, `q`, `Q`, and `price`) matched exactly, not merely within tolerance.

3. **PASS — executable instrument timing and exclusion distinction.** The executable order draws `z_cost` before `omega` and `eta`; quantity and price use only demand intercept, marginal costs, and `beta`; only after those outcomes does the code draw independent noise and form `z_invalid_post = eta + noise`. The seed replay reproduced this ordering and all arrays exactly. The valid instrument, mean `z_cost`, is absent from inverse demand and shifts marginal cost/output. The invalid instrument contains `eta` directly and therefore violates demand exclusion. Recovered invalid-noise diagnostics are mean `-0.0006419901497830702`, SD `0.04985075438266283`, and correlation with `eta` `0.007062245882361306`.

4. **PASS — instrument results.** Independent calculations give `corr(z_valid, eta)=0.013601559298342012`, `corr(z_valid,Q)=-0.5353375132966784`, and valid-IV slope `0.7196258126936521` versus truth `0.7`. For the post-outcome invalid instrument, `corr(z_invalid,eta)=0.9924409483701151` and the IV slope is `-0.2438869172965705`. These support the stated finite-sample near-exclusion/relevance result for the valid instrument and the exclusion failure/distortion result for the invalid instrument; they are not population or Monte Carlo claims.

5. **PASS — bounded valid estimator starts.** The independently solved linear moment root is `[18.30006468092623, 0.7196258126936522, 3.9009829552525344, 0.8138124452218396]`, inside the declared box `[10,.2,2,.1]` to `[25,1.5,6,1.5]`. All six saved terminals are within `2.5224267119483557e-13` of that root and all six pass. Across starts, maximum raw residuals range from `2.015054789694659e-16` to `1.5654144647214707e-15`; maximum scaled residuals range from `2.015054789694659e-16` to `4.6926121997114575e-15`, below the respective `1e-9` and `1e-8` rules.

6. **PASS — bounded invalid estimator result and wording.** The independently solved unconstrained moment root is `[3.8478968487499134, -0.24388691729657083, 8.72550649322977, -0.005495055829637759]`, outside the declared box in all four coordinates. All six bounded optimizer terminals coincide to maximum spread `6.026059651276228e-10` and put the cost intercept at its upper bound `6` within `8.881784197001252e-16`. Solver termination is reported, but all six acceptance decisions are correctly false: maximum raw residuals are `0.09295335475503101`–`0.09295335476091907` and maximum scaled residuals are `0.22883926771210966`–`0.2288392677266053`. `response.md` correctly calls this a rejected **boundary candidate**, while reserving **root** for the unconstrained solution; it does not mislabel bounded optimizer termination as an accepted moment root.

7. **PASS — every estimator evaluation trace.** I recomputed the raw and scaled moment vectors for all 613 JSONL estimator evaluations. The maximum discrepancy from the recorded raw vectors and from the recorded scaled vectors is exactly `0.0`. Every one of the 12 estimator terminal vectors occurs exactly in its corresponding trace.

8. **PASS — equilibrium starts, uniqueness, and bounds.** For each of markets `0,17,901,2026,3999`, I independently solved the linear FOC system. Its eigenvalues are approximately `[0.7,0.7,2.8]`, so the system is nonsingular and has a unique solution. All 20 saved terminals (four starts per market) lie in `[0,20]^3`, with quantities ranging from `3.713570884998204` to `6.274462549746297`, and are within `3.8902214782865485e-13` of the analytic solution. Every start passes. The largest raw equilibrium residual is `3.055333763768431e-13`; the largest scaled residual is `1.7190735071606562e-14`.

9. **PASS — every equilibrium evaluation trace.** I recomputed raw and economically scaled FOC residual vectors for all 580 JSONL equilibrium evaluations. Maximum raw-vector and scaled-vector discrepancies are exactly `0.0`. Every one of the 20 equilibrium terminal vectors occurs exactly in its corresponding trace.

10. **PASS — full-precision save/load round trip.** Actual disk reload shows all three terminal arrays are binary64. For all 32 terminals (six valid, six invalid, twenty equilibrium), the NPZ value is bitwise identical to both the saved `float.hex` reconstruction and the JSON terminal value. Independent residual recomputation reproduces all six valid acceptances, all six invalid rejections, and all twenty equilibrium acceptances. The 32 stored round-trip records also all have `bitwise_equal=true` and `diagnostic_reproduced=true`.

11. **PASS — accounting levels and identities.** Independent levels are: consumer expenditure `450274.0678393667`; producer revenue `450274.0678393667`; variable cost `237372.48455230324`; producer profit `212901.5832870634`; consumer surplus `315357.8373235403`; total welfare `528259.4206106038`. They match `accounting.json` exactly. Identity residuals are `0.0` for expenditure minus revenue, `-2.9103830456733704e-11` for profit minus revenue plus cost, and `5.820766091346741e-11` for welfare minus consumer surplus minus profit. The stated scope—variable cost only, no fixed costs or transfers—is consistent with the executable accounting.

12. **PASS — isolated failures diagnose before nonzero exit.** I copied only `failure_modes.py` to a fresh temporary directory and executed each mode there. Simulation wrote a parseable diagnostic with `required_unit_failed=true`, `accepted=false`, then exited `31`; equilibrium did the same and exited `32`; estimation did the same and exited `33`. In each case `process_must_exit_nonzero=true`. This fresh process test agrees with, but does not rely on, `process_failure_manifest.json`.

## Verifier independence: PASS

Static inspection of `verifier.py` finds imports only from `__future__`, `json`, `pathlib`, and `numpy`; it neither imports `model.py` nor uses SciPy/production solver functions. It reconstructs outcomes from primitives, solves estimator roots with `numpy.linalg.solve`, solves Cournot systems separately, recomputes every trace residual, rebuilds accounting, and checks persisted failure and round-trip records. Its 12-item coverage map matches the requested decisive claims. My seed replay, closed-form roots, trace-wide checks, accounting reconstruction, and isolated process reruns add checks not dependent on the verifier's pass flags.

One scope qualification is important: the verifier checks the five declared markets and 20 declared equilibrium starts, not all 4,000 markets through the numerical equilibrium solver. `response.md` states this accurately as “all 20 equilibrium solves (five markets, four starts each),” while all 4,000 DGP outcomes are separately reproduced algebraically.

## Commit scope and provenance: PASS, with a reproducibility caveat

The recorded abbreviated commit resolves to `539a1e860be4ef84e26b86e433a8ec56c67ba072`, which is the current repository `HEAD`; parent is `77aa2f194a2326326fa7def380907aaf81e06dc0`. The commit's exact scope is one tracked file only:

- `skills/junzi-economist/references/SOFTWARE_AND_COMPUTATION.md`, blob `6e2cd603837eaec088b263421cf388f098754603`, with three insertions and one deletion in the commit summary. The substantive additions require headline-matched independent coverage and full-precision executed save/load checks.

The other three files named in `provenance.json` resolve at that commit to these blobs:

- `skills/junzi-economist/SKILL.md`: `18ff06b418f47e640387f409aa330a56fcde34b8`
- `skills/junzi-economist/references/EMPIRICAL_AND_STRUCTURAL_METHODS.md`: `5278c1511d098212cc251f7be73ac8963cfd9f9c`
- `skills/junzi-economist/references/THEORY_MODELING.md`: `21ab5fa1d14a89c93b1e7faf4c563b73e4b99867`

At audit time, the repository has a post-artifact working-tree modification to `EMPIRICAL_AND_STRUCTURAL_METHODS.md` (mtime `2026-07-13 15:31:58`, after the artifact files at about `15:26`–`15:28`) and unrelated untracked earlier evaluation directories. Neither is part of commit `539a1e8`, so neither changes the verified commit scope. Caveat: `provenance.json` records the commit and file names but not their blob IDs or a hash manifest linking code, inputs, and outputs. Thus the commit's contents and scope are exact and verified, while historical proof that those exact blobs were what the generating process opened rests on the provenance record and timestamps rather than a cryptographic run manifest.

## Final claim status

The artifact supports all 12 requested computational claims as a deterministic, single-seed, finite-sample demonstration under the declared linear Cournot specification and parameter box. It does not support Monte Carlo coverage, external validity, global population identification, or a claim that the numerical equilibrium solver was run on all 4,000 markets. Those limits are already stated in `response.md` and do not weaken the audited claims above.
