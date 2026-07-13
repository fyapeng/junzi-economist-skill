# Independent audit of `junzi-economist-struct-x047`

## Overall verdict: MIXED

The central simulated-data results are numerically reproducible: transition counts and conditional-frequency estimates, fixed-beta and joint NFXP, the Hotz–Miller/CCP estimate, the continuous beta minimizer, the local-rank Jacobian, Bellman residuals, recovery summaries, and the reported policy-accounting numbers all agree with separate recomputation. The main interpretation is also appropriately limited to local identification and specification-conditional welfare.

The package nevertheless does not merit an unqualified `PASS` for two material reasons. First, the supposedly constrained alternative search uses a soft penalty and returns a point that violates the stated distance constraint. Second, `verify.py` is only a separately coded Bellman/rank checker; it inherits production estimates and estimated transition matrices from `results.json` and does not independently reproduce most of the claims to which its blanket `PASS` can easily be read as applying. There are also smaller trace, provenance, and subsidy-support qualifications detailed below.

## Audit method

I did not import `analysis.py`, modify the repository, rerun production in place, or overwrite any supplied artifact. I loaded `panel.npy` and independently reconstructed sufficient cell counts, transition estimators, Bellman solutions, likelihoods, the CCP inversion, profile objectives, finite-difference Jacobians, an actually constrained alternative search, stationary distributions, and private/resource accounts. I also regenerated every recovery panel from its declared seed to audit every stored objective and gradient. The supplied SHA-256 manifest was checked before this audit file was added; every listed hash matched.

## Claim-by-claim results

### 1. Data and controlled-transition estimation — PASS

- `panel.npy` has exactly 96,000 rows, 2,400 asset IDs, periods 0–39, and 48,000 observations in each subsidy regime. It is byte-for-byte reproducible from seed 47013 and the declared simulation algorithm.
- Action counts are 74,313 run and 21,687 overhaul.
- Independently reconstructed run-transition counts are
  `[[22076,11879,3754,0,0],[0,13731,7580,2395,0],[0,0,6062,3357,1049],[0,0,0,1252,944],[0,0,0,0,234]]`.
- Independently reconstructed pooled overhaul-reset counts are `[18718,2969,0,0,0]`.
- Conditional-frequency estimates on the declared state-specific supports and the pooled overhaul estimate match `results.json` exactly (maximum absolute discrepancy 0).
- The code correctly handles support collapse from capping: state 3 has destinations 3/4 and state 4 has destination 4 only. It estimates state-specific controlled transition rows; it does not claim to recover the three primitive deterioration-increment probabilities by pooling.

### 2. NFXP and CCP recovery — PASS

Using a separate Bellman and likelihood implementation with cell-count sufficient statistics and Nelder–Mead starts, I obtain:

- joint NFXP: objective `40408.07693676965`, `(theta,F,beta)=(0.17668248,3.19987934,0.91604081)`;
- fixed `beta=0.91`: objective `40408.14420733288`, `(theta,F)=(0.17796034,3.19372051)`;
- CCP/Hotz–Miller WLS: `(theta,F)=(0.17670599,3.18712971)`, objective `457.62846244`.

These match the supplied results at the displayed precision. The CCP implementation is genuinely distinct from NFXP in estimation: it uses smoothed empirical cell CCPs, a run-reference linear value equation, log-odds inversion, and WLS without a Bellman solve inside its estimator. The response correctly treats agreement as recovery evidence, not general validation.

### 3. Continuous beta profile — PASS numerically; MIXED as a global-search record

Independent nested profiling gives `beta=0.91604079735`, objective `40408.076936769656`, and inner `(theta,F)=(0.17668247,3.19987927)`, matching production. An independent broad scan gives profiled objective differences from the minimum of approximately:

| beta | objective difference |
|---:|---:|
| 0.55 | 187.1978 |
| 0.70 | 73.0246 |
| 0.80 | 22.7577 |
| 0.85 | 7.6658 |
| 0.90 | 0.4706 |
| 0.91 | 0.0673 |
| 0.9160408 | 0.0000 |
| 0.93 | 0.3650 |
| 0.95 | 2.1955 |
| 0.98 | 7.9803 |
| 0.995 | 12.3126 |

Thus the reported continuous minimizer is accurate and not a finite-grid selection. The stored outer trace, however, is only the ten evaluations chosen by the bounded scalar optimizer (recorded beta range about 0.71997–0.92729); it is not a full-range profile or a certificate of global unimodality. The response does not explicitly claim such a certificate, so this is a documentation/evidentiary limitation rather than a numerical contradiction.

### 4. Population local-rank calculation — PASS

Separate central differences of the ten true-population CCP logits give, at step `1e-5`, singular values
`(30.09776738, 2.99778424, 1.01211429)` and rank 3. Results remain stable for steps `1e-4`, `3e-5`, `1e-5`, and `3e-6`; the smallest singular value stays about 1.01211.

