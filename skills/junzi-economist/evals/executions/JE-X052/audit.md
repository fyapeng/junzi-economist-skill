# Independent audit: `junzi-economist-struct-x052`

## Overall judgment: MIXED

The central numerical and claim-calibration results reproduce independently: panel timing and state links are coherent; controlled reliability transitions reproduce exactly; independent NFXP and two-step CCP estimates match; the continuous Jacobian has stable rank four; the selected restricted candidate is genuinely feasible at the stated `1e-12` tolerance; policy-support labels are correct; and the counterfactual accounting identities reproduce with negligible stationary-distribution residuals. There is no global-identification overclaim.

The result is **MIXED**, rather than an unqualified PASS, for two auditability/optimization reasons. First, the restricted optimizer also bounds the transformed coordinate at `z_beta <= 8`, so its effective upper bound is `beta <= 0.7799228694699928`, not the full stated closed set `beta <= 0.78`. A separate direct-boundary solve at `beta = 0.78` achieves objective `15515.522637775135`, improving on the reported candidate's `15515.525096916721` by `0.002459141586`. The reported candidate remains feasible, and the response correctly declines to claim a global restricted optimum. Second, the search files retain the claimed starts, terminals, and generation-best summaries, but not every generation population, function evaluation, or polishing iterate; they are not replay-complete search traces.

No production code or existing artifact was changed or overwritten. Recomputations used a separate contraction-mapping Bellman solver, direct parameter coordinates, fresh optimizer starts, and a fresh output outside this directory.

## Evidence by audit target

### 1. Model timing and transitions — PASS

- Saved rows: `16,800 = 1,200 households x 14 decisions`.
- Every household has exactly 14 rows with period labels `0,...,13`.
- Regime assignment is time invariant within household: 600 households in each regime and zero regime-switching households.
- For every within-household adjacent pair, the preceding `next_state` equals the following current state: zero link errors across 15,600 adjacent links.
- Each row contains a post-decision transition, including period 13. Thus the file represents 14 decisions and 14 simulated transitions per household, with the last next state retained but not used as another decision row.
- Reliability transition estimates, recomputed from current reliability, action, and next reliability with the stated Jeffreys-style smoothing `(success + 0.5)/(n + 1)`, match exactly:

| action | current reliability | n | successes | recomputed probability |
|---:|---:|---:|---:|---:|
| 0 | 0 | 2,474 | 719 | 0.2907070707070707 |
| 0 | 1 | 6,064 | 4,716 | 0.7776586974443529 |
| 1 | 0 | 1,907 | 827 | 0.4337002096436059 |
| 1 | 1 | 3,028 | 2,577 | 0.8509409045889733 |
| 2 | 0 | 1,154 | 611 | 0.5294372294372295 |
| 2 | 1 | 2,173 | 1,988 | 0.9146734130634775 |

- Among 1,462 retrofit transitions eligible to raise insulation, 1,208 raise it by one, an empirical rate of `0.826265389876881`; none moves insulation by an invalid amount. The production transition matrix nevertheless uses the maintained fixed probability `0.82`; it does not estimate this probability. The comment in `run_model.py` saying “retrofit success estimated” is inaccurate, but `response.md` correctly describes `0.82` as part of the maintained transition law.

### 2. NFXP estimate and Bellman solution — PASS

I rebuilt the likelihood from saved choice counts and independently recomputed values by ordinary Bellman contraction rather than importing or calling the production Newton solver. Three fresh starts converged to objectives within `5.3e-8` of each other. The best independent result is:

| object | insulation | generator | retrofit | beta | objective |
|---|---:|---:|---:|---:|---:|
| reported | 1.1695613858 | 1.3117408484 | 2.0675870696 | 0.9164678693 | 15513.190451495360 |
| independent | 1.1695634882 | 1.3117401675 | 2.0675864612 | 0.9164664126 | 15513.190451493420 |

The objective difference is `-1.94e-9`. At the independent estimate, contraction converged in 342 iterations per regime and produced Bellman residuals `4.33e-13` and `4.41e-13`. The six saved production local terminals also independently reevaluate to their stored likelihoods with maximum absolute difference `6.06e-10`; all six reported terminal estimates lie in the same likelihood basin.

This verifies the implementation on this saved simulated sample. It does not establish repeated-sample recovery, coverage, or estimator robustness beyond this draw, and the response does not claim those stronger results.