Under the maintained transition, EV1, stationarity, subsidy-exogeneity, and parametric-utility restrictions, full column rank of this 10-by-3 derivative supports the stated local injectivity argument. The response correctly does not promote it to global identification or infer identification from the sample Hessian.

### 5. Continuous alternative search and interpretation — MIXED

**Exact defect A (constraint violation):** `analysis.py` does not impose the stated scaled-distance constraint. It minimizes
`max_abs_CCP_gap + 1000*max(0,1-distance)^2`, a soft-penalty objective. The reported candidate has scaled distance `0.9999945034155397`, so it is infeasible for the asserted constraint `distance >= 1` by about `5.50e-6`. Therefore the sentence that the search was “constrained to remain a scaled distance of at least one” and the stored candidate are not exactly correct.

Using SciPy's explicit nonlinear constraint, two independent differential-evolution seeds converge to the feasible boundary candidate approximately
`(0.19637313,3.02894709,0.81070331)`, distance at least 1 to numerical tolerance, with maximum absolute population-CCP gap `0.0114854481`. This differs from the reported gap by only about `6.0e-8`, so the substantive finding of a practically close, lower-beta alternative survives the correction.

The cautious interpretation—bounded heuristic search evidence, not proof of global injectivity—is appropriate. A nonzero value at a heuristic optimizer's best candidate is not a mathematical lower-bound certificate against exact equivalence.

### 6. Optimizer-start traces, gradients, and KKT rule — PASS for all recorded starts; MIXED for optimizer-wide trace coverage

`full_start_traces.json` contains 72 start records:

- 6 joint-NFXP starts;
- 4 fixed-beta starts;
- 30 profile-inner starts (10 beta evaluations times 3 starts);
- 32 recovery starts (16 panels times 2 starts).

Every record has the advertised initial/final points, objective, raw/projected gradients, projected-gradient infinity norm, active bounds, solver status/message, iteration count, objective distance, and KKT acceptance flag. Independent recomputation found:

- maximum objective discrepancy over joint/fixed/profile records: `1.46e-11`;
- maximum raw-gradient discrepancy there: `1.10e-6`;
- maximum recovery objective discrepancy: `1.82e-12`;
- maximum recovery raw-gradient discrepancy: `9.10e-8`;
- zero KKT-acceptance mismatches under the declared `<0.01` rule.

Counts also match the narrative: 5/6 joint starts, 3/4 fixed-beta starts, 22/30 profile-inner starts, and 32/32 recovery starts pass the declared rule. The selected joint, fixed, profile, and recovery solutions all pass and are interior. Failed starts are retained. The projected-gradient formula has the correct minimization sign convention at lower and upper bounds, though no selected solution needs a bound adjustment.

The acceptance threshold `0.01` is declared but fairly loose: the selected joint solution has projected-gradient norm about `0.00795`, while an independently refined solution reaches the same objective more tightly. This does not change the estimates at reported precision.

**Trace-coverage limitation:** the file does not contain the differential-evolution population/history or a raw alternative-search trace, and the beta outer optimizer is represented by evaluation records rather than a complete optimizer state/history. Thus it is complete for the explicitly launched local multistarts, but not for every stochastic/global optimizer operation in `analysis.py`.

### 7. Repeated-sample recovery — PASS

All 16 panels and their two starts were exactly reproducible from seeds 47113–47128. The independently verified selected mean is `(0.17864987,3.19558273)`, with ranges theta `[0.16775683,0.19214261]` and F `[3.07273991,3.29232798]`. All selected replications pass the declared KKT rule. The response correctly labels this a finite recovery demonstration and does not claim coverage, general failure rates, or broad estimator performance.

### 8. Bellman residuals and EV1 value normalization — PASS

For the joint estimate and all six reported subsidy values, independent fixed-point residuals are between about `1.69e-13` and `1.81e-13`. The supplied verifier's reported residuals below `2e-13` are consistent with its stopping convention.

The EV1 level normalization is correct. Standard type-I extreme-value shocks have mean Euler's constant; subtracting that constant from every action shock makes each shock mean zero and changes the expected maximum from `gamma + logsumexp(v)` to `logsumexp(v)`. CCPs are invariant. A common per-period location shift changes all value levels by the same constant divided by `1-beta`, so same-beta policy value differences are invariant as stated.

### 9. Independent verifier — FAIL as an end-to-end verifier; PASS for its narrow checks

**Exact defect B (overbroad independence/PASS):** `verify.py` is separately coded and does not import `analysis.py`, but it is not an independent reconstruction of the full analysis.

- It reads the selected joint parameter and estimated run/overhaul matrices directly from `results.json` for its policy checks.
- It never reads `panel.npy` and therefore does not re-estimate transitions.
- It does not recompute the NFXP likelihood or optimum, CCP estimator, beta profile, alternative search, recovery panels, optimizer objectives/gradients/KKT flags, stationary distributions, or welfare accounts.
- Only for the local-rank derivative does it replace the result-supplied matrices with the declared true primitive matrices.

Accordingly, its `status: PASS` validly covers a separately implemented Bellman check at inherited production inputs plus a separately finite-differenced primitive rank calculation. It cannot validate the package as a whole, and the response's phrase “independently reconstructs transitions” is misleading for the estimated-transition Bellman checks. The stronger numerical verification in this audit was necessary precisely because the shipped verifier omits those objects.

### 10. Subsidy support and private/resource accounting — MIXED on support wording; PASS on arithmetic conditional on the declared criterion

The data contain observed subsidy support only at `{0,0.75}`. Values 0.25 and 0.50 are unobserved, within-convex-hull model interpolations; they do not have “actual” empirical support. The table itself labels them `interpolation`, and 1.25/2.00 correctly as extrapolation, but the sentence that the two regimes provide “actual policy interpolation support” should be read as bracketing, not observed support at intermediate subsidy values.

The independently recomputed counterfactual table matches the response. For subsidies `(0,0.75,0.25,0.50,1.25,2.00)`, respectively:

- overhaul rates are `(0.2077164,0.2441927,0.2181040,0.2301551,0.2797569,0.3582523)`;
- private stationary-initial value changes are `(0,2.0939491,0.6637069,1.3599277,3.7017269,6.5934150)`;
- transfer flows are `(0,0.1831445,0.0545260,0.1150776,0.3496961,0.7165046)`;
- resource-cost flows are `(0.8491679,0.9261074,0.8691287,0.8944243,1.0136751,1.2271410)`;
- social-flow changes are `(0,-0.0769395,-0.0199609,-0.0452564,-0.1645073,-0.3779732)`.

For every policy, the accounting identity
`private deterministic flow - government transfer + resource cost = 0`
holds to at most `1.2e-16`. The subsidy is counted as an owner receipt and government outflow, not as a real resource saving; it cancels from the unweighted social account. The conclusion that subsidies lower the declared social-flow criterion follows mechanically because the model assigns no reliability, safety, output, or external benefit to improved condition and interprets `theta*x^2` and `F` as real resource costs.

One interpretation detail should remain explicit: the reported private-value comparison uses each policy's own stationary distribution, `mu_s' V_s - mu_0' V_0`, rather than evaluating both policies for a common initial-state distribution. The phrase “stationary-initial” is accurate, but this is not the same welfare object as a common-cohort policy change.

### 11. Provenance, hashes, and raw outputs — MIXED

- Commit `e25b4d0cd1a3812911be2094197c5b61110189aa` exists and has the stated subject/time; the provenance file identifies the files said to have been read through `git show`.
- All ten supplied SHA-256 entries matched their files before this audit artifact was created.
- Commands, seed, raw panel, structured numerical results, local-start traces, stdout captures, and the verifier output are present.
- `run_output.txt` is a genuine but minimal stdout summary; most raw diagnostics live in JSON rather than stdout.

Reproducibility is not fully sealed: `results.json` records Python, NumPy, and platform but omits the SciPy version even though optimization behavior is central (the currently installed version is 1.17.1), and there is no environment lock. `PROVENANCE.md` uses a short commit identifier rather than the full hash and does not preserve snapshots/hashes of the four skill-source files. Assertions that no eval/prior-task artifacts were read and that the repository was not modified by the production process cannot be independently proven from these output files alone; the production script itself contains no repository or eval-file reads.

## Exact defects requiring correction

1. Replace the alternative-search soft penalty with an explicit feasibility constraint or project/parameterize candidates onto `scaled_distance >= 1`; update the candidate and gap to the feasible values above.
2. Narrow the shipped verifier's `PASS` label and response wording to the two objects it actually verifies, or extend it to load `panel.npy` and independently recompute transitions, estimators, profile/search, traces, and policy accounting.
3. Preserve the differential-evolution population/history (or at least convergence history, constraint violation, seed, and best feasible candidate path) if claiming optimizer-wide trace completeness.
4. Replace “actual policy interpolation support” with “two observed endpoints that bracket model-based interpolations”; intermediate subsidy values are not observed.
5. Record SciPy and ideally an environment lock; use the full commit hash and hash/snapshot the referenced skill files for stronger provenance.

## Bottom line

The estimates and substantive local-identification/recovery conclusions survive independent recomputation. The counterfactual arithmetic is correct under its deliberately narrow resource criterion. The package is `MIXED`, not `FAIL`, because the material numerical conclusions remain intact after correcting the alternative-search feasibility error. It is not `PASS` because the search violates its own stated constraint and the advertised independent verification is materially narrower than the response suggests.