### 3. Two-step CCP minimum-distance estimate — PASS

I independently rebuilt the smoothed empirical CCPs, solved the action-0 value equation, and minimized the stated log-choice-odds residual criterion in direct parameter coordinates from three fresh starts. All starts converged to the same minimum:

| object | insulation | generator | retrofit | beta | MD objective |
|---|---:|---:|---:|---:|---:|
| reported | 1.8131687641 | 1.3773176353 | 2.0259315162 | 0.7828421456 | 0.1064428506428799 |
| independent | 1.8131717472 | 1.3773174826 | 2.0259315738 | 0.7828416676 | 0.1064428506429957 |

The largest parameter difference is about `2.98e-6`, and the objective difference is `1.16e-13`. The response's description of the CCP estimator and its poorer recovery is accurate.

### 4. Continuous local rank — PASS, narrowly interpreted

I rebuilt the exact-policy log-odds map using the true transition matrix and the independent contraction solver, then recomputed centered finite-difference Jacobians at four step sizes. Every Jacobian has numerical column rank four under the reported relative threshold `1e-7`:

| finite-difference step | singular values, largest to smallest | rank |
|---:|---|---:|
| `1e-3` | 21.45632954, 3.42171694, 2.00090589, 0.57486046 | 4 |
| `1e-4` | 21.45633067, 3.42171694, 2.00090587, 0.57485951 | 4 |
| `1e-5` | 21.45633068, 3.42171694, 2.00090587, 0.57485950 | 4 |
| `1e-6` | 21.45633067, 3.42171694, 2.00090587, 0.57485950 | 4 |

The transition-probability entries appended to this map are constant with respect to the four preference/discount parameters and therefore add zero derivative rows; the rank is supplied by the policy log-odds. The response limits the claim to a continuous local population-rank result at the generating point, conditional on support, normalization, transition law, and equilibrium selection. It explicitly says this does not establish global point identification. That wording is appropriately narrow: a numerical full-rank derivative is not a global injectivity proof, a repeated-sample recovery study, or a formal analysis of observational equivalence.

### 5. Hard-restricted alternative — MIXED

**Feasibility and hardness pass.** The transformation

`beta = 0.55 + 0.23 logistic(z_beta)`

mathematically enforces `0.55 < beta < 0.78`; there is no penalty that can be traded against likelihood. The selected candidate has `beta = 0.7799228694699928`, so its recomputed slack is

`0.78 - beta = 0.00007713053000724113`.

This is positive and therefore feasible under the stated acceptance tolerance `1e-12`. The stored feasibility flag is correct.

**Coverage of the stated restricted set is qualified.** Differential evolution and every polishing run additionally impose `z_beta <= 8`, implying the tighter effective bound

`beta <= 0.55 + 0.23 logistic(8) = 0.7799228694699928`.

Seven of eight polishing terminals hit `z_beta = 8`; the selected candidate is one of them. A fresh differential-evolution search in direct coordinates followed by four bounded local solves places every solution at the actual stated boundary `beta = 0.78`. The best result is:

| object | insulation | generator | retrofit | beta | objective | gap from independent NFXP |
|---|---:|---:|---:|---:|---:|---:|
| reported candidate | 1.8257586687 | 1.2939584814 | 2.0381771258 | 0.7799228695 | 15515.525096916721 | 2.334645421361 |
| direct-boundary candidate | 1.8253204901 | 1.2939677451 | 2.0381927035 | 0.7800000000 | 15515.522637775135 | 2.332186281716 |

Thus the selected reported candidate is feasible but is not the best candidate found for the full closed set `beta <= 0.78`; its reported positive slack is induced by the finite transformed-coordinate cap. This is not a contradiction of `response.md`, because it expressly calls the search numerical and disclaims proof of a global restricted optimum. It does mean the reported objective gap should not be treated as the optimized profile-likelihood gap at the exact restriction boundary.

### 6. Restricted and unrestricted search records — MIXED

The exact retention claims in `response.md` are true:

- 32 differential-evolution initial candidates and objectives are present.
- 30 generation-best records are present with consecutive labels 0 through 29.
- Eight polishing starts and terminals are present.
- Six unrestricted local starts and terminals are present.

Independent reevaluation gives maximum absolute objective discrepancies of `5.43e-8` for the restricted initial population, `2.36e-11` for generation-best records, `1.82e-11` for restricted polishing terminals, and `6.06e-10` for unrestricted local terminals. The slightly larger initial-population discrepancy is consistent with the independent contraction tolerance and is economically immaterial.

The records are not a complete optimizer replay: they omit each differential-evolution generation's full population, rejected/trial candidates, all objective evaluations, and intermediate polishing iterates. Accordingly, “retains all 32 initial candidates, 30 generation-best records, and all starts/terminals” passes, while any stronger characterization as a full search trace would fail.

### 7. Policy support labels — PASS

- Regime 0 and regime 1 each contain 8,400 rows and 600 households.
- The model maps them to observed rebates 0 and 0.8, respectively.
- Rebate 0.4 never appears as an observed regime and is correctly labeled model-based interpolation between the two maintained policy values.
- All 36 regime-state-action cells occur in the simulated data; the smallest cell contains 4 choices and the largest 3,034. This confirms literal support, though the smallest cells are thin and smoothing materially governs their empirical CCPs.
- The response does not label 0.4 as a reduced-form causal estimate and does not claim extrapolation beyond the observed rebate interval.

### 8. Counterfactual accounting — PASS, conditional on the stated criterion

I independently solved each counterfactual policy, formed its induced state transition matrix, and iterated to stationarity. Maximum stationary residuals are between `2.89e-15` and `5.00e-15`. Using the independently estimated NFXP parameters gives:

| rebate | private payoff | transfers | resources | private - transfers - resources | retrofit share |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 2.393590751 | 0.000000000 | 0.277500711 | 2.116090040 | 0.083849859 |
| 0.4 | 2.379340677 | 0.048114125 | 0.309853293 | 2.021373259 | 0.120285311 |
| 0.8 | 2.382448045 | 0.135751965 | 0.353770645 | 1.892925435 | 0.169689956 |

These differ from the stored table by at most about `4.4e-6`, entirely explained by the approximately `1e-6` difference between the independent and reported NFXP estimates. Transfers equal `rebate x retrofit share`. Resources equal `0.55 x generator share + 1.1 x retrofit share`. The welfare identity holds by construction and is numerically exact to displayed precision.

The exercise is a stationary flow accounting, not lifetime welfare, and the utility/resource commensurability is maintained rather than validated. `response.md` appropriately labels the results model-implied and provisional and names omitted distributional weights, fiscal distortion, emissions, outage externalities, and liquidity constraints as failure conditions. There is no unsupported normative claim.

### 9. Published verifier and coverage claims — PASS with a wording qualification

The verifier is genuinely separate in the limited sense stated: it does not import `run_model.py` or call its solver. Its five checks reproduce saved-row transitions, singular-value arithmetic on the **saved** Jacobian, candidate slack, welfare row identities, and metadata counts. All five pass, and `blanket_pipeline_pass_claimed` is explicitly false.

Its limitations are substantive:

- It does not reconstruct or estimate NFXP or CCP preferences.
- It does not independently solve a Bellman equation or check the stored fixed-point residuals.
- It recomputes rank arithmetic from the saved Jacobian but does not rebuild the population mapping or Jacobian.
- It checks selected-candidate feasibility but not whether the implemented search spans the full stated restricted set or whether a better boundary point exists.
- It checks the welfare identity but not stationarity, action shares, resource formulas, normative completeness, or external validity.
- It checks metadata counts but not objective correctness or replay completeness.

`response.md` communicates these exclusions and correctly avoids a blanket pipeline PASS. Strictly, not every exclusion is written as a dedicated field in `verification.json`—Bellman-solver independence, for example, is inferred from absent coverage and source inspection—but the substantive coverage characterization is accurate.

## Final claim-status decision

- **Supported on this saved simulation:** timing, transition arithmetic, NFXP and CCP numerical reproduction, stable rank-four derivative at the stated point, selected-candidate feasibility under a hard restriction, observed/interpolated policy labels, stationary counterfactual accounting, and the limited verifier's five PASS results.
- **Qualified:** the reported restricted point and objective gap are for a slightly tighter transformed-coordinate search than the full closed restriction `beta <= 0.78`; retained optimizer records are summary traces rather than replay-complete traces.
- **Not established and not claimed:** global point identification, a global restricted optimum, repeated-sample estimator performance, external validity, or normatively complete welfare.

On balance, the economic and numerical conclusions are responsibly stated, but the exact restricted-boundary implementation and trace completeness prevent an unqualified overall PASS.
